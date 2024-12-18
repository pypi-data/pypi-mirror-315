"""Module for all device drivers."""
import typing as t

from zhinst.qcodes.driver.devices.base import ZIBaseInstrument
from zhinst.qcodes.driver.devices.hdawg import HDAWG
from zhinst.qcodes.driver.devices.pqsc import PQSC
from zhinst.qcodes.driver.devices.shfqa import SHFQA
from zhinst.qcodes.driver.devices.shfqc import SHFQC
from zhinst.qcodes.driver.devices.shfsg import SHFSG
from zhinst.qcodes.driver.devices.uhfli import UHFLI
from zhinst.qcodes.driver.devices.uhfqa import UHFQA

DeviceType = t.Union[ZIBaseInstrument, HDAWG, PQSC, SHFQA, SHFQC, SHFSG, UHFLI, UHFQA]

DEVICE_CLASS_BY_MODEL = {
    "SHFQA": SHFQA,
    "SHFQC": SHFQC,
    "SHFSG": SHFSG,
    "HDAWG": HDAWG,
    "PQSC": PQSC,
    "UHFQA": UHFQA,
    "UHFLI": UHFLI,
}

__all__ = [
    "DeviceType",
    "DEVICE_CLASS_BY_MODEL",
    "ZIBaseInstrument",
    "HDAWG",
    "PQSC",
    "SHFQA",
    "SHFQC",
    "SHFSG",
    "UHFLI",
    "UHFQA",
]
