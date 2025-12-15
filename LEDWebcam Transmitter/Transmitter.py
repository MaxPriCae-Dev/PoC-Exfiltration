import cv2
import time

# Mensaje a enviar
mensaje = "OK"

# Convertimos a binario con cabecera 10101010
def texto_a_binario(texto):
    return '10101010' + ''.join(f"{ord(c):08b}" for c in texto)

bits = texto_a_binario(mensaje)
print("Bits a enviar:", bits)

# Abrimos la webcam (LED se enciende)
cap = cv2.VideoCapture(0)

for bit in bits:
    if bit == '1':
        # LED encendido: mantenemos la webcam abierta
        ret, frame = cap.read()
        time.sleep(1)  # duración del bit
    else:
        # LED apagado: cerramos y reabrimos la webcam
        cap.release()
        time.sleep(1)
        cap = cv2.VideoCapture(0)

cap.release()
print("Transmission completed.")

