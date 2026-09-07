# NG COUVREUR — Banque visuelle du site web

Phase 1 : conception et production de la bibliothèque photographique.
Aucun travail de design ou de développement du site n'est engagé à ce stade.

## Contenu

| Fichier | Objet |
|---|---|
| `docs/00-bible-visuelle.md` | Bible visuelle NG Couvreur — 15 sections de paramètres imposés |
| `docs/01-shot-list.md` | Shot list des 28 visuels, par catégorie A→K |
| `docs/02-prompts-higgsfield.md` | Les 28 prompts de génération définitifs, tels qu'exécutés |
| `docs/03-manifeste-images.csv` | Correspondance n° / nom / ratio / job_id / URL du fichier 2K |
| `banque-ng-couvreur.html` | Page de référence navigable (bible + shot list + accès aux fichiers) |

## Production

Plateforme : **Higgsfield** · Modèle : `nano_banana_pro` · Résolution : `2k`
28 visuels générés, dont 2 ancres d'identité du personnage récurrent.

Cohérence du personnage : l'ancre `00A` fixe le visage, la carrure et la tenue du
couvreur ; son `job_id` est passé en `image_references` sur les 14 visuels où il est
reconnaissable. Les deux paires avant/après (11 → 13 et 21 → 23) sont générées en
injectant l'image AVANT comme référence, afin que la maison, le cadrage et la lumière
restent identiques d'un volet à l'autre.

## Fichiers image

Les PNG 2K sont hébergés sur le CDN Higgsfield. Leurs URLs figurent dans
`docs/03-manifeste-images.csv` et sont accessibles depuis la page de référence.
Ils ne sont pas versionnés ici : le CDN est bloqué par la politique de sortie réseau
de l'environnement d'exécution, le téléchargement n'a donc pas pu être effectué
depuis cette session.

## Étape suivante

Sélection et validation des visuels, puis conception du site web autour de la banque.
