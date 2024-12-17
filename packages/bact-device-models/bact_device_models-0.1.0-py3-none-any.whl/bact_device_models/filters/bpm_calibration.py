from dataclasses import dataclass


@dataclass
class BPMCalibrationPlane:
    """scale and offset for the bpm (both in millimeter)

    Todo:
        check if calc functionality should be singled out to a filter

    """

    #: from bits to -10/10 volt, assuming that bits are signed
    #: bact2 used 10/(2**15)
    bit2val: float
    #: from volt to meter ... 1.0 for most bpm's
    scale: float
    #: offset to correct meter for
    offset: float
    active: bool

    def __init__(self, *, bit2val=10 / (2 ** 15), scale=1e-3, offset=0.0, active=True):
        self.bit2val = bit2val
        self.scale = scale
        self.offset = offset
        self.active = active

    def to_bits(self, pos: float) -> int:
        """convert position to bit representation

        Todo:
            clipping etc...
        """
        bitv = (pos + self.offset) / self.scale / self.bit2val
        return int(round(bitv))

    def to_pos(self, bits: int) -> float:
        """
        Todo:
            cross check with bact2 that the arithmetic is consistent
        """
        return (bits * self.bit2val) * self.scale - self.offset

    def to_rms(self, bits: int) -> float:
        """
        Todo:
            check that the scale is positive ?
        """
        return abs((bits * self.bit2val) * self.scale)

    def inverse(self, bits: int) -> float:
        """bluesky / ophyd convention"""
        return self.to_pos(bits)

    def forward(self, pos: float) -> int:
        """bluesky / ophyd convention"""
        return self.to_bits(pos)


@dataclass
class BPMCalibration:
    x: BPMCalibrationPlane
    y: BPMCalibrationPlane
