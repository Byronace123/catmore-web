from PIL import Image
import numpy as np

SRC = "catmore-logo-src.png"
WHITE_THRESH = 235
SOFT = 60

src = Image.open(SRC).convert("RGB")
rgb = np.array(src)
a = rgb.astype(np.int32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
mn = np.minimum(np.minimum(r, g), b)
alpha = np.clip((WHITE_THRESH - mn) * 255 // SOFT, 0, 255).astype(np.uint8)

navy = (b > r + 40) & (b > g + 10) & (r < 140)
cyan = (b > r + 30) & (g > r + 5) & (r >= 140)

def build(recolor):
    out = rgb.copy()
    if recolor:
        out[navy] = (246, 244, 239)       # 深藏青 -> 纸白
        out[cyan] = (120, 205, 245)       # 浅蓝提亮
    img = Image.fromarray(np.dstack([out, alpha]), "RGBA")
    ys, xs = np.where(alpha > 0)
    if len(ys):
        img = img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    return img

build(True).save("catmore-logo-light.png")   # 深色背景用
build(False).save("catmore-logo.png")        # 原色透明版
print("完成")