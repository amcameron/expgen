"""Exposure: a combination of settings determining photographic exposure."""
from math import log, sqrt
import re

# Decimal matching pattern, e.g. "4", "2.", "35.5", "0.0051", etc.
_number_pattern = r'(\d+(?:\.\d*)?|\.\d+)'

def ev_to_seconds(evShutter):
    """Convert EV to string representing seconds or fractions of a second."""
    # Based on EV 0 = 1 s.  If brighter: more light, faster speed, higher EV.
    # Represent faster shutter speeds fractionally, like a camera.
    power = 2**abs(evShutter)
    seconds = '%d s' % power #if evShutter <= 0 else '1/%d s'
    if evShutter > 0:
        seconds = '1/' + seconds
    return seconds

# Pattern to match seconds or fractional seconds input.
_reSeconds = re.compile(
        _number_pattern + r' ?s' + # number, optional space, 's'
        r'|' + # or...
        r'1/' + _number_pattern + r' ?s') # '1/', number, optional space, 's'

def seconds_to_ev(seconds):
    """Convert string representing seconds to EV.

    Accepted formats are "#s", "# s", "1/#s", "1/# s"."""
    match = _reSeconds.match(seconds)
    if not match:
        raise ValueError("Unable to parse seconds value.", seconds)
    if seconds.startswith('1/'):
        sec = 1/float(match.group(2))
    else:
        sec = float(match.group(1))
    stops = -log(sec, 2)
    return stops

def ev_to_fnumber(evAperture):
    """Convert EV to string representing aperture (f-number)."""
    # Based on EV 0 = f/1.0
    fnum = sqrt(2)**evAperture
    return 'f/{0:.1f}'.format(fnum)

# Pattern to match aperture values.
_reFnumber = re.compile(r'f/?' + _number_pattern)

def fnumber_to_ev(aperture):
    """Convert string representing aperture (e.g. "f/1.4", "f2.8") to EV."""
    match = _reFnumber.match(aperture)
    if not match:
        raise ValueError("Unable to parse aperture value.", aperture)
    fnum = float(match.group(1))
    stops = log(fnum, sqrt(2))
    return stops

def ev_to_iso(evIso):
    """Convert EV to string representing sensitivity (ISO)."""
    # Assumes EV 0 = ISO 3
    return '{0:.0f} ISO'.format(3*2**-evIso)

# Pattern to match ISO values.
_reIso = re.compile(r'(\d+)(?: [iI][sS][oO])?')

def iso_to_ev(iso):
    """Convert string representing ISO (e.g. "200 ISO", "1600") to EV."""
    match = _reIso.match(iso)
    if not match:
        raise ValueError("Unable to parse ISO value.", iso)
    num = float(match.group(1))
    stops = -log(num/3, 2)
    return stops

def evs_to_exposure(evShutter, evAperture, evIso):
    """Convert EVs to string representing exposure."""
    sExp = ', '.join((
            ev_to_seconds(evShutter),
            ev_to_fnumber(evAperture),
            ev_to_iso(evIso)))
    return sExp + ' ({0:.0f} EV)'.format(evShutter + evAperture + evIso)

# Sunny 16 rule says that at f/16 (EV +8), use shutter = 1/iso.
# E.g., 100 ISO (EV +5) and 1/100 s (EV +6.67). 8+5+7 = 20.
SUNNY = fnumber_to_ev('f/16') + seconds_to_ev('1/100 s') + iso_to_ev('100 ISO')
