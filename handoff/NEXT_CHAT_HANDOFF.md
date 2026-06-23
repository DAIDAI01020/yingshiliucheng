# 新聊天最快交接

用途：换新聊天窗口时，不复制整段历史，只复制下面这一段或让 Codex 读取本文件。

## 直接复制到新窗口

```text
用 $zongkong 接着 H:\yingshi 这个影视 AI 工作流。
先读取并遵守：
1. H:\yingshi\handoff\NEXT_CHAT_HANDOFF.md
2. H:\yingshi\WORKFLOW.md
3. H:\yingshi\sync-logs\2026-06-04.md
4. H:\yingshi\sync-logs\2026-06-05.md

不要从头重新设计 workflow。当前 skill 规则已经写入并同步到：
H:\yingshi\skills\
C:\Users\admin\.codex\skills\

当前已完成的核心更新：
1. 通用短剧项目状态层：project-state-manager 支持 short-drama workflow、storyboard-execution route、generation gate。
2. 正式短剧生成门槛：project-intake / style-lock / scene-map / shot-audit / prompt-audit / generation-ready。
3. image 出图提示词优化：吸收字段化分镜方式，按全局 style-lock + 当前镜头字段 + 连续性锁定 + 精简自包含执行提示词处理。
4. 视频平台提示词优化：新增 video_platform_prompt_packet，区分 Jimeng / Seedance-Ark / Kling / Kling O1 / Kling VIDEO 3.0 Omni。
5. Omni/O1 多参考任务必须先做 kling_omni_reference_role_map，明确 @Image / @Element / @Video / audio 各自控制什么和 do_not_inherit。
6. 母库作用：母库定审美，style-lock 固化审美，视频阶段只压缩成 video_style_lock_compact，不把长母库说明塞进平台提示词。
7. 可灵出视频 agent 优化：AI 视频提示词 agent 先区分普通可灵 / O1 / VIDEO 3.0 Omni；O1/Omni 必须先输出 kling_omni_reference_role_map，再写 video_platform_prompt_packet 和可复制提示词；正式/托管项目的可灵外部执行通过 video-generation-controller 写 manual_handoff manifest，后续回写项目状态和 QC。
8. 母库强应用规则：新增 mother_library_application_packet，母库不再只是参考片单或审美来源，而是控制项目DNA、场戏功能、镜头执行和平台风险；正式出图/出视频如果没有该包或等效场戏母库应用规则，必须回到 style-reference-director / scene-style-map-director / project-style-lock 补齐。
9. 工作 Agent 持续优化规则：以后优化 workflow / skill / agent 默认先解释、再确认、后修改；优先优化具体 agent 行为，慎改总控、状态门、模板和脚本；正式项目可完整，quick/test 必须保持轻量。
10. 视频提示词默认音频规则：除非用户明确要求音乐、配乐、对白、旁白或参考声音，所有可复制视频提示词默认加入“保留真实环境音效，不要音乐，不要配乐，不要额外旁白”。
11. 工作流质量/速度分层：新增 prompt_only / quick_test / formal_managed 三档；单条可灵/Omini/即梦提示词和单镜头测试默认快速直出或轻量检查，正式项目、批量、交付、manifest、QC 才走完整状态门、母库、style-lock、prompt-audit 和 generation-ready。
12. 母库电影风格扩展：短剧/剧情母库新增华语/东亚现实主义、夜城市新黑色、机构/学校/医院/职场压迫、日常仪式/感官现实主义等风格种类；顶级摄影锚点补充 Yu Lik-wai、Sayombhu Mukdeeprom、Hélène Louvart、Claire Mathon、Chung Chung-hoon 及 Hou Hsiao-hsien、Jia Zhangke、Bi Gan、Diao Yinan、Ryusuke Hamaguchi、Wim Wenders 等可执行机制。
13. TVC广告大段故事板 Image 出图路线：新增 quick_test 路线，用户要“每一大段故事板 / 直接给 image 出故事板 / TVC广告故事板测试 / 剧情包装广告故事板”时，默认继承已有导演/提示词输出的人物、道具、产品、场景、风格和小分镜 beat，由 storyboard-planner 输出 tvc_segment_storyboard_lock，再由 scene-board-image-prompter 输出一段一张横版 storyboard board 提示词；不走短剧线，不重设人物道具，不强制正式状态门。
14. 即梦/Seedance 直接参考故事板规则：image 出的 TVC 故事板可作为整张参考图直接上传给即梦/Seedance；故事板可分为广告连续画面板、角色道具场景设定板、空间/机位/节拍控制板。视频提示词必须明确只继承人物、道具/产品、场景、色调、光线和关键 beat，并忽略白底排版、分格线、编号、箭头、标题栏、注释区、小字和 storyboard sheet 本身。
15. 导演层故事板类型决策：TVC/节目宣传等商业导演必须先分析并输出 recommended_board_type：`ad_sequence_board`、`design_reference_board` 或 `spatial_continuity_board`，并说明 board_type_reason 和是否 `jimeng_direct_reference_board`；storyboard-planner 优先继承该选择，不再自己猜。

如果是继续具体项目，先问/确认项目目录，然后用 project-state-manager check 状态，不要靠聊天记忆继续。
如果是继续优化 workflow，先看 sync-logs 最近记录，再决定改哪个 skill。
```

## 当前补充更新

16. TVC 单独小分镜 image 提示词路线：当用户要“每个小分镜提示词 / 单独小分镜出图 / 逐镜出图提示词”时，默认保持 quick_test。`storyboard-planner` 先从 `tvc_segment_storyboard_lock` 输出 `tvc_shot_prompt_handoff`，继承 `recommended_board_type/board_type`、`jimeng_direct_reference_board`、人物、服装、道具、产品、场景和风格锁；`frame-vision-director` 再输出 `tvc_shot_image_prompt_packet` 和逐镜自包含 image prompt。不要重新设计人物、道具、产品、场景或风格；只有用户明确说正式批量、客户交付、QC、入项目状态时才升级完整正式流程。

17. TVC 逐镜 image prompt 标准输出样例：`frame-vision-director` 现在要求逐镜提示词输出为：模式、继承来源、用途、每个 S/A 镜头的画面目标、锁定项、单段可复制 Image 提示词、负面项、后续视频用途。B/C 镜头默认只给短说明，除非用户要求全部逐镜。用于即梦/Seedance首帧时，要说明视频模型继承人物、产品、场景、光线、机位和动作起点，同时不要继承故事板分格线、编号、标签、箭头、注释区和小字。

## 以后怎么用

新窗口最短一句：

```text
用 $zongkong 继续 H:\yingshi 工作流，先读 H:\yingshi\handoff\NEXT_CHAT_HANDOFF.md。
```

如果继续具体项目，再补一句：

```text
项目目录：H:\yingshi\projects\xxx
这次任务：继续出图 / 重出某镜 / 出视频 / QC / 优化工作流
继续使用已有 style-lock，不要重定风格。
```

## 每次更新 skill 后

让 Codex 追加一句：

```text
把这次 skill 更新追加到 H:\yingshi\sync-logs\YYYY-MM-DD.md，并同步更新 H:\yingshi\handoff\NEXT_CHAT_HANDOFF.md 的“当前已完成的核心更新”。
```

记录格式：

```text
时间：
主题：
涉及 skill：
改动原因：
新增规则：
影响流程：
是否同步到 C:\Users\admin\.codex\skills：
```

## 不放进交接文件的内容

```text
API key / token / .env
临时公网 URL
生成图片、视频、音频
projects/ 下的客户素材和生成资产
私密参考图下载地址
```
