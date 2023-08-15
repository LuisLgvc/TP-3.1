from flask import render_template, request, Flask, jsonify
from config import Config


def ej_8_app():
    """Crea y configura la aplicación Flask"""

    app = Flask(__name__, static_folder=Config.STATIC_FOLDER,
                template_folder=Config.TEMPLATE_FOLDER)

    app.config.from_object(Config)

    @app.route('/title/<string:word>')
    def titulo(word):
        formatted_word = word.capitalize()

        return ({"formatted_word": formatted_word}, 200)

    return app
