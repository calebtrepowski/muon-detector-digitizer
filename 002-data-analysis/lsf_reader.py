import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir(os.path.dirname(__file__))

FILE_PATH = "sample_waveforms/CHMID_VDIV_1V.LSF"

numbers = []
with open(FILE_PATH, "rb") as f:
    header = ""
    while True:
        byte = f.read(1)
        header += byte.decode()
        if byte.decode() == "#":
            header += f.read(6).decode()
            break
    data = header.split(";")
    info = {}
    for field in data[:-2]:
        field_split = field.split(",")
        key = field_split[0]
        value = field_split[1]
        info[key] = value

    while True:
        byte_pair = f.read(2)

        if not byte_pair:
            break

        value = byte_pair[0] << 8 | byte_pair[1]

        numbers.append(value)

STEPS_PER_DIV = 3200*2
ADC_CENTER = 16384*2

memory_length = int(info["Memory Length"])
vertical_scale = float(info["Vertical Scale"])
vertical_position = float(info["Vertical Position"])
horizontal_scale = float(info["Horizontal Scale"])
horizontal_position = float(info["Horizontal Position"])
dt = float(info["Sampling Period"])
time = np.linspace(-2.4998e-06, 2.4998e-06, memory_length)

dv = vertical_scale/STEPS_PER_DIV
vcenter = int(vertical_position/dv) + ADC_CENTER
for i in range(len(numbers)):
    numbers[i] -= vcenter

voltage = np.asarray(numbers).astype(np.float32)*dv

print(f"Min Voltage: {min(voltage)}\t Max voltage: {max(voltage)}")
plt.plot(time, voltage)
plt.title("LSF waveform")
plt.ylabel("Voltaje (V)")
plt.xlabel("Tiempo (s)")
plt.grid(True)
plt.show()