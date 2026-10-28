# NG COUVREUR — site vitrine

Couvreur à Propriano, Corse-du-Sud · 07 44 81 79 45

**Site en ligne :** https://rockandberg.github.io/mediavote-preview/ng-couvreur/site/

> Le site est en `noindex` tant qu'il n'est pas sur son domaine définitif
> (`PREVIEW` dans `build/build.py`, surchargeable par `NG_PREVIEW=0`).

---

## Organisation

| Chemin | Rôle |
|---|---|
| `build/build.py` | Générateur du site. Source unique : navigation, prestations, communes, conseils, SEO, sitemap. |
| `build/site.css` | Système graphique. |
| `build/site.js` | Menu mobile, apparition au scroll, validation du formulaire. |
| `build/optimize-images.py` | Fabrique les dérivés web depuis la banque d'images. |
| `site/` | Site généré. **Ne pas éditer à la main** : le build l'écrase. |
| `docs/` | Bible visuelle, shot list, prompts, manifeste des visuels. |
| `banque-ng-couvreur.html` | Page de référence de la banque d'images. |

## Fabriquer le site

```bash
python3 -m pip install Pillow pillow-avif-plugin
python3 ng-couvreur/build/optimize-images.py   # visuels → site/assets/img/
python3 ng-couvreur/build/build.py             # pages HTML
```

L'ordre compte : `build.py` préserve `site/assets/img/`, mais efface tout le reste.

## Déploiement

`.github/workflows/deploy-pages.yml` publie le dépôt entier sur GitHub Pages
à chaque poussée sur `main` : optimisation des visuels, génération des pages,
contrôles, puis publication. **Le site Media Vote reste servi à la racine, sans
transformation.**

Le cache des originaux et les scripts de fabrication sont retirés avant
publication.

## Modifier le contenu

| Pour… | Éditer dans `build/build.py` |
|---|---|
| Retirer ou ajouter une prestation | la table `SERVICES` (§3) — répercuté partout |
| Ajouter une commune | la table `COMMUNES` (§4) ; renseigner `page` crée une page locale |
| Ajouter un conseil | la table `CONSEILS` (§4) |
| Changer un texte alternatif | la table `ALT` (§2) |
| Recadrer un visuel | la table `FOCUS` — `object-position` par image |
| Changer la boîte de réception | `FORM_TO` (§13) |
| Activer le captcha FormSubmit | `FORM_CAPTCHA = True` (§13) — si du spam passe |

## Reste à faire avant la mise en ligne définitive

1. **Formulaire de devis** — relié à FormSubmit. La première soumission
   déclenche un e-mail d'activation à valider une fois, sans quoi rien n'est
   transmis. Remplacer ensuite `FORM_TO` par l'alias fourni par FormSubmit.

   Protections anti-robots : l'adresse d'envoi est absente du HTML et
   reconstituée en JavaScript ; le bouton n'est armé qu'à ce moment ; un
   délai minimum de 3 s est imposé ; un pot de miel (`_honey`) est vérifié
   par FormSubmit. Si du spam finit par passer, `FORM_CAPTCHA = True`
   active le captcha FormSubmit, seule protection vérifiée côté serveur.
2. **Mentions légales** — SIRET, forme juridique, adresse du siège, hébergeur,
   assurance décennale et médiateur sont marqués « à compléter ».
3. **Domaine** — renseigner `SITE_ORIGIN` et passer `PREVIEW` à `False`.
