from gds_3354 import list_resources, GDS3354

list_resources()
RESOURCE_NAME = 'ASRL/dev/ttyACM0::INSTR'

dso = GDS3354(RESOURCE_NAME)
dso.ping()
dso.flush()

waveform = dso.get_waveform(1, update_wave=False)
len(waveform)

dso.instrument.write(":SINGLE")
dso.instrument.query(':ACQuire1:STATe?', 1)
dso.instrument.write(":ACQuire1:MEMory?")
raw_bytes = dso.get_raw_bytes()
raw_bytes[:448]
len(raw_bytes)

f = open("waveform.LSF", "wb")
f.write(waveform)
f.close()

dso.save_waveform(1, f"USB:/waveform.CSV", format="csv")
dso.save_waveform(1, f"USB:/waveform.LSF", format="lsf")

dso.close_connection()
