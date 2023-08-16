from flask import render_template, request, Flask
from datetime import datetime
import json
import os
from config import Config

direccion_actual = os.path.dirname(os.path.abspath(__file__))
json_dir = os.path.join(direccion_actual, "static", "json", "morse_code.json")


def ejercicios_td_app():
    """Crea y configura la aplicación Flask"""

    app = Flask(__name__, static_folder=Config.STATIC_FOLDER,
                template_folder=Config.TEMPLATE_FOLDER)

    app.config.from_object(Config)

    # Ejercicio 8
    @app.route('/title/<string:word>')
    def formato_titulo(word):
        formatted_word = word.capitalize()

        return ({"formatted_word": formatted_word}, 200)
    
    # Ejercicio 10
    def format_name(name):
        return name.capitalize()

    def format_lastname(lastname):
        return lastname.capitalize()

    def format_dob(dob):
        dob = datetime.strptime(dob, '%Y-%m-%d')
        hoy = datetime.now()
        age = hoy.year - dob.year - \
            ((hoy.month, hoy.day) < (dob.month, dob.day))
        return age

    def format_dni(dni):
        dni = dni.replace(".", "").replace("-", "")
        if not dni.isdigit() or len(dni) != 8:
            return None
        return int(dni)

    @app.route('/format')
    def persona_dat():
        firstname = format_name(request.args.get('firstname'))
        lastname = format_lastname(request.args.get('lastname'))
        age = format_dob(request.args.get('dob'))
        dni = format_dni(request.args.get('dni'))
        if dni is None:
            return {'error': 'El DNI no es válido'}, 400
        if age <= 0:
            return {'error': 'La fecha de nacimiento no es valida'}, 400

        return {'firstname': firstname, 'lastname': lastname, 'age': age, 'dni': dni}, 200

    # Ejercicio 11
    with open(json_dir, 'r', encoding="utf-8") as data:
        datos = json.load(data)

    @app.route('/encode/<string:keyword>')
    def codifica_morse(keyword):
        keyword1 = keyword.upper()
        texto_codif = ""
        for letra in keyword1:
            if letra in datos["letters"]:
                texto_codif += datos["letters"][letra] + "+"

        return {'Mensaje en codigo morse': texto_codif}, 200

    return app