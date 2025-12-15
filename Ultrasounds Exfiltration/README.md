# Ultrasonic Speaker Exfiltration (PoC)

> **Educational demo** showing how text can be sent using sound from a **speaker** and received by a **microphone**, then turned back into readable text.  
>  
> ⚠️ **For research only**: Use in controlled environments, never on production systems or with sensitive data.

---

## How It Works

* Two tones represent data:  
  * **7000 Hz → 0**  
  * **10000 Hz → 1**  
* The transmitter converts text into bits and plays the tones.  
* The receiver listens, detects the tones, and rebuilds the original text.

---

## Setup

* **Transmitter (Computer A)** → needs a speaker.  
* **Receiver (Computer B)** → needs a decent microphone.  
* Running both on one machine is possible but less reliable.

---

## Requirements

* Python 3.x  
* Hardware: speaker + microphone  
* Libraries: `numpy`, `pyaudio`  

---

## Install

```bash
git clone <repo-url>
cd <repo>
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# Windows: .venv\Scripts\activate
pip install numpy pyaudio
```

---

## Ethics & Disclaimer

* Use only with permission and in safe test setups.  
* Do not send real credentials or personal data.  
* This is a **concept demo** — no error correction, encryption, or integrity checks.  
* Author is not responsible for misuse.

---

## License

MIT
