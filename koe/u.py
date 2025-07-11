import numpy as np
import sounddevice as sd

def generate_u_wave(duration=15.0, fs=44100):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)

    # 包絡：語頭立ち上がり＋語尾沈み＋感情揺らぎ
    env = (1 - np.exp(-4 * t)) * np.exp(-1.6 * t) * (1 + 0.04 * np.sin(2 * np.pi * 0.35 * t))

    # ソース：120Hzサイン波（声帯振動の代用）
    source = np.sin(2 * np.pi * 120 * t)

    # フォルマント構成：「う」型（F1=350Hz, F2=800Hz, F3=2200Hz）
    freqs = [350, 800, 2200]
    amps  = [1.0, 0.5, 0.3]
    wave = sum(amp * np.sin(2 * np.pi * f * t) for f, amp in zip(freqs, amps))

    # 合成：ソース × フォルマント × 包絡
    output = source * wave * env
    output /= np.max(np.abs(output) + 1e-7)  # 安全な正規化
    return output.astype(np.float32)

# 再生：15秒版「語るうーーー」
wave = generate_u_wave()
sd.play(wave, samplerate=44100)
sd.wait()
