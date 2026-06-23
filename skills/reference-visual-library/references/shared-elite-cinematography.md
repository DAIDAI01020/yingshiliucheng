# Shared Elite Cinematography Anchors v1

Use this file when a project needs high-level cinematic discipline across commercial/promo or short-drama workflows.

This layer is not a list of names to paste into prompts. It converts cinematographer/director reference into camera, light, color, material, and composition decisions.

## Usage Rule

Choose one anchor only when it clarifies the camera/light system.

Do not stack many cinematographer names inside the final prompt. Final prompts should describe the visual mechanism, not depend on name-dropping.

If the user gives no reference, actively recommend one suitable cinematography anchor for the project type instead of leaving the style generic. Short drama and promo work should receive a professional camera/light floor before prompt writing.

If the user gives reference images, use them to infer the closest camera/light/material mechanism, then match that mechanism to this library. Do not copy the reference image blindly and do not paste the reference name as the final style.

Names are internal selection tools only. Final prompts must convert the selected anchor into:

```text
camera system / lens feeling / light source and direction / color boundary / spatial relationship / composition discipline / material texture / performance exposure / AI risk control
```

Reject or rewrite final prompt language that says only:

```text
Roger Deakins style, Fincher style, Nolan style, cinematic, premium, realistic, low saturation
```

## Cinematography Anchors

| Reference system | Transferable principles | Best use | Prompt translation |
| --- | --- | --- | --- |
| Roger Deakins | motivated natural light, controlled darkness, negative space, restrained movement, emotional clarity | crime, drama, brand trust, industrial dignity | motivated practical light, disciplined shadow, clean negative space, restrained camera |
| Emmanuel Lubezki | immersive long takes, available light, bodies moving through real space, organic camera drift | one-take, human scale, memory, crisis | continuous camera path, natural light, handheld/Steadicam immersion, real spatial geography |
| Hoyte van Hoytema | large-format depth, architectural scale, textured naturalism, restrained spectacle | tech, city, engineering, large-screen visuals | large-format depth, architectural composition, textured natural light, no fake spectacle |
| Greig Fraser | monumental shadow, spiritual scale, tactile low light, restrained color worlds | epic, history, ritual, power, large-scale themes | monumental silhouette, tactile dust/smoke, limited palette, controlled vastness |
| Bradford Young | soft low exposure, warm shadow, human skin, poetic darkness | intimate drama, memory, humanist stories | underexposed warmth, soft falloff, skin-first light, quiet frame |
| Darius Khondji | textured darkness, painterly contrast, sensual surfaces, noir atmosphere | thriller, desire, premium suspense | rich shadow texture, practical pools of light, sensual material surfaces |
| Rodrigo Prieto | adaptive realism, period/contemporary flexibility, emotional color shifts | multi-era stories, brand/city history | era-specific texture, emotional color contrast, credible period light |
| Linus Sandgren | classical film color, musical rhythm, expressive lensing, warm nostalgia | aspirational brand, romance, performance | warm film color, expressive lens flare with control, rhythmic camera |
| Christopher Doyle | expressive color, urban motion, subjective rhythm | city night, youth, romance, memory fragments | saturated practical colors, subjective motion, urban reflections, narrow spaces |
| Mark Lee Ping-bing | slow emotional distance, soft natural light, spatial melancholy | restrained romance, Asian art-house tone | slow static/float camera, soft daylight, emotional distance, sparse composition |
| Claudio Miranda | polished large-scale naturalism, clean digital latitude, atmospheric spectacle | sci-fi realism, aviation, premium visual scale | clean high dynamic range, elegant backlight, atmospheric depth, precise highlights |
| Janusz Kaminski | expressive backlight, haze, historical emotion, sharp contrast | historical drama, memory, moral conflict | strong backlight, visible haze, expressive contrast, period texture |
| Ellen Kuras | intimate realism, human proximity, documentary sensitivity | character portrait, social realism, human story | close natural light, tactile faces, observational handheld restraint |
| Lol Crawley | textured film grain, architectural pressure, austere period realism, monumental interiors | architecture, ambition, period-inspired drama, institutional power | film-grain texture, deep architectural perspective, hard geometric light, tactile concrete/wood/stone |
| Łukasz Żal | austere composition, moral distance, faces in restrained light, controlled stillness | memory, guilt, institutional or spiritual pressure | static frames, subdued natural light, desaturated faces, negative space with moral weight |
| Jarin Blaschke | controlled chiaroscuro, period texture, psychological unease, sculpted faces | gothic suspense, psychological isolation, historical dread | hard directional practical light, deep shadow, textured skin/fabric, restrained period atmosphere |
| Rina Yang | modern intimate naturalism, skin sensitivity, available light, emotional immediacy | youth, contemporary relationships, intimate drama | soft available light, close human proximity, gentle falloff, lived-in modern texture |
| Vittorio Storaro | expressive color theory, sculpted shadow, operatic psychological space | moral collapse, power, war, desire, theatrical psychological drama | warm/cool symbolic color contrast, carved directional light, deep shadow, faces shaped by color temperature |
| Gordon Willis | disciplined darkness, underexposure, controlled interiors, power encoded by shadow | family power, institutional secrecy, crime dynasty, moral rot | low-key interiors, top/side practical pools, faces partially withheld, brown-black palette, rigid blocking |
| Sven Nykvist | natural window light, spiritual intimacy, unadorned faces, quiet moral exposure | chamber drama, family confession, guilt, faith, intimacy | soft window daylight, sparse rooms, close faces with honest skin, minimal camera movement |
| Robby Muller | road light, neon realism, melancholy color, drifting outsiders | road stories, exile, night city, emotional wandering | available street light, sodium/neon color separation, loose compositions, weathered surfaces |
| Gregg Toland | deep focus, layered blocking, power through space, high-contrast classic geometry | courtroom, family systems, institutional rooms, memory structure | deep-focus foreground/midground/background, strong architectural lines, low angle, high-contrast black-white discipline |
| Nestor Almendros | naturalistic daylight, gentle observation, period realism, emotional restraint | rural memory, romance, childhood, quiet period drama | soft natural daylight, restrained palette, simple blocking, faces integrated into landscape |
| Yu Lik-wai | Chinese urban transformation, documentary-fiction texture, county/city night, social drift | small-town crime, city migration, industrial edges, ordinary people under change | available street light, faded signs, concrete/river/road texture, handheld or patient observation, no glossy city beauty |
| Sayombhu Mukdeeprom | soft natural color, intimate daylight, time passing through faces and rooms | restrained romance, memory, rural/urban quiet drama | gentle daylight, warm skin without beauty smoothing, still rooms, human distance, tactile everyday objects |
| Hélène Louvart | social realism, child/person proximity, textured natural light, imperfect locations | children, social margins, intimate family pressure | close observational camera, real location light, unpolished surfaces, skin and clothes kept imperfect |
| Claire Mathon | luminous restraint, feminine subjectivity, period/contemporary natural light | memory, romance, female perspective, quiet mystery | soft directional daylight, painterly but realistic skin, controlled color, intimate negative space |
| Chung Chung-hoon | elegant tension, precise color, sharp psychological framing, object detail | revenge, desire, thriller, premium suspense | clean dangerous composition, refined color contrast, precise object close-ups, restrained camera before sudden tension |

## Director / Visual System Anchors

| Reference system | Transferable principles | Best use | Prompt translation |
| --- | --- | --- | --- |
| Christopher Nolan | large-format realism, physical spectacle, clear temporal architecture, restrained VFX | engineering, time, historical scale, high-stakes systems | practical large-scale environment, IMAX-like depth, grounded spectacle, clear spatial logic |
| Denis Villeneuve | monumental silence, controlled color worlds, architecture as psychology | epic brand, tech, power, mystery, sci-fi realism | vast negative space, restrained palette, massive architecture, slow pressure |
| David Fincher | precision, procedural control, low-key modern interiors, visual discipline | suspense, investigation, institutional control | exact composition, muted palette, long-lens face pressure, no visual mess |
| Alfonso Cuaron | immersive one-take human experience, real-time geography | one-take, crisis, memory, public space | continuous shot, human-scale camera, environment changes through motion |
| Bong Joon-ho | class encoded in architecture, tonal shift, object-based reveal | social drama, class conflict, spatial reversal | vertical architecture, stairs/windows/basement logic, precise object reveal |
| Park Chan-wook | symmetrical desire, elegant danger, object fetish detail | revenge, psychological romance, premium suspense | elegant symmetry, rich interiors, controlled color, dangerous close-up |
| Sean Baker | street-level immediacy, non-glossy urban energy, social collision, intimate chaos | urban short drama, class collision, nightlife, marginal characters | handheld proximity, practical location light, real surfaces, energetic but readable blocking |
| Justine Triet | legal/domestic ambiguity, performance-led realism, moral uncertainty | courtroom, family accusation, testimony, public/private truth | restrained medium frames, winter daylight, practical interior light, ambiguous face blocking |
| Todd Field | institutional precision, polished coldness, status anxiety | elite workplace, authority collapse, professional scrutiny | exact room geometry, cold neutral palette, restrained camera, status encoded by blocking |
| Terrence Malick | subjective memory, natural light fragments, spiritual landscape, tactile childhood detail | memory, grief, childhood, inner voice, nature-driven emotion | golden natural light, close tactile hands/grass/fabric, drifting camera, human small inside landscape |
| Stanley Kubrick | geometric control, one-point perspective, institutional unease, ritualized movement | power systems, psychological control, sterile interiors, formal dread | centered perspective, exact symmetry, slow controlled movement, cold architectural space |
| Michael Mann | nocturnal urban realism, professional bodies, digital night texture, clean action geography | crime professionalism, pursuit, city pressure, night confrontation | cool city night, practical street and car reflections, long-lens urban geometry, disciplined body blocking |
| Ridley Scott | atmospheric industrial scale, smoke, backlight, tactile production worlds | future noir, industrial suspense, brand/tech world-building | layered haze, hard backlight, wet metal/glass, dense foreground detail, believable industrial depth |
| Hou Hsiao-hsien | patient observation, time inside rooms, memory through daily gestures, restrained emotion | family history, youth drift, quiet social change | static or slow-drifting camera, available window/practical light, lived-in rooms, people observed across distance |
| Jia Zhangke | ordinary bodies inside social change, county/city texture, industrial edges, road and river geography | small-town revenge, migration, money/status change, working-class realism | real streets/construction/shops, faded signage, concrete/dust/river texture, character small inside changing space |
| Bi Gan | humid memory, physical dream logic, long-take wandering, object-led mystery | subjective memory, missing person, rural mystery, emotional search | continuous path through real spaces, damp green night, tactile clues, slow reveal, no fantasy glow |
| Diao Yinan | cold crime realism, exhausted bodies, wet night streets, northern industrial pressure | murder, fugitive, police/crime night, hidden transaction | wet asphalt, sodium/neon practical sources, winter breath, long-lens observation, tired faces |
| Ryusuke Hamaguchi | dialogue as architecture, emotional delay, cars/rooms as confession spaces | confession, unresolved relationship, quiet confrontation | patient medium frames, windshield/window reflections, still faces, natural city/road light, pauses preserved |
| Wim Wenders | everyday ritual, road/city solitude, humane observation, simple repeated actions | lonely worker, journey, quiet healing, urban routine | soft morning/daylight, repeated gestures, clean negative space, ordinary objects as emotional anchors |

## How To Convert To Final Prompt Language

Instead of:

```text
Roger Deakins style, Nolan style, Apple style
```

Use:

```text
motivated practical side light, restrained camera movement, large-format architectural depth,
low-saturation realistic color, tactile metal/stone/fabric surfaces, clean negative space,
clear subject hierarchy, no fake HUD, no glossy AI plastic texture
```

For formal short-drama, promo, TVC, brand-film, event, or LED workflows, every downstream prompt must carry the anchor as executable language:

```text
光线方向 + 空间关系 + 焦段心理效果 + 构图调度 + 材质触感 + 人物表演状态 + AI风险控制
```

Example conversion:

```text
Roger Deakins is not written as a name only. Convert it to motivated practical side light, disciplined shadow, restrained camera movement, clean negative space, natural skin exposure, tactile room materials, and no glossy AI plastic texture.
```

## Camera And Lens Discipline

| Need | Better lens/camera logic |
| --- | --- |
| Product clarity | 50mm-100mm macro, controlled reflections, stable camera |
| Engineering scale | 24mm-35mm wide, low angle, architectural depth |
| Human pressure | 65mm-100mm long lens, compressed space, shallow depth |
| One-take immersion | 24mm-35mm, stabilized handheld/Steadicam, clear path |
| LED/stage readability | wide composition, center-safe, large simple forms |
| Short-drama vertical close emotion | 50mm-85mm equivalent, face and hands readable, background simplified |

## Global AI Risk Control

```text
Do not copy exact film frames, exact celebrity faces, exact brand marks, or protected designs.
Do not paste many reference names into final prompts.
Do not allow the model to turn elite cinema into generic teal-orange, fake anamorphic flares,
random smoke, plastic skin, glossy CG, unreadable text, or chaotic composition.
Preserve photographic imperfections where realism matters: skin texture, fabric wrinkles,
environment dust, worn objects, natural shadow grain, real depth of field, and source-motivated light.
Avoid over-sharpening, beauty smoothing, fake HDR, overfilled shadows, platform-template lighting,
web-drama soft light, and short-video filter taste.
```
