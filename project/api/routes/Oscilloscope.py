from flask import Blueprint
from controllers import Oscilloscope

from middleware.Async import asyncMiddleware

oscilloscope = Blueprint('oscilloscope', __name__)

@oscilloscope.route('oscilloscope/', methods=['POST'])
@asyncMiddleware
async def connect():
    return Oscilloscope.connect() 

@oscilloscope.route('oscilloscope/channel/<int:channel>', methods=['GET'])
@asyncMiddleware
async def show_channel(channel):
    return Oscilloscope.show_channel(channel)

@oscilloscope.route('oscilloscope/measurement/<int:channel>', methods=['GET'])
@asyncMiddleware
async def get_full_measurement(channel):
    return Oscilloscope.get_full_measurement(channel)

@oscilloscope.route('oscilloscope/vrange/<int:channel>', methods=['POST'])
@asyncMiddleware
async def set_channel_vrange(channel):
    return Oscilloscope.set_channel_vrange(channel)

@oscilloscope.route('oscilloscope/offset/<int:channel>', methods=['POST'])
@asyncMiddleware
async def set_channel_offset(channel):
    return Oscilloscope.set_channel_offset(channel)

@oscilloscope.route('oscilloscope/waveform/', methods=['GET'])
@asyncMiddleware
async def get_waveform_samples():
    return Oscilloscope.get_waveform_samples()