from gds_3354 import GDS3354, list_resources
import logging
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=(
                        logging.FileHandler("waveform.log"),
                        logging.StreamHandler())
                    )
logger = logging.getLogger(__file__.split("\\")[-1])
pyvisa_logger = logging.getLogger("pyvisa")
pyvisa_logger.setLevel(logging.INFO)

list_resources()
RESOURCE_NAME = 'ASRL/dev/ttyACM0::INSTR'
dso = GDS3354(RESOURCE_NAME)

for i in range(10):
    if dso.ping():
        logger.info("Initial ping successful")
        break

try:
    for j in range(10):
        logger.info(f"Batch number: {j}")
        for i in range(1000):
            logger.info(f"Saving waveform: {i}")
            wf = dso.get_waveform(1)
            file_path = f"CH_MID_1V/{j:0{2}d}/"
            file_name = f"CH1_pulse_{i:0{3}d}.LSF"
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            with open(file_path+file_name, "wb") as f:
                f.write(wf)
                f.close()
except Exception as e:
    logger.error(e)
finally:
    dso.close_connection()
