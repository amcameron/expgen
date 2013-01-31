from collections import namedtuple
from fractions import Fraction
from exposure import *

ExpTime = namedtuple("ExpTime", "ev secs")
known_times = []
known_times.append(ExpTime(ev=0, secs=1))
known_times.append(ExpTime(ev=1, secs=1./2))

def test_ev_to_seconds():
    for ev, seconds in known_times:
        assert Fraction(seconds) == Fraction(ev_to_seconds(ev).rstrip(' s'))

def test_seconds_to_ev():
    for ev, seconds in known_times:
        strSecFraction = str(Fraction(seconds)) + " s"
        assert ev == seconds_to_ev(strSecFraction)

def test_ev_to_fnumber():
    raise NotImplementedError()

def test_fnumber_to_ev():
    raise NotImplementedError()

def test_ev_to_iso():
    raise NotImplementedError()

def test_iso_to_ev():
    raise NotImplementedError()
