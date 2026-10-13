import numpy as np, wave, sys
sr = 44100; DUR = 15.0; N = int(sr * DUR); t = np.arange(N) / sr
rng = np.random.default_rng(7)
SA = 146.83  # D3 as Sa

def ks(freq, dur, decay=0.996, bright=0.5):
    n = int(sr * dur); p = int(sr / freq)
    buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        nxt = buf[(i + 1) % p]
        buf[i % p] = decay * (bright * buf[i % p] + (1 - bright) * nxt)
    return out

def add(sig, x, start, gain=1.0):
    s = int(start * sr); e = min(len(sig), s + len(x)); sig[s:e] += gain * x[:e - s]

def tanpura():
    sig = np.zeros(N); notes = [SA * 1.5 / 2 * 2 / 2 * 2 * 0.5 * 1.5, SA, SA, SA / 2]  # Pa(low) Sa Sa Sa(low)
    notes = [SA * 0.75, SA, SA, SA * 0.5]
    tt = 0.0; i = 0
    while tt < DUR:
        x = ks(notes[i % 4], 3.0, decay=0.9985, bright=0.55)
        x *= np.exp(-np.arange(len(x)) / sr * 0.6)
        add(sig, x, tt, 0.5); tt += 0.95; i += 1
    return sig

# Raag Yaman-ish scale ratios (Sa Re Ga Ma# Pa Dha Ni Sa')
R = {"S":1,"R":9/8,"G":5/4,"M":45/32,"P":3/2,"D":5/3,"N":15/8,"S'":2,"R'":9/4,"G'":5/2}
def flute_note(f, dur):
    n = int(sr * dur); tt = np.arange(n) / sr
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.2 * tt) * np.clip(tt / 0.4, 0, 1)
    ph = 2 * np.pi * f * np.cumsum(vib) / sr
    tone = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    breath = rng.normal(0, 1, n); breath = np.convolve(breath, np.ones(30) / 30, "same") * 0.08
    env = np.clip(tt / 0.12, 0, 1) * np.clip((dur - tt) / 0.25, 0, 1)
    return (tone + breath) * env

def bansuri():
    sig = np.zeros(N); f0 = SA * 2
    phrase = [("N",0.6),("R'",0.6),("G'",1.4),("R'",0.5),("S'",1.6),("rest",0.5),
              ("N",0.5),("D",0.5),("P",1.5),("M",0.5),("G",1.2),("rest",0.4),
              ("G",0.5),("M",0.5),("D",0.6),("N",0.6),("S'",2.2)]
    tt = 0.9
    for n, d in phrase:
        if n != "rest": add(sig, flute_note(f0 * R[n] / 2 * 2 if False else f0 * R[n], d * 1.05), tt, 0.42)
        tt += d
    return sig

def tabla():
    sig = np.zeros(N); bpm = 72; beat = 60 / bpm / 2  # 8 matra keherwa at eighths
    def na():
        n = int(sr * 0.5); tt = np.arange(n) / sr
        return (np.sin(2*np.pi*520*tt) + 0.5*np.sin(2*np.pi*1040*tt)) * np.exp(-tt * 9)
    def ge():
        n = int(sr * 0.7); tt = np.arange(n) / sr
        f = 95 + 60 * np.exp(-tt * 6)
        return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt * 4.5)
    def ti():
        n = int(sr * 0.15); tt = np.arange(n) / sr
        return rng.normal(0, 1, n) * np.exp(-tt * 40) * 0.4 + np.sin(2*np.pi*780*tt) * np.exp(-tt*30) * 0.4
    pattern = ["dha","ge","na","ti","na","ka","dhi","na"]
    tt = 2.0; i = 0
    while tt < DUR - 0.8:
        b = pattern[i % 8]
        if b in ("dha","dhi"): add(sig, ge(), tt, 0.55); add(sig, na(), tt, 0.3)
        elif b == "ge": add(sig, ge(), tt, 0.4)
        elif b == "na": add(sig, na(), tt, 0.3)
        elif b == "ti": add(sig, ti(), tt, 0.5)
        tt += beat; i += 1
    return sig

def reverb(x):
    out = x.copy()
    for d, g in [(0.029, .35), (0.047, .28), (0.071, .22), (0.113, .16), (0.167, .1)]:
        k = int(d * sr); out[k:] += g * x[:-k]
    return out

mix = 0.9 * tanpura() + bansuri() + 0.8 * tabla()
mix = reverb(mix)
fade = np.clip(t / 1.2, 0, 1) * np.clip((DUR - t) / 1.8, 0, 1)
mix *= fade; mix = mix / np.max(np.abs(mix)) * 0.5
st = np.stack([mix, np.roll(mix, int(0.012 * sr))], axis=1)
with wave.open(sys.argv[1], "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok")
