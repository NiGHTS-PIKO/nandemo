import numpy as np
import sounddevice as sd

def generate_vowel(freqs, amps, duration=0.5, fs=44100):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)

    # 包絡：語頭アタック＋語尾沈み＋息膜揺らぎ
    env = (1 - np.exp(-4 * t)) * np.exp(-0.5 * t) * (1 + 0.06 * np.sin(2 * np.pi * 0.7 * t))

    # 声帯ソース：120Hz＋倍音＋微揺らぎ
    jitter = 0.5 * np.sin(2 * np.pi * 0.3 * t)
    source = (
        np.sin(2 * np.pi * (120 + jitter) * t) +
        0.2 * np.sin(2 * np.pi * 240 * t) +
        0.1 * np.sin(2 * np.pi * 360 * t)
    )
    source *= (1 + 0.05 * np.sin(2 * np.pi * 3.5 * t))

    # フォルマント構成（口腔共鳴）
    wave = sum(amp * np.sin(2 * np.pi * f * t) for f, amp in zip(freqs, amps))

    # 声化ノイズ群（息膜・shimmer・摩擦音）
    breath_noise = np.random.normal(0, 0.002, size=t.shape)
    breath_noise = np.convolve(breath_noise, np.ones(40)/40, mode='same') * env * 0.3
    shimmer = 0.001 * np.sin(2 * np.pi * 7000 * t) * env * 0.2
    burst = np.random.normal(0, 1.0, size=t.shape) * np.exp(-40 * t) * 0.1

    # 合成
    output = source * wave * env + breath_noise + shimmer + burst
    output /= np.max(np.abs(output) + 1e-7)
    return output.astype(np.float32)

# 母音テンプレート（フォルマント構成）
vowel_profiles = {
    "a": ([560, 1100, 1950], [1.5, 0.7, 0.4]),
    "i": ([300, 2200, 3000], [1.4, 0.6, 0.3]),
    "u": ([360, 800, 2200], [1.5, 0.7, 0.4]),
    "e": ([500, 1700, 2600], [1.4, 0.6, 0.3]),
    "o": ([450, 1000, 2400], [1.4, 0.6, 0.3]),
}

# 母音列を連結：「あ→い→う→え→お」各0.5秒
wave = np.concatenate([
    generate_vowel(freqs, amps)
    for freqs, amps in vowel_profiles.values()
])

# 再生：スピーカーに語らせる波形
sd.play(wave, samplerate=44100)
sd.wait()
