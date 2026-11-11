# Landing page

The English page is `index.html`. The Korean page is `ko/index.html`. Both use `assets/tokens.css`, `assets/site.css`, and the same `assets/site.js`. The site has no build step, login, backend, analytics, or model API. JavaScript adds clipboard copying only. Without it, the text, installation command, invocation instructions, and links remain available.

## Preview locally

From the repository root, run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory site
```

Open <http://127.0.0.1:8000/> and <http://127.0.0.1:8000/ko/>. Open <http://127.0.0.1:8000/styleguide.html> to inspect the shared design system. Stop the server with Ctrl+C.

## Change the design

Start with the rendered catalog in `styleguide.html`. It shows the components the landing actually uses, rather than an unrelated UI library. New pages use its tokens and components. Add a missing component there before using it elsewhere.

Put color, font, typography, spacing, and control values in `assets/tokens.css`. `assets/site.css` owns layout and component states. The only JavaScript contract is `#install-command`, `#copy-install`, and `#copy-status`. Copy labels and status messages come from the button's data attributes in each HTML page.

Run the dependency-free boundary check:

```sh
python3 site/check-design.py
```

It rejects undefined token references, inline CSS, and raw visual declarations outside the token file. This is a constrained stylesheet check, not a full CSS parser or an accessibility certification. Browser verification is still required. Inspect both languages and the catalog at 320, 375, 414, 768, and desktop widths. Check content clipping, keyboard focus, installation navigation, both language links, and clipboard success and denial. Also check the no-JavaScript path and reduced-motion preference. Do not hide layout defects with clipping.

The English page requests Archivo and Source Serif 4 through Google Fonts. These optional requests go to Google, even though the site has no analytics. Text falls back to platform fonts if the font service is unavailable. [Archivo](https://github.com/google/fonts/blob/main/ofl/archivo/OFL.txt) and [Source Serif 4](https://github.com/google/fonts/blob/main/ofl/sourceserif4/OFL.txt) retain their SIL Open Font License 1.1 terms.

The Korean page serves SUIT Variable for body text and UI, and Paperlogy Bold 700 for headings, from `assets/fonts/`. It does not request Google Fonts. The font files are official, unmodified distributions with their original copyright notices and complete OFL 1.1 texts. [Font sources, pinned revisions, hashes, and licenses](assets/fonts/NOTICE.md) are separate from the site's MIT license. Code keeps the platform monospace stack. The design catalog renders both language-specific type systems.

## Keep content accurate

The README and the example guides are the source for product and example copy. Keep the illustration's technical facts and its label. Do not turn an illustration into a recorded model result. Keep installation and evidence facts equivalent in both languages.

Use the landing for the example, installation steps, and dated tool statuses. Keep explanations of the checks and their limits in the linked documentation. Do not repeat them below the example or support list.

Both landing pages use declarative descriptions throughout, including installation steps and error messages. Imperative, exhortative, and obligation phrasing do not belong in this copy.

The coverage section summarizes the checks recorded on 2026-11-10. Update it only with new evidence from `docs/tool-support.md` and `docs/verification.md`. Target runtimes are not an all-five compatibility claim. Source-fidelity and loading checks do not establish improved comprehension, reading time, or writing quality. Do not change historical research records to suit the page.

## Deployment

### Vercel

The public landing is hosted in the `rhizome` team's `human-readable-writing` project:

- [English](https://human-readable-writing.vercel.app/)
- [한국어](https://human-readable-writing.vercel.app/ko/)

Deployment is a manual CLI upload with no Git integration. The upload contains only `index.html`, `styleguide.html`, `assets/`, and `ko/` from `site/`. Font copyright notices and complete licenses ship with the fonts. Repository documents, research records, the installable skill, and `check-design.py` are excluded.

From the repository root, a preview update uses a temporary public-only directory:

```sh
deployment_dir=$(mktemp -d) &&
cp site/index.html site/styleguide.html "$deployment_dir/" &&
cp -R site/assets site/ko "$deployment_dir/" &&
vercel deploy --cwd "$deployment_dir" --project human-readable-writing --scope rhizome --yes &&
rm -r "$deployment_dir"
```

An approved update to the public site adds `--prod` to the deployment command. Vercel treats a new project's first deployment as production even without that flag. The command above targets the existing project.

The initial public deployment on 2026-11-11 was checked in Chromium at mobile and desktop widths. Both languages, rendered fonts, language navigation, and native clipboard success and denial were checked. All 12 uploaded files matched the local snapshot by SHA-256, including the original fonts and licenses. Excluded repository paths returned 404. Other browsers were not checked.

### GitHub Pages

The alternative `.github/workflows/landing-pages.yml` remains manual-only and accepts `main` only. Pushing a branch does not trigger it. It checks the design boundaries and uploads only `site/`, not the research records or skill package. The workflow follows GitHub's [static Pages workflow](https://github.com/actions/starter-workflows/blob/main/pages/static.yml), with its actions pinned to commit revisions.

When GitHub Pages deployment is approved:

1. Merge the reviewed site and workflow into `main`.
2. In repository Settings, open Pages and select GitHub Actions as the source.
3. In Actions, run **Deploy landing page** on `main`. This step publishes the site.
4. Open the URL returned by the deployment. Check the English page, `ko/`, assets, copy behavior, and the catalog under the actual project path.

The GitHub Pages workflow was not run. Its repository settings, permissions, and hosted URL remain unverified.

## 한국어

저장소 루트에서 위의 Python 서버 명령을 실행하면 영문, `ko/`의 한국어, `styleguide.html`의 디자인 기준을 확인할 수 있습니다. 별도 빌드나 Node.js 의존성은 없습니다. JavaScript를 끄면 복사 버튼만 사라지고 명령과 본문은 남습니다.

시각 값을 바꿀 때는 `assets/tokens.css`부터 수정하고 `python3 site/check-design.py`를 실행하세요. 두 언어와 디자인 기준 페이지를 모바일·데스크톱에서 직접 확인해야 합니다. 한국어 페이지는 본문·UI에 SUIT Variable, 제목에 페이퍼로지 Bold 700 원본을 자체 호스팅합니다. [저작권·OFL 전문과 출처](assets/fonts/NOTICE.md)를 폰트와 함께 보존하며 MIT로 바꾸지 않습니다. 영문 페이지의 Archivo와 Source Serif 4는 Google Fonts에 요청하며, 차단되면 시스템 글꼴을 사용합니다.

수정 전후 문구는 설명용 예시입니다. 도구별 상태는 2026-11-10의 제한된 검사이며 전 도구의 호환성이나 글쓰기 효과를 보장하지 않습니다. 과거 연구 기록과 설치되는 스킬은 변경하지 않습니다.

랜딩에는 예시, 설치 방법, 날짜가 붙은 도구별 상태를 싣습니다. 검사 방법과 한계는 상세 문서로 연결하고 예시 아래에서 반복하지 않습니다.

한·영 랜딩의 제목·소개·설치 설명·오류 안내는 모두 설명형입니다. 명령형·권유형 문장이나 사용자에게 의무를 부과하는 표현은 쓰지 않습니다.

현재 공개 사이트는 Vercel의 `rhizome / human-readable-writing` 프로젝트에 있습니다. [영문](https://human-readable-writing.vercel.app/)과 [한국어](https://human-readable-writing.vercel.app/ko/)를 실제 주소에서 확인했습니다. 배포에는 공개 HTML과 에셋만 포함하며, 연구 기록·설치 스킬·검사용 스크립트는 제외합니다. Git 자동 배포는 연결하지 않았습니다.

추가 공개 배포에는 별도 승인이 필요합니다. 위의 CLI 명령은 프리뷰를 만들며, 승인된 공개 업데이트에는 `--prod`를 사용합니다. GitHub Pages workflow는 실행하지 않았고 수동 실행 방식으로 남아 있습니다.
