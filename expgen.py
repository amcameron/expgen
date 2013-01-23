#!/usr/bin/env python
from optparse import OptionParser
import random
import exposure

LUCK_SCALE_FACTOR = 2
MIN_ISO = exposure.iso_to_ev('1600 ISO')
MAX_ISO = exposure.iso_to_ev('100 ISO')
MIN_APERTURE = exposure.fnumber_to_ev('f/1.4')
MAX_APERTURE = exposure.fnumber_to_ev('f/22.0')

def synthesize(exp, luck, focal):
    # TODO: use bounds during synthesis so we can't generate invalid values.
    random.seed()
    evFocal = exposure.seconds_to_ev('1/' + focal + 's')
    evShutter = evFocal + random.uniform(
            -LUCK_SCALE_FACTOR*luck, LUCK_SCALE_FACTOR*luck)
    evTarget = exp + random.uniform(
            -LUCK_SCALE_FACTOR*luck, LUCK_SCALE_FACTOR*luck)
    # evTarget = evShutter + evAperture + evIso
    # evTarget - evShutter = evAperture + evIso
    remainder = evTarget - evShutter
    isoLower = max(MIN_ISO, remainder - MAX_APERTURE)
    isoUpper = min(MAX_ISO, remainder - MIN_APERTURE)
    evIso = random.uniform(isoLower, isoUpper)
    evAperture = evTarget - evIso - evShutter
    return evShutter, evAperture, evIso

if __name__ == "__main__":
    usage = "usage: %prog [options]"
    parser = OptionParser()
    parser.add_option(
            '-e', '--exposure',
            action='store', type='int', dest='exp', default=exposure.SUNNY,
            help='Exposure value in EV (Sunny 16: ~{0:.0f} EV)'.format(
                exposure.SUNNY))
    parser.add_option(
            '-l', '--luck',
            action='store', type='float', dest='luck', default=1,
            help='How lucky are you feeling? (variability)')
    parser.add_option(
            '-f', '--focal',
            action='store', type='string', dest='focal', default='50',
            help='Lens focal length (for handheld limit)')
    (options, args) = parser.parse_args()

    evShutter, evAperture, evIso = synthesize(
            options.exp, options.luck, options.focal)
    print exposure.evs_to_exposure(evShutter, evAperture, evIso)
