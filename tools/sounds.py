"""Five original 15-second background tracks for the quote reels (v2: stereo, humanized, mixed).
Everything is synthesized here; no samples or existing melodies are used.
Usage: python3 sounds.py <out_dir>"""
import sys, os, wave
import numpy as np
from scipy.signal import lfilter, butter, sosfilt

SR = 44100; DUR = 15.0; N = int(SR * DUR)
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(23)
T = np.arange(N) / SR

# ---------------- helpers ----------------
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def lp(x, fc, o=2): return sosfilt(butter(o, min(fc, SR / 2 - 100) / (SR / 2), output="sos"), x)
def hp(x, fc, o=2): return sosfilt(butter(o, fc / (SR / 2), "high", output="sos"), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo / (SR / 2), hi / (SR / 2)], "band", output="sos"), x)
def hum(): return rng.normal(0, 0.008)  # timing humanize (s)
def vel(v): return v * rng.uniform(0.85, 1.05)

class Mix:
    def __init__(self): self.L = np.zeros(N); self.R = np.zeros(N)
    def add(self, x, start, g=1.0, pan=0.0):
        s = int(max(0, start) * SR); e = min(N, s + len(x)); seg = x[:e - s] * g
        self.L[s:e] += seg * np.sqrt(0.5 * (1 - pan)); self.R[s:e] += seg * np.sqrt(0.5 * (1 + pan))
    def bus(self, other, g=1.0):
        self.L += other.L * g; self.R += other.R * g

def reverb(L, R, mix=0.3, size=1.0, damp=5000, predelay=0.02):
    def ch(x, combs, aps):
        x = np.concatenate([np.zeros(int(predelay * SR)), x])[:N]
        out = np.zeros(N)
        for d in combs:
            D = int(d * size); a = np.zeros(D + 1); a[0] = 1; a[-1] = -0.84
            out += lfilter([1], a, lp(x, damp, 1))
        out /= len(combs)
        for d in aps:
            b = np.zeros(d + 1); b[0] = -0.5; b[-1] = 1; a = np.zeros(d + 1); a[0] = 1; a[-1] = -0.5
            out = lfilter(b, a, out)
        return out
    wl = ch(L, [1557, 1617, 1491, 1422, 1277, 1356, 1188, 1116], [556, 441, 341, 225])
    wr = ch(R, [1580, 1640, 1514, 1445, 1300, 1379, 1211, 1139], [579, 464, 364, 248])
    return L * (1 - mix) + wl * mix * 1.4, R * (1 - mix) + wr * mix * 1.4

def compress(L, R, thr=0.25, ratio=3.0, att=0.005, rel=0.12):
    lvl = np.maximum(np.abs(L), np.abs(R))
    a = np.exp(-1 / (att * SR)); r = np.exp(-1 / (rel * SR))
    env = lfilter([1 - r], [1, -r], lvl)  # smooth (release-dominated follower)
    env = np.maximum(env, lfilter([1 - a], [1, -a], lvl) * 0.0 + env)
    gain = np.where(env > thr, (thr + (env - thr) / ratio) / np.maximum(env, 1e-9), 1.0)
    return L * gain, R * gain

def master(m, name, rv=0.3, size=1.0, damp=5000, width=1.0):
    L, R = reverb(m.L, m.R, rv, size, damp)
    mid, side = (L + R) / 2, (L - R) / 2 * width; L, R = mid + side, mid - side
    L, R = hp(L, 30), hp(R, 30)
    L, R = compress(L, R)
    fade = np.clip(T / 0.6, 0, 1) * np.clip((DUR - T) / 1.6, 0, 1)
    L, R = L * fade, R * fade
    rms = np.sqrt(np.mean(((L + R) / 2) ** 2)); g = 0.16 / max(rms, 1e-9)  # ~ -16 dBFS RMS
    L, R = np.tanh(L * g * 1.1) / 1.1, np.tanh(R * g * 1.1) / 1.1
    pk = max(np.abs(L).max(), np.abs(R).max()); L, R = L / pk * 0.89, R / pk * 0.89
    p = os.path.join(OUT, name + ".wav")
    with wave.open(p, "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.stack([L, R], 1) * 32767).astype(np.int16).tobytes())
    print(p)

# ---------------- instruments ----------------
def piano(f, dur, v=0.6, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for det in (0.9993, 1.0007):  # two strings per note
        for k in range(1, 10):
            fk = f * k * np.sqrt(1 + 0.00035 * k * k) * det
            if fk > 16000: break
            x += (1 / k ** (1.6 - 0.4 * v * bright)) * np.sin(2 * np.pi * fk * t + rng.uniform(0, 6)) * \
                 (0.6 * np.exp(-t * (0.9 + 0.7 * k)) + 0.4 * np.exp(-t * (0.25 + 0.2 * k)))
    x += hp(rng.normal(0, 1, n), 1500) * np.exp(-t * 90) * 0.03 * v
    x = lp(x, 1800 + 5000 * v * bright)
    return x * v * np.clip((dur - t) / 0.25, 0, 1)

def ks(f, dur, decay=0.997, bright=0.5, pick=0.3):
    n = int(dur * SR); p = max(2, int(round(SR / f)))
    buf = lp(rng.uniform(-1, 1, p * 3), 2500 + 6000 * pick)[-p:]
    out = np.zeros(n); b = buf.copy()
    for i in range(n):
        j = i % p; out[i] = b[j]; b[j] = decay * (bright * b[j] + (1 - bright) * b[(j + 1) % p])
    body = bp(out, 90, 260) * 0.6 + bp(out, 380, 900) * 0.3 + out * 0.6
    return body * np.clip((dur - np.arange(n) / SR) / 0.15, 0, 1)

def bansuri(notes, start=0.0, base=1.0):
    """notes: list of (midi, dur, glide_from or None). Continuous phrase with meend (glides) and breath."""
    total = sum(d for _, d, _ in notes) + 0.4; n = int(total * SR)
    f = np.zeros(n); amp = np.zeros(n); pos = 0; prev = None
    for m, d, g in notes:
        k = int(d * SR); tt = np.arange(k) / SR; tgt = hz(m)
        if g is not None or prev is not None:
            src = hz(g) if g is not None else prev
            gl = np.minimum(tt / 0.12, 1) ** 0.6
            ff = src * (tgt / src) ** gl
        else: ff = np.full(k, tgt)
        vib = 1 + 0.007 * np.sin(2 * np.pi * 5.0 * tt) * np.clip((tt - 0.25) / 0.4, 0, 1)
        f[pos:pos + k] = ff * vib
        a = np.clip(tt / 0.08, 0, 1) * (0.85 + 0.15 * np.sin(np.pi * np.clip(tt / d, 0, 1)))
        amp[pos:pos + k] = a; pos += k; prev = tgt
    f[pos:] = prev; amp[pos:] = np.linspace(amp[pos - 1] if pos else 0, 0, n - pos)
    amp = lp(amp, 25, 1)
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.12 * np.sin(2 * ph) + 0.04 * np.sin(3 * ph)
    breath = bp(rng.normal(0, 1, n), 800, 4000) * 0.09
    return (tone + breath * (0.6 + amp)) * amp * base

def strings(freqs, dur, cutoff=1400, lfo=0.15):
    n = int(dur * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f in freqs:
        for det in (0.996, 1.0, 1.004, 1.008):
            ph = (f * det * t + rng.uniform(0, 1)) % 1
            x += 2 * ph - 1
    x = lp(x, cutoff * (1 + 0.3 * np.sin(2 * np.pi * lfo * t)) .mean())
    return x * np.clip(t / 1.0, 0, 1) * np.clip((dur - t) / 1.0, 0, 1) / len(freqs)

def harmonium(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f in freqs:
        for det in (0.997, 1.0, 1.0035):  # three reeds
            ph = (f * det * t + rng.uniform(0, 1)) % 1
            x += np.where(ph < 0.3, 1.0, -0.43)  # reed-like pulse
    bel = 0.85 + 0.15 * np.sin(2 * np.pi * 0.7 * t + rng.uniform(0, 6))  # bellows
    x = bp(lp(x, 3200), 120, 5000) * bel
    return x * np.clip(t / 0.09, 0, 1) * np.clip((dur - t) / 0.2, 0, 1) / len(freqs)

def sub(f, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * np.clip(t / 0.02, 0, 1) * np.exp(-t * 0.6) * np.clip((dur - t) / 0.1, 0, 1)

def kick(soft=1.0):
    t = np.arange(int(0.5 * SR)) / SR; f = 46 + 110 * np.exp(-t * 28)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) + hp(rng.normal(0, 1, len(t)), 3000) * np.exp(-t * 200) * 0.2) * soft
def snare(dusty=True):
    t = np.arange(int(0.3 * SR)) / SR; nz = bp(rng.normal(0, 1, len(t)), 1200, 7000)
    x = nz * np.exp(-t * 18) * 0.7 + np.sin(2 * np.pi * 185 * t) * np.exp(-t * 30) * 0.5
    return lp(x, 4500) if dusty else x
def hat(open_=False):
    t = np.arange(int((0.25 if open_ else 0.07) * SR)) / SR
    return hp(rng.normal(0, 1, len(t)), 7500) * np.exp(-t * (14 if open_ else 70)) * 0.35
def shaker():
    t = np.arange(int(0.12 * SR)) / SR
    return bp(rng.normal(0, 1, len(t)), 4000, 10000) * np.sin(np.pi * t / t[-1]) ** 2 * 0.25
def dholak_ge():
    t = np.arange(int(0.6 * SR)) / SR; f = 85 + 70 * np.exp(-t * 9)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5) + lp(rng.normal(0, 1, len(t)), 600) * np.exp(-t * 40) * 0.3
def dholak_na():
    t = np.arange(int(0.35 * SR)) / SR
    return (np.sin(2 * np.pi * 480 * t) + 0.6 * np.sin(2 * np.pi * 960 * t) + 0.3 * np.sin(2 * np.pi * 1450 * t)) * np.exp(-t * 14) + \
        bp(rng.normal(0, 1, len(t)), 2000, 6000) * np.exp(-t * 60) * 0.3
def clap():
    t = np.arange(int(0.25 * SR)) / SR; x = np.zeros(len(t))
    for o in (0, 0.011, 0.023, 0.03):
        s = int(o * SR); x[s:] += bp(rng.normal(0, 1, len(t) - s), 900, 5000) * np.exp(-np.arange(len(t) - s) / SR * 28)
    return x * 0.35
def vinyl(n):
    x = np.zeros(n); idx = rng.integers(0, n, 900); x[idx] = rng.normal(0, 1, 900) * rng.uniform(0.2, 1, 900)
    return lp(x, 6000) * 0.5 + lp(rng.normal(0, 1, n), 1200) * 0.015

def sidechain(x, hits, depth=0.45, rel=0.35):
    g = np.ones(N)
    for h in hits:
        s = int(h * SR); k = min(N - s, int(rel * SR))
        if k > 0: g[s:s + k] = np.minimum(g[s:s + k], 1 - depth * np.exp(-np.arange(k) / SR / (rel / 3)))
    return x * g

# ---------------- tracks ----------------
def t1_lofi():
    """Lofi udaas piano, 74 bpm, swing, Am9 - Fmaj7 - C/E - G6sus."""
    m = Mix(); beat = 60 / 74; bar = 4 * beat
    chords = [[57, 60, 64, 67, 71], [53, 57, 60, 64], [52, 55, 60, 64], [55, 57, 62, 64]]
    basses = [45, 41, 40, 43]
    kicks = []
    for b in range(5):
        st = 0.3 + b * bar; c = chords[b % 4]
        for k, n_ in enumerate(c): m.add(piano(hz(n_), bar + 0.4, vel(0.32), 0.7), st + k * 0.018 + hum(), 1, -0.2 + 0.1 * k)
        m.add(sub(hz(basses[b % 4]), bar), st, 0.35)
    mel = [(76, 0.75), (74, 0.5), (72, 0.75), (71, 1.0), (72, 0.5), (69, 1.5), (67, 0.5), (69, 0.75), (72, 0.75),
           (71, 0.5), (69, 0.75), (67, 0.75), (64, 2.0), (67, 0.5), (69, 0.5), (71, 0.75), (72, 1.5)]
    tt = 0.3 + bar
    for n_, d in mel:
        if tt < DUR - 1.4: m.add(piano(hz(n_), d * beat * 1.8, vel(0.5), 0.9), tt + hum(), 1, 0.15)
        tt += d * beat
    dr = Mix()
    for i in range(int(DUR / beat)):
        s = 0.3 + bar + i * beat
        if s > DUR - 1: break
        sw = beat * 0.58
        if i % 4 in (0, 2) or (i % 8 == 7): dr.add(kick(0.9), s + hum(), 0.55); kicks.append(s)
        if i % 4 in (1, 3): dr.add(snare(), s + hum(), 0.32, 0.05)
        dr.add(hat(), s + hum(), 0.35, 0.3); dr.add(hat(), s + sw + hum(), 0.22, 0.3)
    m.L, m.R = sidechain(m.L, kicks, 0.3), sidechain(m.R, kicks, 0.3)
    m.L, m.R = lp(m.L, 4200), lp(m.R, 4200)
    m.bus(dr); v = vinyl(N); m.L += v * 0.35; m.R += np.roll(v, 300) * 0.35
    master(m, "1_lofi_udaas_piano", 0.22, 1.0, 4000)

def t2_sufi():
    """Sufi harmonium + dholak + taali, Bhairavi-ish, 92 bpm keherwa."""
    m = Mix(); sa = 50  # D3
    drone = harmonium([hz(sa), hz(sa + 7), hz(sa + 12)], DUR)
    m.add(drone, 0, 0.35, -0.1)
    # call phrase (Bhairavi: S r g M P d n)
    ph = [(12, .45), (13, .45), (15, .9), (13, .45), (12, .45), (10, .9), (8, .45), (7, 1.35),
          (8, .45), (10, .45), (12, .9), (13, .45), (15, .45), (17, .9), (15, .45), (13, .45), (12, 1.6)]
    tt = 1.4
    for s, d in ph:
        if tt < DUR - 1: m.add(harmonium([hz(sa + 12 + s)], d * 1.05), tt + hum(), 0.55, 0.15)
        tt += d
    beat = 60 / 92 / 2
    patt = ["ge", "na", "-", "na", "ge", "ge", "na", "-"]
    i = 0
    while 1.4 + i * beat < DUR - 0.8:
        s = 1.4 + i * beat; p = patt[i % 8]
        if p == "ge": m.add(dholak_ge(), s + hum(), vel(0.55), -0.15)
        elif p == "na": m.add(dholak_na(), s + hum(), vel(0.3), 0.2)
        if i % 8 in (2, 6) and s > 5: m.add(clap(), s + hum(), vel(0.6), 0.35); m.add(clap(), s + 0.02, 0.4, -0.35)
        i += 1
    master(m, "2_sufi_harmonium", 0.25, 1.1, 5500)

def t3_bansuri():
    """Bansuri over strings, slow cinematic, Yaman-ish with meend."""
    m = Mix(); sa = 62  # D4
    m.add(strings([hz(50), hz(57), hz(62), hz(66)], 7.6, 1100), 0, 0.5, -0.3)
    m.add(strings([hz(47), hz(54), hz(59), hz(62)], 7.6, 1100), 7.3, 0.5, -0.3)
    m.add(sub(hz(38), 7.5), 0.2, 0.4); m.add(sub(hz(35), 7.5), 7.4, 0.4)
    phrase = [(sa + 11, 0.5, None), (sa + 14, 0.9, sa + 12), (sa + 16, 1.3, None), (sa + 14, 0.5, None), (sa + 12, 0.6, None),
              (sa + 11, 1.4, None), (sa + 9, 0.5, None), (sa + 7, 0.9, sa + 9), (sa + 9, 0.6, None), (sa + 11, 0.6, None),
              (sa + 12, 2.6, sa + 11)]
    m.add(bansuri(phrase, base=0.55), 1.2, 1, 0.1)
    for s in (0.2, 7.3, 13.0):
        m.add(kick(1.3), s, 0.45)
    m.add(lp(rng.normal(0, 1, int(3 * SR)), 300) * np.linspace(0, 1, int(3 * SR)) * 0.15, 4.3, 1)  # swell
    master(m, "3_bansuri_cinematic", 0.36, 1.35, 5000, 0.8)

def t4_guitar():
    """Romantic fingerstyle guitar, D - Bm - G - A, with a soft lead and shaker."""
    m = Mix(); beat = 60 / 80 / 2
    chords = [[50, 57, 62, 66, 69], [47, 54, 59, 62, 66], [43, 50, 55, 59, 62], [45, 52, 57, 61, 64]]
    order = [0, 2, 3, 4, 1, 3, 2, 4]
    i = 0
    while 0.2 + i * beat < DUR - 0.6:
        c = chords[(i // 8) % 4]; s = 0.2 + i * beat
        m.add(ks(hz(c[order[i % 8]]), 2.2, 0.9975, 0.5, 0.35), s + hum(), vel(0.42), -0.25)
        m.add(ks(hz(c[order[i % 8]]) * 1.002, 2.2, 0.9975, 0.5, 0.35), s + 0.012 + hum(), vel(0.25), 0.3)  # double
        if i % 2 == 1 and s > 3.6: m.add(shaker(), s + hum(), vel(0.5), 0.4)
        i += 1
    lead = [(74, 1.0), (76, .5), (78, 1.5), (76, .5), (74, 1.0), (73, 1.0), (71, 2.0), (73, .5), (74, .5), (76, 1.0), (74, 2.0)]
    tt = 0.2 + 16 * beat
    for n_, d in lead:
        if tt < DUR - 1.2: m.add(ks(hz(n_), d * beat * 2.4, 0.998, 0.62, 0.6), tt + hum(), vel(0.33), 0.05)
        tt += d * beat * 2
    master(m, "4_romantic_guitar", 0.3, 1.1, 6000)

def t5_slowed():
    """Slowed + reverb sad: dark strings, detuned piano, heartbeat, rain-like air."""
    m = Mix(); slow = 0.94
    m.add(strings([hz(45) * slow, hz(52) * slow, hz(57) * slow, hz(60) * slow], 8.0, 800), 0, 0.55, -0.2)
    m.add(strings([hz(41) * slow, hz(48) * slow, hz(53) * slow, hz(57) * slow], 8.0, 800), 7.2, 0.55, 0.2)
    notes = [(76, 0.9), (74, 2.4), (72, 3.9), (71, 5.0), (69, 6.4), (72, 8.4), (71, 9.9), (67, 11.2), (69, 12.4)]
    for n_, s in notes: m.add(piano(hz(n_) * slow, 3.2, vel(0.45), 0.6), s + hum(), 1, 0.2)
    for s in np.arange(1.0, DUR - 1.2, 1.7):
        m.add(kick(0.8), s, 0.4); m.add(kick(0.55), s + 0.27, 0.3)
        m.add(sub(hz(33) * slow, 1.2), s, 0.25)
    air = hp(lp(rng.normal(0, 1, N), 6000), 1500) * 0.025
    m.L += air; m.R += np.roll(air, 4000)
    m.L, m.R = lp(m.L, 3200), lp(m.R, 3200)
    master(m, "5_slowed_reverb_sad", 0.45, 1.7, 3000, 0.7)

for fn in (t1_lofi, t2_sufi, t3_bansuri, t4_guitar, t5_slowed): fn()
