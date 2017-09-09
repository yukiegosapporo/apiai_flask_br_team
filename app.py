from flask import Flask, request, jsonify
import colorlog
import json

logger = colorlog.getLogger()
logger.setLevel(colorlog.colorlog.logging.INFO)
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    }))
logger.addHandler(handler)

app = Flask(__name__)


@app.route("/", methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    resp = jsonify(process_request(req))
    return resp


def process_request(request_data):
    if "result" not in request_data:
        return {}
    logger.info(json.dumps(request_data["result"], indent=4, sort_keys=True))
    nba_team = request_data['result']['parameters']['team']
    message = "There you go :) \n http://bleacherreport.com/" + nba_team
    return {
            "data": {"slack": {"text": message}},
        }

if __name__ == "__main__":
    app.run()