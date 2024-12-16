from ..api import DLNApi
from ..types import *


class SPIMaster(DLNApi):

    def get_c_pol(self, port: int = 0) -> int:
        port = ctypes.c_uint8(port)
        c_pol = ctypes.c_uint8()
        if api_result := DLN_RESULT(self._library.DlnSpiMasterGetCpol(self._handle, port, ctypes.byref(c_pol))):
            raise RuntimeError(str(api_result))
        return c_pol.value

    def set_c_pol(self, port: int = 0, c_pol: int = 0):
        port = ctypes.c_uint8(port)
        c_pol = ctypes.c_uint8(c_pol)
        if api_result := DLN_RESULT(self._library.DlnSpiMasterSetCpol(self._handle, port, c_pol)):
            raise RuntimeError(str(api_result))

    def get_spi_master_frequency(self, port: int = 0) -> int:
        frequency = ctypes.c_uint32()
        port = ctypes.c_uint8(port)
        if api_result := DLN_RESULT(
                self._library.DlnSpiMasterGetFrequency(self._handle, port, ctypes.byref(frequency))):
            raise RuntimeError(str(api_result))
        return frequency.value

    def set_spi_master_frequency(self, port: int = 0, frequency: int = 1000000):
        port = ctypes.c_uint8(port)
        frequency = ctypes.c_uint32(frequency)
        actual_frequency = ctypes.c_uint32()
        if api_result := DLN_RESULT(self._library.DlnSpiMasterSetFrequency(self._handle,
                                                                           port,
                                                                           frequency,
                                                                           ctypes.byref(actual_frequency))):
            raise RuntimeError(str(api_result))
        if frequency.value != actual_frequency.value:
            raise RuntimeError

    def enable(self, port: int = 0):
        port = ctypes.c_uint8(port)
        conflicts = ctypes.c_uint16()
        if api_result := DLN_RESULT(self._library.DlnSpiMasterEnable(self._handle, port, ctypes.byref(conflicts))):
            raise RuntimeError(str(api_result))
        if conflicts.value:
            raise RuntimeError(conflicts.value)

    def set_spi_master_frame_size(self, port: int = 0, frame_size: int = 16):
        port = ctypes.c_uint8(port)
        frame_size = ctypes.c_uint8(frame_size)
        if api_result := DLN_RESULT(self._library.DlnSpiMasterSetFrameSize(self._handle, port, frame_size)):
            raise RuntimeError(str(api_result))

    def set_spi_master_configuration(self, port: int = 0, frequency: int = 1000000, frame_size: int = 16) -> int:
        port = ctypes.c_uint8(port)
        frequency = ctypes.c_uint32(frequency)
        frame_size = ctypes.c_uint8(frame_size)
        actual_frequency = ctypes.c_uint32()
        if api_result := DLN_RESULT(self._library.DlnSpiMasterSetFrequency(self._handle,
                                                                           port,
                                                                           frequency,
                                                                           ctypes.byref(actual_frequency))):
            raise RuntimeError(str(api_result))
        if frequency.value != actual_frequency.value:
            raise RuntimeError
        conflicts = ctypes.c_uint16()
        if api_result := DLN_RESULT(self._library.DlnSpiMasterEnable(self._handle, port, ctypes.byref(conflicts))):
            raise RuntimeError(str(api_result))
        if conflicts.value:
            raise RuntimeError(conflicts.value)
        if api_result := DLN_RESULT(self._library.DlnSpiMasterSetFrameSize(self._handle, port, frame_size)):
            raise RuntimeError(str(api_result))
        return 0

    def get_spi_master_frame_size(self, port: int = 0) -> int:
        frame_size = ctypes.c_uint8()
        port = ctypes.c_uint8(port)
        if api_result := DLN_RESULT(
                self._library.DlnSpiMasterGetFrameSize(self._handle, port, ctypes.byref(frame_size))):
            raise RuntimeError(str(api_result))
        return frame_size.value

    def full_duplex_transaction(self, tx_data: bytearray, port: int = 0) -> bytearray:
        port = ctypes.c_uint8(port)
        tx_data = (ctypes.c_uint8 * len(tx_data))(*tx_data)
        rx_data = (ctypes.c_uint8 * len(tx_data))(*([0] * len(tx_data)))
        if len(tx_data) <= 8:
            dln_function = self._library.DlnSpiMasterReadWrite
        elif len(tx_data) <= 16:
            dln_function = self._library.DlnSpiMasterReadWrite16
        else:
            raise ValueError(len(tx_data))
        if api_result := DLN_RESULT(dln_function(self._handle, port, ctypes.c_uint16(len(tx_data)), tx_data, rx_data)):
            raise RuntimeError(str(api_result))
        return bytearray(rx_data)
