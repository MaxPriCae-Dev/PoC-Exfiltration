#!/usr/bin/env python3
import pyaudio
import numpy as np
import time

# Parametros compartidos
FREQ_0 = 7000
FREQ_1 = 10000
BIT_RATE = 30
RATE = 44100
CHUNK = int(RATE / BIT_RATE)
CODE = "12345"
START_MARKER = f"START:{CODE}"
END_MARKER = f"END:{CODE}"

def detect_bit(chunk):
    chunk = chunk * np.hanning(len(chunk))
    fft = np.abs(np.fft.rfft(chunk))
    freqs = np.fft.rfftfreq(len(chunk), d=1/RATE)
    idx_0 = np.logical_and(freqs >= FREQ_0-100, freqs <= FREQ_0+100)
    idx_1 = np.logical_and(freqs >= FREQ_1-100, freqs <= FREQ_1+100)
    energy_0 = np.sum(fft[idx_0])
    energy_1 = np.sum(fft[idx_1])
    min_energy = 5.0
    if energy_0 > energy_1 and energy_0 > min_energy:
        return '0'
    elif energy_1 > energy_0 and energy_1 > min_energy:
        return '1'
    else:
        return ''

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            continue
        try:
            char = chr(int(byte, 2))
            chars.append(char)
        except:
            continue
    return ''.join(chars)

def extract_and_save_messages(full_text):
    idx = 0
    while True:
        start_idx = full_text.find(START_MARKER, idx)
        if start_idx == -1:
            break
        end_idx = full_text.find(END_MARKER, start_idx)
        if end_idx == -1:
            break
        payload = full_text[start_idx + len(START_MARKER): end_idx].strip()
        if payload:
            filename = f"exfil_{int(time.time())}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(payload)
            print(f"\n[INFO] Message saved to {filename}")
        idx = end_idx + len(END_MARKER)

def record_and_decode():
    print("Listening... (cleaning mic buffer first)")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
    # Limpieza del buffer del micro
    for _ in range(40):
        stream.read(CHUNK, exception_on_overflow=False)

    bits = ''
    print("Recording started. Press Ctrl+C to stop.")

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=np.float32)
            bit = detect_bit(samples)
            if bit in ('0', '1'):
                bits += bit
            # Busca los marcadores en varias alineaciones
            if len(bits) > 8*len(START_MARKER):
                for offset in range(8):
                    test_bits = bits[offset:]
                    window_text = bits_to_text(test_bits)
                    if START_MARKER in window_text and END_MARKER in window_text:
                        extract_and_save_messages(window_text)
                        bits = ''
                        break
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == '__main__':
    record_and_decode()

