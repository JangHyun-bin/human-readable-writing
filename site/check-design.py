from html.parser import HTMLParser
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
TOKENS = ROOT / "assets" / "tokens.css"
GLOBAL_VALUES = {"0", "auto", "inherit", "initial", "unset", "none", "normal", "transparent", "currentcolor", "solid", "dashed", "dotted", "double"}
TOKEN_PROPERTIES = {
    "color", "background", "background-color", "fill", "stroke", "accent-color",
    "caret-color", "outline-color", "text-decoration-color", "font", "font-family",
    "font-size", "font-weight", "line-height", "letter-spacing", "border-radius",
    "box-shadow", "text-shadow", "gap", "row-gap", "column-gap",
}
DECLARATION = re.compile(r"([a-z][a-z-]*)\s*:\s*([^;{}]+)", re.IGNORECASE)
REFERENCE = re.compile(r"var\(\s*(--[\w-]+)")
WHOLE_REFERENCE = re.compile(r"var\(\s*--[\w-]+\s*\)")
RAW_COLOR = re.compile(r"#[0-9a-f]{3,8}\b|\b(?:rgba?|hsla?|oklch|oklab|lab|lch|color)\(", re.IGNORECASE)
errors = []


def report(path, source, offset, message):
    line = source.count("\n", 0, offset) + 1
    errors.append(f"{path.relative_to(ROOT)}:{line}: {message}")


class InlineStyleCheck(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def handle_starttag(self, tag, attrs):
        if tag == "style" or any(name.lower() == "style" for name, _ in attrs):
            errors.append(f"{self.path.relative_to(ROOT)}:{self.getpos()[0]}: use the shared stylesheets, not inline CSS")


if not TOKENS.is_file():
    sys.exit("Missing site/assets/tokens.css")
token_source = TOKENS.read_text(encoding="utf-8")
declared = set(re.findall(r"(--[\w-]+)\s*:", token_source))
stylesheets = sorted(ROOT.rglob("*.css"))
for path in stylesheets:
    source = path.read_text(encoding="utf-8")
    source = re.sub(r"/\*.*?\*/", lambda match: "\n" * match.group().count("\n"), source, flags=re.DOTALL)
    for reference in REFERENCE.finditer(source):
        if reference.group(1) not in declared:
            report(path, source, reference.start(), f"undefined design token {reference.group(1)}")
    if path == TOKENS:
        continue
    for declaration in DECLARATION.finditer(source):
        property_name, value = declaration.group(1).lower(), declaration.group(2).strip()
        if RAW_COLOR.search(value):
            report(path, source, declaration.start(), "define color values in assets/tokens.css")
        requires_token = property_name in TOKEN_PROPERTIES or property_name.startswith(("margin", "padding", "border", "outline"))
        if requires_token:
            remaining = WHOLE_REFERENCE.sub(" ", value).lower().split()
            if any(part not in GLOBAL_VALUES for part in remaining):
                report(path, source, declaration.start(), f"{property_name} must use shared design tokens")

for path in sorted(ROOT.rglob("*.html")):
    InlineStyleCheck(path).feed(path.read_text(encoding="utf-8"))

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"Design boundaries passed for {len(stylesheets)} stylesheets. No inline CSS or undefined tokens.")
