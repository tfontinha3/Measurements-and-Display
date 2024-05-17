import os
from dotenv import load_dotenv
from flask import Flask, make_response

load_dotenv()

app = Flask(__name__)

hostname = os.getenv("HOSTNAME")
port = os.getenv("PORT")

#Routes and Controllers
from routes.Oscilloscope import oscilloscope

# Routes registers
app.register_blueprint(oscilloscope, url_prefix='/api')

@app.route('/api/loopback/<string:msg>')
def loopback(msg):
    if msg=="PING":
         msg = "PONG"
    elif msg != "":
        msg = "msg received:"+ msg
    else:
        msg = "No message Sent"

    return make_response({"Message": msg}, 200)

# Listening server
if __name__ == "__main__":
    app.run(host=hostname, port=port, debug=True)
