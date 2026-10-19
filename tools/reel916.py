"""House style since 18 Oct 2026 (owner approved design "E"): 1080x1920 (9:16), light background,
Lora Bold (line 1, dark ink) + Lora Italic (line 2, maroon), only the @handle as watermark, no CTA on video.
Usage: python3 reel916.py <out_dir> <posts.json>   (env SEED)
Writes per post: <id>_bg.png, <id>_dust.png, <id>_l1.png, <id>_l2.png, <id>_brand.png, <id>.png (preview)."""
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import premium  # scenes only

FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
W, H = 1080, 1920
CX, MAXW, TEXT_Y = 540, 780, 820          # text exactly centred (owner, 19 Oct 2026); above the caption area
INK = (33, 26, 22); MAROON = (122, 34, 40); GREY = (80, 70, 62)
CREAMBG = np.array([247, 240, 228]) / 255
def font(n, s): return ImageFont.truetype(os.path.join(FD, n), s)

def light_bg(scene, rng):
    img = np.clip(premium.SCENES[scene](rng), 0, 255) / 255.0
    img = (img - img.min()) / (img.max() - img.min() + 1e-6)
    im = Image.fromarray((img * 255).astype(np.uint8)).resize((int(1080 * 1920 / 1350), 1920), Image.LANCZOS)
    x0 = (im.width - W) // 2
    a = np.asarray(im.crop((x0, 0, x0 + W, H)).filter(ImageFilter.GaussianBlur(3))).astype(float) / 255
    g = a.mean(axis=2, keepdims=True); a = np.clip(g + (a - g) * 1.8, 0, 1)
    a = 0.60 + 0.40 * a
    a = a * 0.80 + CREAMBG * 0.20
    a = a * np.array([1.03, 1.0, 0.94])
    yy = np.arange(H)[:, None, None]
    panel = np.exp(-((yy - TEXT_Y) / 430) ** 2)
    a = a * (1 - 0.30 * panel) + CREAMBG * 0.30 * panel
    a += rng.normal(0, 0.018, (H, W, 1))
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))

def dust(rng):
    lay = Image.new("RGBA", (W, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for _ in range(160):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H * 2), rng.uniform(1.5, 4.5)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(170, 120, 60, int(rng.uniform(25, 70))))
    return lay.filter(ImageFilter.GaussianBlur(1.5))

def glow(lay):
    al = lay.split()[3].filter(ImageFilter.GaussianBlur(12))
    sh = Image.new("RGBA", lay.size, (255, 250, 240, 0)); sh.putalpha(al.point(lambda v: int(v * 0.9)))
    return Image.alpha_composite(sh, lay)

def spaced(d, cx, y, text, f, sp, fill):
    w = sum(d.textlength(c, font=f) for c in text) + sp * (len(text) - 1); x = cx - w / 2
    for c in text: d.text((x, y), c, font=f, fill=fill); x += d.textlength(c, font=f) + sp

def text_layers(p):
    # shrink the text until everything (label .. @handle) fits inside the safe zone y 300..1260
    d0 = ImageDraw.Draw(Image.new("RGBA", (W, H)))
    for sz in range(80, 50, -4):
        f1, f2 = font("lora700.woff", sz), font("lora600i.woff", sz - 4)
        s1, s2, gap = sz * 1.28, (sz - 4) * 1.28, 34
        l1 = premium.wrap(d0, p["line1"], f1, MAXW); l2 = premium.wrap(d0, p["line2"], f2, MAXW)
        block = 120 + len(l1) * s1 + gap + len(l2) * s2
        total = 70 + block + 29 + (66 if p.get("author") else 0) + 110
        if total <= 960: break
    y0 = max(370, TEXT_Y - block / 2 - (33 if p.get("author") else 0))
    if y0 - 70 + total > 1260: y0 = 1260 - total + 70
    a = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(a)
    spaced(d, CX, y0 - 70, p["label"], font("dm700.ttf", 30), 8, MAROON + (255,))
    d.text((CX, y0 + 95), "“", font=font("lora700.woff", 150), fill=MAROON + (255,), anchor="ms")
    y = y0 + 120
    for ln in l1: d.text((CX, y + s1 / 2), ln, font=f1, fill=INK + (255,), anchor="mm"); y += s1
    b = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    y += gap
    for ln in l2: d.text((CX, y + s2 / 2), ln, font=f2, fill=MAROON + (255,), anchor="mm"); y += s2
    y += 26; d.rectangle([CX - 50, y, CX + 50, y + 3], fill=MAROON + (235,))
    if p.get("author"):  # famous line: credit the poet / source under the divider
        y += 22; d.text((CX, y + 22), "— " + p["author"], font=font("dm700.ttf", 36), fill=MAROON + (255,), anchor="mm"); y += 44
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.text((CX, y + 110), "@quotations_and_quotes", font=font("dm500.ttf", 34), fill=GREY + (240,), anchor="ms")
    return glow(a), glow(b), glow(c)

if __name__ == "__main__":
    OUT, POSTS = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
    for i, p in enumerate(json.load(open(POSTS))):
        rng = np.random.default_rng(int(os.environ.get("SEED", "100")) + i)
        bg = light_bg(p["scene"], rng); bg.save(f"{OUT}/{p['id']}_bg.png")
        dust(rng).save(f"{OUT}/{p['id']}_dust.png")
        prev = bg.convert("RGBA")
        for n, l in zip(["l1", "l2", "brand"], text_layers(p)):
            l.save(f"{OUT}/{p['id']}_{n}.png"); prev = Image.alpha_composite(prev, l)
        prev.convert("RGB").save(f"{OUT}/{p['id']}.png")
        print(p["id"])
