# NG COUVREUR — PROMPTS DE GENERATION DEFINITIFS
Plateforme : **Higgsfield** · Modele : `nano_banana_pro` · Resolution : `2k`

Les prompts sont rediges en anglais : c'est la langue sur laquelle les modeles de
diffusion sont le mieux alignes, et elle donne un controle nettement plus fin sur
la focale, la lumiere et la matiere. Chaque prompt integre, en fin de chaine, le
bloc BIBLE DE SERIE et le bloc de contraintes negatives, ce qui garantit la
continuite photographique de toute la banque.

Cohérence du personnage : le prompt de l'ancre `00A` fixe l'identite physique et la
tenue ; son `job_id` est ensuite passe en `image_references` sur chaque plan ou le
couvreur est reconnaissable. Les couples avant/apres (11 → 13 et 21 → 23) sont
generes en passant l'image AVANT en reference, afin que la maison, le cadrage et la
lumiere soient rigoureusement identiques.

---

## ANCRES DE SERIE

### 00A — `ancre-couvreur-A`

**Objectif sur le site** : Ancre d'identite du personnage recurrent  
**Cadrage / note** : Reference passee en image_references sur tous les plans ou le couvreur est reconnaissable  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `73f3462c-dcf3-4ae0-82d1-f0e368ac3292`

**Prompt Higgsfield :**

```text
Documentary editorial photograph, natural daylight. Environmental half-body portrait of a French Corsican roofing craftsman, age 42, standing on a residential street in Propriano, southern Corsica. Physical identity to lock: Mediterranean Corsican man, sun-weathered olive-tanned skin, deep crow's feet, short dark brown hair cut close at the sides with grey at the temples, short salt-and-pepper stubble beard, straight nose, calm dark brown eyes, medium athletic build, broad shoulders, working hands with visible calluses and short clean nails. Clothing to lock: plain charcoal-grey heavy cotton work trousers with reinforced knee panels and a folded tape-measure clip, a faded slate-blue long-sleeve work t-shirt with sleeves pushed to the forearms, absolutely no logos, no branding, no text anywhere. He is not posing for an advertisement: he stands three-quarter to camera, weight on one leg, looking slightly off-axis past the lens with a composed neutral expression, mouth closed, no wide smile. Background softly out of focus: a Corsican stone house wall in warm ochre lime render, a terracotta canal-tile roof edge, a green shuttered window. Late afternoon Mediterranean sunlight, warm but not orange, soft directional key from camera left, gentle fill from the render wall. Shot on a full-frame camera with an 85mm lens at f/2.0, shallow depth of field, natural skin texture with visible pores and fine sweat sheen, no retouching, no beauty smoothing, restrained natural colour grade, muted earth palette, controlled contrast, slight film grain. Absolute photorealism, indistinguishable from a professional reportage photograph.
```

### 00B — `ancre-couvreur-B`

**Objectif sur le site** : Ancre alternative  
**Cadrage / note** : Variante candide, utilisable comme reference de substitution  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `edc6ffa9-bffa-4ba4-9799-1ab58aa1b032`

**Prompt Higgsfield :**

```text
Documentary editorial photograph, natural daylight, candid reportage. Waist-up portrait of a French Corsican roofing craftsman, age 42, on a residential worksite in southern Corsica. Physical identity to lock: Mediterranean Corsican man, sun-weathered olive-tanned skin, pronounced crow's feet, short dark brown hair cropped at the sides with grey at the temples, short salt-and-pepper stubble beard, straight nose, calm dark brown eyes, medium athletic build, broad shoulders, thick working hands with calluses. Clothing to lock: plain charcoal-grey heavy cotton work trousers with reinforced knee panels, a faded slate-blue long-sleeve work t-shirt with sleeves rolled up the forearms, no logos, no branding, no text, no lettering anywhere in frame. He has just paused between two tasks: standing beside a stack of terracotta canal roof tiles, one hand resting on the tile stack, head turned slightly away from camera scanning the roofline, jaw relaxed, no smile, entirely unaware of the photographer. Environment: Corsican vernacular house, lime-rendered wall in pale sand tone, weathered green wooden shutter, dry maquis vegetation and a distant hillside softly blurred behind. Morning Mediterranean light, clear sky, soft directional sun from the left, luminous open shade on the face. Full-frame camera, 50mm lens at f/2.2, shallow depth of field, hyper-realistic skin texture with pores and fine dust on the forearms, natural unsaturated colour, controlled contrast, subtle grain, no retouching. Absolute photorealism, reportage aesthetic, not advertising.
```

## A — HERO / IDENTITE

### 01 — `hero-couvreur-toiture`

**Objectif sur le site** : Hero page d'accueil  
**Cadrage / note** : Titre + CTA dans la moitie superieure gauche restee vide  
**Ratio** : `16:9` · **Sortie** : 2752×1536 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 73f3462c-dcf3-4ae0-82d1-f0e368ac3292  
**job_id** : `4a050cec-2022-4c56-83eb-6e54f2de6d8d`

**Prompt Higgsfield :**

```text
Documentary reportage photograph. A roofing craftsman kneels on the sloping roof of a Corsican house, mid-gesture, setting an aged terracotta canal tile into a course. The canal-tile roof is correctly built: concave under-tiles laid in straight parallel channels running down the slope, convex cover-tiles bedded over the joints, courses perfectly aligned, a bed of lime mortar visible under the tile he is placing. A stack of six spare canal tiles rests beside his knee on a plank. He is safely equipped: a fall-arrest harness over his shoulders with a lanyard clipped to a visible ridge anchor point, and a tubular steel scaffold with guardrail and toe board running along the eave in the lower right foreground. THE CRAFTSMAN, recurring across the series: Corsican, 42, sun-weathered olive-tanned skin, short dark brown hair greying at the temples, short salt-and-pepper stubble beard, calm dark brown eyes, medium athletic build, thick calloused hands, plain charcoal-grey heavy cotton work trousers with reinforced knee panels, faded slate-blue work shirt with sleeves pushed to the forearms, worn leather tool belt, brown leather safety boots, no logos or text. He does not look at the camera and does not smile; he is absorbed in the tile. COMPOSITION, critical: the roof slope runs as a strong diagonal from the lower right to the middle left; the craftsman sits on the lower right third; the entire upper-left half of the frame is open clear sky, deliberately empty negative space reserved for a website headline and call-to-action button. Wide-angle 24mm lens at f/8, large depth of field, verticals corrected, camera positioned slightly above roof level. Late morning Mediterranean sunlight raking across the tiles from the left, revealing the barrel texture and lichen patina of the terracotta. SERIES BIBLE, mandatory: real documentary architectural photograph, southern Corsica near Propriano, Gulf of Valinco. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Clear sky with thin high clouds, dry luminous air. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre, sand, grey granite, patinated zinc, maquis green. Full-frame camera, fine film grain, high micro-contrast on material texture, no oversharpening, no HDR, no vignette, no lens flare. Vernacular Corsican architecture only: simple compact volumes, granite or lime-render walls in sand and pale ochre, solid wooden shutters in olive green, aged terracotta canal tiles, short roof overhang, low pitch. Absolute photorealism, indistinguishable from professional reportage, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: deformed hands, extra fingers, melted or bent tools, floating objects, impossible or misaligned tile courses, absurd architectural junctions, impossible perspective, American or Northern European houses, asphalt shingles, red brick, white PVC, bright orange new machine tiles, dramatic sky, HDR, oversaturation, smiling at camera, catalogue posing, plastic smooth skin, unsafe posture, unclipped harness, missing guardrail.
```

### 02 — `hero-maison-mediterraneenne`

**Objectif sur le site** : Hero alternatif / bandeau haut de page service  
**Cadrage / note** : Titre dans le tiers droit  
**Ratio** : `16:9` · **Sortie** : 2752×1536 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `0b27f7e2-ffa7-4bba-9359-45561684265c`

**Prompt Higgsfield :**

```text
Architectural documentary photograph, no people. A single-family Corsican house near Propriano seen in three-quarter view from a slightly elevated position, so that the entire roof surface reads clearly as the subject of the image. The roof is a low-pitch hipped roof in aged terracotta canal tiles, immaculately laid: straight parallel channels of concave under-tiles running down the slope, convex cover-tiles bedded over every joint, courses perfectly regular, a mortared ridge line of half-round ridge tiles, a clean patinated zinc half-round gutter on visible brackets along the eave with a correctly aligned downpipe descending the corner of the wall. The house has thick lime-rendered walls in pale sand ochre, granite stone quoins at the corners, solid olive-green wooden shutters, a stone-paved terrace and a low dry-stone wall. Around it: dry maquis scrub, an old olive tree, a cypress, ochre stony ground. Far background: soft granite hills of the Gulf of Valinco, atmospheric and pale. COMPOSITION, critical: the house occupies the left two thirds of the frame; the right third is open sky and distant hillside, deliberately kept as calm empty negative space for website headline text. Wide-angle 35mm lens at f/11, deep depth of field, verticals perfectly corrected, tripod-level horizon. Late afternoon Mediterranean sunlight from the left at a low grazing angle, sculpting the barrel relief of every tile and casting a long soft shadow of the eave on the render. SERIES BIBLE, mandatory: real documentary architectural photograph, southern Corsica near Propriano. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Clear sky with thin high clouds, dry luminous air. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre, sand, grey granite, patinated zinc, maquis green. Full-frame camera, fine film grain, high micro-contrast on material texture, no oversharpening, no HDR, no vignette, no lens flare. Absolute photorealism, indistinguishable from professional architectural reportage, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: impossible or misaligned tile courses, gutters without slope brackets or downpipe, gutters passing through walls, absurd architectural junctions, impossible perspective, American or Northern European houses, asphalt shingles, red brick, white PVC, bright orange new machine tiles, dramatic sky, HDR, oversaturation, postcard tourism look, 3D render.
```

### 03 — `hero-artisan-paysage`

**Objectif sur le site** : Hero Notre territoire / bandeau A propos  
**Cadrage / note** : Titre sur les deux tiers gauches (paysage)  
**Ratio** : `16:9` · **Sortie** : 2752×1536 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 73f3462c-dcf3-4ae0-82d1-f0e368ac3292  
**job_id** : `bf4264d1-d6a6-4643-966d-8a3e4e6916de`

**Prompt Higgsfield :**

```text
Documentary reportage photograph. A roofing craftsman stands upright astride the ridge of a Corsican house roof, seen from behind and slightly to the side, one hand resting on the mortared half-round ridge tiles, looking out across the landscape as he checks the alignment of the finished slope. He wears a fall-arrest harness with the lanyard clipped to a roof anchor on the ridge; a hooked roof ladder is correctly engaged over the ridge beside him and a scaffold guardrail is visible at the eave below. THE CRAFTSMAN, recurring across the series: Corsican, 42, sun-weathered olive-tanned skin, short dark brown hair greying at the temples, short salt-and-pepper stubble beard, medium athletic build, thick calloused hands, plain charcoal-grey heavy cotton work trousers with reinforced knee panels, faded slate-blue work shirt with sleeves pushed to the forearms, worn leather tool belt, brown leather safety boots, no logos or text. He is not aware of the camera and does not smile. COMPOSITION, critical: the craftsman and the roof ridge occupy the right third of the frame; the left two thirds open onto the Corsican landscape — dry maquis-covered granite slopes, scattered olive trees and cypresses, terracotta rooftops of a small hillside village, and a thin restrained band of the Mediterranean far behind, all held as calm negative space for website headline text. Medium telephoto 35mm lens at f/4, craftsman sharp, landscape gently softened by atmospheric depth. Late afternoon Mediterranean sunlight from behind camera left, warm rim light along his shoulder and the ridge tiles. SERIES BIBLE, mandatory: real documentary architectural photograph, southern Corsica near Propriano, Gulf of Valinco. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Clear sky with thin high clouds, dry luminous air. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre, sand, grey granite, patinated zinc, maquis green. Full-frame camera, fine film grain, high micro-contrast on material texture, no oversharpening, no HDR, no vignette, no lens flare. Vernacular Corsican architecture only. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. The Corsican setting must be perceptible but restrained, never a tourism postcard, no beach, no boats. Strictly avoid: deformed hands, impossible tile courses, impossible perspective, dramatic sky, HDR, oversaturation, heroic advertising pose, arms raised in triumph, plastic smooth skin, unsafe posture, unclipped harness.
```

### 04 — `hero-toiture-renovee`

**Objectif sur le site** : Hero Realisations, ouverture de page  
**Cadrage / note** : Titre dans la bande de ciel superieure  
**Ratio** : `16:9` · **Sortie** : 2752×1536 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `349cba26-bf4a-4045-a8d2-febc8e0f255e`

**Prompt Higgsfield :**

```text
Premium architectural photograph, no people. Elevated three-quarter view looking down onto a freshly renovated roof of a Corsican stone house near Propriano. The renovated covering is the subject: aged-tone terracotta canal tiles, correctly laid with concave under-tiles forming straight parallel channels down the slope and convex cover-tiles bedded over the joints, courses rigorously regular, a crisply mortared half-round ridge, a clean hip line, a newly formed patinated zinc valley gutter running between two roof planes, a zinc half-round eaves gutter on regularly spaced brackets, and a correctly flashed stone chimney with a zinc apron and back gutter. The wall below is granite rubble stone with lime pointing; an olive-green shuttered dormer window sits in the slope. Surroundings: stone terrace, dry-stone wall, olive tree, maquis scrub, pale ochre ground. COMPOSITION, critical: the roof planes form clean converging geometric shapes filling the lower two thirds; the upper portion holds calm open sky and the soft distant granite ridge line, kept as usable negative space for a page title. Wide-angle 24mm lens at f/11, deep depth of field, verticals corrected, no distortion. Late afternoon Mediterranean sunlight raking low from the left, revealing the barrel relief and subtle colour variation of every single tile, soft long shadows along the courses. SERIES BIBLE, mandatory: real documentary architectural photograph, southern Corsica near Propriano. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Clear sky with thin high clouds. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre, sand, grey granite, patinated zinc, maquis green. Full-frame camera, fine film grain, very high micro-contrast on the ceramic and zinc texture, no oversharpening, no HDR, no vignette, no lens flare. Absolute photorealism, publishable in a contemporary architecture magazine, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: impossible or misaligned tile courses, valley gutters without slope, chimneys without flashing, gutters without brackets or downpipe, absurd architectural junctions, impossible perspective, American or Northern European houses, asphalt shingles, red brick, white PVC, bright orange new machine tiles, dramatic sky, HDR, oversaturation, 3D render look.
```

## B — ENTREPRISE / ARTISAN

### 05 — `portrait-couvreur`

**Objectif sur le site** : Bloc Qui sommes-nous, page A propos  
**Cadrage / note** : Portrait editorial, non corporate  
**Ratio** : `3:4` · **Sortie** : 1792×2400 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 73f3462c-dcf3-4ae0-82d1-f0e368ac3292  
**job_id** : `391450b3-eebf-4c0c-9a77-2c68ba3ee1e2`

**Prompt Higgsfield :**

```text
Documentary editorial portrait, natural daylight, candid and unposed. Chest-up portrait of the recurring roofing craftsman, photographed on his worksite during a pause. THE CRAFTSMAN, identity to preserve exactly: Corsican man, 42, sun-weathered olive-tanned skin with pronounced crow's feet and open pores, short dark brown hair cropped at the sides and greying at the temples, short salt-and-pepper stubble beard, straight nose, calm dark brown eyes, medium athletic build, broad shoulders. He wears a faded slate-blue work shirt with the sleeves pushed up to the forearms, revealing tanned forearms with fine terracotta dust, and a worn leather tool belt at the edge of frame; no logos, no branding, no text. ATTITUDE, critical: this is not a corporate portrait. He stands three-quarter to camera, weight settled on one leg, one hand loosely holding a folded tape measure at his side, head turned slightly off-axis, eyes looking past the lens toward his roof, jaw relaxed, mouth closed, expression composed and quietly self-assured. No smile, no direct eye contact with the camera, no crossed arms, no folded-arms pose. Background: the lime-rendered sand-ochre wall of a Corsican house with a weathered olive-green shutter and the terracotta eave line above, thrown far out of focus. Framing: he sits on the lower two thirds, with head room above. Full-frame camera, 85mm lens at f/2.0, very shallow depth of field, background rendered as soft creamy planes of ochre and green. Late afternoon Mediterranean sunlight, soft directional key from camera left, warm bounce fill from the render wall, luminous open shade on the shadow side of the face. Hyper-realistic skin: visible pores, fine lines, faint sweat sheen, a little dust on the temple, absolutely no retouching, no skin smoothing, no beauty filter. SERIES BIBLE, mandatory: about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette. Fine film grain. Absolute photorealism, indistinguishable from a professional reportage portrait, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: deformed hands, extra fingers, smiling at camera, catalogue posing, thumbs up, crossed arms, plastic smooth skin, beauty retouching, studio lighting, flash, grey backdrop, corporate suit.
```

### 06 — `artisan-preparation`

**Objectif sur le site** : Section Notre methode, etape 1  
**Cadrage / note** : Preparation du materiel  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 73f3462c-dcf3-4ae0-82d1-f0e368ac3292  
**job_id** : `5a8b7214-e81a-4e92-a006-f74f2f62fca4`

**Prompt Higgsfield :**

```text
Documentary reportage photograph, candid, ground level. The recurring roofing craftsman prepares his materials at the foot of a Corsican house before going up. He is bent forward over a pair of wooden trestles, both hands flat on a long sheet of natural zinc that he is about to mark, a chalk line box and a folding rule beside his fingers. Around him, laid out with real working logic: a cerclé pallet of aged terracotta canal tiles, a roll of underlay membrane standing on end, a bucket of lime mortar with a trowel resting across the rim, a hand seamer and tin snips on the trestle, a coil of zinc gutter brackets, and a tubular steel scaffold rising behind him with guardrails and toe boards. THE CRAFTSMAN, recurring across the series: Corsican, 42, sun-weathered olive-tanned skin, short dark brown hair greying at the temples, short salt-and-pepper stubble beard, medium athletic build, thick calloused hands correctly gripping the material, plain charcoal-grey heavy cotton work trousers with reinforced knee panels, faded slate-blue work shirt with sleeves pushed to the forearms, worn leather tool belt, brown leather safety boots, no logos or text. He is fully concentrated on the zinc sheet, head down, unaware of the photographer, no smile. Composition: he is placed on the right of frame in a low three-quarter view, the tile pallet leading the eye in from the lower left, the render wall and the shuttered window behind. Full-frame camera, 50mm lens at f/2.8, subject sharp, background gently dissolved. Late morning Mediterranean sunlight, hard directional sun from the upper left, crisp shadows on the ground, warm bounce from the ochre wall. SERIES BIBLE, mandatory: real documentary photograph, southern Corsica near Propriano. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre, sand, grey granite, patinated zinc, maquis green. Full-frame camera, fine film grain, high micro-contrast on material texture, no oversharpening, no HDR, no vignette, no lens flare. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: deformed hands, extra fingers, melted or bent tools, tools held incorrectly, floating objects, impossible tile stacks, dramatic sky, HDR, oversaturation, smiling at camera, catalogue posing, plastic smooth skin, brand-new unused tools, unrealistically tidy worksite.
```

### 07 — `detail-mains-geste`

**Objectif sur le site** : Respiration graphique, bloc savoir-faire  
**Cadrage / note** : Detail du geste  
**Ratio** : `1:1` · **Sortie** : 2048×2048 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `7cd90c8a-c583-4796-8c18-0e00dc8bfa4c`

**Prompt Higgsfield :**

```text
Macro documentary photograph, human hands only, no face in frame. Extreme close-up of the thick calloused hands of a Corsican roofing craftsman, aged 42, sun-tanned skin, short clean nails, fine terracotta dust in the knuckle creases and a small healed scar on the back of one hand. The left hand steadies an aged terracotta canal tile at its edge while the right hand presses it down into a fresh bed of pale lime mortar spread along the tile course, a small pointing trowel resting in the mortar bucket just at the edge of the frame. The gesture is technically exact: the tile is being seated at the correct overlap onto the course below, the mortar squeezing slightly at the joint. The frayed cuff of a faded slate-blue work shirt is pushed up the forearm. Surrounding surface: the barrel channels of the canal-tile roof, warm terracotta with grey lichen patina and micro-porous ceramic texture. COMPOSITION: the hands fill the frame diagonally, mortar joint at the centre of interest, tiles falling out of focus toward the corners. 100mm macro lens at f/4, very shallow plane of focus locked on the fingertips and the mortar, creamy fall-off. Late morning Mediterranean sunlight raking from the left, sharp texture on skin and ceramic. SERIES BIBLE, mandatory: natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre and sand. Full-frame camera, fine film grain, extremely high micro-contrast on skin pores and ceramic grain, no oversharpening, no HDR, no vignette. Absolute photorealism, indistinguishable from a professional craft reportage photograph, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid, this is the critical risk of this image: deformed hands, extra fingers, missing fingers, fused fingers, wrong thumb placement, impossible wrist angle, doll-like smooth skin, manicured hands, clean unused hands, melted tools, floating tile, tile held in a physically impossible grip, oversaturation, HDR.
```

## C — COUVERTURE & TOITURE

### 08 — `couverture-pose`

**Objectif sur le site** : Page service Couverture, visuel principal  
**Cadrage / note** : Pose de couverture  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 73f3462c-dcf3-4ae0-82d1-f0e368ac3292  
**job_id** : `23924a7f-8d0b-440b-827c-1f50a1add91c`

**Prompt Higgsfield :**

```text
Documentary reportage photograph on a roof. Close-medium view of the recurring roofing craftsman kneeling on a roof plank, laying a new course of aged terracotta canal tiles onto freshly fixed wooden battens over a dark underlay membrane. The construction sequence is visible and technically correct from right to left: bare rafters and dark breathable underlay at the right, horizontal wooden battens fixed over it in the middle, then the first concave under-tiles seated in their parallel channels, then completed courses with convex cover-tiles bedded over the joints at the left. He holds one canal tile in both hands, lowering it into position at the correct overlap; a second tile waits by his knee. He wears a fall-arrest harness with the lanyard clipped to a visible anchor, and knee pads; a scaffold guardrail runs along the eave at the bottom edge of frame. THE CRAFTSMAN, recurring across the series: Corsican, 42, sun-weathered olive-tanned skin, short dark brown hair greying at the temples, short salt-and-pepper stubble beard, thick calloused hands, plain charcoal-grey heavy cotton work trousers with reinforced knee panels, faded slate-blue work shirt with sleeves pushed to the forearms, worn leather tool belt, brown leather safety boots, no logos or text. His face is angled down at the tile, entirely concentrated, no smile, no camera awareness. Composition: the tile courses run as a strong diagonal across the frame, craftsman on the right two thirds. 50mm lens at f/4, subject and near tile courses sharp, far eave softening. Late morning Mediterranean sunlight raking across the tiles from the left, strong barrel relief and clear shadow lines between the courses. SERIES BIBLE, mandatory: real documentary photograph, southern Corsica near Propriano. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette. Full-frame camera, fine film grain, high micro-contrast on ceramic and timber texture, no oversharpening, no HDR, no vignette. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: deformed hands, extra fingers, impossible or misaligned tile courses, tiles overlapping in an impossible direction, battens missing under the tiles, floating tiles, absurd roof structure, impossible perspective, dramatic sky, HDR, oversaturation, smiling at camera, catalogue posing, plastic smooth skin, unsafe posture, unclipped harness, missing guardrail.
```

### 09 — `couverture-tuiles`

**Objectif sur le site** : Page service Couverture, visuel secondaire  
**Cadrage / note** : Manutention des tuiles  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 73f3462c-dcf3-4ae0-82d1-f0e368ac3292  
**job_id** : `fe86274f-f3a1-4eff-87b5-6a5837883101`

**Prompt Higgsfield :**

```text
Documentary reportage photograph, candid. The recurring roofing craftsman carries a short stack of four aged terracotta canal tiles cradled against his hip and forearm, the correct way a roofer actually carries them, as he steps along the boarded platform of a tubular steel scaffold beside a Corsican house. His other hand rests lightly on the scaffold guardrail. The tiles show authentic weight in his posture: shoulder slightly dropped, forearm tendons engaged, body counterbalanced. Behind him on the platform, a neat pile of tiles and a bucket of mortar; above, the partially re-covered roof slope; below and behind, the lime-rendered sand-ochre wall of the house and an olive-green shutter. THE CRAFTSMAN, recurring across the series: Corsican, 42, sun-weathered olive-tanned skin, short dark brown hair greying at the temples, short salt-and-pepper stubble beard, medium athletic build, thick calloused hands, plain charcoal-grey heavy cotton work trousers with reinforced knee panels, faded slate-blue work shirt with sleeves pushed to the forearms, grey work gloves on his hands for the tile handling, worn leather tool belt, brown leather safety boots, no logos or text. He looks at the platform ahead of his feet, focused, no smile, unaware of the camera. Composition: he is offset to the left of frame walking into the open right side, scaffold tubes creating a clean vertical rhythm. 35mm lens at f/3.5, subject sharp, background compressed and soft. Late morning Mediterranean sunlight from the upper left, warm highlights on the terracotta stack, crisp shadow of the scaffold on the render wall. SERIES BIBLE, mandatory: real documentary photograph, southern Corsica near Propriano. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette. Full-frame camera, fine film grain, high micro-contrast on ceramic texture, no oversharpening, no HDR, no vignette. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: deformed hands, extra fingers, impossible tile stack, tiles floating or fused together, weightless posture, scaffold without guardrail or toe board, impossible perspective, dramatic sky, HDR, oversaturation, smiling at camera, catalogue posing, plastic smooth skin, unsafe posture.
```

### 10 — `couverture-terminee`

**Objectif sur le site** : Bandeau bas de page service  
**Cadrage / note** : Toiture achevee en contexte  
**Ratio** : `16:9` · **Sortie** : 2752×1536 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `7e480776-be02-4646-b8d4-b0b239d31ebe`

**Prompt Higgsfield :**

```text
Architectural documentary photograph, no people. A completed roof covering seen in its built environment: a Corsican village house near Propriano whose newly finished aged-terracotta canal-tile roof is read against the neighbouring rooftops. The covering is technically exemplary: concave under-tiles in straight parallel channels down the slope, convex cover-tiles bedded over every joint, courses rigorously regular, a mortared half-round ridge, a clean tiled verge at the gable edge, a patinated zinc half-round eaves gutter on evenly spaced brackets with a correctly positioned downpipe, and a stone chimney properly flashed with a zinc apron. Beyond it, the roofs of two adjacent older houses in weathered terracotta at slightly different tones and pitches, granite stone walls, olive-green shutters, a narrow stone lane, and dry maquis slopes rising softly in the far background. COMPOSITION: horizontal layering of rooftops receding into depth, the finished roof clearly dominant in the lower left two thirds, sky and pale hillside forming a calm band across the top for optional overlay text. 35mm lens at f/11, deep depth of field, verticals corrected, level horizon. Late afternoon Mediterranean sunlight low from the right, grazing the tiles so every barrel channel casts a fine shadow, subtle tonal separation between the new covering and the older neighbouring roofs. SERIES BIBLE, mandatory: real documentary architectural photograph, southern Corsica near Propriano. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Clear sky with thin high clouds. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre, sand, grey granite, patinated zinc, maquis green. Full-frame camera, fine film grain, high micro-contrast on ceramic texture, no oversharpening, no HDR, no vignette, no lens flare. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: impossible or misaligned tile courses, gutters without brackets or downpipe, chimneys without flashing, absurd architectural junctions, impossible perspective, American or Northern European houses, asphalt shingles, red brick, white PVC, bright orange new machine tiles, dramatic sky, HDR, oversaturation, tourism postcard look.
```

## D — RENOVATION

### 11 — `renovation-avant`

**Objectif sur le site** : Page Renovation, volet AVANT du comparateur  
**Cadrage / note** : Cadrage jumeau du n.13  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `b3e1cc0b-e41f-4a72-ad42-f28af238a0b9`

**Prompt Higgsfield :**

```text
Documentary photograph of a degraded roof, no people. BEFORE state of a renovation sequence. A Corsican stone house near Propriano photographed in three-quarter view from a slightly elevated position: the reference framing of this before-and-after pair. The old canal-tile roof is visibly failing but still standing: courses sagging in a shallow dip where a rafter has deflected, several cover-tiles slipped out of line or missing so the dark batten and under-tile show through, two tiles cracked across the barrel, thick green-grey moss cushions and pale lichen colonising the lower third of the slope, the mortared ridge crumbling with open joints and vegetation rooted in one gap, a rusted and sagging old gutter pulling away from the eave with a bent bracket, dark water staining running down the render below a failed junction. The house itself: granite rubble walls with tired lime pointing, faded blue-grey wooden shutters, one closed, ochre stony ground, dry maquis scrub, an old olive tree at the left edge. COMPOSITION, critical: this framing must be reproducible exactly — house three-quarter view, roof filling the upper two thirds, camera slightly above ground level, horizon level, verticals corrected. 35mm lens at f/11, deep depth of field. Neutral late morning Mediterranean sunlight, clear sky, even and unflattering, honest rather than dramatic. SERIES BIBLE, mandatory: real documentary architectural photograph, southern Corsica near Propriano. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre, sand, grey granite, moss green. Full-frame camera, fine film grain, high micro-contrast on weathered ceramic and stone, no oversharpening, no HDR, no vignette. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. The degradation must be plausible and specific, never cartoonish ruin, never a collapsed or abandoned house. Strictly avoid: total collapse, holes through the whole roof, burnt ruin, American or Northern European houses, asphalt shingles, red brick, white PVC, dramatic stormy sky, HDR, oversaturation, 3D render.
```

### 12 — `renovation-pendant`

**Objectif sur le site** : Page Renovation, etape chantier  
**Cadrage / note** : Sequence constructive lisible  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 73f3462c-dcf3-4ae0-82d1-f0e368ac3292  
**job_id** : `2069a621-8e3d-48a3-81b8-a8e351d781d4`

**Prompt Higgsfield :**

```text
Documentary reportage photograph, renovation in progress. The DURING state of a roof renovation sequence on a Corsican stone house near Propriano. The roof is half stripped and half rebuilt, and the sequence reads clearly across the slope: at the right, the old covering removed down to bare timber rafters, the sky visible between them; in the middle, a dark breathable underlay membrane rolled out and lapped correctly over the rafters with new horizontal wooden battens being fixed over it, bright pale sawn timber against the dark membrane; at the left, the first courses of aged terracotta canal tiles already re-laid, concave under-tiles in their parallel channels with convex cover-tiles bedded over the joints. The recurring roofing craftsman kneels at the boundary between battens and tiles, driving a batten nail with a hammer, body weight properly supported on a roof plank, fall-arrest harness on with the lanyard clipped to a visible anchor. Around the working area: a bundle of battens, a stack of salvaged tiles sorted for reuse, an offcut of underlay, a hooked roof ladder engaged over the ridge. A tubular steel scaffold with guardrails and toe boards surrounds the eave. THE CRAFTSMAN, recurring across the series: Corsican, 42, sun-weathered olive-tanned skin, short dark brown hair greying at the temples, short salt-and-pepper stubble beard, thick calloused hands, plain charcoal-grey heavy cotton work trousers with reinforced knee panels, faded slate-blue work shirt with sleeves pushed to the forearms, worn leather tool belt, brown leather safety boots, no logos or text. Focused on the nail, no smile, unaware of the camera. Composition: the three construction states layered as horizontal bands, craftsman at the centre-left junction. 35mm lens at f/5.6, generous depth of field. Late morning Mediterranean sunlight from the upper left, strong shadows of the battens across the membrane. SERIES BIBLE, mandatory: natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette. Full-frame camera, fine film grain, high micro-contrast on timber, membrane and ceramic, no oversharpening, no HDR, no vignette. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: deformed hands, extra fingers, melted or bent tools, hammer held incorrectly, battens fixed under the membrane instead of over it, tiles laid directly on rafters with no battens, floating materials, impossible roof structure, impossible perspective, dramatic sky, HDR, oversaturation, smiling at camera, plastic smooth skin, unsafe posture, unclipped harness, missing guardrail.
```

### 13 — `renovation-apres`

**Objectif sur le site** : Page Renovation, volet APRES du comparateur  
**Cadrage / note** : Genere a partir du n.11 : meme maison, meme cadrage, meme lumiere  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : b3e1cc0b-e41f-4a72-ad42-f28af238a0b9  
**job_id** : `e223ac5b-40c1-42d0-94d1-49070b908fa9`

**Prompt Higgsfield :**

```text
Documentary architectural photograph, no people. AFTER state of a renovation sequence, to be shown as a strict before-and-after pair with the reference image. Reproduce the reference photograph exactly — the same Corsican stone house, the same three-quarter viewpoint, the same camera height and distance, the same lens, the same framing, the same wall, the same shutters, the same olive tree, the same ground and vegetation, the same sunlight direction and time of day — and change ONLY the roof, which is now completely renovated. The new covering: aged-tone terracotta canal tiles laid to perfection, concave under-tiles forming straight parallel channels down the slope, convex cover-tiles bedded over every joint, courses rigorously regular with no sagging and no dip, the rafter deflection corrected so the roof plane is now true and flat, a crisply mortared half-round ridge with clean tight joints and no vegetation, a new patinated zinc half-round gutter sitting straight on evenly spaced brackets with a correctly aligned downpipe, and the water staining on the render below cleaned away. No moss, no lichen, no slipped or missing tiles, no cracked tiles. The tiles read as reclaimed and colour-matched to the region, warm and slightly varied, not factory-new and not bright orange. COMPOSITION: identical to the reference, house three-quarter view, roof filling the upper two thirds, horizon level, verticals corrected, 35mm lens at f/11, deep depth of field. Same neutral late morning Mediterranean sunlight, clear sky, honest rather than dramatic. SERIES BIBLE, mandatory: real documentary architectural photograph, southern Corsica near Propriano. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre, sand, grey granite, maquis green. Full-frame camera, fine film grain, high micro-contrast on ceramic and stone texture, no oversharpening, no HDR, no vignette. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: changing the house, the viewpoint, the framing or the light; impossible or misaligned tile courses; gutters without brackets or downpipe; bright orange new machine tiles; asphalt shingles; dramatic sky; HDR; oversaturation; 3D render.
```

## E — REPARATION & RECHERCHE DE FUITE

### 14 — `reparation-inspection`

**Objectif sur le site** : Page Recherche de fuite, visuel principal  
**Cadrage / note** : Inspection  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 73f3462c-dcf3-4ae0-82d1-f0e368ac3292  
**job_id** : `f4766e5e-8c1f-4792-943f-aeaa2ad92879`

**Prompt Higgsfield :**

```text
Documentary reportage photograph, roof inspection and leak investigation. The recurring roofing craftsman crouches low on a Corsican canal-tile roof, one knee down on a roof plank, upper body leaning forward, lifting the edge of a single convex cover-tile with his gloved left hand to look underneath at the batten and underlay, his right hand braced flat on the course beside him. His head is close to the tile and his eyes are narrowed in concentration on what he has found. A moisture meter and a torch lie on the plank within reach; a small pile of three tiles he has already lifted sits beside him. He wears a fall-arrest harness with the lanyard clipped to a visible roof anchor, and knee pads; a hooked roof ladder is correctly engaged over the ridge behind him and a scaffold guardrail runs along the eave. The roof shows the honest signs of a leak investigation: a slightly darker damp patch on the underlay visible in the gap, faint moss in the channel, one hairline-cracked tile set aside. THE CRAFTSMAN, recurring across the series: Corsican, 42, sun-weathered olive-tanned skin, short dark brown hair greying at the temples, short salt-and-pepper stubble beard, thick calloused hands, plain charcoal-grey heavy cotton work trousers with reinforced knee panels, faded slate-blue work shirt with sleeves pushed to the forearms, worn leather tool belt, brown leather safety boots, no logos or text. Entirely absorbed in the inspection, no smile, no camera awareness. Composition: low camera angle almost at tile level looking along the slope, craftsman in the right two thirds, the tile courses receding as leading lines. 50mm lens at f/3.5, plane of focus on his hands and the lifted tile, ridge softening behind. Late morning Mediterranean sunlight raking from the left. SERIES BIBLE, mandatory: natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette. Full-frame camera, fine film grain, high micro-contrast on ceramic texture, no oversharpening, no HDR, no vignette. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: deformed hands, extra fingers, melted or bent tools, floating objects, impossible tile courses, tiles lifted in a physically impossible way, absurd roof structure, impossible perspective, dramatic sky, HDR, oversaturation, smiling at camera, catalogue posing, plastic smooth skin, unsafe posture, unclipped harness, missing guardrail.
```

### 15 — `reparation-intervention`

**Objectif sur le site** : Page Reparation, visuel principal  
**Cadrage / note** : Intervention localisee  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 73f3462c-dcf3-4ae0-82d1-f0e368ac3292  
**job_id** : `1db7da34-3a6d-4126-8e7f-55e358cd0f90`

**Prompt Higgsfield :**

```text
Documentary reportage photograph, localised roof repair. The recurring roofing craftsman kneels on a roof plank on a Corsican canal-tile roof, carrying out a targeted repair on a small opened zone. The repair is technically exact and legible: within an otherwise intact roof, a patch of about one square metre has been carefully opened — the cover-tiles and under-tiles removed and stacked in two neat piles beside him, the batten and dark underlay exposed, one cracked tile set aside face down. With both hands he is sliding a sound replacement canal tile into position at the correct overlap under the course above. A slate hook and a small pointing trowel rest on the tiles at his knee, a bucket of lime mortar behind him. He wears a fall-arrest harness with the lanyard clipped to a visible roof anchor, knee pads, and grey work gloves; a hooked roof ladder is engaged over the ridge and a scaffold guardrail runs along the eave below. THE CRAFTSMAN, recurring across the series: Corsican, 42, sun-weathered olive-tanned skin, short dark brown hair greying at the temples, short salt-and-pepper stubble beard, thick calloused hands, plain charcoal-grey heavy cotton work trousers with reinforced knee panels, faded slate-blue work shirt with sleeves pushed to the forearms, worn leather tool belt, brown leather safety boots, no logos or text. Head down, precise, no smile, unaware of the camera. Composition: slightly high three-quarter angle looking down onto the opened patch, craftsman on the left, the repair zone as the bright centre of interest, intact courses framing it. 50mm lens at f/4. Late morning Mediterranean sunlight from the upper left, the opened patch clearly lit against the surrounding tiles. SERIES BIBLE, mandatory: natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette. Full-frame camera, fine film grain, high micro-contrast on ceramic and timber, no oversharpening, no HDR, no vignette. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: deformed hands, extra fingers, melted or bent tools, floating tiles, tiles slid in an impossible direction, battens missing under the covering, absurd roof structure, impossible perspective, dramatic sky, HDR, oversaturation, smiling at camera, plastic smooth skin, unsafe posture, unclipped harness.
```

### 16 — `reparation-detail-fuite`

**Objectif sur le site** : Encart technique Diagnostic  
**Cadrage / note** : Detail du desordre  
**Ratio** : `1:1` · **Sortie** : 2048×2048 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `d8bd5b3a-89dc-43b4-b4e5-871af24d3079`

**Prompt Higgsfield :**

```text
Macro documentary photograph, technical diagnostic detail, no people. Extreme close-up of a roof defect at the junction between an aged terracotta canal-tile covering and a granite stone chimney stack on a Corsican house. The defect is specific and technically credible: the zinc apron flashing at the base of the chimney has lifted slightly and its mortar fillet has cracked and partly fallen away, leaving an open joint of a few millimetres; immediately below, one canal tile carries a fine hairline crack running across its barrel; and on the stone and the tile beneath the open joint there is a darker damp stain with a faint white efflorescence bloom and a thin trace of moss taking hold in the wet line. Materials in full texture: porous warm terracotta with grey lichen freckling, rough granite with quartz grain, dull patinated zinc with fine scratches, crumbly pale lime mortar. COMPOSITION: the chimney base and flashing run diagonally across the frame, the cracked joint at the golden-section point, the damp stain leading the eye down and out of the lower left. 100mm macro lens at f/5.6, shallow plane of focus locked on the cracked mortar fillet and the lifted zinc, the tile field falling softly out of focus. Late morning Mediterranean sunlight raking hard from the left so the crack and the lifted zinc edge cast their own small shadows and read unmistakably. SERIES BIBLE, mandatory: natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, grey granite, patinated zinc, pale lime. Full-frame camera, fine film grain, extremely high micro-contrast on ceramic, stone and metal grain, no oversharpening, no HDR, no vignette. Absolute photorealism, indistinguishable from a professional building-diagnosis photograph, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: absurd or impossible flashing geometry, zinc passing through stone, chimney with no flashing at all, cartoonish damage, dramatic water gushing, oversaturation, HDR, 3D render.
```

## F — ETANCHEITE

### 17 — `etancheite-intervention`

**Objectif sur le site** : Page service Etancheite, visuel principal  
**Cadrage / note** : Mise en oeuvre membrane  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 73f3462c-dcf3-4ae0-82d1-f0e368ac3292  
**job_id** : `ea0c0593-dede-47b4-bd5b-81b046096535`

**Prompt Higgsfield :**

```text
Documentary reportage photograph, waterproofing work on a flat roof terrace. The recurring roofing craftsman is applying a bituminous waterproofing membrane on the flat terrace roof of a Corsican house near Propriano. He is crouched with both knees on a protective board, rolling out a heavy dark bitumen membrane sheet across the primed concrete deck, both hands pressing and guiding the roll forward at the leading edge so the sheet lies flat with a correct side lap over the previously laid sheet. Beside him: two more rolls of membrane standing upright, a stiff pressing roller, a seam roller, a tin of bituminous primer with a brush laid across it, and a propane torch with its hose coiled and the flame not lit, resting safely away from the roll. The already-laid area behind him is smooth and continuous, with the laps clearly visible as regular parallel lines. A low rendered parapet wall runs along the far edge with the membrane turned up correctly against it. He wears heat-resistant gloves, knee pads and safety glasses pushed up on his forehead. THE CRAFTSMAN, recurring across the series: Corsican, 42, sun-weathered olive-tanned skin, short dark brown hair greying at the temples, short salt-and-pepper stubble beard, thick calloused hands, plain charcoal-grey heavy cotton work trousers with reinforced knee panels, faded slate-blue work shirt with sleeves pushed to the forearms, brown leather safety boots, no logos or text. Head down, absorbed, no smile, unaware of the camera. Composition: the membrane laps run as strong parallel diagonals from the lower left, craftsman at the centre-right, the parapet and a slice of Corsican hillside and sky across the top. 35mm lens at f/5.6. Late morning Mediterranean sunlight from the upper left; the matt black membrane reads with subtle sheen and granular mineral texture, not as a flat black shape. SERIES BIBLE, mandatory: natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette with the dark membrane as the graphic anchor. Full-frame camera, fine film grain, high micro-contrast on the mineral membrane surface, no oversharpening, no HDR, no vignette. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: deformed hands, extra fingers, melted or bent tools, lit torch pointed at the operator or at the roll, torch used without gloves, floating rolls, membrane laps running in impossible directions, membrane with no upstand at the parapet, impossible perspective, dramatic sky, HDR, oversaturation, smiling at camera, plastic smooth skin, unsafe posture.
```

### 18 — `etancheite-detail`

**Objectif sur le site** : Page Etancheite, encart materiau  
**Cadrage / note** : Releve d'etancheite  
**Ratio** : `1:1` · **Sortie** : 2048×2048 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `ddf4f3bc-ce08-4c91-8840-a4032118255b`

**Prompt Higgsfield :**

```text
Macro documentary photograph, waterproofing detail, no people. Extreme close-up of a correctly executed waterproofing upstand at the foot of a rendered parapet wall on a Corsican flat roof terrace. The detail is technically exemplary and clearly legible: the dark mineral-surfaced bitumen membrane runs across the deck, turns up the face of the parapet to a proper height, and is terminated at the top by a slim folded zinc capping bead mechanically fixed and sealed, with a clean continuous bead of grey mastic along its lower edge. At the base of the upstand the membrane forms a smooth, regular cove fillet with no wrinkle, no crease and no trapped air, and a horizontal side lap on the deck is welded flat with a fine bitumen bleed line visible along its edge — the signature of a correct seam. Materials in full texture: dark grey-black membrane with fine mineral granules catching the light, pale sand lime render above with its sandy tooth, dull patinated zinc, matt grey mastic. COMPOSITION: the upstand runs as a strong horizontal band across the lower two thirds, the parapet render filling the top third, the lap line entering from the lower left corner. 100mm macro lens at f/5.6, plane of focus on the cove fillet and the lap, softening toward the corners. Late afternoon Mediterranean sunlight raking low from the right so the granular membrane surface, the fold of the zinc and the fillet radius each read in relief. SERIES BIBLE, mandatory: natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, restrained palette of charcoal, sand and zinc grey. Full-frame camera, fine film grain, extremely high micro-contrast on the mineral granules and the render tooth, no oversharpening, no HDR, no vignette. Absolute photorealism, indistinguishable from a professional building-detail photograph, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: membrane ending flat with no upstand, upstand with no capping or seal, wrinkled or blistered membrane presented as finished work, impossible geometry, absurd junctions, oversaturation, HDR, 3D render, CGI look.
```

## G — ZINGUERIE & GOUTTIERES

### 19 — `zinguerie-gouttiere`

**Objectif sur le site** : Page service Zinguerie, visuel principal  
**Cadrage / note** : Pose de gouttiere zinc  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 73f3462c-dcf3-4ae0-82d1-f0e368ac3292  
**job_id** : `1f681eda-3258-4a8d-bf02-bbd87f1d697b`

**Prompt Higgsfield :**

```text
Documentary reportage photograph, gutter installation. The recurring roofing craftsman stands on the boarded platform of a tubular steel scaffold at eave level of a Corsican house, fitting a length of natural zinc half-round gutter into its brackets. The work is technically exact: a run of zinc gutter brackets is already fixed to the eave board at regular spacing and, critically, set at a slightly descending line to give the gutter its fall toward the downpipe; he is lowering the half-round zinc section into the brackets with both hands, the rear edge already engaged under the tile overhang and the front bead about to drop into the bracket lip. A second gutter length rests on the platform, along with a hand seamer, tin snips, a spirit level and a soldering iron with a block of tin. The terracotta canal-tile eave course projects correctly above the gutter; further along, the downpipe outlet and the first bracket of the vertical downpipe are already in place on the render wall. He wears grey work gloves; the scaffold has guardrails and toe boards. THE CRAFTSMAN, recurring across the series: Corsican, 42, sun-weathered olive-tanned skin, short dark brown hair greying at the temples, short salt-and-pepper stubble beard, thick calloused hands, plain charcoal-grey heavy cotton work trousers with reinforced knee panels, faded slate-blue work shirt with sleeves pushed to the forearms, worn leather tool belt, brown leather safety boots, no logos or text. Concentrated on the bracket, no smile, unaware of the camera. Composition: camera on the scaffold beside him, the gutter run receding as a strong perspective line to the right, craftsman on the left two thirds, tiles above, render wall below. 50mm lens at f/4. Late afternoon Mediterranean sunlight from the right, warm reflected light along the curved zinc, cool shadow under the eave. SERIES BIBLE, mandatory: natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, sand and patinated zinc. Full-frame camera, fine film grain, high micro-contrast on the zinc and ceramic, no oversharpening, no HDR, no vignette. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: deformed hands, extra fingers, melted or bent tools, floating gutter, gutter with no brackets, gutter with no fall, gutter with no downpipe, gutter passing through the wall, gutter above the tile line, absurd junctions, impossible perspective, white PVC gutter, dramatic sky, HDR, oversaturation, smiling at camera, plastic smooth skin, scaffold without guardrail, unsafe posture.
```

### 20 — `zinguerie-detail`

**Objectif sur le site** : Page Zinguerie, encart finitions  
**Cadrage / note** : Raccord de noue soude  
**Ratio** : `1:1` · **Sortie** : 2048×2048 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `7207e76c-176c-4833-b10f-bb687e22bc92`

**Prompt Higgsfield :**

```text
Macro documentary photograph, zinc work detail, no people. Extreme close-up of a hand-formed natural zinc valley gutter where two terracotta canal-tile roof planes meet on a Corsican house. The zinc work is exemplary and technically credible: the valley tray is folded with crisp straight standing edges on both sides, its centre channel running true down the slope; two tray sections are joined by a soldered lap, the tin solder line visible as a slightly brighter, subtly rippled seam running across the tray, cleanly wiped, with faint flux discolouration around it; the cut ends of the canal tiles on both sides are trimmed to a regular straight line along the standing edge and bedded in pale lime mortar, leaving an even water channel down the middle. Materials in full texture: dull patinated zinc, matt grey-blue with fine hammer and tool marks, light oxidation bloom and a few pale scratches; warm porous terracotta with grey lichen freckling and sharp cut edges. COMPOSITION: the valley runs as a powerful diagonal from the bottom centre of the frame to the upper right, tiles closing in symmetrically on both sides, the soldered seam placed at the strongest third. 100mm macro lens at f/5.6, plane of focus locked on the solder seam and the near standing edge, tiles softening toward the top of frame. Late afternoon Mediterranean sunlight raking low from the left, a long soft specular reflection travelling down the zinc channel, every fold catching a fine highlight. SERIES BIBLE, mandatory: natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, palette of patinated zinc grey against warm terracotta. Full-frame camera, fine film grain, extremely high micro-contrast on the metal grain and ceramic pores, no oversharpening, no HDR, no vignette. Absolute photorealism, indistinguishable from a professional craft-detail photograph, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: impossible metal geometry, zinc folded in a physically impossible way, valley with no fall, valley narrower at the bottom, tiles floating over the zinc with no bedding, absurd junctions, mirror-polished chrome look, oversaturation, HDR, 3D render, CGI.
```

## H — NETTOYAGE & DEMOUSSAGE

### 21 — `demoussage-avant`

**Objectif sur le site** : Page Demoussage, volet AVANT  
**Cadrage / note** : Cadrage jumeau du n.23  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `2d19c093-4e0c-42ab-bf32-fa3c6da21295`

**Prompt Higgsfield :**

```text
Documentary photograph of a heavily soiled roof, no people. BEFORE state of a roof-cleaning sequence. A Corsican house near Propriano photographed in three-quarter view from a slightly elevated position: the reference framing of this before-and-after pair. The structure of the roof is entirely sound — courses straight, no sagging, no missing tiles — but the covering is biologically colonised: thick dark green moss cushions filling the channels between the canal tiles, especially on the lower and shaded north-facing part of the slope, pale grey-green crustose lichen freckling spreading across the exposed barrels, blackish algae staining in the run-off lines, a few small tufts of dry grass rooted in the ridge joints, and the zinc eaves gutter partly filled with moss debris and leaf litter with a dark damp streak below its outlet. The house: lime-rendered walls in pale sand ochre, granite quoins, faded olive-green wooden shutters, ochre stony ground, dry maquis scrub, a fig tree at the right edge whose shade explains the heavier moss on that side. COMPOSITION, critical: this framing must be reproducible exactly — house three-quarter view, roof filling the upper two thirds, camera slightly above ground level, horizon level, verticals corrected. 35mm lens at f/11, deep depth of field. Neutral late morning Mediterranean sunlight, clear sky, even and honest, never dramatic. SERIES BIBLE, mandatory: real documentary architectural photograph, southern Corsica near Propriano. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre, sand, grey granite and deep moss green. Full-frame camera, fine film grain, extremely high micro-contrast on the moss cushions and lichen crust, no oversharpening, no HDR, no vignette. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: structural damage, collapse, missing or slipped tiles, abandoned ruin, cartoonish overgrowth, ivy covering the whole house, American or Northern European houses, asphalt shingles, red brick, white PVC, dramatic sky, HDR, oversaturation, 3D render.
```

### 22 — `demoussage-pendant`

**Objectif sur le site** : Page Demoussage, etape intervention  
**Cadrage / note** : Nettoyage basse pression  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 73f3462c-dcf3-4ae0-82d1-f0e368ac3292  
**job_id** : `1887a616-badf-44be-87ed-779a05bf9aab`

**Prompt Higgsfield :**

```text
Documentary reportage photograph, roof cleaning in progress. The recurring roofing craftsman is cleaning a moss-covered Corsican canal-tile roof with a low-pressure lance. He stands braced and stable on a hooked roof ladder correctly engaged over the ridge, both feet on the rungs, body upright, holding the lance in two hands with the jet directed DOWN the slope from ridge toward eave — the correct direction, never up under the tiles. The lance produces a wide, soft, low-pressure fan of water, not a violent jet, and a fine mist drifts and catches the light. The cleaning progress is visible as a clear diagonal boundary across the slope: behind and below the lance the tiles are already stripped back to clean warm terracotta and glisten dark with water; ahead of it the moss cushions and grey lichen remain. Loosened moss debris slides in a wet mat toward the eave and gathers at the gutter. He wears a fall-arrest harness with the lanyard clipped to a visible ridge anchor, safety glasses, waterproof gloves and boots; a scaffold with guardrails runs along the eave. THE CRAFTSMAN, recurring across the series: Corsican, 42, sun-weathered olive-tanned skin, short dark brown hair greying at the temples, short salt-and-pepper stubble beard, thick calloused hands, plain charcoal-grey heavy cotton work trousers with reinforced knee panels, faded slate-blue work shirt with sleeves pushed to the forearms and darkened with spray, brown leather safety boots, no logos or text. Watching the cleaning line intently, no smile, unaware of the camera. Composition: the clean-versus-moss boundary is the graphic subject, running as a diagonal across the frame; craftsman in the upper right third. 35mm lens at f/4.5. Late morning Mediterranean sunlight from behind camera left, backlighting the water mist into a soft luminous veil without any flare. SERIES BIBLE, mandatory: natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of wet terracotta against moss green. Full-frame camera, fine film grain, high micro-contrast on wet ceramic and moss, no oversharpening, no HDR, no vignette, no lens flare. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: deformed hands, extra fingers, melted or bent tools, lance held one-handed at arm's length, jet aimed up the slope under the tiles, high-pressure jet blasting tiles apart, craftsman standing directly on wet mossy tiles without a ladder, ladder not hooked over the ridge, unclipped harness, missing guardrail, impossible perspective, dramatic sky, HDR, oversaturation, smiling at camera, plastic smooth skin.
```

### 23 — `demoussage-apres`

**Objectif sur le site** : Page Demoussage, volet APRES  
**Cadrage / note** : Genere a partir du n.21 : meme maison, meme cadrage, meme lumiere  
**Ratio** : `3:2` · **Sortie** : 2528×1696 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 2d19c093-4e0c-42ab-bf32-fa3c6da21295  
**job_id** : `6fbe21ec-2f6e-4ee5-b0be-eed679ea9357`

**Prompt Higgsfield :**

```text
Documentary architectural photograph, no people. AFTER state of a roof-cleaning sequence, to be shown as a strict before-and-after pair with the reference image. Reproduce the reference photograph exactly — the same Corsican house, the same three-quarter viewpoint, the same camera height and distance, the same lens, the same framing, the same lime-rendered sand-ochre walls, the same granite quoins, the same faded olive-green shutters, the same fig tree at the right edge, the same ground, the same vegetation, the same sunlight direction and time of day — and change ONLY the state of the roof covering, which has now been fully cleaned and treated. The canal tiles are stripped back to clean warm terracotta with their natural colour variation restored: no moss cushions in the channels, no crustose lichen on the barrels, no black algae staining in the run-off lines, no grass tufts in the ridge joints. The tiles look genuinely cleaned rather than new — they keep their age, their slight tonal differences from tile to tile, faint permanent shadow-marks where the moss had sat for years, and the honest patina of an old covering. The zinc eaves gutter is emptied and clear, its outlet free, and the dark damp streak below it has been washed away. The roof surface is dry, not wet. COMPOSITION: identical to the reference, house three-quarter view, roof filling the upper two thirds, horizon level, verticals corrected, 35mm lens at f/11, deep depth of field. Same neutral late morning Mediterranean sunlight, clear sky, even and honest, never dramatic. SERIES BIBLE, mandatory: real documentary architectural photograph, southern Corsica near Propriano. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre, sand, grey granite. Full-frame camera, fine film grain, high micro-contrast on the ceramic texture, no oversharpening, no HDR, no vignette. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: changing the house, the viewpoint, the framing or the light; replacing the tiles with new ones; bright orange factory-fresh machine tiles; a uniformly flat single-colour roof; wet glossy tiles; impossible or misaligned tile courses; dramatic sky; HDR; oversaturation; 3D render.
```

## I — DETAILS / SAVOIR-FAIRE

### 24 — `detail-faitage`

**Objectif sur le site** : Mosaique savoir-faire  
**Cadrage / note** : Detail faitage  
**Ratio** : `1:1` · **Sortie** : 2048×2048 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `7e0212e6-ee79-4c30-8aa9-2010e249e9de`

**Prompt Higgsfield :**

```text
Macro documentary photograph, ridge detail, no people. Extreme close-up along the finished ridge of a Corsican canal-tile roof. The half-round terracotta ridge tiles run away from the camera in a perfectly straight line, each one overlapping the next in the correct direction, bedded on a fillet of pale lime mortar that has been struck off neatly and cleanly along both sides with the trowel, the mortar joint regular and continuous with no gaps and no smears on the tile faces. Beneath the ridge, the topmost courses of canal tiles rise to meet it from both slopes: concave under-tiles in their parallel channels, convex cover-tiles bedded over the joints. Materials in full texture: warm terracotta with visible ceramic porosity, subtle colour variation from tile to tile, delicate grey lichen freckling on the older cover-tiles, the pale sandy tooth of fresh lime mortar, a faint dusting of mortar grit in one channel. COMPOSITION: the ridge line runs as a strong diagonal from the lower left to the upper right, dividing the frame into two slopes of receding tile channels, the nearest mortar joint at the golden section. 100mm macro lens at f/5.6, plane of focus locked on the second and third ridge tiles and their mortar joint, the line dissolving softly into the distance. Late afternoon Mediterranean sunlight raking low from the left so each ridge tile casts a crisp shadow on the next and every tile channel reads in deep relief. SERIES BIBLE, mandatory: natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre and pale lime. Full-frame camera, fine film grain, extremely high micro-contrast on the ceramic grain and mortar aggregate, no oversharpening, no HDR, no vignette. Absolute photorealism, indistinguishable from a professional craft-detail photograph, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. Strictly avoid: ridge tiles overlapping in alternating or impossible directions, ridge tiles floating with no mortar bedding, wavy or misaligned ridge line, impossible tile geometry, bright orange new machine tiles, oversaturation, HDR, 3D render, CGI look.
```

### 25 — `detail-outils`

**Objectif sur le site** : Mosaique savoir-faire, bloc Nos gestes  
**Cadrage / note** : Nature morte outils  
**Ratio** : `1:1` · **Sortie** : 2048×2048 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `bcecbee7-a4d3-4447-a568-f8129a707358`

**Prompt Higgsfield :**

```text
Macro documentary still-life photograph, no people, nothing staged. A roofer's tools resting on the canal tiles of a Corsican roof exactly where he set them down during the work. Laid across the warm terracotta barrels: a worn leather tool belt with darkened, cracked leather and a scuffed brass buckle, its pouch open; a roofer's hammer with a hickory handle polished dark by use and a slightly chipped, unpolished steel head; a pair of tin snips with red-worn handles and a fine metallic sheen on the cutting edges; a chalk line box dusted with blue pigment, a short length of line trailing across a tile channel; a folding wooden rule half opened; and a small pointing trowel with dried pale lime mortar crusted near the heel. The objects sit with real weight and real contact shadows, slightly askew, one tool bridging two tile barrels rather than lying impossibly flat. A scatter of terracotta dust and one dry pine needle complete the scene. COMPOSITION: seen from directly above at a slight angle, the tile channels running as parallel diagonals from the lower left to the upper right, the tools arranged in a loose natural cluster occupying the centre and lower right, with two empty tile channels at the upper left as breathing space. 90mm macro lens at f/5.6, plane of focus on the hammer head and the belt buckle, edges of frame gently softening. Late afternoon Mediterranean sunlight raking low from the left, long tool shadows across the tile relief, warm reflected bounce from the terracotta into the steel. SERIES BIBLE, mandatory: natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, aged leather brown, worn steel grey. Full-frame camera, fine film grain, extremely high micro-contrast on leather grain, steel patina, timber and ceramic pores, no oversharpening, no HDR, no vignette. Absolute photorealism, indistinguishable from a professional craft-reportage still life, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand, engraving or watermark on any tool or anywhere in the frame. Strictly avoid: melted, bent, duplicated or invented tools, tools with impossible geometry, brand-new shiny unused tools, catalogue product-shot lighting, objects floating without contact shadows, perfectly symmetrical arrangement, oversaturation, HDR, 3D render, CGI look.
```

## J — PROPRIANO / CORSE-DU-SUD

### 26 — `contexte-propriano`

**Objectif sur le site** : Page Zone d'intervention, visuel principal  
**Cadrage / note** : Architecture residentielle  
**Ratio** : `16:9` · **Sortie** : 2752×1536 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `918e96d5-5706-491d-94c8-ab0f7c0b1ab0`

**Prompt Higgsfield :**

```text
Documentary architectural photograph, contextual, no people. A quiet residential street in the hills above Propriano, southern Corsica, showing the everyday domestic architecture the roofer works on. Three or four modest houses step down the slope, each with its own roof clearly readable: low-pitch hipped and gabled roofs in aged terracotta canal tiles at slightly different tones and ages, mortared half-round ridges, patinated zinc gutters on brackets with downpipes running down the corners of the walls, one stone chimney with a zinc flashing apron. The buildings are vernacular and unglamorous: thick lime-rendered walls in sand, pale ochre and weathered white, exposed granite quoins and lintels, solid wooden shutters in olive green and faded blue, a small first-floor balcony with a simple painted iron rail, an outside stair, a stone-paved forecourt, a low dry-stone wall. Around them: dry maquis scrub, an old olive tree, two cypresses, a fig, ochre stony ground, a narrow tarred lane. Far background: the pale granite ridges of the Valinco hinterland, soft with distance, and a thin restrained sliver of the Mediterranean glimpsed between two roofs. COMPOSITION: the rooftops layer into depth across the frame, the nearest roof anchoring the lower left, the sky and pale ridge line forming a calm horizontal band across the top for overlay text. 35mm lens at f/11, deep depth of field, verticals corrected, level horizon. Late afternoon Mediterranean sunlight low from the right, grazing the tiles and the render, long soft shadows, warm but unspectacular light. SERIES BIBLE, mandatory: real documentary architectural photograph, southern Corsica near Propriano, Gulf of Valinco. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Clear sky with thin high clouds. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre, sand, grey granite, patinated zinc, maquis green. Full-frame camera, fine film grain, high micro-contrast on render and ceramic texture, no oversharpening, no HDR, no vignette, no lens flare. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand, road sign, shop sign or watermark anywhere. The Corsican identity must be perceptible but restrained — this is a working residential street, not a tourism postcard: no beach, no harbour, no boats, no parasols, no tourists, no bougainvillea-covered picture-perfect alley. Strictly avoid: American or Northern European houses, asphalt shingles, red brick, white PVC, Provencal postcard cliches, bright orange new machine tiles, dramatic sky, HDR, oversaturation, tilt-shift toy look, 3D render.
```

### 27 — `contexte-valinco`

**Objectif sur le site** : Bandeau Nos communes, fond de section  
**Cadrage / note** : Toiture + relief corse  
**Ratio** : `16:9` · **Sortie** : 2752×1536 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : aucune (text-to-image)  
**job_id** : `e4cf4ef3-3ace-413e-9d87-003c4326672b`

**Prompt Higgsfield :**

```text
Documentary architectural photograph, contextual, no people. A single Corsican house roof read against the landscape of the Valinco hinterland. The camera is positioned on the slope above the house, so the aged terracotta canal-tile roof fills the lower third of the frame as a strong, textured, warm foreground plane — courses straight and regular, concave under-tiles in parallel channels, convex cover-tiles over the joints, mortared half-round ridge running horizontally, a patinated zinc gutter and a stone chimney with zinc flashing at the left edge. Beyond and above the ridge line, the land opens out: dry maquis-covered granite hillsides in layered receding planes, scattered holm oaks, olive trees and dark cypresses, outcrops of pale weathered granite, a distant terracotta-roofed hamlet small on a far spur, and at the very back a thin restrained band of the Mediterranean in the Gulf of Valinco, pale and desaturated, more atmosphere than subject. COMPOSITION: the roof ridge divides the frame as a firm horizontal at the lower third; the hillside planes stack above it into haze; the upper band of sky and the softest distant ridge are kept calm and empty as usable negative space for a section title. Telephoto 50mm lens at f/8 with a compressed, layered perspective, deep depth of field, level horizon, verticals corrected. Late afternoon Mediterranean sunlight low from the left, raking the tile barrels in the foreground into strong relief while the successive hillsides fall away into progressively paler atmospheric layers. SERIES BIBLE, mandatory: real documentary architectural photograph, southern Corsica near Propriano, Gulf of Valinco. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Clear sky with thin high clouds, dry luminous air. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre, sand, grey granite, maquis green, muted Mediterranean blue. Full-frame camera, fine film grain, high micro-contrast on the near ceramic texture, no oversharpening, no HDR, no vignette, no lens flare. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand or watermark anywhere. The Corsican identity must be perceptible but restrained — not a tourism postcard: no beach, no harbour, no boats, no sunset spectacle. Strictly avoid: dramatic golden-hour sky, fiery clouds, oversaturated turquoise sea, HDR, impossible tile courses, American or Northern European houses, bright orange new machine tiles, 3D render, matte-painting look.
```

## K — CONTACT / CONVERSION

### 28 — `contact-cta`

**Objectif sur le site** : Bloc Un projet de toiture ? Parlons-en. + tel.  
**Cadrage / note** : Negative space sur le tiers droit pour le CTA  
**Ratio** : `16:9` · **Sortie** : 2752×1536 px  
**Modele** : `nano_banana_pro` (2k) · **Reference d'identite** : 73f3462c-dcf3-4ae0-82d1-f0e368ac3292  
**job_id** : `5cd16df7-58b4-4d74-9b8b-d5094ae0414f`

**Prompt Higgsfield :**

```text
Documentary reportage photograph, end of the working day, reassuring and human. The recurring roofing craftsman stands at the open rear doors of a plain white work van parked on the stone forecourt of a Corsican house, having just come down from the roof. He is stowing his tools: one hand resting on the open van door, the other lowering a coiled length of rope and a hand seamer into a battered wooden tool crate in the van, his body turned three-quarters away from the camera, head slightly lowered, expression calm and unguarded, the loose attentiveness of a man finishing a job well. Inside the van, ordinary working order: stacked crates, a folded tarpaulin, a bundle of battens, a short ladder on the roof rack above. Behind him the house he has been working on, its freshly finished aged-terracotta canal-tile roof catching the low light, a section of tubular steel scaffold still standing at the gable with guardrails. THE CRAFTSMAN, recurring across the series: Corsican, 42, sun-weathered olive-tanned skin, short dark brown hair greying at the temples, short salt-and-pepper stubble beard, medium athletic build, thick calloused hands, plain charcoal-grey heavy cotton work trousers with reinforced knee panels, faded slate-blue work shirt with sleeves pushed to the forearms, worn leather tool belt, brown leather safety boots, all lightly dusted from the day. The van is entirely unmarked: no logo, no lettering, no signwriting, no number plate text. He does not look at the camera and does not smile for it. COMPOSITION, critical: the craftsman and the van occupy the LEFT third of the frame; the centre and the entire RIGHT third open onto the sunlit stone forecourt, the low dry-stone wall, an olive tree and the soft maquis hillside, deliberately held as calm uncluttered negative space for a website call-to-action headline, a phone number and a button. 35mm lens at f/4, craftsman sharp, background gently softened. Late afternoon Mediterranean sunlight low from the right, warm and settled, long soft shadows across the forecourt, warm rim light along his shoulder. SERIES BIBLE, mandatory: real documentary photograph, southern Corsica near Propriano. Natural sunlight only, no flash, about 5400K, warm but neutral, never orange. Controlled contrast, soft tonal curve, slightly lifted blacks, natural to slightly desaturated colour, earth palette of terracotta, ochre, sand, grey granite, maquis green. Full-frame camera, fine film grain, high micro-contrast on material texture, no oversharpening, no HDR, no vignette, no lens flare. Absolute photorealism, never stock advertising, never 3D render, never illustration, never AI-looking. No text, lettering, logo, brand, signwriting, licence plate characters or watermark anywhere in the frame. Strictly avoid: deformed hands, extra fingers, melted or bent tools, floating objects, smiling at camera, thumbs up, crossed arms, handshake, catalogue posing, salesman look, plastic smooth skin, dramatic sunset sky, HDR, oversaturation, impossible perspective, branded van, clean showroom van.
```
