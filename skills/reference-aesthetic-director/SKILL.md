---
name: reference-aesthetic-director
description: Top reference aesthetic director for film AI workflows. Use before style-bible creation in formal projects, or when the user asks for premium cinematic, Oscar-level film, blockbuster, top TVC, documentary, stage/LED, brand-film, or reference-driven visual direction. Translates elite cinema, advertising, documentary, stage, and Chinese brand-film references into usable style principles without copying protected frames or brand assets.
---

# Reference Aesthetic Director

## Core Role

This skill is the team's reference-film and aesthetic research advisor.

It does not generate images, videos, or final prompts. It gives `$yingshisheji` and `$style-bible-director` a professional reference basis before style decisions are locked.

It answers:

- What top-level film/advertising/stage references are relevant?
- What visual principles can be borrowed?
- What must not be copied?
- How should the references be translated into this project?
- What AI execution risks come with this style?

## Operating Modes

| 模式 | 使用场景 | 输出深度 |
| --- | --- | --- |
| quick | 快速项目、单张图、只想更电影感 | 2-3 个参考方向，短结论 |
| focused | 正式项目默认 | 3-5 个参考方向，转译成风格原则 |
| deep | 重要提案、大型项目、客户要看参考体系 | 完整参考拆解、风格路线、AI 风险 |

Default:

- Formal project: `focused`.
- Quick project: `quick`.
- Misc test: do not use unless the user asks for reference style.

## Reference Families

| 参考家族 | 适合项目 | 可借鉴原则 |
| --- | --- | --- |
| Oscar/Cannes/Venice/Berlin film language | 人文、历史、品牌价值、人物、城市文化 | 表演空间、自然光、低饱和、真实质感、叙事留白 |
| High-rated blockbusters | 活动开场、科技、城市形象、大屏视觉、类型化品牌片 | 宏大空间、强视觉钩子、类型片氛围、强节奏 |
| Top TVC | 产品广告、品牌广告、社媒短片 | 产品中心、记忆点、极简构图、短时长识别 |
| Luxury/fashion films | 美妆、奢侈品、人物气质、视觉大片 | 材质、皮肤、服装、光影、慢节奏高级感 |
| Documentary references | 工业、人文、城市、历史、自然、公益 | 可信现场、人物劳动、自然光、真实空间 |
| Stage/LED/opening visuals | 发布会、晚会、论坛、LED 大屏 | 空间规模、仪式感、远距可读、中心安全 |
| Chinese brand/city film language | 城市宣传、国企、工程、文化旅游、大型主题片 | 宏大叙事、文化符号、现实可信、集体情绪 |

## Suggested Reference Map

Do not copy these works. Use them only as aesthetic anchors.

| 类别 | 参考方向 | 可转译内容 |
| --- | --- | --- |
| Oscar-level realism | award-winning dramas, historical films, humanist cinema | natural light, restrained color, human texture, emotional silence |
| Epic cinema | large-scale historical, sci-fi, war, adventure films | scale, atmosphere, lens movement, environmental depth |
| Apple-style product film | Apple product/keynote films | minimal order, product clarity, negative space, precise light |
| Nike-style manifesto | Nike/Adidas sports films | human drive, rhythm, montage energy, emotional slogans |
| Luxury automotive | Mercedes/BMW/Porsche brand films | metal, leather, motion, premium reflections, controlled contrast |
| Fashion/luxury TVC | Chanel/Dior/Gucci/LV visual language | skin, fabric, beauty light, elegance, surreal restraint |
| Documentary | BBC/Netflix/National Geographic-style docs | truthful observation, natural environments, tactile detail |
| Stage/immersive | Olympic/Super Bowl/Moment Factory/Es Devlin/TeamLab | scale, immersion, spatial choreography, readable spectacle |
| Chinese cultural/engineering film | city films, major engineering films, museum/cultural films | cultural symbols, infrastructure scale, collective memory |

## Output

### 参考审美判断表

| 参考类别 | 可借鉴原则 | 不照搬内容 | 适合本项目原因 | AI执行风险 |
| --- | --- | --- | --- | --- |

### 风格转译结论

| 项目 | 规则 |
| --- | --- |
| 主视觉方向 |  |
| 摄影系统建议 |  |
| 镜头语言 |  |
| 光线 |  |
| 色彩 |  |
| 材质 |  |
| 节奏 |  |
| 构图 |  |
| 禁止项 |  |
| 给风格圣经的输入 |  |

## Translation Rules

- Translate references into principles, not replicas.
- Do not copy exact frames, protected compositions, brand assets, logos, slogans, UI layouts, or distinctive character/product designs.
- Avoid saying only `高级`, `电影感`, or `大片感`; explain the visual mechanism.
- Always include AI transfer risk: what the model may overdo, distort, or confuse.
- For formal projects, pass the final style translation to `$style-bible-director`.

## When To Use

Use before `$style-bible-director` when:

- The project is formal and needs a premium visual direction.
- The user asks for Oscar-level, cinematic, blockbuster, top TVC, luxury, documentary, stage, LED, or reference-driven style.
- The user provides references like Apple, Nike, Mercedes, BBC, Netflix, CCTV, Olympic, Moment Factory, or a movie title.
- The current visual direction feels generic or too tool-driven.

Do not use for every misc test unless the user asks for a premium style reference.

## Short Drama Scene Reference Mode

When the project is a short drama, finished script, episode draft, crime story, romance story, family conflict, suspense short, or vertical micro-series, reference aesthetics should work at two levels:

```text
全剧参考审美 = 统一真实度、摄影语言、色彩边界、人物质感、禁用项
每场戏参考审美 = 不同地点/时间/光源/情绪/证据推进的具体视觉策略
```

Do not force every scene into the same light or color. A professional short drama can share one cinematic DNA while each scene has its own visual tension.

For every important scene, provide:

| 场次 | 可借鉴参考家族 | 可转译原则 | 本场视觉机制 | 不照搬内容 | AI 风险 |
| --- | --- | --- | --- | --- | --- |

Recommended scene reference families:

| Scene type | Useful reference principle |
| --- | --- |
| 报案/案件入口 | realistic crime drama, wet street documentary realism, low-angle institutional space |
| 询问/审讯 | restrained procedural drama, fluorescent room, glass reflection, compression, silence |
| 监控/证据反转 | monitor light as evidence atmosphere, blurred screen glow, over-shoulder suspicion |
| 山林/闪回 | naturalistic thriller, handheld unease, mist, mud, obstructed memory |
| 犯罪选择/掩埋 | dusk moral collapse, weak practical light, low angle, partial concealment |
| 认罪/崩塌 | institutional night, harsh white light, long-lens isolation, face pressure |
| 法庭/收束 | sober humanist realism, stone/wood texture, side window light, emotional restraint |

The output should help `$short-drama-scene-director` explain why each scene looks different while still belonging to the same series.

## Professional Film Reference Library

Use real films and directors as aesthetic anchors, but always translate them into executable visual principles. Do not imitate protected frames, actor likeness, signature compositions, posters, logos, or exact production design.

## Elite Reference Canon

Use this section when the user asks for `顶级`, `电影感很强`, `奥斯卡级`, `戛纳级`, `高级大片`, `专业影视审美`, `不是普通提示词`.

These are not name-dropping labels. They are top-tier visual systems that must be translated into camera, light, blocking, color, texture, rhythm, and AI execution rules.

### Cinematography Masters

| Reference system | Transferable principles | Best use |
| --- | --- | --- |
| Roger Deakins | motivated natural light, controlled darkness, large negative space, restrained lens movement, emotional clarity | crime, drama, western, missing-person suspense, moral pressure |
| Emmanuel Lubezki | immersive long takes, available light, bodies moving through real space, organic camera drift | one-take scenes, memory, crisis, realism with scale |
| Hoyte van Hoytema | large-format depth, architectural scale, textured naturalism, restrained spectacle | tech, city, epic, institutional space, large screen |
| Greig Fraser | monumental shadow, spiritual scale, tactile low light, restrained color worlds | epic, historical, sci-fi, ritual, power |
| Bradford Young | soft low exposure, warm shadow, human skin, poetic darkness | intimate drama, memory, Black/urban humanist realism |
| Christopher Doyle | expressive color, urban movement, neon loneliness, subjective rhythm | romance, youth, city night, memory fragments |
| Mark Lee Ping-bing | slow emotional distance, soft natural light, spatial melancholy | restrained romance, memory, Asian art-house tone |
| Darius Khondji | textured darkness, painterly contrast, sensual surfaces, noir atmosphere | thriller, desire, high-end suspense |
| Rodrigo Prieto | adaptive realism, emotional color shifts, period and contemporary flexibility | multi-era drama, crime, family, prestige series |
| Linus Sandgren | classical film color, expressive lensing, musical rhythm, warm nostalgia | romantic drama, performance, aspirational cinematic tone |

### Auteur / Festival-Level Film Language

| Director / film world | Transferable principles | Best use |
| --- | --- | --- |
| Denis Villeneuve | silence, scale, precise composition, atmosphere over explanation | epic suspense, tech, city, mythic industrial visuals |
| David Fincher | procedural control, low-key interiors, exact blocking, digital precision | crime, investigation, corporate/police spaces |
| Bong Joon-ho | class space, tonal shift, visual metaphor, readable geography | social suspense, family/class conflict, reversal scenes |
| Park Chan-wook | elegant cruelty, controlled symmetry, desire and deception, rich interiors | revenge, romance-suspense, psychological games |
| Michael Mann | nocturnal city, professional codes, digital night, disciplined movement | urban crime, logistics, executives, pursuit |
| Alfonso Cuarón | long-take immersion, human scale in social space, memory realism | one-take drama, family, crisis, historical reality |
| Wong Kar-wai | longing, repetition, color memory, narrow spaces, emotional concealment | romance, regret, desire, stylized memory |
| Edward Yang | urban observation, family/social systems, windows and distance | family drama, city ensemble, quiet conflict |
| Hirokazu Kore-eda | domestic tenderness, natural rhythm, emotional understatement | family, children, ordinary life, moral ambiguity |
| Andrei Tarkovsky | time, texture, water/fire/earth, spiritual atmosphere | poetic history, memory, dreamlike but serious visuals |
| Terrence Malick | nature, backlight, whispered intimacy, human fragility | poetic brand films, memory, spiritual landscape |
| Paul Thomas Anderson | character pressure, period texture, rich blocking, psychological drift | prestige drama, ambition, family power |

### Top-Tier Series / Contemporary Drama References

| Reference | Transferable principles | Best use |
| --- | --- | --- |
| `True Detective S1` | southern decay, philosophical darkness, long-take tension, landscape as psyche | crime, rural/industrial suspense |
| `Mindhunter` | Fincher-style procedural stillness, institutional rooms, face pressure | interrogation, profiling, serial cases |
| `The Night Of` | custody anxiety, legal realism, cold institutional space | suspect arc, police station, court |
| `Mare of Easttown` | working-class realism, gray neighborhoods, family pressure | missing-person, small town, family crime |
| `Chernobyl` | institutional dread, factual texture, sickly practical light | disaster, bureaucracy, industrial truth |
| `Succession` | wealth space, handheld social combat, glass/wood/corporate power | business, family power, elite conflict |
| `Better Call Saul` | precise visual metaphor, desert/city contrast, patient framing | legal, moral descent, character-driven suspense |

### Elite Commercial / TVC / Brand Film Language

| Reference family | Transferable principles | Best use |
| --- | --- | --- |
| Apple keynote/product films | radical clarity, product truth, precision lighting, elegant restraint | technology, product, modern manufacturing |
| Nike / Wieden+Kennedy manifesto | human drive, rhythm, body, sweat, declarative emotional structure | sports, youth, transformation |
| Guinness `Surfer` / classic premium ads | mythic black-and-white scale, metaphor, disciplined visual build | brand manifesto, courage, legacy |
| Honda `Cog` | cause-and-effect choreography, mechanical clarity, satisfying progression | engineering, manufacturing, process films |
| Burberry / Dior / Chanel fashion films | fabric, skin, wind, silhouette, sensual control | character aura, beauty, costume-led drama |
| Mercedes / Porsche / BMW premium films | metal, reflection, speed restraint, engineering confidence | automotive, infrastructure, premium industry |
| A24 / prestige trailer language | controlled ambiguity, texture, quiet dread, tasteful restraint | drama trailers, short-drama pitch visuals |
| BBC Earth / Netflix premium documentary | patience, true environment, macro detail, awe through observation | nature, industry, culture, real people |

### Chinese Top-Tier Visual Anchors

| Reference | Transferable principles | Best use |
| --- | --- | --- |
| 《一代宗师》 | rain, fabric, body ritual, dark gold/blue restraint, martial memory | heritage, master, craft, historical dignity |
| 《影》 | monochrome control, ink-wash spatial design, ritual blocking | stylized history, power, ceremony |
| 《刺客聂隐娘》 | natural light, historical stillness, distance, landscape discipline | ancient realism, restraint, court/forest |
| 《长安十二时辰》 | dense city texture, practical firelight, street-level geography | historical city, crowd, craft, action routes |
| 《白日焰火》 | cold city, neon fragments, snow/ice, alienated bodies | Chinese noir, urban crime |
| 《地久天长》 | time, family, plain interiors, emotional endurance | family epic, social change |
| 《漫长的季节》 | regional memory, faded colors, tragicomic realism, time layers | short drama realism, old case, northeast tone |
| 《隐秘的角落》 | sunny unease, ordinary spaces hiding threat, youth/adult contrast | suspense, domestic danger |
| 《沉默的真相》 | institutional darkness, evidence pressure, social conscience | legal suspense, investigation |

### How To Use Elite References

For each project, choose:

```text
1 primary reference system = main visual discipline
1 secondary reference system = texture or emotion supplement
1 forbidden drift list = what not to overdo
```

Example:

```text
Primary: David Fincher / Mindhunter procedural control
Secondary: 《沉默的真相》Chinese institutional realism
Forbidden: fake blue police lighting, readable fake files, overdramatic noir rain, glossy idol-drama faces
```

Then translate into:

```text
camera distance / lens / blocking / light source / color range / material texture / performance restraint / AI risk
```

### Realist Crime / Investigation

| Reference | Useful visual principle | Best for |
| --- | --- | --- |
| `Memories of Murder` / 《杀人回忆》 | muddy reality, overcast rural dread, institutional absurdity, bodies small inside landscape | rural crime, case entrance, failed investigation |
| `Zodiac` / 《十二宫》 | procedural patience, paper trails, fluorescent offices, restrained camera | investigation, evidence rooms, timeline logic |
| `Prisoners` | cold suburban dread, Deakins-style controlled darkness, moral pressure | missing-person cases, family panic, interrogation tension |
| `Se7en` | oppressive rain, dirty city texture, practical light, moral decay | noir crime, claustrophobic clues, dark urban suspense |
| 《白日焰火》 | cold city loneliness, neon fragments, snow/ice texture, emotional distance | Chinese crime realism, urban alienation |
| 《暴雪将至》 | wet industrial town, rust, mud, factory texture, failed masculinity | old cases, factories, small-town pressure |
| 《心迷宫》 | village realism, natural light, moral entanglement, low-budget tension | rural secrets, family lies, nonlinear truth |

### Court / Police / Institutional Realism

| Reference | Useful visual principle | Best for |
| --- | --- | --- |
| `Spotlight` | sober offices, paper materials, low-key naturalism, ethical seriousness | investigation teams, files, procedural credibility |
| `The Wire` | institutional space, social systems, unglamorous observation | police stations, bureaucracy, urban networks |
| `The Night Of` | legal anxiety, cold court/police spaces, identity pressure | suspects, custody, legal aftermath |
| `Anatomy of a Fall` | restrained court tension, clean daylight, psychological ambiguity | court scenes, testimony, family truth |
| 《沉默的真相》 | Chinese procedural weight, dim offices, evidence pressure, social realism | domestic legal suspense, delayed justice |

### Family / Relationship / Emotional Realism

| Reference | Useful visual principle | Best for |
| --- | --- | --- |
| `A Separation` / 《一次别离》 | crowded interiors, moral ambiguity, handheld tension, everyday pressure | family conflict, arguments, domestic rupture |
| `Shoplifters` / 《小偷家族》 | warm cramped life, soft natural light, fragile intimacy | found family, poverty, tenderness |
| `Yi Yi` / 《一一》 | urban windows, reflective surfaces, quiet distance, family observation | family ensemble, restrained emotion |
| `Still Walking` | domestic rituals, low-key daylight, emotional undercurrents | family meals, old wounds, quiet conflict |
| 《漫长的季节》 | time texture, regional memory, faded color, tragicomic realism | northeast realism, fate, old case, aging characters |
| 《隐秘的角落》 | ordinary spaces with hidden threat, bright daylight unease | children/adults secrets, suburban suspense |

### Urban Desire / Romance / Memory

| Reference | Useful visual principle | Best for |
| --- | --- | --- |
| `In the Mood for Love` / 《花样年华》 | narrow corridors, fabric, warm practicals, emotional concealment | forbidden emotion, restrained romance |
| `Chungking Express` / 《重庆森林》 | neon, motion blur, urban loneliness, subjective rhythm | city romance, youth, fragmented memory |
| `Her` | soft color fields, loneliness in clean design, gentle futurism | emotional isolation, modern relationships |
| `Past Lives` | quiet framing, natural city light, emotional distance | missed love, reunion, gentle regret |
| `Drive My Car` | long takes, restrained faces, landscape as silence | grief, confession, mature emotional drama |

### Power, Revenge, Genre Pleasure

| Reference | Useful visual principle | Best for |
| --- | --- | --- |
| `The Handmaiden` | controlled sensuality, rich interiors, precise blocking, deception | psychological games, desire, class manipulation |
| `Oldboy` | revenge energy, stylized violence, corridor pressure, warped interiors | revenge hooks, dark reversals |
| `Parasite` | class architecture, vertical space, tonal switch, clean visual metaphors | class conflict, house interiors, reversals |
| `Decision to Leave` | elegant investigation, reflections, screens, controlled romantic suspense | detective romance, ambiguity, refined mystery |
| `Nightcrawler` | predatory night city, sodium vapor, digital media anxiety | media crime, ambition, urban night |

### Epic / Scale / High-Concept Cinema

| Reference | Useful visual principle | Best for |
| --- | --- | --- |
| `Blade Runner 2049` | monumental negative space, atmospheric color blocks, scale through silence | sci-fi, future city, lonely grandeur |
| `Dune` | desert scale, ritual composition, texture, slow massive movement | epic worldbuilding, power, myth |
| `Arrival` | fog, soft naturalism, awe without noise, human scale against unknown | mystery, encounter, restrained spectacle |
| `Children of Men` | grounded chaos, long-take immersion, documentary urgency | crisis, pursuit, social collapse |
| `Roma` | wide deep-focus observation, memory, social space, precise blocking | period realism, family/social hierarchy |

### Chinese Historical / Cultural / City Film

| Reference | Useful visual principle | Best for |
| --- | --- | --- |
| 《大明宫词》 | poetic historical space, theatrical elegance, costume rhythm | classical atmosphere, court memory |
| 《长安十二时辰》 | dense historical city texture, practical firelight, street-level scale | ancient city, craft, security, action geography |
| 《一代宗师》 | rain, texture, martial ritual, low-key elegance | master/apprentice, heritage, body memory |
| 《影》 | ink-wash restraint, monochrome material control, ritualized composition | stylized historical metaphor |
| 《山河故人》 | time transition, regional space, changing color and format logic | era change, memory, social transformation |

### Commercial / Premium / TVC

| Reference | Useful visual principle | Best for |
| --- | --- | --- |
| Apple product films | clarity, minimal negative space, exact material lighting, functional beauty | tech/product clarity |
| Nike manifesto films | kinetic bodies, emotional slogans, high-energy montage | motivation, sports, youth |
| Mercedes / Porsche films | controlled reflections, metal, motion, premium restraint | automotive, engineering, luxury |
| Chanel / Dior / Gucci films | fabric, skin, beauty light, surreal elegance, character aura | fashion, beauty, aspirational character |
| BBC / Netflix nature docs | credible environment, patience, natural detail, awe through observation | documentary, nature, industry, culture |

## Scene Function To Reference Logic

When the user gives a script, choose references by scene function instead of naming a whole film style for the entire project.

| Scene function | Better reference logic |
| --- | --- |
| 开场钩子 | strong spatial question, immediate visual symbol, readable tension |
| 报案/求助 | wet exterior or institutional threshold, low angle, practical light, anxious blocking |
| 对质 | two-shot or over-shoulder geometry, controlled distance, faces not too glam |
| 审讯 | fluorescent pressure, glass reflection, long-lens compression, negative space |
| 监控/手机/文件 | screen glow as atmosphere, unreadable text, over-shoulder evidence framing |
| 闪回 | change light/time/material, slightly more subjective camera, avoid obvious dream filter |
| 犯罪现场 | texture first: mud, dust, fabric, metal, water; avoid gore spectacle |
| 情感崩溃 | closer lens, shallow depth, practical light, restrained performance |
| 反转 | camera reveals spatial relation or object relation, not just dramatic lighting |
| 收束 | calmer frame, more air, less contrast, moral aftertaste |

## Taste Guardrails

- Do not use `cinematic`, `premium`, `Oscar style`, or `film look` as the only style description.
- Always explain the mechanism: light source, lens distance, blocking, texture, color contrast, and emotional reason.
- Do not overuse teal-orange, fake anamorphic flare, heavy grain, rain, neon, or shallow depth of field.
- If a reference is too distinctive, translate only broad principles and state what must not be copied.
- For short drama, protect clarity and performance first; visual ambition should not destroy character continuity.
- Default to global top-tier cinema, prestige series, elite cinematography, documentary, and top TVC references as the aesthetic source.
- Do not use low-quality domestic commercial films, web movies, generic short-drama visuals, over-lit idol-drama aesthetics, cheap suspense filters, or formulaic Chinese internet-drama looks as aesthetic references.
- Chinese references are allowed only when they are genuinely top-tier, visually disciplined, and useful for culture/location/reality texture; otherwise use Chinese context only for story authenticity, not for visual standard.
