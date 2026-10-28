#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NG COUVREUR — générateur du site vitrine.

Source unique de vérité : toute la navigation, la liste des prestations, les
visuels, le maillage interne, le sitemap et les données structurées sont
dérivés des tables ci-dessous.

    python3 ng-couvreur/build/build.py

Retirer une prestation  : supprimer son entrée de SERVICES (§3).
Passer en production    : PREVIEW = False et renseigner SITE_ORIGIN (§1).
Basculer les images     : IMAGES_LOCAL = True une fois les fichiers dans
                          site/assets/img/ (§2).
"""

import base64, csv, html, os, re, shutil, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)          # ng-couvreur/
OUT  = os.path.join(ROOT, "site")     # ng-couvreur/site/

# ---------------------------------------------------------------------------
# §1  CONFIGURATION
# ---------------------------------------------------------------------------
# Surchargeables par l'environnement, pour que la CI construise aux bonnes URLs
# sans modifier ce fichier.
PREVIEW      = os.environ.get("NG_PREVIEW", "1") != "0"
SITE_ORIGIN  = os.environ.get("NG_SITE_ORIGIN", "https://www.ngcouvreur.fr").rstrip("/")
BASE         = os.environ.get("NG_BASE", "/mediavote-preview/ng-couvreur/site").rstrip("/")

NOM       = "NG Couvreur"
VILLE     = "Propriano"
DEPT      = "Corse-du-Sud"
TEL_TXT   = "07 44 81 79 45"
TEL_HREF  = "tel:+33744817945"
TEL_E164  = "+33744817945"

# Point de bascule des visuels : CDN Higgsfield → fichiers locaux
IMAGES_LOCAL = True
CDN_ORIGIN   = "https://d8j0ntlcm91z4.cloudfront.net"

# ---------------------------------------------------------------------------
# §2  VISUELS — banque produite en phase 1
# ---------------------------------------------------------------------------
DIMS = {"16:9": (2752, 1536), "3:2": (2528, 1696), "1:1": (2048, 2048), "3:4": (1792, 2400)}

ALT = {
 "01": "Couvreur de NG Couvreur posant une tuile canal sur une toiture à Propriano",
 "02": "Maison corse avec toiture en tuiles canal entièrement rénovée près de Propriano",
 "03": "Couvreur sur le faîtage d'une toiture, collines de Corse-du-Sud en arrière-plan",
 "04": "Vue d'ensemble d'une toiture rénovée en tuiles canal avec noue et solin en zinc",
 "05": "Portrait du couvreur de NG Couvreur sur un chantier à Propriano",
 "06": "Couvreur préparant une feuille de zinc sur tréteaux avant intervention",
 "07": "Mains du couvreur scellant une tuile canal dans un lit de mortier de chaux",
 "08": "Pose de couverture en tuiles canal sur liteaux et écran de sous-toiture",
 "09": "Couvreur transportant des tuiles canal sur le plancher d'un échafaudage",
 "10": "Toiture en tuiles canal terminée, intégrée aux toits voisins d'un village corse",
 "11": "Toiture ancienne dégradée avant rénovation : tuiles déplacées et faîtage abîmé",
 "12": "Rénovation de toiture en cours : chevrons, écran de sous-toiture et liteaunage neufs",
 "13": "La même toiture après rénovation complète en tuiles canal",
 "14": "Couvreur inspectant une toiture pour localiser une fuite",
 "15": "Réparation localisée d'une toiture : remplacement de tuiles cassées",
 "16": "Solin de cheminée défaillant et tuile fissurée à l'origine d'une infiltration",
 "17": "Pose d'une membrane d'étanchéité bitumineuse sur un toit-terrasse",
 "18": "Détail d'un relevé d'étanchéité en pied d'acrotère avec bande de solin en zinc",
 "19": "Pose d'une gouttière demi-ronde en zinc sur crochets le long de l'égout",
 "20": "Détail d'une noue en zinc avec joint soudé à l'étain",
 "21": "Toiture envahie par la mousse et le lichen avant démoussage",
 "22": "Nettoyage basse pression d'une toiture en tuiles canal",
 "23": "La même toiture après nettoyage et démoussage",
 "24": "Faîtage en tuiles faîtières scellées au mortier de chaux",
 "25": "Outils de couvreur posés sur une toiture en tuiles canal",
 "26": "Rue résidentielle de la région de Propriano et ses toitures en tuiles canal",
 "27": "Toiture corse au premier plan et arrière-pays du golfe du Valinco",
 "28": "Couvreur rangeant son matériel en fin de chantier en Corse-du-Sud",
}

def load_images():
    imgs = {}
    path = os.path.join(ROOT, "docs", "03-manifeste-images.csv")
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            n = row["num"]
            if n not in ALT:
                continue
            w, h = DIMS[row["ratio"]]
            imgs[n] = {
                "cdn": row["url"], "w": w, "h": h, "ratio": row["ratio"],
                "alt": ALT[n], "name": row["nom"],
                "stem": "%s/assets/img/%s-%s" % (BASE, n, row["nom"]),
            }
    missing = sorted(set(ALT) - set(imgs))
    if missing:
        raise SystemExit("Visuels absents du manifeste : %s" % ", ".join(missing))
    return imgs

IMG = load_images()

def e(s):
    return html.escape(str(s), quote=True)

# Échelles de largeurs — doivent rester identiques à celles de optimize-images.py
LADDERS = {
    "16:9": [640, 960, 1280, 1920, 2560],
    "3:2":  [480, 720, 960, 1440, 1920],
    "1:1":  [400, 600, 800, 1200],
    "3:4":  [480, 720, 960, 1200],
}
FALLBACK_W = {"16:9": 1280, "3:2": 960, "1:1": 800, "3:4": 720}

# Recadrage : où doit rester le sujet quand la photo est rognée (mobile surtout).
# Par défaut le centre ; ces visuels ont leur sujet ailleurs.
FOCUS = {
    "01": "62% 55%",   # couvreur assis en bas à droite
    "03": "70% 50%",   # artisan sur le tiers droit
    "22": "68% 45%",   # lance et limite de propreté en haut à droite
    "28": "30% 55%",   # artisan et fourgon sur le tiers gauche
    "09": "40% 50%",
    "27": "50% 65%",   # toiture au premier plan
}

_WIDTHS_CACHE = {}

def available_widths(num):
    """Largeurs réellement disponibles sur le disque.

    Le srcset ne doit jamais être déduit de dimensions supposées : il se lit
    sur les fichiers que optimize-images.py a effectivement produits. Sinon le
    HTML référence des variantes qui n'existent pas et le navigateur affiche
    une image cassée.
    """
    if num in _WIDTHS_CACHE:
        return _WIDTHS_CACHE[num]
    d = IMG[num]
    folder = os.path.join(OUT, "assets", "img")
    got = []
    for w in LADDERS[d["ratio"]]:
        base = os.path.join(folder, "%s-%s-%d" % (num, d["name"], w))
        if all(os.path.exists(base + "." + ext) for ext in ("avif", "webp", "jpg")):
            got.append(w)
    if not got:
        # Aucune variante sur le disque : on retombe sur l'échelle théorique,
        # pour que le build reste utilisable sans passe d'optimisation.
        got = [w for w in LADDERS[d["ratio"]] if w <= d["w"]]
    _WIDTHS_CACHE[num] = got
    return got

def srcset(num, ext):
    d = IMG[num]
    return ", ".join("%s-%d.%s %dw" % (e(d["stem"]), w, ext, w) for w in available_widths(num))

def img_tag(num, cls="", sizes="100vw", eager=False):
    """<picture> complet : AVIF, puis WebP, puis JPEG en dernier recours."""
    d = IMG[num]
    if not IMAGES_LOCAL:
        return ('<img src="%s" alt="%s" width="%d" height="%d" decoding="async" %s%s>'
                % (e(d["cdn"]), e(d["alt"]), d["w"], d["h"],
                   'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"',
                   (' class="%s"' % e(cls)) if cls else ""))

    widths = available_widths(num)
    target = FALLBACK_W[d["ratio"]]
    fw = min(widths, key=lambda w: (abs(w - target), w))
    fh = round(d["h"] * fw / d["w"])
    style = ""
    if num in FOCUS:
        style = ' style="object-position:%s"' % FOCUS[num]
    loading = ('loading="eager" fetchpriority="high"' if eager
               else 'loading="lazy" fetchpriority="low"')
    return (
        '<picture>'
        '<source type="image/avif" srcset="%s" sizes="%s">'
        '<source type="image/webp" srcset="%s" sizes="%s">'
        '<img src="%s-%d.jpg" srcset="%s" sizes="%s" alt="%s" '
        'width="%d" height="%d" decoding="async" %s%s%s>'
        '</picture>'
    ) % (srcset(num, "avif"), e(sizes),
         srcset(num, "webp"), e(sizes),
         e(d["stem"]), fw, srcset(num, "jpg"), e(sizes), e(d["alt"]),
         fw, fh, loading,
         (' class="%s"' % e(cls)) if cls else "", style)

ARROW = ('<svg width="15" height="10" viewBox="0 0 15 10" fill="none" aria-hidden="true">'
         '<path d="M0 5h13M9.5 1 13.5 5 9.5 9" stroke="currentColor" stroke-width="1.8"/></svg>')
PHONE_ICON = ('<svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
              '<path d="M3.7 1.2a1.2 1.2 0 0 0-1.6.1L1.4 2c-.7.8-.8 2 0 3.5C2.3 7.4 4 9.4 6 10.9c1.9 1.5 3.9 2.4 5.2 2.4'
              '.7 0 1.3-.2 1.7-.7l.7-.7a1.2 1.2 0 0 0-.1-1.7l-2-1.6a1.2 1.2 0 0 0-1.6.1l-.6.7c-.9-.4-1.8-1-2.6-1.8'
              'S5.4 5.9 5 5l.7-.6a1.2 1.2 0 0 0 .1-1.6l-2-1.6Z"/></svg>')

# ---------------------------------------------------------------------------
# §3  PRESTATIONS — retirer une entrée suffit à la supprimer partout
# ---------------------------------------------------------------------------
SERVICES = [
 {"slug":"couverture-toiture", "nav":"Couverture & toiture",
  "h1":"Couverture &amp; toiture",
  "court":"Travaux de couverture et interventions sur votre toiture.",
  "img":"08", "hero":"10",
  "title":"Couvreur à Propriano — travaux de couverture et toiture | NG Couvreur",
  "meta":"NG Couvreur réalise vos travaux de couverture et de toiture à Propriano et en Corse-du-Sud. Devis sur demande, %s." % TEL_TXT,
  "intro":"Poser ou reprendre une couverture, c'est remettre en ordre tout ce qui protège la maison : le support, l'écran, le liteaunage, puis les tuiles. Nous intervenons sur les toitures de Propriano et du sud de la Corse.",
  "blocs":[
    ("Ce que nous faisons",
     ["Pose de couverture neuve en tuiles canal ou en tuiles plates.",
      "Reprise partielle d'une couverture existante.",
      "Remplacement de l'écran de sous-toiture et du liteaunage.",
      "Traitement des points singuliers : faîtage, rives, noues, solins de cheminée."]),
    ("Comment nous travaillons",
     ["Nous regardons d'abord l'état du support avant de parler tuiles : une couverture posée sur une charpente ou un liteaunage fatigué ne tient pas.",
      "Nous réemployons les tuiles saines quand leur état le permet, pour garder la teinte du bâti existant.",
      "Le chantier est protégé et l'accès en hauteur sécurisé pendant toute la durée des travaux."]),
  ],
  "gallery":[("09","Manutention des tuiles sur le plancher d'échafaudage."),
             ("24","Faîtage scellé au mortier de chaux.")],
 },
 {"slug":"renovation-toiture", "nav":"Rénovation",
  "h1":"Rénovation de toiture",
  "court":"Rénovation partielle ou complète selon l'état de la couverture.",
  "img":"12", "hero":"04",
  "title":"Rénovation de toiture à Propriano et en Corse-du-Sud | NG Couvreur",
  "meta":"Rénovation partielle ou complète de toiture à Propriano et en Corse-du-Sud. NG Couvreur évalue l'état de votre couverture. %s." % TEL_TXT,
  "intro":"Toutes les toitures fatiguées ne se refont pas entièrement. Nous regardons l'état réel de la couverture avant de proposer une reprise partielle ou une rénovation complète.",
  "blocs":[
    ("Quand une rénovation s'impose",
     ["Des tuiles glissent ou se cassent régulièrement, rang après rang.",
      "Le faîtage se désagrège et laisse passer l'eau.",
      "La couverture se creuse ou ondule, signe que le support travaille.",
      "Les infiltrations reviennent malgré des réparations ponctuelles."]),
    ("Deux niveaux d'intervention",
     ["Rénovation partielle : reprise d'un pan, d'un versant ou d'une zone dégradée, en conservant le reste de la couverture.",
      "Rénovation complète : dépose de l'ancienne couverture, mise en place d'un écran de sous-toiture et d'un liteaunage neufs, puis repose."]),
  ],
  "sequence":[("11","Avant","Tuiles déplacées, faîtage désagrégé, couverture qui se creuse."),
              ("12","Pendant","Dépose, écran de sous-toiture et liteaunage neufs, repose des tuiles."),
              ("13","Après","Couverture remise à plat, faîtage refait, évacuations reprises.")],
  "gallery":[],
 },
 {"slug":"reparation-fuite", "nav":"Réparation & fuite",
  "h1":"Réparation &amp; recherche de fuite",
  "court":"Recherche de fuite et réparation des éléments endommagés.",
  "img":"14", "hero":"14",
  "title":"Recherche de fuite et réparation de toiture à Propriano | NG Couvreur",
  "meta":"Recherche de fuite et réparation de toiture à Propriano et en Corse-du-Sud. NG Couvreur localise l'origine de l'infiltration. %s." % TEL_TXT,
  "intro":"Une trace au plafond apparaît rarement à l'aplomb du défaut : l'eau circule sous les tuiles avant de se voir. La première étape est donc de localiser l'origine réelle de l'infiltration.",
  "blocs":[
    ("Où se situent le plus souvent les fuites",
     ["Au raccord entre la couverture et une cheminée, quand le solin a bougé.",
      "En noue, à la jonction de deux pans de toiture.",
      "Sur une tuile fissurée ou déplacée par le vent.",
      "Au niveau d'une gouttière débordante qui rejette l'eau contre le mur."]),
    ("Notre façon de procéder",
     ["Nous inspectons la couverture et les points singuliers avant de démonter quoi que ce soit.",
      "Nous soulevons les tuiles nécessaires pour vérifier l'écran et le support en dessous.",
      "Nous réparons la cause identifiée, pas seulement la trace visible."]),
  ],
  "gallery":[("16","Solin défaillant et tuile fissurée à l'origine d'une infiltration."),
             ("15","Remplacement localisé des tuiles endommagées.")],
 },
 {"slug":"etancheite", "nav":"Étanchéité",
  "h1":"Étanchéité",
  "court":"Solutions pour protéger la toiture contre les infiltrations.",
  "img":"17", "hero":"17",
  "title":"Étanchéité de toiture et toit-terrasse à Propriano | NG Couvreur",
  "meta":"Travaux d'étanchéité de toiture et de toit-terrasse à Propriano et en Corse-du-Sud. NG Couvreur. %s." % TEL_TXT,
  "intro":"Sur un toit-terrasse ou une surface plane, l'eau ne s'écoule pas d'elle-même : c'est la continuité du revêtement et la qualité des relevés qui font l'étanchéité.",
  "blocs":[
    ("Nos interventions",
     ["Pose de membrane d'étanchéité sur toit-terrasse.",
      "Reprise d'une étanchéité existante fissurée, décollée ou boursouflée.",
      "Traitement des relevés en pied d'acrotère et des points de pénétration.",
      "Reprise des évacuations d'eaux pluviales."]),
    ("Les points qui font la différence",
     ["Un relevé doit remonter suffisamment haut et être arrêté proprement en tête.",
      "Les recouvrements entre lés doivent être continus et soudés sur toute leur longueur.",
      "Une étanchéité qui retient l'eau au lieu de l'évacuer finira toujours par céder."]),
  ],
  "gallery":[("18","Relevé d'étanchéité en pied d'acrotère : gorge, bande de solin, arrêt en tête.")],
 },
 {"slug":"zinguerie-gouttieres", "nav":"Zinguerie & gouttières",
  "h1":"Zinguerie &amp; gouttières",
  "court":"Pose, entretien et réparation des éléments d'évacuation des eaux.",
  "img":"19", "hero":"19",
  "title":"Zinguerie et gouttières à Propriano et en Corse-du-Sud | NG Couvreur",
  "meta":"Pose et réparation de gouttières, noues et solins en zinc à Propriano et en Corse-du-Sud. NG Couvreur. %s." % TEL_TXT,
  "intro":"La zinguerie conduit l'eau hors de la toiture et loin des murs. C'est une part discrète du métier, et souvent celle qui explique une infiltration.",
  "blocs":[
    ("Ce que nous posons et réparons",
     ["Gouttières et chéneaux : pose, remplacement, remise en pente.",
      "Descentes d'eaux pluviales et raccordements.",
      "Noues en zinc entre deux pans de toiture.",
      "Solins et bandes de rive au raccord des cheminées et des murs."]),
    ("Pourquoi la pente compte",
     ["Une gouttière posée à l'horizontale stagne, se charge de dépôts et déborde.",
      "Les crochets doivent suivre une ligne légèrement descendante vers la descente.",
      "Un joint soudé correctement essuyé tient bien plus longtemps qu'un joint collé."]),
  ],
  "gallery":[("20","Noue en zinc, joint soudé à l'étain, tuiles coupées au cordeau.")],
 },
 {"slug":"nettoyage-demoussage", "nav":"Nettoyage & démoussage",
  "h1":"Nettoyage &amp; démoussage",
  "court":"Entretien permettant de préserver la toiture.",
  "img":"22", "hero":"22",
  "title":"Nettoyage et démoussage de toiture à Propriano | NG Couvreur",
  "meta":"Nettoyage et démoussage de toiture à Propriano et en Corse-du-Sud. NG Couvreur entretient votre couverture. %s." % TEL_TXT,
  "intro":"La mousse retient l'eau dans les canaux, garde l'humidité contre la terre cuite et finit par charger la toiture. L'enlever régulièrement prolonge la vie d'une couverture.",
  "blocs":[
    ("Comment nous nettoyons",
     ["Nettoyage basse pression, du faîtage vers l'égout, pour ne jamais pousser l'eau sous les tuiles.",
      "Retrait des dépôts accumulés dans les gouttières et les descentes.",
      "Contrôle des tuiles au passage : une tuile fendue apparaît souvent au nettoyage."]),
    ("Ce que nous ne faisons pas",
     ["Pas de haute pression sur une couverture ancienne : elle décape la terre cuite et déplace les tuiles.",
      "Pas de traitement présenté comme définitif : la mousse revient, l'entretien est périodique."]),
  ],
  "sequence":[("21","Avant","Mousse dans les canaux, lichen sur les tuiles, gouttière encombrée."),
              ("22","Pendant","Nettoyage basse pression, du faîtage vers l'égout."),
              ("23","Après","Couverture dégagée, évacuations libres, tuiles contrôlées.")],
  "gallery":[],
 },
]

# ---------------------------------------------------------------------------
# §4  COMMUNES  et  CONSEILS
# ---------------------------------------------------------------------------
COMMUNES = [
 {"nom":"Propriano",  "cp":"20110", "page":"couvreur-propriano", "note":"Notre point d'ancrage"},
 {"nom":"Sartène",    "cp":"20100", "page":None, "note":""},
 {"nom":"Olmeto",     "cp":"20113", "page":None, "note":""},
 {"nom":"Viggianello","cp":"20110", "page":None, "note":""},
 {"nom":"Serra-di-Ferro","cp":"20140", "page":None, "note":""},
 {"nom":"Porto-Pollo","cp":"20140", "page":None, "note":""},
]

CONSEILS = [
 {"slug":"reconnaitre-fuite-toiture",
  "titre":"Comment reconnaître une fuite de toiture ?",
  "resume":"Les signes qui doivent alerter, et pourquoi la trace au plafond n'indique presque jamais l'endroit du défaut.",
  "img":"14",
  "title":"Comment reconnaître une fuite de toiture ? | NG Couvreur",
  "meta":"Auréole au plafond, humidité dans les combles, enduit qui cloque : les signes d'une fuite de toiture et les réflexes à avoir. Conseils NG Couvreur, Propriano.",
  "corps":[
   ("Les signes visibles depuis l'intérieur",
    "<p>Une fuite se manifeste rarement au moment où elle commence. Le premier indice est souvent une auréole brunâtre au plafond ou en haut d'un mur, dont les contours foncent après chaque pluie. Dans les combles, l'humidité se voit d'abord sur la charpente : un bois qui fonce, une trace de coulure sur un chevron, une odeur de renfermé qui s'installe.</p>"
    "<p>À l'extérieur, l'enduit qui cloque ou se détache sous un débord de toit, une trace verticale sombre sur la façade, une mousse qui se développe toujours au même endroit du mur : ce sont des symptômes d'eau mal évacuée.</p>"),
   ("Pourquoi la trace n'indique pas l'endroit du défaut",
    "<p>C'est le point que l'on nous signale le plus souvent. L'eau entre par un défaut de couverture, puis circule : elle suit la pente de l'écran de sous-toiture, longe un liteau, descend le long d'un chevron, et ne se révèle qu'à l'endroit où elle finit par tomber. Il n'est pas rare que l'entrée d'eau se situe à plusieurs mètres de la tache visible, voire sur un autre versant.</p>"
    "<p>C'est pourquoi une réparation faite à l'aplomb de la tache, sans recherche préalable, échoue souvent : le défaut réel n'a pas été touché.</p>"),
   ("Les origines les plus fréquentes",
    "<ul><li>Un solin de cheminée décollé ou dont le mortier s'est fissuré.</li>"
    "<li>Une noue encombrée ou percée, à la jonction de deux pans.</li>"
    "<li>Une ou plusieurs tuiles fissurées, déplacées par le vent ou par un passage sur le toit.</li>"
    "<li>Une gouttière bouchée qui déborde et rejette l'eau contre le mur ou sous les tuiles de rive.</li>"
    "<li>Un écran de sous-toiture ancien, devenu cassant, qui ne joue plus son rôle de seconde barrière.</li></ul>"),
   ("Ce que vous pouvez faire, et ce qu'il vaut mieux éviter",
    "<p>Repérez le moment où la trace évolue : après une pluie battante, après un vent fort, ou en continu. Cette information est utile, elle oriente déjà la recherche. Photographiez la trace et, si vous y avez accès en sécurité, les combles. Videz ce qui est accessible depuis le sol dans les gouttières.</p>"
    "<p>En revanche, ne montez pas sur la couverture pour chercher vous-même. Une toiture mouillée ou couverte de mousse est glissante, les tuiles se cassent sous le poids et un pas mal placé transforme un défaut ponctuel en dégât plus large.</p>"),
  ]},
 {"slug":"quand-renover-sa-toiture",
  "titre":"Quand faut-il rénover sa toiture ?",
  "resume":"Les signaux qui font passer d'une réparation ponctuelle à une rénovation, et la différence entre reprise partielle et réfection complète.",
  "img":"11",
  "title":"Quand faut-il rénover sa toiture ? | NG Couvreur",
  "meta":"Réparations qui se répètent, couverture qui se creuse, faîtage désagrégé : les signes qui justifient une rénovation de toiture. Conseils NG Couvreur, Propriano.",
  "corps":[
   ("Le seuil : quand la réparation ne suffit plus",
    "<p>Une tuile cassée se remplace. Deux tuiles cassées par an au même endroit, c'est autre chose : cela signifie que le support bouge, que le liteaunage est fatigué, ou que la couverture a atteint un âge où la terre cuite devient fragile.</p>"
    "<p>Le vrai signal n'est pas un défaut isolé, c'est la répétition. Quand les réparations reviennent chaque hiver, leur cumul finit par coûter plus cher qu'une reprise raisonnée.</p>"),
   ("Les signes qui ne trompent pas",
    "<ul><li>La couverture se creuse ou ondule : le support travaille, le problème est sous les tuiles.</li>"
    "<li>Le faîtage se désagrège, les joints s'ouvrent, de la végétation s'y installe.</li>"
    "<li>Des tuiles glissent régulièrement hors de leur rang.</li>"
    "<li>L'écran de sous-toiture, quand il est visible depuis les combles, se déchire au toucher.</li>"
    "<li>Les infiltrations réapparaissent à des endroits différents.</li></ul>"),
   ("Partielle ou complète ?",
    "<p>Une rénovation partielle est justifiée quand la dégradation est localisée : un versant plus exposé, une zone autour d'une cheminée, un pan qui a subi un dégât. On reprend la zone, on conserve le reste.</p>"
    "<p>Une rénovation complète s'impose quand le support ou l'écran sont en cause sur l'ensemble de la toiture. On dépose alors la couverture, on remet un écran de sous-toiture et un liteaunage neufs, puis on repose — en réemployant les tuiles saines lorsque leur état le permet, ce qui préserve la teinte du bâti.</p>"),
   ("Le bon moment dans l'année",
    "<p>En Corse-du-Sud, la fenêtre la plus confortable va du printemps au début de l'automne : temps sec, journées longues, et surtout une couverture ouverte qui ne risque pas de prendre la pluie. Anticiper une rénovation hors urgence permet aussi de programmer le chantier sereinement plutôt que dans la précipitation d'un épisode pluvieux.</p>"),
  ]},
 {"slug":"demoussage-toiture-corse",
  "titre":"Quand et comment démousser une toiture en Corse ?",
  "resume":"Pourquoi la mousse s'installe, à quelle fréquence intervenir, et pourquoi la haute pression est à proscrire sur une couverture ancienne.",
  "img":"21",
  "title":"Quand et comment démousser une toiture en Corse ? | NG Couvreur",
  "meta":"Fréquence, méthode et précautions pour le démoussage d'une toiture en tuiles canal en Corse-du-Sud. Conseils NG Couvreur, Propriano.",
  "corps":[
   ("Pourquoi la mousse s'installe",
    "<p>La mousse a besoin d'humidité qui stagne et de peu de soleil. Sur une toiture en tuiles canal, elle se loge d'abord dans les canaux, sur le versant le moins exposé, et sous les arbres. En Corse-du-Sud, l'alternance d'automnes humides et d'étés très secs favorise aussi le lichen, cette croûte grise qui s'accroche directement à la terre cuite.</p>"
    "<p>Le problème n'est pas esthétique. La mousse retient l'eau contre la tuile, la maintient humide, et gêne l'écoulement. Les dépôts qu'elle libère finissent par encombrer les gouttières et les descentes.</p>"),
   ("À quelle fréquence intervenir",
    "<p>Il n'existe pas de règle universelle : tout dépend de l'exposition, de la végétation autour et de l'âge de la couverture. Un contrôle visuel une fois par an, depuis le sol, suffit à voir si les canaux se garnissent. Une toiture ombragée demande une attention plus régulière qu'une toiture plein sud et dégagée.</p>"
    "<p>Le bon réflexe est de faire coïncider le nettoyage avec un contrôle de la couverture : c'est au moment où l'on dégage les tuiles que les fissures et les tuiles déplacées apparaissent.</p>"),
   ("La haute pression abîme les toitures anciennes",
    "<p>C'est l'erreur la plus courante. Un jet haute pression décape la surface de la terre cuite, la rend plus poreuse et donc plus accueillante pour la mousse suivante. Il déplace les tuiles, casse les plus fragiles, et peut projeter l'eau sous la couverture s'il est dirigé vers le haut de la pente.</p>"
    "<p>Un nettoyage correct se fait à basse pression, en travaillant toujours du faîtage vers l'égout, jamais l'inverse. Le rythme est plus lent, le résultat tient mieux et la couverture n'est pas fragilisée.</p>"),
   ("Ne montez pas seul sur votre toiture",
    "<p>Une toiture mouillée et couverte de mousse est l'une des surfaces les plus glissantes qui soient. Les accidents domestiques en hauteur sont fréquents et graves. L'accès se fait avec une échelle de toit correctement engagée sur le faîtage et un dispositif d'assurage — pas depuis une échelle simple posée contre la gouttière.</p>"),
  ]},
]

# ---------------------------------------------------------------------------
# §5  NAVIGATION
# ---------------------------------------------------------------------------
NAV = [
 ("",                   "Accueil"),
 ("services/",          "Services"),
 ("entreprise/",        "NG Couvreur"),
 ("zones-intervention/","Zones d'intervention"),
 ("conseils/",          "Conseils"),
 ("contact/",           "Contact"),
]

def url(path=""):
    return BASE + "/" + path if path else BASE + "/"

def abs_url(path=""):
    return SITE_ORIGIN + "/" + path if path else SITE_ORIGIN + "/"

# ---------------------------------------------------------------------------
# §6  GABARIT
# ---------------------------------------------------------------------------
def og_image_url(num):
    """URL absolue d'une variante servie — pour Open Graph et JSON-LD."""
    d = IMG[num or "01"]
    if not IMAGES_LOCAL:
        return d["cdn"]
    widths = available_widths(num or "01")
    w = min(widths, key=lambda x: (abs(x - 1280), x))
    return SITE_ORIGIN + d["stem"][len(BASE):] + "-%d.jpg" % w

def head(title, meta, path, og_img="01", schema=""):
    robots = "noindex, nofollow" if PREVIEW else "index, follow"
    preconnect = ""
    if not IMAGES_LOCAL:
        preconnect = ('\n  <link rel="preconnect" href="%s" crossorigin>'
                      '\n  <link rel="dns-prefetch" href="%s">' % (CDN_ORIGIN, CDN_ORIGIN))
    hero_pre = ""
    if og_img and IMAGES_LOCAL:
        d = IMG[og_img]
        hero_pre = ('\n  <link rel="preload" as="image" type="image/avif" fetchpriority="high"'
                    '\n        imagesrcset="%s" imagesizes="100vw">' % srcset(og_img, "avif"))
    elif og_img:
        hero_pre = '\n  <link rel="preload" as="image" href="%s" fetchpriority="high">' % e(IMG[og_img]["cdn"])
    return """<!DOCTYPE html>
<html lang="fr" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="%(robots)s">
  <title>%(title)s</title>
  <meta name="description" content="%(meta)s">
  <link rel="canonical" href="%(canon)s">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="NG Couvreur">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:title" content="%(title)s">
  <meta property="og:description" content="%(meta)s">
  <meta property="og:url" content="%(canon)s">
  <meta property="og:image" content="%(ogimg)s">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#101418">
  <meta name="geo.region" content="FR-2A">
  <meta name="geo.placename" content="Propriano">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,400..800&display=swap">%(pre)s%(heropre)s
  <link rel="icon" href="%(icosvg)s" type="image/svg+xml">
  <link rel="apple-touch-icon" href="%(icopng)s">
  <link rel="stylesheet" href="%(css)s">
  <script>/* Repli image : doit s'attacher avant tout chargement, donc en ligne. */
  document.addEventListener("error",function(e){var i=e.target;
  if(!(i instanceof HTMLImageElement)||i.getAttribute("data-repli"))return;
  i.setAttribute("data-repli","1");var p=i.parentNode;
  if(p&&p.tagName==="PICTURE"){var s=p.querySelectorAll("source");
  for(var n=0;n<s.length;n++)s[n].parentNode.removeChild(s[n]);}
  var u=i.getAttribute("src");i.removeAttribute("srcset");i.removeAttribute("sizes");
  if(u)i.setAttribute("src",u);},true);</script>
%(schema)s</head>
<body class="has-dock">
<a class="skip" href="#contenu">Aller au contenu</a>
""" % {
  "robots": robots, "title": e(title), "meta": e(meta),
  "canon": e(abs_url(path)), "ogimg": e(og_image_url(og_img)),
  "pre": preconnect, "heropre": hero_pre, "css": e(url("assets/css/site.css")),
  "icosvg": e(url("assets/icon/favicon.svg")), "icopng": e(url("assets/icon/apple-touch-icon.png")),
  "schema": schema,
}

def header(current):
    items = ""
    for path, label in NAV:
        cur = ' aria-current="page"' if path == current else ""
        items += '<li><a href="%s"%s>%s</a></li>' % (e(url(path)), cur, e(label))
    drawer = ""
    for path, label in NAV:
        cur = ' aria-current="page"' if path == current else ""
        drawer += '<a class="drawer__link" href="%s"%s>%s</a>' % (e(url(path)), cur, e(label))
    return """<header class="header">
  <div class="shell header__in">
    <a class="brand" href="%(home)s">
      <span class="brand__name">NG Couvreur</span>
      <span class="brand__sub">Propriano — Corse-du-Sud</span>
    </a>
    <nav class="nav" aria-label="Navigation principale"><ul>%(items)s</ul></nav>
    <a class="header__tel" href="%(tel)s">%(icon)s %(teltxt)s</a>
    <a class="btn btn--primary header__cta" href="%(contact)s">Demander un devis</a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu-mobile" aria-label="Ouvrir le menu"><span></span></button>
  </div>
  <div class="drawer" id="menu-mobile" data-open="false">
    <nav aria-label="Navigation mobile">%(drawer)s</nav>
    <div class="drawer__foot">
      <a class="btn btn--primary btn--block" href="%(contact)s">Demander un devis</a>
      <a class="btn btn--outline btn--block btn__tel" href="%(tel)s">%(teltxt)s</a>
    </div>
  </div>
</header>
<main id="contenu">
""" % {"home": e(url()), "items": items, "drawer": drawer, "tel": TEL_HREF,
       "teltxt": TEL_TXT, "icon": PHONE_ICON, "contact": e(url("contact/"))}

def footer():
    svc = "".join('<li><a href="%s">%s</a></li>' % (e(url("services/%s/" % s["slug"])), e(s["nav"])) for s in SERVICES)
    nav = "".join('<li><a href="%s">%s</a></li>' % (e(url(p)), e(l)) for p, l in NAV if p)
    return """</main>
<footer class="footer">
  <div class="shell">
    <div class="footer__top">
      <div class="footer__brand">
        <span class="brand__name">NG Couvreur</span>
        <p>Couvreur à Propriano — Corse-du-Sud. Couverture, rénovation, réparation et entretien de toiture.</p>
        <a class="footer__tel" href="%(tel)s">%(teltxt)s</a>
      </div>
      <div><h4>Prestations</h4><nav aria-label="Prestations"><ul>%(svc)s</ul></nav></div>
      <div><h4>Le site</h4><nav aria-label="Navigation secondaire"><ul>%(nav)s</ul></nav></div>
    </div>
    <div class="footer__bottom">
      <span>© %(year)d NG Couvreur</span>
      <a href="%(ml)s">Mentions légales</a>
      <a href="%(pc)s">Politique de confidentialité</a>
    </div>
  </div>
</footer>
<div class="dock">
  <a href="%(tel)s">%(icon)s Appeler</a>
  <a href="%(contact)s">Devis</a>
</div>
<script src="%(js)s" defer></script>
</body>
</html>
""" % {"tel": TEL_HREF, "teltxt": TEL_TXT, "svc": svc, "nav": nav,
       "year": datetime.date.today().year, "icon": PHONE_ICON,
       "ml": e(url("mentions-legales/")), "pc": e(url("politique-confidentialite/")),
       "contact": e(url("contact/")), "js": e(url("assets/js/site.js"))}

def crumbs(trail):
    out = ['<a href="%s">Accueil</a>' % e(url())]
    for label, path in trail:
        out.append('<span aria-hidden="true">/</span>')
        out.append('<a href="%s">%s</a>' % (e(url(path)), e(label)) if path else '<span>%s</span>' % e(label))
    return '<nav class="crumbs" aria-label="Fil d\'Ariane">%s</nav>' % "".join(out)

def hero_page(num, label, title, sub, trail):
    return """<section class="hero hero--page">
  <div class="hero__media">%(img)s</div>
  <div class="shell hero__in">
    %(crumbs)s
    <p class="label label--light" style="margin-top:1.5rem">%(label)s</p>
    <h1 class="hero__title" style="margin-top:1rem">%(title)s</h1>
    <p class="hero__sub">%(sub)s</p>
  </div>
</section>
""" % {"img": img_tag(num, sizes="100vw", eager=True), "crumbs": crumbs(trail),
       "label": e(label), "title": title, "sub": e(sub)}

def cta_block(num="28"):
    return """<section class="cta">
  <div class="cta__media">%(img)s</div>
  <div class="shell cta__in reveal">
    <p class="label label--light">Contact</p>
    <h2>Un projet&nbsp;? Parlons-en.</h2>
    <p>Contactez NG Couvreur pour nous expliquer votre besoin. Nous vous répondons et nous convenons de la suite.</p>
    <div class="actions">
      <a class="btn btn--onphoto" href="%(contact)s">Demander un devis</a>
      <a class="btn btn--ghostphoto btn__tel" href="%(tel)s">%(icon)s %(teltxt)s</a>
    </div>
  </div>
</section>
""" % {"img": img_tag(num, sizes="100vw"), "contact": e(url("contact/")),
       "tel": TEL_HREF, "teltxt": TEL_TXT, "icon": PHONE_ICON}

def services_grid():
    out = '<div class="services">'
    for s in SERVICES:
        out += """<article class="service"><a class="service__link" href="%s">
        <div class="service__media">%s</div>
        <div class="service__body"><h3>%s</h3><p>%s</p>
        <span class="service__more">Voir %s</span></div></a></article>""" % (
            e(url("services/%s/" % s["slug"])),
            img_tag(s["img"], sizes="(min-width:64rem) 33vw, (min-width:40rem) 50vw, 100vw"),
            s["h1"], e(s["court"]), ARROW)
    return out + "</div>"

def write(path, content):
    full = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    return path

# ---------------------------------------------------------------------------
# §7  DONNÉES STRUCTURÉES
# ---------------------------------------------------------------------------
def jsonld(*blocks):
    return "".join('  <script type="application/ld+json">%s</script>\n' % b for b in blocks)

LOCALBUSINESS = """{
  "@context":"https://schema.org","@type":"RoofingContractor","@id":"%(o)s/#entreprise",
  "name":"NG Couvreur","url":"%(o)s/","telephone":"%(tel)s","image":"%(img)s",
  "description":"Couvreur à Propriano, en Corse-du-Sud. Couverture, rénovation, réparation et recherche de fuite, étanchéité, zinguerie et gouttières, nettoyage et démoussage de toiture.",
  "address":{"@type":"PostalAddress","addressLocality":"Propriano","postalCode":"20110","addressRegion":"Corse-du-Sud","addressCountry":"FR"},
  "areaServed":[%(zones)s],
  "knowsLanguage":"fr-FR",
  "hasOfferCatalog":{"@type":"OfferCatalog","name":"Travaux de toiture","itemListElement":[%(svc)s]}
}""" % {
  "o": SITE_ORIGIN, "tel": TEL_E164, "img": og_image_url("01"),
  "zones": ",".join('{"@type":"City","name":"%s"}' % c["nom"] for c in COMMUNES),
  "svc": ",".join('{"@type":"Offer","itemOffered":{"@type":"Service","name":"%s"}}'
                  % re.sub("&nbsp;|&amp;", lambda m: " " if m.group() == "&nbsp;" else "&", s["nav"])
                  for s in SERVICES),
}

def breadcrumb(trail):
    items = ['{"@type":"ListItem","position":1,"name":"Accueil","item":"%s"}' % abs_url()]
    for i, (label, path) in enumerate(trail, start=2):
        items.append('{"@type":"ListItem","position":%d,"name":"%s","item":"%s"}'
                     % (i, label.replace('"', ""), abs_url(path) if path else abs_url()))
    return '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}' % ",".join(items)

# ---------------------------------------------------------------------------
# §8  ACCUEIL
# ---------------------------------------------------------------------------
def page_home():
    steps = [
      ("01", "Vous nous contactez", "Expliquez-nous votre besoin et, si possible, envoyez quelques photos."),
      ("02", "Nous évaluons votre toiture", "Nous échangeons avec vous afin de comprendre l'intervention nécessaire."),
      ("03", "Vous recevez votre devis", "Une proposition claire, adaptée aux travaux à réaliser."),
      ("04", "Intervention", "Les travaux sont réalisés selon le périmètre convenu."),
    ]
    steps_html = "".join(
      '<li><span class="n">%s</span><h3>%s</h3><p>%s</p></li>' % (n, e(t), e(d)) for n, t, d in steps)

    zones_html = ""
    for c in COMMUNES:
        inner = '<span class="zone__name">%s</span><span class="zone__meta">%s</span>' % (
            e(c["nom"]), e(c["note"] or c["cp"]))
        zones_html += ('<a class="zone" href="%s">%s</a>' % (e(url("zones-intervention/%s/" % c["page"])), inner)
                       if c["page"] else '<div class="zone">%s</div>' % inner)

    posts = "".join(
      '<article class="post"><a href="%s"><h3>%s</h3><p>%s</p><span class="service__more">Lire %s</span></a></article>'
      % (e(url("conseils/%s/" % a["slug"])), e(a["titre"]), e(a["resume"]), ARROW) for a in CONSEILS)

    body = """<section class="hero">
  <div class="hero__media">%(heroimg)s</div>
  <div class="shell hero__in">
    <p class="label label--light">NG Couvreur</p>
    <h1 class="display hero__title">Votre toiture.<br>Notre métier.</h1>
    <p class="hero__sub">Couvreur à Propriano. Couverture, rénovation, réparation et entretien de toiture en Corse-du-Sud.</p>
    <div class="actions hero__actions">
      <a class="btn btn--onphoto" href="%(contact)s">Demander un devis</a>
      <a class="btn btn--ghostphoto btn__tel" href="%(tel)s">%(icon)s %(teltxt)s</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="head head--split reveal">
      <p class="label">Nos prestations</p>
      <h2>Votre toiture,<br>de A à Z.</h2>
      <p class="lead">Six interventions qui couvrent la vie d'une toiture, de la pose à l'entretien. Si vous ne savez pas dans quelle catégorie se range votre problème, appelez-nous&nbsp;: nous vous le dirons.</p>
    </div>
  </div>
  <div class="reveal">%(services)s</div>
</section>

<section class="section section--sable">
  <div class="shell">
    <div class="split split--wide-media reveal">
      <div class="split__media"><figure class="figure">%(portrait)s
        <figcaption>Chaque chantier est mené par le même couvreur, de la première visite à la fin des travaux.</figcaption></figure></div>
      <div class="split__body">
        <p class="label">NG Couvreur</p>
        <h2>Un couvreur proche de chez vous.</h2>
        <div class="prose">
          <p>NG Couvreur est une entreprise de couverture installée à Propriano. Nous intervenons sur les toitures des particuliers du sud de la Corse&nbsp;: pose, rénovation, réparation, étanchéité, zinguerie et entretien.</p>
          <p>L'entreprise est récente. Ce qui la définit tient en peu de choses&nbsp;: on regarde la toiture avant de proposer quoi que ce soit, on explique ce qu'on a vu, et on s'en tient au périmètre convenu.</p>
        </div>
        <div class="actions"><a class="arrow" href="%(entreprise)s">En savoir plus %(arrow)s</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="head head--split reveal">
      <p class="label">La marche à suivre</p>
      <h2>Comment ça se passe&nbsp;?</h2>
      <p class="lead">Quatre étapes, sans rendez-vous inutile ni démarche compliquée.</p>
    </div>
    <ol class="steps reveal">%(steps)s</ol>
  </div>
</section>

<section class="section section--sable">
  <div class="shell">
    <div class="head head--split reveal">
      <p class="label">Zone d'intervention</p>
      <h2>Propriano &amp;<br>Corse-du-Sud.</h2>
      <p class="lead">Nous sommes basés à Propriano et intervenons dans les communes alentour. Votre commune n'est pas listée&nbsp;? Appelez-nous, nous vous dirons si nous pouvons nous déplacer.</p>
    </div>
  </div>
  <div class="reveal">%(zones)s</div>
  <div class="shell" style="margin-top:2.5rem">
    <a class="arrow" href="%(zonesurl)s">Voir la zone d'intervention %(arrow)s</a>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="head head--split reveal">
      <p class="label">Conseils toiture</p>
      <h2>Comprendre<br>votre toiture.</h2>
      <p class="lead">Quelques repères simples pour savoir quand s'inquiéter, quand entretenir, et quand faire appel à un couvreur.</p>
    </div>
  </div>
  <div class="reveal">%(posts)s</div>
</section>

%(cta)s""" % {
      "heroimg": img_tag("01", sizes="100vw", eager=True),
      "contact": e(url("contact/")), "tel": TEL_HREF, "teltxt": TEL_TXT, "icon": PHONE_ICON,
      "services": services_grid(),
      "portrait": img_tag("03", sizes="(min-width:56rem) 55vw, 100vw"),
      "entreprise": e(url("entreprise/")), "arrow": ARROW,
      "steps": steps_html, "zones": zones_html, "zonesurl": e(url("zones-intervention/")),
      "posts": posts, "cta": cta_block("28"),
    }

    h = head("Couvreur à Propriano — couverture et toiture en Corse-du-Sud | NG Couvreur",
             "NG Couvreur, couvreur à Propriano. Couverture, rénovation, réparation de fuite, étanchéité, zinguerie et démoussage de toiture en Corse-du-Sud. Devis sur demande, %s." % TEL_TXT,
             "", og_img="01",
             schema=jsonld(LOCALBUSINESS,
               '{"@context":"https://schema.org","@type":"WebSite","name":"NG Couvreur","url":"%s"}' % abs_url()))
    write("", h + header("") + body + footer())

# ---------------------------------------------------------------------------
# §9  SERVICES
# ---------------------------------------------------------------------------
def page_services_index():
    trail = [("Services", None)]
    body = hero_page("02", "Nos prestations", "Votre toiture, de A à Z.",
        "Six interventions qui couvrent la vie d'une toiture, de la pose à l'entretien. Toutes réalisées à Propriano et dans le sud de la Corse.", trail)
    body += '<section class="section"><div class="reveal">%s</div></section>' % services_grid()
    body += cta_block("28")
    h = head("Travaux de toiture à Propriano — nos prestations | NG Couvreur",
             "Couverture, rénovation, réparation de fuite, étanchéité, zinguerie et gouttières, nettoyage et démoussage. NG Couvreur intervient à Propriano et en Corse-du-Sud.",
             "services/", og_img="02", schema=jsonld(breadcrumb(trail)))
    write("services", h + header("services/") + body + footer())

def page_service(s):
    path = "services/%s/" % s["slug"]
    trail = [("Services", "services/"), (re.sub("&amp;", "&", s["nav"]), None)]

    blocs = ""
    for titre, points in s["blocs"]:
        lis = "".join("<li>%s</li>" % e(p) for p in points)
        blocs += ('<div class="split__body" style="align-content:start">'
                  '<h2 style="font-size:clamp(1.4rem,2.4vw,1.85rem)">%s</h2>'
                  '<ul class="article__body" style="display:grid;gap:.6rem">%s</ul></div>' % (e(titre), lis))

    seq = ""
    if s.get("sequence"):
        steps = "".join(
          '<div class="step">%s<span class="step__tag">%s</span><p>%s</p></div>'
          % (img_tag(n, sizes="(min-width:48rem) 33vw, 100vw"), e(tag), e(txt))
          for n, tag, txt in s["sequence"])
        seq = ("""<section class="section section--sable"><div class="shell">
          <div class="head reveal"><p class="label">En images</p>
          <h2 style="font-size:clamp(1.5rem,2.8vw,2.1rem)">Avant, pendant, après.</h2></div>
          <div class="sequence reveal">%s</div></div></section>""" % steps)

    gal = ""
    if s.get("gallery"):
        figs = "".join(
          '<figure class="figure">%s<figcaption>%s</figcaption></figure>'
          % (img_tag(n, sizes="(min-width:56rem) 50vw, 100vw"), e(cap)) for n, cap in s["gallery"])
        cols = "grid-template-columns:repeat(auto-fit,minmax(min(20rem,100%),1fr))"
        gal = ('<section class="section"><div class="shell"><div class="reveal" '
               'style="display:grid;gap:2rem;%s">%s</div></div></section>' % (cols, figs))

    body = hero_page(s["hero"], "Prestation", s["h1"], s["court"], trail)
    body += """<section class="section"><div class="shell">
      <p class="lead reveal" style="max-width:44ch;font-size:clamp(1.15rem,2vw,1.5rem);color:var(--ink)">%s</p>
      <div class="split reveal" style="margin-top:clamp(2.5rem,5vw,4rem);align-items:start">%s</div>
    </div></section>""" % (e(s["intro"]), blocs)
    body += seq + gal

    autres = [x for x in SERVICES if x["slug"] != s["slug"]]
    liens = "".join('<article class="service"><a class="service__link" href="%s">'
                    '<div class="service__media">%s</div><div class="service__body"><h3>%s</h3>'
                    '<p>%s</p><span class="service__more">Voir %s</span></div></a></article>'
                    % (e(url("services/%s/" % x["slug"])),
                       img_tag(x["img"], sizes="(min-width:64rem) 33vw, 50vw"),
                       x["h1"], e(x["court"]), ARROW) for x in autres[:3])
    body += ('<section class="section section--sable"><div class="shell"><div class="head reveal">'
             '<p class="label">Autres prestations</p></div></div>'
             '<div class="services reveal">%s</div></section>' % liens)
    body += cta_block("28")

    svc_schema = ('{"@context":"https://schema.org","@type":"Service","name":"%s",'
                  '"serviceType":"%s","url":"%s",'
                  '"provider":{"@type":"RoofingContractor","name":"NG Couvreur","telephone":"%s"},'
                  '"areaServed":[%s]}'
                  % (re.sub("&amp;", "&", s["nav"]), re.sub("&amp;", "&", s["nav"]), abs_url(path), TEL_E164,
                     ",".join('{"@type":"City","name":"%s"}' % c["nom"] for c in COMMUNES)))
    h = head(s["title"], s["meta"], path, og_img=s["hero"], schema=jsonld(svc_schema, breadcrumb(trail)))
    write("services/%s" % s["slug"], h + header("services/") + body + footer())

# ---------------------------------------------------------------------------
# §10  NG COUVREUR (entreprise)
# ---------------------------------------------------------------------------
def page_entreprise():
    trail = [("NG Couvreur", None)]
    body = hero_page("03", "L'entreprise", "Un couvreur proche de chez vous.",
        "NG Couvreur est une entreprise de couverture installée à Propriano, en Corse-du-Sud.", trail)
    body += """<section class="section"><div class="shell">
  <div class="split reveal" style="align-items:start">
    <div class="split__body">
      <p class="label">Qui nous sommes</p>
      <h2 style="font-size:clamp(1.5rem,2.8vw,2.1rem)">Une entreprise récente,<br>un métier qui ne l'est pas.</h2>
      <div class="prose">
        <p>NG Couvreur est une jeune entreprise. Nous ne le cachons pas, et nous n'allons pas vous raconter des décennies d'histoire que nous n'avons pas.</p>
        <p>Ce que nous pouvons dire tient à la façon de travailler&nbsp;: nous montons voir la toiture avant d'établir un devis, nous vous expliquons ce que nous avons constaté, et nous nous en tenons au périmètre convenu. Quand une intervention dépasse ce que nous savons faire correctement, nous le disons.</p>
      </div>
    </div>
    <div class="split__media"><figure class="figure">%(portrait)s
      <figcaption>Le même interlocuteur du premier appel à la fin du chantier.</figcaption></figure></div>
  </div>
</div></section>

<section class="section section--sable"><div class="shell">
  <div class="head head--split reveal">
    <p class="label">Notre approche</p>
    <h2>Trois principes.</h2>
  </div>
  <ol class="steps reveal">
    <li><span class="n">01</span><h3>Regarder avant de chiffrer</h3><p>Un devis établi sans avoir vu la toiture ne vaut rien. Nous constatons d'abord, nous chiffrons ensuite.</p></li>
    <li><span class="n">02</span><h3>Expliquer ce que l'on voit</h3><p>Vous devez comprendre ce qui ne va pas et pourquoi l'intervention proposée y répond. Sans jargon.</p></li>
    <li><span class="n">03</span><h3>Travailler en sécurité</h3><p>Accès en hauteur sécurisé, chantier protégé. Cela vaut pour nous comme pour ce qui vous entoure.</p></li>
  </ol>
</div></section>

<section class="section"><div class="shell">
  <div class="head head--split reveal">
    <p class="label">Le métier</p>
    <h2>Ce que recouvre<br>le travail de couvreur.</h2>
    <p class="lead">Une toiture n'est pas seulement une surface de tuiles. C'est un ensemble&nbsp;: un support, un écran, un liteaunage, une couverture, et tout ce qui conduit l'eau à l'écart du bâtiment.</p>
  </div>
  <div class="reveal" style="display:grid;gap:2rem;grid-template-columns:repeat(auto-fit,minmax(min(17rem,100%%),1fr))">
    <figure class="figure">%(d1)s<figcaption>Le geste&nbsp;: sceller une tuile dans son lit de mortier de chaux.</figcaption></figure>
    <figure class="figure">%(d2)s<figcaption>Le faîtage&nbsp;: la ligne qui ferme la toiture en tête.</figcaption></figure>
    <figure class="figure">%(d3)s<figcaption>La zinguerie&nbsp;: conduire l'eau hors de la couverture.</figcaption></figure>
  </div>
</div></section>
%(cta)s""" % {
      "portrait": img_tag("05", sizes="(min-width:56rem) 45vw, 100vw"),
      "d1": img_tag("07", sizes="(min-width:56rem) 33vw, 100vw"),
      "d2": img_tag("24", sizes="(min-width:56rem) 33vw, 100vw"),
      "d3": img_tag("20", sizes="(min-width:56rem) 33vw, 100vw"),
      "cta": cta_block("06"),
    }
    h = head("NG Couvreur — entreprise de couverture à Propriano | Corse-du-Sud",
             "NG Couvreur, entreprise de couverture installée à Propriano. Notre approche du métier de couvreur en Corse-du-Sud. %s." % TEL_TXT,
             "entreprise/", og_img="03", schema=jsonld(LOCALBUSINESS, breadcrumb(trail)))
    write("entreprise", h + header("entreprise/") + body + footer())

# ---------------------------------------------------------------------------
# §11  ZONES D'INTERVENTION
# ---------------------------------------------------------------------------
def page_zones():
    trail = [("Zones d'intervention", None)]
    zones = ""
    for c in COMMUNES:
        inner = '<span class="zone__name">%s</span><span class="zone__meta">%s</span>' % (
            e(c["nom"]), e("%s — %s" % (c["cp"], c["note"]) if c["note"] else c["cp"]))
        zones += ('<a class="zone" href="%s">%s</a>' % (e(url("zones-intervention/%s/" % c["page"])), inner)
                  if c["page"] else '<div class="zone">%s</div>' % inner)

    body = hero_page("26", "Où nous intervenons", "Propriano &amp; Corse-du-Sud.",
        "Nous sommes basés à Propriano et intervenons dans les communes du sud de la Corse.", trail)
    body += """<section class="section"><div class="shell">
  <p class="lead reveal" style="max-width:46ch;font-size:clamp(1.15rem,2vw,1.5rem);color:var(--ink)">Être installé sur place change deux choses&nbsp;: le délai pour venir voir une toiture, et la connaissance du bâti local — tuile canal, exposition au vent, épisodes pluvieux d'automne.</p>
</div>
<div class="reveal" style="margin-top:clamp(2.5rem,5vw,4rem)">%(zones)s</div>
<div class="shell"><div class="formnote reveal" style="margin-top:2.5rem;max-width:52ch">
  <strong>Votre commune n'est pas listée&nbsp;?</strong> Appelez-nous au <a href="%(tel)s" style="font-weight:700">%(teltxt)s</a>. Nous vous dirons franchement si nous pouvons nous déplacer chez vous.
</div></div></section>

<section class="section section--sable"><div class="shell">
  <div class="split reveal" style="align-items:center">
    <div class="split__media">%(paysage)s</div>
    <div class="split__body">
      <p class="label">Le bâti local</p>
      <h2 style="font-size:clamp(1.5rem,2.8vw,2.1rem)">Des toitures qui ont<br>leurs habitudes.</h2>
      <div class="prose">
        <p>Dans la région du golfe du Valinco, la tuile canal domine, souvent posée sur des supports anciens et sur des pentes faibles. C'est un système qui vieillit bien, à condition que les canaux restent dégagés et que les points singuliers — faîtage, rives, solins — soient tenus.</p>
        <p>Les épisodes pluvieux d'automne et le vent sont les deux causes les plus fréquentes des interventions que nous voyons&nbsp;: tuiles déplacées, gouttières saturées, infiltrations aux raccords.</p>
      </div>
    </div>
  </div>
</div></section>
%(cta)s""" % {"zones": zones, "tel": TEL_HREF, "teltxt": TEL_TXT,
              "paysage": img_tag("27", sizes="(min-width:56rem) 50vw, 100vw"),
              "cta": cta_block("28")}
    h = head("Couvreur à Propriano, Sartène, Olmeto — zones d'intervention | NG Couvreur",
             "NG Couvreur intervient à Propriano, Sartène, Olmeto, Viggianello, Serra-di-Ferro et Porto-Pollo. Travaux de toiture en Corse-du-Sud. %s." % TEL_TXT,
             "zones-intervention/", og_img="26", schema=jsonld(breadcrumb(trail)))
    write("zones-intervention", h + header("zones-intervention/") + body + footer())

def page_commune(c):
    """Gabarit de page locale. Dupliquer une entrée COMMUNES avec 'page' pour en créer une autre."""
    path = "zones-intervention/%s/" % c["page"]
    trail = [("Zones d'intervention", "zones-intervention/"), (c["nom"], None)]
    svc = "".join('<li><a href="%s">%s</a></li>' % (e(url("services/%s/" % s["slug"])), s["h1"]) for s in SERVICES)

    body = hero_page("26", c["nom"], "Couvreur à %s." % c["nom"],
        "NG Couvreur est installé à %s. Couverture, rénovation, réparation de fuite, étanchéité, zinguerie et démoussage." % c["nom"], trail)
    body += """<section class="section"><div class="shell">
  <div class="article">
    <div class="article__body reveal">
      <h2>Notre implantation à %(nom)s</h2>
      <p>NG Couvreur est basé à %(nom)s (%(cp)s), dans le golfe du Valinco. C'est depuis là que nous nous déplaçons sur l'ensemble de nos interventions en Corse-du-Sud, ce qui nous permet de venir constater une toiture rapidement.</p>
      <h2>Les interventions que nous réalisons à %(nom)s</h2>
      <ul>%(liste)s</ul>
      <h2>Les toitures de %(nom)s</h2>
      <p>Le bâti de %(nom)s et de ses environs est majoritairement couvert en tuile canal, sur des pentes faibles et des supports parfois anciens. Les désordres que nous rencontrons le plus souvent sont les tuiles déplacées après un coup de vent, les canaux encombrés de mousse sur les versants ombragés, et les infiltrations aux raccords de cheminée.</p>
      <p>La proximité de la mer accentue par ailleurs l'usure des éléments métalliques&nbsp;: les gouttières et les solins demandent d'être contrôlés régulièrement.</p>
      <h2>Nous contacter</h2>
      <p>Pour une intervention à %(nom)s, appelez-nous au <a href="%(tel)s" style="font-weight:700">%(teltxt)s</a> ou envoyez votre demande depuis la page contact. Décrivez le problème et joignez quelques photos si vous en avez&nbsp;: cela nous fait gagner du temps à tous les deux.</p>
    </div>
    <aside class="aside reveal">
      <p class="label">Intervention</p>
      <p class="small muted">NG Couvreur<br>%(nom)s — %(cp)s<br>Corse-du-Sud</p>
      <a class="btn btn--primary btn--block btn__tel" href="%(tel)s">%(teltxt)s</a>
      <a class="btn btn--outline btn--block" href="%(contact)s">Demander un devis</a>
    </aside>
  </div>
</div></section>
%(cta)s""" % {"nom": e(c["nom"]), "cp": e(c["cp"]), "liste": svc, "tel": TEL_HREF,
              "teltxt": TEL_TXT, "contact": e(url("contact/")), "cta": cta_block("28")}
    h = head("Couvreur à %s (%s) — travaux de toiture | NG Couvreur" % (c["nom"], c["cp"]),
             "NG Couvreur, couvreur à %s. Couverture, rénovation, réparation de fuite, étanchéité, zinguerie et démoussage de toiture. %s." % (c["nom"], TEL_TXT),
             path, og_img="26", schema=jsonld(LOCALBUSINESS, breadcrumb(trail)))
    write("zones-intervention/%s" % c["page"], h + header("zones-intervention/") + body + footer())

# ---------------------------------------------------------------------------
# §12  CONSEILS
# ---------------------------------------------------------------------------
def page_conseils_index():
    trail = [("Conseils", None)]
    posts = "".join(
      '<article class="post"><a href="%s"><h3>%s</h3><p>%s</p><span class="service__more">Lire %s</span></a></article>'
      % (e(url("conseils/%s/" % a["slug"])), e(a["titre"]), e(a["resume"]), ARROW) for a in CONSEILS)
    body = hero_page("25", "Conseils toiture", "Comprendre votre toiture.",
        "Des repères simples pour savoir quand s'inquiéter, quand entretenir, et quand faire appel à un couvreur.", trail)
    body += '<section class="section"><div class="reveal">%s</div></section>' % posts
    body += cta_block("28")
    h = head("Conseils toiture — fuite, rénovation, démoussage | NG Couvreur",
             "Conseils pratiques sur l'entretien et la rénovation de toiture en Corse-du-Sud, par NG Couvreur, couvreur à Propriano.",
             "conseils/", og_img="25", schema=jsonld(breadcrumb(trail)))
    write("conseils", h + header("conseils/") + body + footer())

def page_conseil(a):
    path = "conseils/%s/" % a["slug"]
    trail = [("Conseils", "conseils/"), (a["titre"], None)]
    corps = "".join("<h2>%s</h2>%s" % (e(t), c) for t, c in a["corps"])
    autres = "".join('<li style="padding-left:0"><a class="arrow" style="font-size:.8125rem" href="%s">%s %s</a></li>'
                     % (e(url("conseils/%s/" % x["slug"])), e(x["titre"]), ARROW)
                     for x in CONSEILS if x["slug"] != a["slug"])
    body = hero_page(a["img"], "Conseils toiture", a["titre"], a["resume"], trail)
    body += """<section class="section"><div class="shell">
  <div class="article">
    <div class="article__body prose reveal">%(corps)s
      <h2>Un doute sur votre toiture&nbsp;?</h2>
      <p>Décrivez-nous ce que vous constatez, si possible avec quelques photos. Nous vous dirons ce que cela évoque et si une visite est nécessaire. Appelez le <a href="%(tel)s" style="font-weight:700">%(teltxt)s</a>.</p>
    </div>
    <aside class="aside reveal">
      <p class="label">Besoin d'un avis</p>
      <p class="small muted">NG Couvreur — couvreur à Propriano, Corse-du-Sud.</p>
      <a class="btn btn--primary btn--block btn__tel" href="%(tel)s">%(teltxt)s</a>
      <a class="btn btn--outline btn--block" href="%(contact)s">Demander un devis</a>
      <div style="margin-top:1rem"><p class="label" style="margin-bottom:.9rem">À lire aussi</p><ul style="display:grid;gap:.9rem">%(autres)s</ul></div>
    </aside>
  </div>
</div></section>
%(cta)s""" % {"corps": corps, "tel": TEL_HREF, "teltxt": TEL_TXT,
              "contact": e(url("contact/")), "autres": autres, "cta": cta_block("28")}
    art = ('{"@context":"https://schema.org","@type":"Article","headline":"%s",'
           '"description":"%s","image":"%s","mainEntityOfPage":"%s",'
           '"author":{"@type":"Organization","name":"NG Couvreur"},'
           '"publisher":{"@type":"Organization","name":"NG Couvreur"},"inLanguage":"fr-FR"}'
           % (a["titre"].replace('"', ""), a["resume"].replace('"', ""), og_image_url(a["img"]), abs_url(path)))
    h = head(a["title"], a["meta"], path, og_img=a["img"], schema=jsonld(art, breadcrumb(trail)))
    write("conseils/%s" % a["slug"], h + header("conseils/") + body + footer())

# ---------------------------------------------------------------------------
# §13  CONTACT / DEVIS
# ---------------------------------------------------------------------------
# Réception des demandes via FormSubmit : aucun compte à créer, la boîte de
# réception suffit. La PREMIÈRE soumission déclenche un e-mail d'activation
# qu'il faut valider une fois, sans quoi rien n'est transmis.
#
# L'adresse apparaît en clair dans le HTML, donc exposée aux robots
# collecteurs. Après activation, FormSubmit fournit un alias aléatoire à
# utiliser à la place : le remplacer ici supprime l'exposition.
FORM_TO       = "Nathanegorreta@outlook.fr"
FORM_ENDPOINT = "https://formsubmit.co/" + FORM_TO

# L'adresse d'envoi n'est PAS écrite dans le HTML : elle est encodée ici et
# remontée par JavaScript au chargement. Un robot qui n'exécute pas JS ne
# trouve aucune cible, et l'adresse échappe aux moissonneurs d'adresses.
# Ce n'est pas du chiffrement — un robot ciblé sait décoder — mais cela
# écarte la quasi-totalité du spam automatisé.
FORM_ENDPOINT_B64 = base64.b64encode(FORM_ENDPOINT.encode("utf-8")).decode("ascii")

# Captcha FormSubmit : désactivé par défaut car il impose une page
# intermédiaire qui fait chuter les demandes sur mobile. À passer à True si
# du spam finit par passer — c'est la seule protection vérifiée côté serveur.
FORM_CAPTCHA = False

def page_contact():
    trail = [("Contact", None)]
    options = "".join('<option value="%s">%s</option>' % (re.sub("&amp;", "&", s["nav"]), s["h1"]) for s in SERVICES)
    communes = "".join('<option value="%s">%s</option>' % (e(c["nom"]), e(c["nom"])) for c in COMMUNES)

    body = hero_page("28", "Contact", "Parlons de votre toiture.",
        "Expliquez-nous votre besoin. Par téléphone, c'est le plus rapide.", trail)
    body += """<section class="section"><div class="shell">
  <div class="split split--wide-media split--rev reveal" style="align-items:start">

    <div class="split__body">
      <p class="label">Demande de devis</p>
      <h2 style="font-size:clamp(1.5rem,2.8vw,2.1rem)">Décrivez votre besoin.</h2>
      <p class="muted small" style="max-width:52ch;margin-bottom:.5rem">Plus votre description est précise, plus notre réponse le sera. Les photos aident beaucoup&nbsp;: une vue d'ensemble de la toiture et un gros plan du problème suffisent.</p>

      <noscript>
        <div class="formnote formnote--alert">
          <strong>Ce formulaire nécessite JavaScript</strong> — c'est ce qui nous protège des robots.
          Appelez-nous directement au <a href="%(tel)s" style="font-weight:700">%(teltxt)s</a>, c'est de toute façon plus rapide.
        </div>
      </noscript>

      <form class="form" data-devis data-ep="%(ep)s" method="post" enctype="multipart/form-data" novalidate>
        <div class="formnote formnote--alert" data-formnote hidden tabindex="-1" role="alert"></div>
        <div class="form__row">
          <div class="field">
            <label for="nom">Nom <span class="req" aria-hidden="true">*</span></label>
            <input type="text" id="nom" name="nom" autocomplete="name" required>
            <p class="err" aria-live="polite"></p>
          </div>
          <div class="field">
            <label for="tel">Téléphone <span class="req" aria-hidden="true">*</span></label>
            <input type="tel" id="tel" name="telephone" autocomplete="tel" inputmode="tel" required>
            <p class="err" aria-live="polite"></p>
          </div>
        </div>

        <div class="form__row">
          <div class="field">
            <label for="email">E-mail</label>
            <input type="email" id="email" name="email" autocomplete="email" inputmode="email">
            <p class="err" aria-live="polite"></p>
          </div>
          <div class="field">
            <label for="commune">Commune <span class="req" aria-hidden="true">*</span></label>
            <input type="text" id="commune" name="commune" list="communes" autocomplete="address-level2" required>
            <datalist id="communes">%(communes)s</datalist>
            <p class="err" aria-live="polite"></p>
          </div>
        </div>

        <div class="field">
          <label for="travaux">Type de travaux <span class="req" aria-hidden="true">*</span></label>
          <select id="travaux" name="type_de_travaux" required>
            <option value="">Sélectionnez…</option>
            %(options)s
            <option value="Je ne sais pas">Je ne sais pas</option>
          </select>
          <p class="err" aria-live="polite"></p>
        </div>

        <div class="field">
          <label for="message">Description <span class="req" aria-hidden="true">*</span></label>
          <textarea id="message" name="message" required placeholder="Ce que vous constatez, depuis quand, et à quel endroit de la toiture si vous le savez."></textarea>
          <p class="err" aria-live="polite"></p>
        </div>

        <div class="field">
          <label for="photos">Photos</label>
          <input type="file" id="photos" name="photos" accept="image/*" multiple>
          <p class="hint">Facultatif. Une vue d'ensemble et un gros plan du problème.</p>
        </div>

        <input type="hidden" name="_subject" value="Demande de devis — site NG Couvreur">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="%(captcha)s">
        <input type="hidden" name="_next" value="%(merci)s">
        <input type="hidden" name="_autoresponse" value="Bonjour, nous avons bien reçu votre demande et nous vous recontactons rapidement. Pour une urgence, appelez directement le 07 44 81 79 45. NG Couvreur, Propriano.">
        <input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">

        <div class="field">
          <label for="consent" class="consent">
            <input type="checkbox" id="consent" name="consentement" value="oui" required>
            <span>J'accepte que mes coordonnées soient utilisées pour répondre à ma demande. <a href="%(pc)s">Politique de confidentialité</a>. <span class="req" aria-hidden="true">*</span></span>
          </label>
          <p class="err" aria-live="polite"></p>
        </div>

        <div>
          <button class="btn btn--primary btn--block" type="button" data-submit>Envoyer ma demande</button>
          <p class="hint" style="margin-top:.85rem">Nous vous répondons par téléphone ou par e-mail. Pour une urgence, appelez plutôt le <a href="%(tel)s" style="font-weight:700">%(teltxt)s</a>.</p>
        </div>
      </form>
    </div>

    <aside class="contactcard">
      <div>
        <dt>L'entreprise</dt>
        <dd><strong>NG Couvreur</strong><br>Propriano — Corse-du-Sud</dd>
      </div>
      <div>
        <dt>Téléphone</dt>
        <dd><a class="tel" href="%(tel)s">%(teltxt)s</a></dd>
      </div>
      <a class="btn btn--primary btn--block btn__tel" href="%(tel)s">%(icon)s Appeler maintenant</a>
      <hr class="rule">
      <div>
        <dt>Le plus rapide</dt>
        <dd class="small muted">Pour une fuite ou une urgence après intempéries, appelez plutôt que d'écrire&nbsp;: nous réagissons immédiatement.</dd>
      </div>
      <div>
        <dt>Zone d'intervention</dt>
        <dd class="small muted">%(zones)s. <a href="%(zonesurl)s">Voir le détail</a>.</dd>
      </div>
    </aside>

  </div>
</div></section>""" % {
      "ep": e(FORM_ENDPOINT_B64), "captcha": "true" if FORM_CAPTCHA else "false",
      "tel": TEL_HREF, "teltxt": TEL_TXT, "icon": PHONE_ICON,
      "options": options, "communes": communes, "pc": e(url("politique-confidentialite/")),
      "merci": e(abs_url("contact/merci/")),
      "zones": e(", ".join(c["nom"] for c in COMMUNES)), "zonesurl": e(url("zones-intervention/")),
    }
    contact_schema = ('{"@context":"https://schema.org","@type":"ContactPage","url":"%s",'
                      '"mainEntity":{"@type":"RoofingContractor","name":"NG Couvreur","telephone":"%s",'
                      '"address":{"@type":"PostalAddress","addressLocality":"Propriano","postalCode":"20110",'
                      '"addressRegion":"Corse-du-Sud","addressCountry":"FR"}}}' % (abs_url("contact/"), TEL_E164))
    h = head("Contact et demande de devis — NG Couvreur, Propriano",
             "Contactez NG Couvreur, couvreur à Propriano. Demande de devis pour vos travaux de toiture en Corse-du-Sud. Téléphone %s." % TEL_TXT,
             "contact/", og_img="28", schema=jsonld(contact_schema, breadcrumb(trail)))
    write("contact", h + header("contact/") + body + footer())

def page_merci():
    """Arrivée après envoi du formulaire. Hors sitemap, non indexée."""
    body = """<section class="section" style="padding-top:clamp(3rem,8vw,6rem)"><div class="shell">
  <p class="label">Demande envoyée</p>
  <h1 style="margin:1.25rem 0 1.5rem;font-size:clamp(2rem,5vw,3.4rem)">Merci, c'est bien parti.</h1>
  <p class="lead">Nous avons reçu votre demande et nous vous recontactons rapidement, par téléphone ou par e-mail.</p>
  <div class="formnote" style="margin-top:2rem;max-width:52ch">
    <strong>Votre toiture prend l'eau&nbsp;?</strong> N'attendez pas notre rappel&nbsp;: appelez-nous, nous réagissons immédiatement.
  </div>
  <div class="actions" style="margin-top:2rem">
    <a class="btn btn--primary btn__tel" href="%(tel)s">%(icon)s %(teltxt)s</a>
    <a class="btn btn--outline" href="%(home)s">Retour à l'accueil</a>
  </div>
</div></section>""" % {"tel": TEL_HREF, "teltxt": TEL_TXT, "icon": PHONE_ICON, "home": e(url())}
    h = head("Demande envoyée | NG Couvreur",
             "Votre demande de devis a bien été transmise à NG Couvreur, couvreur à Propriano.",
             "contact/merci/", og_img=None, schema="")
    h = h.replace('<meta name="robots" content="index, follow">',
                  '<meta name="robots" content="noindex, follow">')
    write("contact/merci", h + header("contact/") + body + footer())


# ---------------------------------------------------------------------------
# §14  PAGES LÉGALES
# ---------------------------------------------------------------------------
TODO = ('<span style="background:#FFF3CD;padding:.1em .45em;font-weight:600" '
        'title="À compléter avant la mise en ligne">[à compléter]</span>')

def page_legal(slug, titre, sections, title, meta):
    trail = [(titre, None)]
    corps = "".join("<h2>%s</h2>%s" % (e(t), c) for t, c in sections)
    body = """<section class="section" style="padding-top:clamp(2.5rem,6vw,4.5rem)"><div class="shell">
  %(crumbs)s
  <h1 style="margin:1.5rem 0 2.5rem;font-size:clamp(1.9rem,4.5vw,3rem)">%(titre)s</h1>
  <div class="article__body prose" style="max-width:64ch">%(corps)s</div>
</div></section>""" % {"crumbs": crumbs(trail).replace('class="crumbs"', 'class="crumbs" style="color:var(--ink-60)"'),
                       "titre": e(titre), "corps": corps}
    h = head(title, meta, "%s/" % slug, og_img=None, schema=jsonld(breadcrumb(trail)))
    write(slug, h + header("") + body + footer())

def pages_legales():
    page_legal("mentions-legales", "Mentions légales", [
      ("Éditeur du site",
       "<p><strong>NG Couvreur</strong><br>Entreprise de couverture<br>Propriano — Corse-du-Sud, France<br>"
       "Téléphone&nbsp;: <a href=\"%s\">%s</a></p>"
       "<p>Forme juridique, numéro SIRET, adresse du siège, numéro de TVA intracommunautaire et nom du "
       "directeur de la publication&nbsp;: %s</p>" % (TEL_HREF, TEL_TXT, TODO)),
      ("Hébergement",
       "<p>Nom, raison sociale, adresse et téléphone de l'hébergeur&nbsp;: %s</p>" % TODO),
      ("Assurance professionnelle",
       "<p>Nom de l'assureur, numéro de police et couverture géographique de la garantie décennale&nbsp;: %s</p>" % TODO),
      ("Propriété intellectuelle",
       "<p>L'ensemble des contenus de ce site — textes, photographies, éléments graphiques et structure — est "
       "protégé par le droit d'auteur. Toute reproduction ou représentation, totale ou partielle, sans "
       "autorisation écrite préalable est interdite.</p>"),
      ("Médiation de la consommation",
       "<p>Conformément à l'article L.612-1 du code de la consommation, le consommateur peut recourir "
       "gratuitement à un médiateur de la consommation en vue de la résolution amiable d'un litige. "
       "Coordonnées du médiateur retenu par l'entreprise&nbsp;: %s</p>" % TODO),
    ], "Mentions légales | NG Couvreur", "Mentions légales du site de NG Couvreur, entreprise de couverture à Propriano, Corse-du-Sud.")

    page_legal("politique-confidentialite", "Politique de confidentialité", [
      ("Données collectées",
       "<p>Ce site collecte uniquement les informations que vous transmettez volontairement via le formulaire "
       "de demande de devis&nbsp;: nom, téléphone, adresse e-mail, commune, type de travaux, description de "
       "votre besoin et, le cas échéant, les photographies que vous joignez. Le consentement que vous donnez en cochant la case du formulaire est également enregistré.</p>"
       "<p>Aucune inscription, aucun compte et aucun paiement en ligne ne sont proposés sur ce site.</p>"),
      ("Finalité",
       "<p>Ces données servent exclusivement à répondre à votre demande et, si elle aboutit, à préparer et à "
       "réaliser l'intervention. Elles ne sont ni vendues, ni cédées, ni utilisées à des fins publicitaires.</p>"),
      ("Base légale et durée de conservation",
       "<p>Le traitement repose sur votre démarche volontaire de prise de contact. Les demandes sans suite "
       "sont conservées le temps nécessaire au traitement de l'échange, puis supprimées. Les demandes ayant "
       "donné lieu à un devis ou à des travaux sont conservées pour la durée requise par les obligations "
       "comptables et de garantie applicables.</p>"),
      ("Destinataires et sous-traitant",
       "<p>Les informations transmises sont destinées à NG Couvreur seul. Elles ne sont ni vendues, ni "
       "cédées à des tiers à des fins commerciales.</p>"
       "<p>L'acheminement technique du formulaire est assuré par <strong>FormSubmit</strong> "
       "(formsubmit.co), qui transmet le contenu du formulaire vers la messagerie de l'entreprise. "
       "Ce prestataire n'exploite pas les données pour son propre compte. Les messages sont ensuite "
       "conservés dans la messagerie professionnelle de NG Couvreur.</p>"),
      ("Cookies et mesure d'audience",
       "<p>Ce site ne dépose aucun cookie publicitaire et n'utilise aucun traceur de mesure d'audience. Les "
       "polices de caractères sont chargées depuis Google Fonts, ce qui implique une connexion à ce service "
       "lors de l'affichage des pages.</p>"),
      ("Vos droits",
       "<p>Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation et d'opposition sur "
       "les données vous concernant. Pour l'exercer, contactez NG Couvreur au "
       "<a href=\"%s\">%s</a>. Vous pouvez également introduire une réclamation auprès de la CNIL "
       "(www.cnil.fr).</p>" % (TEL_HREF, TEL_TXT)),
    ], "Politique de confidentialité | NG Couvreur", "Politique de confidentialité et traitement des données personnelles — NG Couvreur, couvreur à Propriano.")

# ---------------------------------------------------------------------------
# §15  ROBOTS, SITEMAP, ASSETS, 404
# ---------------------------------------------------------------------------
def page_404():
    body = """<section class="section" style="padding-top:clamp(3rem,8vw,6rem)"><div class="shell">
  <p class="label">Erreur 404</p>
  <h1 style="margin:1.25rem 0 1.5rem;font-size:clamp(2rem,5vw,3.4rem)">Cette page n'existe pas.</h1>
  <p class="lead">Le lien est peut-être ancien ou mal recopié. Vous pouvez repartir de l'accueil, ou nous appeler directement.</p>
  <div class="actions" style="margin-top:2rem">
    <a class="btn btn--primary" href="%(home)s">Retour à l'accueil</a>
    <a class="btn btn--outline btn__tel" href="%(tel)s">%(teltxt)s</a>
  </div>
</div></section>""" % {"home": e(url()), "tel": TEL_HREF, "teltxt": TEL_TXT}
    h = head("Page introuvable | NG Couvreur", "La page demandée n'existe pas.", "404/", og_img=None)
    h = h.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex, follow">')
    full = os.path.join(OUT, "404.html")
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(h + header("") + body + footer())

def sitemap(paths):
    today = datetime.date.today().isoformat()
    prio = {"": "1.0", "services/": "0.9", "contact/": "0.9"}
    urls = ""
    for p in paths:
        urls += ('  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n'
                 % (abs_url(p), today, prio.get(p, "0.7")))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls)
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(xml)

    if PREVIEW:
        robots = "User-agent: *\nDisallow: /\n\n# Site en préparation. PREVIEW = False dans build.py avant mise en ligne.\n"
    else:
        robots = ("User-agent: *\nAllow: /\n\nSitemap: %s\n" % (SITE_ORIGIN + "/sitemap.xml"))
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(robots)

def main():
    # On repart d'un dossier propre, MAIS on préserve assets/img : les dérivés
    # web y sont déposés par optimize-images.py, qui tourne avant nous.
    if os.path.isdir(OUT):
        keep = {os.path.join(OUT, "assets", "img"), os.path.join(OUT, "assets", "icon")}
        for entry in os.listdir(OUT):
            path = os.path.join(OUT, entry)
            if entry != "assets":
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
        assets = os.path.join(OUT, "assets")
        if os.path.isdir(assets):
            for entry in os.listdir(assets):
                path = os.path.join(assets, entry)
                if path not in keep:
                    shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
    os.makedirs(os.path.join(OUT, "assets", "css"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets", "js"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets", "img"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets", "icon"), exist_ok=True)
    # Marque géométrique : un pan de toiture. Deux initiales seraient
    # illisibles à 16 px, une pente se lit encore à cette taille.
    open(os.path.join(OUT, "assets", "icon", "favicon.svg"), "w", encoding="utf-8").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        '<rect width="32" height="32" fill="#8A3A1E"/>'
        '<path d="M5 19.5 16 9l11 10.5" fill="none" stroke="#FDFCFA" '
        'stroke-width="3.4" stroke-linecap="square"/>'
        '<path d="M9.5 24.5h13" stroke="#E3A98C" stroke-width="2.6" stroke-linecap="square"/>'
        '</svg>\n')
    # Domaine personnalisé : GitHub Pages lit ce fichier à la racine de
    # l'artefact. Dérivé de SITE_ORIGIN, jamais saisi deux fois.
    if not PREVIEW:
        host = SITE_ORIGIN.split("//", 1)[-1].split("/", 1)[0]
        open(os.path.join(OUT, "CNAME"), "w", encoding="utf-8").write(host + "\n")
    shutil.copy(os.path.join(HERE, "site.css"), os.path.join(OUT, "assets", "css", "site.css"))
    shutil.copy(os.path.join(HERE, "site.js"),  os.path.join(OUT, "assets", "js",  "site.js"))
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    gitkeep = os.path.join(OUT, "assets", "img", ".gitkeep")
    if not os.path.exists(gitkeep):
        open(gitkeep, "w").write(
            "# Dérivés web produits par build/optimize-images.py.\n"
            "# Régénérés à chaque déploiement, jamais versionnés.\n")

    paths = [""]
    page_home()
    page_services_index();      paths.append("services/")
    for s in SERVICES:
        page_service(s);        paths.append("services/%s/" % s["slug"])
    page_entreprise();          paths.append("entreprise/")
    page_zones();               paths.append("zones-intervention/")
    for c in COMMUNES:
        if c["page"]:
            page_commune(c);    paths.append("zones-intervention/%s/" % c["page"])
    page_conseils_index();      paths.append("conseils/")
    for a in CONSEILS:
        page_conseil(a);        paths.append("conseils/%s/" % a["slug"])
    page_contact();             paths.append("contact/")
    page_merci()   # hors sitemap : page d'arrivée, pas une page d'entrée
    pages_legales();            paths += ["mentions-legales/", "politique-confidentialite/"]
    page_404()
    sitemap(paths)

    print("NG Couvreur — %d pages générées dans %s" % (len(paths), os.path.relpath(OUT)))
    print("  PREVIEW=%s  IMAGES_LOCAL=%s" % (PREVIEW, IMAGES_LOCAL))
    for p in paths:
        print("   /%s" % p)

if __name__ == "__main__":
    main()
