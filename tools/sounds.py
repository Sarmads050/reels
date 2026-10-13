"""Five original 15-second background tracks for the quote reels (all composed here, no samples).
Usage: python3 sounds.py <out_dir>"""
import sys, os
import numpy as np
from scipy.signal import lfilter, butter

SR = 44100; DUR = 15.0; N = int(SR * DUR)
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(11)
t_all = np.arange(N) / SR

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)  # MIDI -> Hz
def env_adsr(n, a=0.01, d=0.2, s=0.6, r=0.3):
    t = np.arange(n) / SR; L = n / SR
    e = np.minimum(t / a, 1)
    e = np.where(t > a, 1 - (1 - s) * np.minimum((t - a) / d, 1), e)
    return e * np.clip((L - t) / r, 0, 1)
def add(buf, x, start, g=1.0):
    s = int(start * SR); e = min(len(buf), s + len(x)); buf[s:e] += g * x[:e - s]
def lowpass(x, fc, order=2):
    b, a = butter(order, fc / (SR / 2)); return lfilter(b, a, x)
def highpass(x, fc, order=2):
    b, a = butter(order, fc / (SR / 2), "high"); return lfilter(b, a, x)

def reverb(x, mix=0.3, size=1.0):
    out = np.zeros_like(x)
    for d, g in [(1557, .84), (1617, .83), (1491, .82), (1422, .81), (1277, .8), (1356, .8)]:
        D = int(d * size); a = np.zeros(D + 1); a[0] = 1; a[-1] = -g
        out += lfilter([1], a, x)
    out /= 6
    for d in (225, 556, 441):
        b = np.zeros(d + 1); b[0] = -0.5; b[-1] = 1; a = np.zeros(d + 1); a[0] = 1; a[-1] = -0.5
        out = lfilter(b, a, out)
    return x * (1 - mix) + out * mix

def piano(f, dur, vel=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    tone = sum((1 / k ** 1.3) * np.sin(2 * np.pi * f * k * (1 + 0.0004 * k * k) * t) * np.exp(-t * (1.2 + 0.9 * k)) for k in range(1, 8))
    ham = rng.normal(0, 1, n) * np.exp(-t * 60) * 0.05
    return (tone + ham) * vel * np.clip((dur - t) / 0.08, 0, 1)

def ks(f, dur, decay=0.996, bright=0.5):
    n = int(dur * SR); p = max(2, int(SR / f)); buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        j = i % p; out[i] = buf[j]; buf[j] = decay * (bright * buf[j] + (1 - bright) * buf[(j + 1) % p])
    return out

def flute(f, dur, vib=0.006):
    n = int(dur * SR); t = np.arange(n) / SR
    v = 1 + vib * np.sin(2 * np.pi * 5.2 * t) * np.clip(t / 0.35, 0, 1)
    ph = 2 * np.pi * f * np.cumsum(v) / SR
    x = np.sin(ph) + 0.15 * np.sin(2 * ph) + 0.05 * np.sin(3 * ph)
    x += lowpass(rng.normal(0, 1, n), 3000) * 0.05
    return x * np.clip(t / 0.12, 0, 1) * np.clip((dur - t) / 0.2, 0, 1)

def harmonium(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f in freqs:
        for det in (0.998, 1.0, 1.003):
            ph = 2 * np.pi * f * det * t
            x += 2 * (ph / (2 * np.pi) % 1) - 1  # saw
    x = lowpass(x, 1800) * (1 + 0.08 * np.sin(2 * np.pi * 5 * t))
    return x * np.clip(t / 0.15, 0, 1) * np.clip((dur - t) / 0.3, 0, 1)

def pad(freqs, dur, cutoff=900):
    n = int(dur * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f in freqs:
        for det in (0.995, 1.0, 1.006):
            x += np.sin(2 * np.pi * f * det * t + rng.uniform(0, 6))
            x += 0.3 * np.sin(2 * np.pi * 2 * f * det * t)
    return lowpass(x, cutoff) * np.clip(t / 1.2, 0, 1) * np.clip((dur - t) / 1.2, 0, 1)

def kick():
    t = np.arange(int(0.4 * SR)) / SR; f = 50 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
def snare(soft=True):
    t = np.arange(int(0.25 * SR)) / SR
    return (highpass(rng.normal(0, 1, len(t)), 1500) * 0.6 + np.sin(2 * np.pi * 190 * t) * 0.4) * np.exp(-t * 22) * (0.5 if soft else 1)
def hat():
    t = np.arange(int(0.06 * SR)) / SR; return highpass(rng.normal(0, 1, len(t)), 7000) * np.exp(-t * 80) * 0.3
def tabla_na():
    t = np.arange(int(0.4 * SR)) / SR; return (np.sin(2 * np.pi * 520 * t) + 0.5 * np.sin(2 * np.pi * 1040 * t)) * np.exp(-t * 10)
def tabla_ge():
    t = np.arange(int(0.6 * SR)) / SR; f = 90 + 50 * np.exp(-t * 6); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)
def clap():
    t = np.arange(int(0.2 * SR)) / SR; x = np.zeros(len(t))
    for o in (0, 0.012, 0.024): x[int(o * SR):] += highpass(rng.normal(0, 1, len(t) - int(o * SR)), 1200) * np.exp(-np.arange(len(t) - int(o * SR)) / SR * 30)
    return x * 0.5
def crackle(n):
    x = np.zeros(n); idx = rng.integers(0, n, 600); x[idx] = rng.normal(0, 1, 600)
    return lowpass(x, 5000) * 0.6 + lowpass(rng.normal(0, 1, n), 800) * 0.02

def finish(x, name, rv=0.3, size=1.0):
    x = reverb(x, rv, size)
    x *= np.clip(t_all / 0.8, 0, 1) * np.clip((DUR - t_all) / 1.5, 0, 1)
    x = np.tanh(x / np.max(np.abs(x)) * 1.2); x = x / np.max(np.abs(x)) * 0.8
    st = np.stack([x, np.roll(x, int(0.011 * SR))], 1)
    import wave
    p = os.path.join(OUT, name + ".wav")
    with wave.open(p, "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
    print(p)

# 1. Lofi udaas piano (72 bpm): Am - F - C - G, soft beat, vinyl crackle
def track1():
    x = np.zeros(N); beat = 60 / 72
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    mel = [76, 74, 72, 71, 72, 69, None, 67, 69, 72, 71, 69, 67, 64, None, 64]
    for bar in range(5):
        c = chords[bar % 4]; st = bar * 4 * beat
        for k, m in enumerate(c): add(x, piano(hz(m), 4 * beat, 0.35), st + k * 0.03)
        add(x, piano(hz(c[0] - 12), 4 * beat, 0.4), st)
    for i, m in enumerate(mel * 2):
        if m and 1.0 + i * beat * 0.75 < DUR - 1.2: add(x, piano(hz(m), beat * 1.6, 0.45), 1.0 + i * beat * 0.75)
    x = lowpass(x, 3500)
    for b in range(int(DUR / beat)):
        s = b * beat
        if b % 2 == 0: add(x, kick(), s, 0.5)
        else: add(x, snare(), s, 0.35)
        add(x, hat(), s + beat / 2, 0.5)
    x += crackle(N) * 0.4
    finish(x, "1_lofi_udaas_piano", 0.25)

# 2. Sufi harmonium + dholak + taali (Bhairavi feel)
def track2():
    x = np.zeros(N)
    sa = 50  # D
    seq = [[0, 7], [1, 8], [0, 7], [-2, 5]]
    for i, s in enumerate(seq * 2):
        add(x, harmonium([hz(sa + s[0]), hz(sa + s[1]), hz(sa + 12)], 2.0), i * 1.9, 0.18)
    phrase = [12, 13, 15, 13, 12, 10, 8, 7, 8, 10, 12, 13, 12]
    tt = 1.2
    for m in phrase:
        d = 0.55 if m != 12 else 0.9
        add(x, harmonium([hz(sa + 12 + m)], d), tt, 0.22); tt += d * 0.95
    beat = 60 / 90 / 2
    patt = ["ge", "na", "na", "ge", "na", "ge", "na", "na"]
    for i in range(int((DUR - 1.5) / beat)):
        s = 1.5 + i * beat; p = patt[i % 8]
        add(x, tabla_ge() if p == "ge" else tabla_na(), s, 0.5 if p == "ge" else 0.3)
        if i % 4 == 2: add(x, clap(), s, 0.5)
    finish(x, "2_sufi_harmonium", 0.22)

# 3. Bansuri cinematic: pad + bansuri + deep hits
def track3():
    x = np.zeros(N); sa = 62
    x += pad([hz(50), hz(57), hz(62)], DUR, 700) * 0.12
    mel = [(0, 1.2), (2, .6), (3, .6), (5, 1.4), (3, .6), (2, .6), (0, 1.6), (-2, .8), (0, 2.4)]
    tt = 1.0
    for m, d in mel:
        add(x, flute(hz(sa + 12 + m), d * 1.05), tt, 0.35); tt += d
    for s in (0.2, 4.0, 8.0, 12.0):
        add(x, kick() * 1.5, s, 0.6)
    finish(x, "3_bansuri_cinematic", 0.4, 1.3)

# 4. Romantic acoustic guitar: D - Bm - G - A fingerpicking
def track4():
    x = np.zeros(N); beat = 60 / 84 / 2
    chords = [[50, 57, 62, 66], [47, 54, 59, 62], [43, 50, 55, 59], [45, 52, 57, 61]]
    order = [0, 2, 1, 3, 2, 3, 1, 2]
    i = 0
    while i * beat < DUR - 0.5:
        c = chords[(i // 8) % 4]
        add(x, ks(hz(c[order[i % 8]]), 1.6, 0.997, 0.45), i * beat, 0.35); i += 1
    mel = [74, 73, 71, 69, 71, 73, 74, 76, 74, 71]
    for k, m in enumerate(mel):
        add(x, ks(hz(m), 1.2, 0.996, 0.6), 2.3 + k * beat * 2.2, 0.25)
    for k in range(int(DUR / (beat * 2))):
        add(x, hat() * 0.6, k * beat * 2 + beat, 0.4)
    finish(x, "4_romantic_guitar", 0.28)

# 5. Slowed + reverb sad: dark pad, sparse piano, heartbeat pulse
def track5():
    x = np.zeros(N)
    x += pad([hz(45), hz(52), hz(57), hz(60)], DUR, 600) * 0.15
    notes = [(72, 1.0), (71, 2.6), (69, 4.2), (64, 6.0), (67, 8.2), (65, 10.0), (64, 11.8)]
    for m, s in notes:
        add(x, piano(hz(m) * 0.94, 3.0, 0.5), s)  # pitched down = slowed feel
    for s in np.arange(0.8, DUR - 1, 1.6):
        add(x, kick() * 0.8, s, 0.35); add(x, kick() * 0.5, s + 0.28, 0.25)
    x = lowpass(x, 2600)
    finish(x, "5_slowed_reverb_sad", 0.5, 1.6)

for f in (track1, track2, track3, track4, track5): f()
