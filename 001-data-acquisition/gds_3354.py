import pyvisa
from pyvisa.resources.messagebased import MessageBasedResource
from pyvisa import ResourceManager
from typing_extensions import Literal
import logging
import time

logger = logging.getLogger("GDS3354")


def list_resources() -> None:
    print(ResourceManager().list_resources())


class GDS3354:
    resource_name: str
    resource_manager: ResourceManager
    instrument: MessageBasedResource
    save_format: Literal["csv", "lsf"]

    def __init__(self, resource_name: str) -> None:
        self.resource_name = resource_name
        self.resource_manager = ResourceManager()

        self.open_connection()
        self.save_format = "lsf"

    def open_connection(self) -> None:
        self.instrument = self.resource_manager.open_resource(
            self.resource_name)

    def close_connection(self) -> None:
        self.instrument.close()
        logger.info("Connection closed")

    def set_timeout(self, timeout: float) -> None:
        self.instrument.timeout = timeout

    def ping(self, delay: float = 1.0) -> bool:
        try:
            response = self.instrument.query("*IDN?", delay)
            return response == "GW,GDS-3354,EL112308,V1.10\n"
        except pyvisa.errors.VisaIOError:
            pass

        return False

    def flush(self) -> int:
        """ Returns bytes flushed """
        counter = 0
        while True:
            try:
                self.instrument.read_bytes(1)
                counter += 1
            except pyvisa.errors.VisaIOError:
                break
        logger.info(f"{counter} bytes flushed")
        return counter

    def save_waveform(self, channel: int, path: str, *, format: Literal["csv", "lsf"]) -> None:
        """ Path formats:
            - Disk:/Folder/filename.CSV
            - Disk:/Folder/filename.LSF
            - USB:/filename.CSV
            - USB:/filename.LSF

            Currently saving inside a folder in USB causes DSO to freeze. """

        if format != self.save_format:
            if format == "csv":
                self.instrument.write(":SAVe:WAVEform:SPREADSheet")
            elif format == "lsf":
                self.instrument.write(":SAVe:WAVEform:INTERNal")
            else:
                raise ValueError("Invalid format")

            self.save_format = format

        self.instrument.write(f':SAVe:WAVEform CH{channel}, "{path}"')

    def get_raw_bytes(self) -> bytes:
        raw_bytes = b""

        while True:
            try:
                raw_bytes += self.instrument.read_bytes(1)
            except pyvisa.errors.VisaIOError:
                break

        return raw_bytes

    def get_waveform(self, channel: int, delay: float = 1.0, *, update_wave: bool = True) -> bytes:
        self.flush()
        if update_wave:
            self.instrument.write(":SINGLE")

        while self.instrument.query(f':ACQuire{channel}:STATe?', delay) != '1\n':
            time.sleep(delay)
            pass

        self.instrument.write(f":ACQuire{channel}:MEMory?")

        header = bytes()
        while True:
            byte = self.instrument.read_bytes(1)
            header += byte
            if byte.decode() == "#":
                header += self.instrument.read_bytes(6)
                break

        waveform = bytes()
        for i in range(25000):
            try:
                byte = self.instrument.read_bytes(2)
            except pyvisa.errors.VisaIOError:
                break

            waveform += GDS3354._convert_hex(byte)

        final_byte = self.instrument.read_bytes(1)
        if final_byte != b"\n":
            raise Exception("Read not successful")

        if update_wave:
            self.instrument.write(":RUN")
        return header + waveform

    @classmethod
    def _convert_hex(cls, num: bytes) -> bytes:
        # TODO: Find out relation between offset and vpos on DSO.
        int_value = (32768+256*int.from_bytes(num, byteorder="big")) & 0xFFFF
        return int_value.to_bytes(2, byteorder="big")

    def __del__(self) -> None:
        self.close_connection()
