# 手账素材索引

所有手账素材统一放在本目录，页面素材预览见上级的 [gallery.html](../../gallery.html)。

## 文件夹

- `collages/`：页面使用的拼贴画。
  - `photos/`：从原始拼贴稿整理出的 36 张单张拼贴，按 01–36 编号。
  - `original-sources/`：从仓库 `feature/photos` 原样收录的 36 张 JPG 原稿，保留原文件名，便于回查与重新提取。
  - `collage-crows.webp`、`collage-tabby.webp`、`collage-tuxedo.webp`：近期新增的三张拼贴画（乌鸦、狸花猫、奶牛猫）。
  - 其余根目录 WebP 为原创日常物件拼贴。
- `doodles/`：手绘小图案与人物/猫狗活动插画，包含原有素材、日常物品与食物，以及新增加的活动场景。
- `textures/tapes/`：胶带纹理；胶带配色和周轮换配置在同级的 `tapes.json`。
- `textures/`：纸张、灰泥、聊天页等背景纹理。
- `badges/`：周徽章、玫瑰徽章及 30 枚习惯徽章。

## 数量与来源

- 页面拼贴：43 张（4 张原创、36 张原稿拆出的单张拼贴、3 张新增动物拼贴）。
- 原始 JPG：36 张，来源 `feature/photos`，不改动像素内容和原文件名。
- 页面手绘：88 张；其中 64 张为每周轮换的人物或猫狗活动素材。
- 胶带纹理：18 款，配置为 9 组每周搭配。

页面运行时使用 `manifest.json` 列出的素材。修改或增加素材后，请同步更新清单并执行 `python scripts/build.py`。
