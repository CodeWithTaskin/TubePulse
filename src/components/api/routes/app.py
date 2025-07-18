import os
import sys

from flask import Blueprint, request, make_response,send_file


from src.exception import MyException
from src.components.engine.tubepluse_engine import TubePulseEngine

api = Blueprint('api', __name__)

engine: TubePulseEngine = TubePulseEngine()

@api.route('/predict_with_timestamps', methods=['POST'])
def predict_with_timestamps():
    try:
        comments = request.json
        result = engine.predict(comments=comments)
        response = make_response(result, 200)
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response
    except Exception as e:
        raise MyException(e, sys) from e

@api.route('/generate_chart', methods=['POST'])
def generate_chart():
    try:
        count = request.json
        result = engine.pie_chart(count)
        response = make_response(send_file(result, mimetype='image/png', download_name='plot.png'), 200)
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response
    except Exception as e:
        raise MyException(e, sys) from e

@api.route('/generate_wordcloud', methods=['POST'])
def generate_wordcloud():
    try:
        comment = request.json
        result = engine.word_cloud(comment=comment)
        response = make_response(send_file(result, mimetype='image/png', download_name='plot.png'), 200)
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response
    except Exception as e:
        raise MyException(e, sys) from e