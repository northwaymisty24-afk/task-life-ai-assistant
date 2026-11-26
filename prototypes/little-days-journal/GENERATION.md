# 拼贴生成记录

使用内置图像生成工具，每张独立生成、透明背景；不是照片保真改图。风格参考为 `feature/photos/e8a6e87adc04ecb3850955def8f60e7d.jpg` 及用户给出的手账参考。只借鉴纸纤维、低饱和配色、胶带叠色和轮廓抽象，不复制参考里的鱼或城市。

共同提示要求：one isolated small flat washi-tape collage, genuine transparent background, 10–16 broad or medium hand-cut pieces, mostly solid colors plus one gingham/dot/grid pattern, translucent overlaps, fibrous edges, shallow contact shadows; sage, dusty blue, muted coral, butter yellow, cream and subtle lilac. No text, watermark, desk background, inflated 3D sculpture, photographic objects or ink outlines.

| ID | 独立主体提示 |
| --- | --- |
| tea-pause | warm tea cup with bent handle and cream steam curl, dusty blue saucer, tiny gingham-covered book |
| sprout-notes | open cream notebook with pale blue taped spine, terracotta flowerpot with two sage sprout leaves, butter-yellow corner tab |
| sunny-window | open dusty-blue window frame, half butter-yellow sun and one cream cloud, sage leaf at the sill |
| garden-pause | small sage tree and narrow dark trunk, muted coral bench, little cream flower on a thin grass strip |

原 PNG 保留在生成结果中；仓库只包含优化后的 480px WebP。后续若重画，请创建新版本文件而非覆盖参考截图。SVG 素材的源代码见 `scripts/create-vector-assets.py`。

## 本轮补充

新增六个透明底彩铅人物，动作是接阳光、趴着翻书、蹲着浇水、踮脚晾手帕、拄杖行走和抱枕打盹。用疏松有断点的铅笔线与不规则轮廓，主要靠姿势表现情绪，道具只加低饱和局部颜色。视觉参考为用户截图和公开的 [heytea-style](https://github.com/Hchen1218/heytea-style) 教程。

灰泥图按浅米色石灰墙、细纤维和克制的抹刀弧纹生成；从原图整理出两种强度作为页面灰泥与卡片纸纹。参考图案按原图行列分割为 53 个图块，保留原线条与顺序。

## 云朵头和烟灰纸

在已生成的六张云朵头线上各加一处蜡笔色，依次为风筝鹅黄、袜子瓦粉、车篮鼠尾草绿、耳机线淡紫、面碗杏橙和水洼雾蓝。烟灰胶带取低对比度雾状斑驳纸纹。浅粉蓝灰小花胶带以参考图片的配色与花序重新画成重复纹样。

## 人物面部修正

按之前的线稿恢复云朵头人物的头部轮廓与眼睛。补袜子、分享耳机直接使用上一版单色原稿，其余四张保留风筝鹅黄、车篮鼠尾草绿、面碗杏橙与水洼雾蓝。

## 拼贴透明底整理

分支中的36张拼贴分9组提取透明底，保留构图主体、盘子、花瓣和奶油等白色内容。图像编辑模型按源图移除外围纸底、附带文字与标记，细小纸边与纹理有重新整理。缩小导出时清理边缘孤立像素，保存为透明 WebP。
