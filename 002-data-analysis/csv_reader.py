import matplotlib.pyplot as plt
import pandas as pd
import os
os.chdir(os.path.dirname(__file__))

FILE_PATH = "sample_waveforms/CHMID_VDIV_1V.CSV"

data = pd.read_csv(FILE_PATH, skiprows=16)
time = data.iloc[:, 0].tolist()
voltage = data.iloc[:, 1].tolist()
print(f"Min Voltage: {min(voltage)}\t Max voltage: {max(voltage)}")
plt.plot(time, voltage)
plt.grid(True)
plt.title("CSV Waveform")
plt.show()
