<p align="center">
  <img src="assets/readme-header.svg" alt="Human-readable writing — conserver les termes, clarifier les relations." width="100%">
</p>

<p align="center">
  <strong>Un skill pour rédiger des textes techniques clairs et précis.</strong><br>
  Conçu pour Codex et Claude Code.
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.ko.md">한국어</a> · <strong>Français</strong> · <a href="README.zh-CN.md">中文（简体）</a> · <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <a href="#démarrage-rapide">Démarrage rapide</a> ·
  <a href="MANIFEST.md">Principes de rédaction</a> ·
  <a href="#installation">Installation</a> ·
  <a href="#langues">Langues</a> ·
  <a href="#éléments-probants-et-limites">Éléments probants</a>
</p>

---

Précisez qui a fait quoi, dans quelles conditions, et ce que les éléments disponibles permettent d’affirmer. Utilisez ce skill pour les descriptions de pull requests, les points de situation sur un incident, les notes de recherche et les consignes d’exploitation.

## Les mêmes faits, plus faciles à suivre

Cet exemple illustratif est adapté d’un [cas de rédaction conservé en coréen](research/structure-layout-responses.json). Il ne s’agit ni d’une nouvelle mesure ni d’un test de préférence en anglais.

**Avant**

> L’évaluateur a indiqué une erreur médiane de 0,8 m sur 68 des 80 sessions, en excluant les 12 qui avaient dépassé le délai imparti ; les erreurs des sessions ayant dépassé ce délai n’ont pas été calculées.

**Après**

> Sur les 80 sessions, 12 ont dépassé le délai imparti. L’évaluateur a indiqué une erreur médiane de 0,8 m sur les 68 sessions restantes.
>
> Les erreurs des 12 sessions ayant dépassé le délai imparti n’ont pas été calculées.

La reformulation distingue explicitement le groupe mesuré du groupe exclu, tout en préservant les chiffres et les limites.

## Démarrage rapide

Une fois le skill installé, invoquez-le en joignant le texte à retravailler.

**Codex**

```text
$human-readable-writing Retravaille cette description de pull request pour la personne qui assure la maintenance du projet.
Préserve les termes techniques, les faits, les conditions et l’incertitude.
```

**Claude Code**

```text
/human-readable-writing Clarifie ce point de situation sur un incident.
Distingue les observations, les causes possibles et les affirmations non vérifiées.
```

Lors de son invocation, le skill lit [MANIFEST.md](MANIFEST.md) et réutilise les consignes déjà présentes dans le contexte. Il produit le texte dans la langue demandée ; lors d’une révision, il conserve la langue de la source, sauf si vous demandez une traduction.

## Ce que le skill améliore

| Point à examiner | Amélioration proposée |
|---|---|
| Accumulations de noms | Expliciter les acteurs, les actions et les relations. |
| Incises et conditions imbriquées | Rendre l’énoncé principal facile à suivre et regrouper les conditions liées. |
| Comparaisons entre plusieurs conditions | Utiliser un tableau s’il facilite la comparaison ; conserver les unités, le périmètre et les réserves. |
| Consignes d’exploitation | Commencer par l’état actuel et la décision ou l’action nécessaire, puis en expliquer les raisons. |
| Interprétation des recherches | Relier les observations au jugement formulé et à ses limites. |

**Ce qui reste intact :** les noms techniques, les identifiants, les quantités, les unités, les exclusions, les négations, ainsi que ce sur quoi porte l’incertitude et son degré. Les relations manquantes restent indéterminées tant que la source ne permet pas de les établir.

Les paragraphes suivent le raisonnement et le format demandé. Aucune règle d’une phrase par paragraphe n’est imposée à toutes les langues ou à tous les types de documents.

## Installation

Clonez le dépôt avec un compte qui y a accès. Exécutez les commandes de création des liens **depuis la racine du dépôt**, en vous assurant que les deux chemins de destination du skill sont libres.

```sh
git clone https://github.com/JangHyun-bin/human-readable-writing.git
cd human-readable-writing

mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$PWD" "$HOME/.agents/skills/human-readable-writing"
ln -s "$PWD" "$HOME/.claude/skills/human-readable-writing"
```

Les deux outils lisent la même copie locale du dépôt. Si vous l’avez déjà cloné, exécutez uniquement les commandes `mkdir` et `ln` depuis ce répertoire.

<details>
<summary><strong>Paramètres des outils et invocation explicite</strong></summary>

| Outil | Point d’entrée | Règle d’invocation |
|---|---|---|
| Codex | `~/.agents/skills/human-readable-writing/SKILL.md` | `agents/openai.yaml` contient `allow_implicit_invocation: false`. |
| Claude Code | `~/.claude/skills/human-readable-writing/SKILL.md` | Intégrez le paramètre `skillOverrides` ci-dessous au fichier de paramètres existant. |

Conservez les autres paramètres de `~/.claude/settings.json` lors de l’ajout :

```json
{
  "skillOverrides": {
    "human-readable-writing": "user-invocable-only"
  }
}
```

Les sessions dans le cloud qui ne peuvent pas lire les répertoires locaux des skills nécessitent une installation distincte. Consultez les instructions relatives aux skills personnels pour [Codex](https://learn.chatgpt.com/docs/build-skills) et [Claude Code](https://code.claude.com/docs/en/skills).

</details>

<details>
<summary><strong>L’essai personnel et distinct d’un noyau de consignes globales</strong></summary>

L’environnement personnel du responsable du projet comprend aussi un noyau de consignes plus ancien et compact, rédigé en coréen et intégré aux instructions globales. La création des liens symboliques ci-dessus n’installe pas ce noyau.

Ce noyau a été activé le 2026-10-29 dans `~/.agents/TERMINOLOGY.md`, via les chemins d’instructions existants de Codex et de Claude Code. Il n’a pas été modifié. Sa taille de 61 tokens est un décompte de référence obtenu avec `o200k_base`, pas une garantie sur la consommation totale d’une requête.

Le [compte rendu de l’essai initial](research/native-pilot.md), en coréen, contient l’historique de l’installation locale et les commandes permettant de revenir en arrière. Le skill conçu d’abord en anglais constitue une couche distincte, utilisable uniquement sur invocation explicite.

</details>

## Langues

L’anglais reste la langue de référence pour la rédaction du skill, de ses exemples et de sa documentation publique. L’ordre de priorité des langues guide le développement et la validation ; il ne remplace pas la langue que vous demandez.

| Priorité | Langue | Périmètre actuel |
|---|---|---|
| 1 | Anglais | Instructions, documentation et exemples de référence, ainsi que vérifications du fonctionnement. L’évaluation par des lecteurs natifs reste à faire. |
| 2 | Coréen | [Guide en coréen](README.ko.md), consignes linguistiques ciblées et résultats de l’essai personnel existant. |
| 3 | Français | [README en français](README.fr.md) disponible. Les consignes propres à la langue et la validation des textes produits sont prévues, mais restent à réaliser. |
| 4 | Chinois simplifié | [README en chinois simplifié](README.zh-CN.md) disponible. Les consignes propres à la langue et la validation des textes produits sont prévues, mais restent à réaliser. |
| 4 | Japonais | [README en japonais](README.ja.md) disponible. Les consignes propres à la langue et la validation des textes produits sont prévues, mais restent à réaliser. |
| 4 | Autres langues | Prévues ; la traduction de la documentation et la validation propre à chaque langue ne sont pas achevées. |

Les cinq README décrivent le même parcours d’installation et d’utilisation. Les instructions communes destinées aux agents restent en anglais ; la documentation traduite ne démontre pas que les textes produits atteignent la qualité attendue d’un locuteur natif.

Le document sur la [prise en charge des langues et les critères de validation](docs/language-support.md), en anglais, distingue la traduction de la documentation, le comportement observé de l’agent et la validation par des lecteurs natifs.

## Éléments probants et limites

**Il s’agit d’un outil de rédaction personnel en cours d’évolution.** Les consignes associent des idées issues de la littérature à des préférences de révision consignées. Aucune amélioration de la compréhension humaine ou du temps de lecture n’a été établie.

| Éléments disponibles | Ce qu’ils permettent d’affirmer |
|---|---|
| [Vérification du fonctionnement de la version conçue d’abord en anglais](docs/language-support.md#workflow-check) (en anglais) | Vérifications limitées du choix de la langue, du format demandé et de la fidélité à la source ; elles ne prouvent pas une qualité équivalente à celle d’un locuteur natif. |
| [Cinq comparaisons de documents en coréen](research/native-pilot.md#2026-10-30-다섯-편집-비교의-최종-집계) | Préférences d’un seul utilisateur concernant les paragraphes, les tableaux et l’ordre des informations. |
| [12 générations de mises en page](research/layout-generation-pilot.md) | L’adoption a été reportée après la découverte d’affirmations de vérification sans fondement et d’altérations de l’incertitude. |
| [Quatre générations évaluées pour leur fidélité à la source](research/source-fidelity-pilot.md) | Les deux variantes ont satisfait aux critères ; la supériorité de la version révisée n’a pas été établie. |
| [Six cas avec le noyau révisé](research/source-fidelity-six-audit.json) | Les six cas ont satisfait aux critères de sens et de format de l’agent ; aucune variante de comparaison n’a été évaluée en parallèle. |

Les études de génération antérieures portaient sur des textes techniques en coréen. Leur noyau révisé expérimental de 93 tokens est distinct du noyau global de 61 tokens et du manifeste complet. Leurs résultats ne valident pas le nouveau skill conçu d’abord en anglais.

## Pour aller plus loin

| Objectif | Documents |
|---|---|
| Consignes de rédaction communes | [Manifeste](MANIFEST.md) · [Point d’entrée du skill](SKILL.md) |
| Consignes propres à chaque langue | [Coréen](references/korean.md) · [Périmètre et validation, en anglais](docs/language-support.md) |
| Analyse de l’article d’origine, en coréen | [Analyse](ANALYSIS.md) · [Examen des éléments probants](research/evidence-review.md) |
| Littérature connexe et applications, en coréen | [Notes de lecture](research/related-literature.md) · [Application à deux articles](research/two-paper-application.md) |
| Études antérieures sur les coûts et les durées, en coréen | [Coût d’invocation](research/invocation-cost.md) · [Comparaison à budget fixe](research/core-refinement.md) · [Textes anonymisés pour l’évaluation à l’aveugle](research/core-refinement-blind.md) |
| Historique des validations et des préférences, en coréen | [Journal de validation](VALIDATION.md) · [Préférences de mise en page](research/structure-layout-pilot.md) |

Même lorsqu’elles n’exigent aucune lecture de fichier supplémentaire, les consignes consomment des tokens en entrée. Les anciennes mesures de tokens et de latence ne mesurent pas le coût de cette révision.

---

Ce projet est né d’une analyse de l’article [Why is AI-generated language so hard to understand?](https://arxiv.org/abs/2610.29162v1) de Thomas Hikaru Clark, Matias B. Martin et Kyle Mahowald. Ses consignes de rédaction et ses exemples sont des propositions pratiques distinctes, et non des interventions validées ou approuvées par les auteurs de l’article.

L’article d’origine est disponible sous licence CC BY 4.0. Le [document d’attribution](NOTICE.md), en coréen, précise les sources et leurs licences respectives. **Ce dépôt ne dispose pas encore d’une licence de distribution propre.**
