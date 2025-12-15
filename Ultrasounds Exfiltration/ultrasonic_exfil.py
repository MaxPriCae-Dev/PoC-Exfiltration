#!/usr/bin/env python3
import numpy as np
import pyaudio

# Parametros compartidos
FREQ_0 = 7000      # Frecuencia para el bit 0 (ultrasonido tipico)
FREQ_1 = 10000      # Frecuencia para el bit 1
BIT_RATE = 30       # Bits por segundo (mas bajo = mas fiable)
RATE = 44100        # Frecuencia de muestreo
DURATION = 1 / BIT_RATE
CODE = "12345"

USER_TEXT = "Hello tester, USER: Admin / Password: P@ssw0rd!123"
START_MARKER = f"START:{CODE}"
END_MARKER = f"END:{CODE}"

def text_to_bits(text):
    return ''.join(f"{ord(c):08b}" for c in text)

def transmit_bits(bits):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, output=True)
    # Silencio inicial de 2 segundos
    silence = np.zeros(int(RATE * 2.0), dtype=np.float32)
    stream.write(silence.tobytes())
    # Transmision de bits
    for bit in bits:
        freq = FREQ_1 if bit == '1' else FREQ_0
        samples = (np.sin(2 * np.pi * np.arange(int(RATE * DURATION)) * freq / RATE) * 0.9).astype(np.float32)
        stream.write(samples.tobytes())
    # Silencio final
    stream.write(silence.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    message = START_MARKER + USER_TEXT + END_MARKER
    bits = text_to_bits(message)
    print(f"Transmitting: '{message}'")
    print(f"Total bits: {len(bits)}")
    transmit_bits(bits)
    print("Transmission completed.")
