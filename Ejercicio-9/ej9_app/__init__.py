from flask import render_template, request, Flask, jsonify
from config import Config

def ej_9_app():
    """Crea y configura la aplicación Flask"""
    
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    
    app.config.from_object(Config)

    def formatear_dni(dni):
        dni = dni.replace(".", "").replace("-", "")
        if not dni.isdigit() or len(dni) != 8:
            return None
        return int(dni)

    @app.route('/formatted/<string:dni>')
    def titulo(dni):
        dni_formateado = formatear_dni(dni)
        if dni_formateado is None:
            return {'Error': 'Ha ocurrido un error'}, 400
        return {"formatted_dni": dni_formateado}, 200

    return app
