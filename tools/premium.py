"""Premium cinematic quote posts for @quotations_and_quotes (1080x1350).
Usage: python3 premium.py <fonts_dir> <out_dir> <posts.json>
Writes <id>_bg.png (cinematic background), <id>_text.png (RGBA overlay), <id>.png (preview)."""
import sys, os, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
W, H = 1080, 1350
GOLD = (230, 178, 92); CREAM = (246, 240, 228); GREY = (200, 196, 188)

def font(n, s): return ImageFont.truetype(os.path.join(FD, n + ".ttf"), s)
def lerp(a, b, t): return a + (b - a) * t
def grad(top, bot, h=H, curve=1.0):
    t = (np.linspace(0, 1, h) ** curve)[:, None, None]
    return (np.array(top)[None, None] * (1 - t) + np.array(bot)[None, None] * t) * np.ones((h, W, 3))

def glow(img, cx, cy, r, color, strength=1.0):
    yy, xx = np.mgrid[0:img.shape[0], 0:W]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    g = np.exp(-(d / r) ** 2)[..., None] * strength
    return img + g * np.array(color)[None, None]

def ridge(rng, base, amp, rough, n=W):
    pts = np.cumsum(rng.normal(0, rough, n))
    pts = np.convolve(pts, np.ones(60) / 60, "same")
    pts = (pts - pts.mean()) / (pts.std() + 1e-6) * amp
    return base + pts

def fill_below(img, ys, color, fade_to=None):
    yy = np.arange(H)[:, None]
    mask = (yy >= ys[None, :]).astype(float)[..., None]
    return img * (1 - mask) + np.array(color)[None, None] * mask

def stars(img, rng, n, ymax):
    for _ in range(n):
        x, y = rng.integers(0, W), rng.integers(0, ymax)
        b = rng.uniform(80, 255)
        img[y, x] = np.clip(img[y, x] + b, 0, 255)
    return img

def bokeh(rng, n, colors, rmin, rmax, ymin=0, ymax=H):
    layer = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(layer)
    for _ in range(n):
        r = rng.uniform(rmin, rmax); x = rng.uniform(0, W); y = rng.uniform(ymin, ymax)
        c = colors[rng.integers(len(colors))]; a = rng.uniform(0.25, 0.9)
        d.ellipse([x - r, y - r, x + r, y + r], fill=tuple(int(v * a) for v in c))
    return np.asarray(layer.filter(ImageFilter.GaussianBlur(6))).astype(float)

def blur(arr, r): return np.asarray(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(float)

# ---------- scenes ----------
def scene_road(rng):  # lonely road, single streetlight, fog
    img = grad((10, 14, 24), (34, 38, 48), curve=0.8)
    img = stars(img, rng, 140, 500)
    hz = 760
    img = fill_below(img, ridge(rng, hz - 30, 18, 1.0), (16, 18, 24))
    yy, xx = np.mgrid[0:H, 0:W]
    t = np.clip((yy - hz) / (H - hz), 0, 1)
    road = (np.abs(xx - W / 2) < lerp(6, 520, t)) & (yy > hz)
    img[road] = [28, 29, 34]
    lines = road & (np.abs(xx - W / 2) < lerp(1, 10, t)) & (yy > 1000) & ((((np.clip(yy - hz,0,None)) ** 0.7).astype(int) // 9) % 2 == 0)
    img[lines] = [150, 140, 110]
    img[(xx > 690) & (xx < 698) & (yy > 430) & (yy < 820)] = [12, 12, 14]
    img[(xx > 640) & (xx < 698) & (yy > 430) & (yy < 438)] = [12, 12, 14]
    img = glow(img, 645, 445, 70, (255, 200, 120), 1.6)
    cone = np.clip(1 - np.abs(xx - 645 - (yy - 445) * 0.15) / (40 + (yy - 445) * 0.55), 0, 1) * (yy > 445) * np.exp(-(yy - 445) / 600)
    img += cone[..., None] * np.array([120, 90, 50])
    fog = np.exp(-((yy - hz) / 140) ** 2)[..., None] * np.array([70, 72, 80])
    return blur(img + fog, 1.2)

def scene_rain(rng):  # rainy window, city bokeh
    img = grad((12, 16, 30), (30, 22, 34))
    img += bokeh(rng, 55, [(255, 170, 80), (255, 210, 140), (120, 160, 230), (230, 110, 90)], 18, 70, 380, 1250) * 0.55
    img = blur(img, 22) * 0.8
    lay = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lay)
    for _ in range(420):
        x = rng.uniform(0, W); y = rng.uniform(0, H); r = rng.uniform(2, 7)
        d.ellipse([x - r, y - r * 1.3, x + r, y + r * 1.3], fill=int(rng.uniform(60, 160)))
    for _ in range(40):
        x = rng.uniform(0, W); y0 = rng.uniform(0, H * 0.7); L = rng.uniform(80, 400)
        d.line([x, y0, x + rng.uniform(-8, 8), y0 + L], fill=int(rng.uniform(40, 110)), width=int(rng.uniform(2, 4)))
    drops = np.asarray(lay.filter(ImageFilter.GaussianBlur(1.2))).astype(float)[..., None] / 255
    return img * (1 - drops * 0.3) + drops * np.array([190, 200, 220]) * 0.55

def scene_moon(rng):  # moon over calm sea
    img = grad((6, 10, 26), (22, 36, 66), curve=1.2)
    img = stars(img, rng, 380, 700)
    img = glow(img, 540, 330, 260, (60, 80, 120), 0.9)
    img = glow(img, 540, 330, 90, (220, 225, 240), 1.0)
    yy, xx = np.mgrid[0:H, 0:W]
    disc = ((xx - 540) ** 2 + (yy - 330) ** 2) < 62 ** 2
    img[disc] = [238, 236, 226]
    hz = 820
    sea = yy > hz
    img[sea] = (np.array([8, 14, 28]) + (yy[sea][:, None] - hz) / (H - hz) * np.array([6, 10, 18]))
    streak = sea & (np.abs(xx - 540 + rng.normal(0, 1, (H, W)) * 30) < 50 * (1 - (yy - hz) / (H - hz) * 0.3))
    shimmer = (np.sin(yy * 0.9) > 0.3)
    img[streak & shimmer] += np.array([120, 125, 140])
    img = fill_below(img, ridge(rng, hz + 2, 6, 0.4), img[hz + 40, 0]) if False else img
    return blur(img, 1.0)

def scene_mist(rng):  # misty layered mountains at dusk
    img = grad((40, 34, 52), (120, 90, 96), curve=0.9)
    img = glow(img, 300, 520, 300, (90, 60, 50), 0.8)
    cols = [(70, 58, 74), (52, 42, 58), (36, 30, 42), (20, 18, 26)]
    for i, c in enumerate(cols):
        img = fill_below(img, ridge(rng, 600 + i * 130, 60 - i * 8, 1.2 + i * 0.3), c)
        yy = np.arange(H)[:, None, None]
        fog = np.exp(-((yy - (640 + i * 130)) / 70) ** 2) * np.array([60, 52, 64]) * 0.6
        img = img + fog
    return blur(img, 1.4)

def scene_sunset(rng):  # warm sunset, lone tree silhouette, bokeh
    img = grad((40, 22, 40), (200, 100, 60), curve=1.1)
    img = glow(img, 540, 1010, 230, (255, 170, 90), 0.85)
    img += bokeh(rng, 25, [(255, 200, 140), (255, 160, 120)], 10, 40, 600, 1100) * 0.5
    img = fill_below(img, ridge(rng, 1060, 14, 0.6), (30, 16, 22))
    lay = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lay)
    def branch(x, y, ang, L, w, depth):
        if depth == 0 or L < 8: return
        x2 = x + L * math.cos(ang); y2 = y - L * math.sin(ang)
        d.line([x, y, x2, y2], fill=255, width=max(1, int(w)))
        for da in (-0.45, 0.35):
            branch(x2, y2, ang + da + rng.uniform(-0.15, 0.15), L * rng.uniform(0.65, 0.8), w * 0.68, depth - 1)
    branch(990, 1065, math.pi / 2 + 0.12, 105, 14, 8)
    m = np.asarray(lay).astype(float)[..., None] / 255
    return blur(img * (1 - m) + m * np.array([24, 12, 18]), 0.8)

def scene_sunrise(rng):  # sunrise rays over mountains
    img = grad((18, 26, 50), (200, 130, 70), curve=1.6)
    yy, xx = np.mgrid[0:H, 0:W]
    ang = np.arctan2(yy - 820, xx - 540)
    rays = (np.sin(ang * 26) * 0.5 + 0.5) ** 6 * np.exp(-np.sqrt((xx - 540) ** 2 + (yy - 820) ** 2) / 700)
    img += rays[..., None] * np.array([255, 200, 120]) * 0.3
    img = glow(img, 540, 820, 140, (255, 220, 150), 1.4)
    img = fill_below(img, ridge(rng, 860, 70, 1.4), (40, 34, 48))
    img = fill_below(img, ridge(rng, 980, 50, 1.6), (22, 20, 30))
    return blur(img, 1.2)

def scene_city(rng):  # night city skyline with lit windows
    img = grad((8, 10, 22), (40, 28, 52))
    img = stars(img, rng, 90, 400)
    img = glow(img, 540, 900, 500, (90, 50, 80), 0.7)
    x = 0
    while x < W:
        bw = int(rng.uniform(60, 140)); bh = int(rng.uniform(90, 260)); top = H - 130 - bh
        img[top:H, x:x + bw] = [14, 14, 22]
        for wy in range(top + 16, H - 140, 26):
            for wx in range(x + 10, x + bw - 14, 20):
                if rng.random() < 0.35:
                    img[wy:wy + 12, wx:wx + 9] = [255, 200, 120] if rng.random() < 0.8 else [170, 200, 255]
        x += bw + int(rng.uniform(4, 16))
    img += bokeh(rng, 30, [(255, 180, 90), (255, 120, 80)], 14, 40, 1100, H) * 0.8
    return blur(img, 1.1)

SCENES = {"road": scene_road, "rain": scene_rain, "moon": scene_moon, "mist": scene_mist,
          "sunset": scene_sunset, "sunrise": scene_sunrise, "city": scene_city}

def cinematic(img, rng):
    img = np.clip(img, 0, 255) / 255.0
    img = img * 0.82  # darken for text
    img = 1 / (1 + np.exp(-(img - 0.42) * 5.5))  # contrast curve
    img = (img - img.min()) / (img.max() - img.min() + 1e-6)
    img[..., 0] = img[..., 0] ** 0.95; img[..., 2] = img[..., 2] ** 1.05  # warm shadows/teal mids
    yy, xx = np.mgrid[0:H, 0:W]
    v = 1 - 0.75 * (((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)
    img *= np.clip(v, 0.15, 1)[..., None]
    band = 1 - 0.58 * np.exp(-((yy - H * 0.5) / (H * 0.24)) ** 2)  # soft dark band behind text
    img *= band[..., None]
    img += rng.normal(0, 0.035, (H, W, 1))  # film grain
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)

# ---------- text ----------
def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    if len(lines) > 1 and len(lines[-1].split()) == 1:  # avoid orphan word
        prev = lines[-2].split(); lines[-2] = " ".join(prev[:-1]); lines[-1] = prev[-1] + " " + lines[-1]
    return lines

def spaced(d, xy_center, text, f, sp, fill):
    w = sum(d.textlength(c, font=f) for c in text) + sp * (len(text) - 1)
    x = xy_center[0] - w / 2
    for c in text:
        d.text((x, xy_center[1]), c, font=f, fill=fill); x += d.textlength(c, font=f) + sp

def text_layer(p):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f1, f2 = font("cg600", 74), font("cg600i", 74)
    l1 = wrap(d, p["line1"], f1, 860); l2 = wrap(d, p["line2"], f2, 860)
    lh = 74 * 1.24; gap = 34
    block = 110 + len(l1) * lh + gap + len(l2) * lh + 60
    y = (H - block) / 2 + 10
    d.text((W / 2, y + 80), "“", font=font("cg600", 170), fill=GOLD + (255,), anchor="ms"); y += 110
    for ln in l1: d.text((W / 2, y + lh / 2), ln, font=f1, fill=CREAM + (255,), anchor="mm"); y += lh
    y += gap
    for ln in l2: d.text((W / 2, y + lh / 2), ln, font=f2, fill=GOLD + (255,), anchor="mm"); y += lh
    y += 30; d.rectangle([W / 2 - 46, y, W / 2 + 46, y + 2], fill=GOLD + (230,))
    spaced(d, (W / 2, 92), p["label"], font("dm700", 24), 7, GREY + (235,))
    # brand watermark
    spaced(d, (W / 2, H - 132), "QUOTATIONS & QUOTES", font("dm700", 22), 6, CREAM + (220,))
    d.text((W / 2, H - 78), "@quotations_and_quotes", font=font("dm500", 26), fill=GREY + (200,), anchor="ms")
    # soft shadow for readability
    a = lay.split()[3].filter(ImageFilter.GaussianBlur(10))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * 0.8)))
    return Image.alpha_composite(sh, lay)

if __name__ == "__main__":  # old 4:5 renderer; scenes are reused by reel916.py
    FD, OUT, POSTS = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(OUT, exist_ok=True)
    posts = json.load(open(POSTS))
    for i, p in enumerate(posts):
        rng = np.random.default_rng(int(os.environ.get("SEED", "100")) + i)
        bg = Image.fromarray(cinematic(SCENES[p["scene"]](rng), rng))
        bg.save(os.path.join(OUT, p["id"] + "_bg.png"))
        tl = text_layer(p); tl.save(os.path.join(OUT, p["id"] + "_text.png"))
        Image.alpha_composite(bg.convert("RGBA"), tl).convert("RGB").save(os.path.join(OUT, p["id"] + ".png"))
        print(p["id"])
