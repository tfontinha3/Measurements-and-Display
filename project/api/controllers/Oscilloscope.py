from flask import jsonify, request

from models.Oscilloscope import Oscilloscope

instrument = Oscilloscope("192.168.1.10")

def connect():
    response = instrument.connect()
    idn = response.body
    return jsonify({"Oscilloscope Model": idn}), 200

def get_waveform():
    response = instrument.get_waveform()

def set_probe(ratio: int):
    response = instrument.set_probe(ratio)
    return jsonify({"message:", f"Probe ratio set to {ratio}."})

def select_channel(channel: int, state: bool):
    if state:
        response = instrument.show_channel(channel)
        return jsonify({"message": f"Showing channel {response.body}."})

    response = instrument.hide_channel(channel)
    return jsonify({"message": f"Showing channel {response.body}."})

def get_full_measurement(channel: int):
    item = dict(request.get_json())["item"]
    response = instrument.get_full_measurement(channel, item)
    return jsonify(response.body)
    
def get_waveform_samples():
    response = instrument.get_waveform_samples()
    return jsonify(response.body)

def set_channel_vrange(channel: int):
    range = dict(request.get_json())["range"]
    response = instrument.set_channel_vrange(channel, range)
    return jsonify(response.body)

def set_channel_offset(channel: int):
    offset = dict(request.get_json())["offset"]
    response = instrument.set_channel_offset(channel, offset)
    return jsonify(response.body)