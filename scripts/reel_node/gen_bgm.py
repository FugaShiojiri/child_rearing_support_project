#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""やさしいオルゴール風BGMを自前生成（著作権リスクゼロ・無料・約31秒）。
numpy + 標準waveのみ。出力: bgm.wav"""
import numpy as np, wave, struct, os

SR = 44100
DUR = 31.0
N = int(SR * DUR)
t = np.arange(N) / SR
out = np.zeros(N)

def note(freq, start, dur=1.4, amp=0.16):
    """ベル風（速いアタック＋指数減衰＋倍音少し）"""
    n0 = int(start * SR); n1 = min(N, n0 + int(dur * SR))
    if n0 >= N: return
    tt = np.arange(n1 - n0) / SR
    env = np.exp(-tt / (dur * 0.32))
    env *= np.minimum(1.0, tt / 0.006)  # 短いアタック
    wave_ = (np.sin(2*np.pi*freq*tt)
             + 0.5*np.sin(2*np.pi*2*freq*tt)
             + 0.25*np.sin(2*np.pi*3*freq*tt))
    out[n0:n1] += amp * env * wave_

# C メジャー・ペンタトニック（やさしい・外れない）
P = {'C':261.63,'D':293.66,'E':329.63,'G':392.00,'A':440.00,
     'C2':523.25,'D2':587.33,'E2':659.25,'G2':783.99,'A2':880.00}
# ゆっくりした分散和音（約0.62秒間隔）。素朴で繰り返しても心地よい並び
seq = ['C2','E2','G2','A2','G2','E2','D2','E2',
       'C2','D2','E2','G2','A2','C2','G2','E2',
       'D2','E2','G2','A2','G2','E2','C2','D2',
       'E2','G2','A2','G2','E2','D2','C2','C2',
       'E2','G2','A2','C2','G2','E2','D2','C2',
       'G2','A2','C2','D2','C2','A2','G2','E2']
step = 0.62
for i, name in enumerate(seq):
    note(P[name], 0.3 + i*step, dur=1.5, amp=0.15)

# 低音のやわらかいパッド（C-G を薄く・温かみ）
for base, st, dr in [('C',0.0,8.0),('G',8.0,8.0),('A',16.0,7.0),('G',23.0,8.0)]:
    n0=int(st*SR); n1=min(N,n0+int(dr*SR)); tt=np.arange(n1-n0)/SR
    env=np.minimum(tt/0.8,1.0)*np.minimum(1.0,(dr-tt)/1.2)
    f=P[base]/2
    out[n0:n1]+=0.05*env*(np.sin(2*np.pi*f*tt)+0.4*np.sin(2*np.pi*2*f*tt))

# 全体フェードイン/アウト
fin=int(1.2*SR); fout=int(2.0*SR)
out[:fin]*=np.linspace(0,1,fin); out[-fout:]*=np.linspace(1,0,fout)

# 正規化（控えめ＝朗読/視聴の邪魔をしない音量）
peak=np.max(np.abs(out)) or 1.0
out=out/peak*0.5

path=os.path.join(os.path.dirname(__file__),'bgm.wav')
w=wave.open(path,'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(b''.join(struct.pack('<h',int(max(-1,min(1,x))*32767)) for x in out))
w.close()
print('[OK] bgm.wav', round(DUR,1),'s ->', path)
