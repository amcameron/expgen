"""Exposure: a combination of settings determining photographic exposure."""
from math import sqrt

# Sunny 16 rule says that at f/16 (EV +8), use shutter = 1/iso.
# E.g., 100 ISO (EV +5) and 1/100 s (EV +6.67). 8+5+7 = 20.
SUNNY = 20

class Exposure(object):
    # Exposure values are stored in EV
    _evShutter = 0
    _evAperture = 0
    _evIso = 0

    def __init__(self, shutter=0, aperture=0, iso=0):
        self._evShutter = shutter
        self._evAperture = aperture
        self._evIso = iso

    def __repr__(self):
        return ', '.join([ev_to_seconds(self._evShutter),
            ev_to_fnumber(self._evAperture),
            ev_to_iso(self._evIso)]) + \
                    ' ({0:.0f} EV)'.format(
                    self._evShutter + self._evAperture + self._evIso)

def ev_to_seconds(shutter):
    """Convert EV to string representing seconds or fractions of a second."""
    # Based on EV 0 = 1 s
    power = 2**abs(shutter)
    fmt = '%d s' if shutter <= 0 else '1/%d s'
    return fmt % power

def ev_to_fnumber(aperture):
    """Convert EV to string representing relative aperture (f-number)."""
    # Based on EV 0 = f/1.0
    fnum = sqrt(2)**aperture
    return 'f/{0:.1f}'.format(fnum)

def ev_to_iso(iso):
    """Convert EV to string representing sensitivity (ISO)."""
    # Assumes EV 0 = ISO 3
    return '{0:.0f} ISO'.format(3*2**iso)
