from flask import render_template, request, Flask
import json
import os
from config import Config

direccion_actual = os.path.dirname(os.path.abspath(__file__))
json_dir = os.path.join(direccion_actual, "static", "json", "morse_code.json")


def ej_11_app():
    """Crea y configura la aplicación Flask"""

    app = Flask(__name__, static_folder=Config.STATIC_FOLDER,
                template_folder=Config.TEMPLATE_FOLDER)

    app.config.from_object(Config)

    with open(json_dir, 'r', encoding="utf-8") as data:
        datos = json.load(data)

    @app.route('/encode/<string:keyword>')
    def titulo(keyword):
        keyword1 = keyword.upper()
        texto_codif = ""
        for letra in keyword1:
            if letra in datos["letters"]:
                texto_codif += datos["letters"][letra] + "+"

        return {'Mensaje en codigo morse': texto_codif}, 200

    return app
