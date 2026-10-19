#!/usr/bin/env python3
"""Soft spa ambient pad (deterministic, royalty-free): ambient.py <dur> out.wav [seed]"""
import sys, numpy as np, soundfile as sf
dur = float(sys.argv[1]); out = sys.argv[2]; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
sr = 48000; n = int(dur * sr); t = np.arange(n) / sr
rng = np.random.default_rng(seed)
# I - vi - IV - V in D major, slow pads
roots = [[146.83, 220.0, 293.66, 369.99], [123.47, 185.0, 246.94, 293.66], [98.0, 196.0, 246.94, 293.66], [110.0, 220.0, 277.18, 329.63]]
bar = 4.0
sig = np.zeros(n)
for i, start in enumerate(np.arange(0, dur, bar)):
    ch = roots[(i + seed) % 4]
    s0 = int(start * sr); s1 = min(n, int((start + bar + 1.5) * sr))
    tt = t[s0:s1] - start
    env = np.minimum(1, tt / 1.4) * np.exp(-np.maximum(0, tt - bar) / 0.6)
    for f in ch:
        det = 1 + rng.uniform(-0.002, 0.002)
        sig[s0:s1] += env * (np.sin(2*np.pi*f*det*tt) + 0.3*np.sin(2*np.pi*2*f*det*tt)) * 0.06
# soft high "chime" notes
for k in range(int(dur / 2)):
    st = k * 2 + 0.5 + rng.uniform(0, 0.4)
    f = rng.choice([587.33, 659.25, 739.99, 880.0])
    s0 = int(st * sr); s1 = min(n, s0 + int(2.5 * sr)); tt = t[s0:s1] - st
    sig[s0:s1] += np.sin(2*np.pi*f*tt) * np.exp(-tt / 0.9) * 0.035
fade = np.minimum(1, t / 1.0) * np.minimum(1, (dur - t) / 1.2)
sig = sig * fade
sig = sig / (np.abs(sig).max() + 1e-9) * 0.6
st = np.stack([sig, np.roll(sig, 240)], 1)
sf.write(out, st, sr)
