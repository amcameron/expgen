#!/usr/bin/env python
from optparse import OptionParser
import random
import exposure

LUCK_SCALE_FACTOR = 2

def synthesize(exp, luck, focal=6):
    random.seed()
    evTarget = exp + random.uniform(-LUCK_SCALE_FACTOR*luck,
            LUCK_SCALE_FACTOR*luck)
    evIso = random.uniform(5, 9.1)
    evShutter = focal + random.uniform(-LUCK_SCALE_FACTOR*luck,
            LUCK_SCALE_FACTOR*luck)
    evAperture = evTarget - evIso - evShutter
    return exposure.Exposure(iso=evIso, shutter=evShutter, aperture=evAperture)

if __name__ == "__main__":
    usage = "usage: %prog [options]"
    parser = OptionParser()
    parser.add_option(
            '-e', '--exposure',
            action='store', type='int', dest='exp', default=exposure.SUNNY,
            help='Exposure value in EV (Sunny 16: ~{0} EV)'.format(
                exposure.SUNNY))
    parser.add_option(
            '-l', '--luck',
            action='store', type='float', dest='luck', default=1,
            help='How lucky are you feeling? (variability)')
    parser.add_option(
            '-f', '--focal',
            action='store', type='int', dest='focal', default=50,
            help='Lens focal length (for handheld limit)')
    (options, args) = parser.parse_args()

    result = synthesize(options.exp, options.luck)
    while result._evAperture > 11 and result._evAperture >= 1:
        result = synthesize(options.exp, options.luck)
    print result
