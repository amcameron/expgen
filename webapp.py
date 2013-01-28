#!/usr/bin/env python
from flask import Flask, render_template, request
from expgen import MIN_EXPOSURE, MAX_EXPOSURE, MIN_ISO, MAX_ISO, \
        MIN_APERTURE, MAX_APERTURE, MIN_SHUTTER, MAX_SHUTTER, \
        synthesize
from exposure import ev_to_seconds, ev_to_fnumber, ev_to_iso
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html',
                expMin=MIN_EXPOSURE, expMax=MAX_EXPOSURE,
                shutterMin=MIN_SHUTTER, shutterMax=MAX_SHUTTER,
                apertureMin=MIN_APERTURE, apertureMax=MAX_APERTURE,
                isoMin=MIN_ISO, isoMax=MAX_ISO)
    elif request.method == 'POST':
        evTarget = float(request.form['target'])
        evS, evA, evI = synthesize(float(evTarget), 1, '50')
        return render_template('form.html',
                expMin=MIN_EXPOSURE, expMax=MAX_EXPOSURE,
                shutterMin=MIN_SHUTTER, shutterMax=MAX_SHUTTER,
                apertureMin=MIN_APERTURE, apertureMax=MAX_APERTURE,
                isoMin=MIN_ISO, isoMax=MAX_ISO,
                target=evTarget, shutter=evS, aperture=evA, iso=evI,
                sShutter=ev_to_seconds(evS),
                sAperture=ev_to_fnumber(evA),
                sIso=ev_to_iso(evI))
    else:
        return "oops"

@app.route('/generate', methods=['POST'])
def generate():
    print request
    return

if __name__ == '__main__':
    app.run(debug=True)