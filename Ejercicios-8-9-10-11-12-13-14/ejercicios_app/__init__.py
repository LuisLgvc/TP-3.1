from flask import render_template, request, Flask, jsonify
from datetime import datetime
import json
import os
from config import Config

direccion_actual = os.path.dirname(os.path.abspath(__file__))
json_dir = os.path.join(direccion_actual, "static", "json", "morse_code.json")


def ejercicios_td_app():
    """Crea y configura la aplicación Flask junto con los endpoints y funciones necesarias"""

    app = Flask(__name__, static_folder=Config.STATIC_FOLDER,
                template_folder=Config.TEMPLATE_FOLDER)

    app.config.from_object(Config)

    # Ejercicio 8
    @app.route('/title/<string:word>')
    def formato_titulo(word):
        formatted_word = word.capitalize()

        return ({"formatted_word": formatted_word}, 200)

    # Ejercicio 9
    def formatear_dni(dni):
        dni = dni.replace(".", "").replace("-", "")
        if not dni.isdigit() or len(dni) != 8:
            return None
        return int(dni)

    @app.route('/formatted/<string:dni>')
    def dar_formato_dni(dni):
        dni_formateado = formatear_dni(dni)
        if dni_formateado is None:
            return {'Error': 'Ha ocurrido un error'}, 400
        return {"formatted_dni": dni_formateado}, 200

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

    # Apertura del json para ejercicio 11 y 12
    with open(json_dir, 'r', encoding="utf-8") as data:
        datos = json.load(data)

    #Ejercicio 11
    @app.route('/encode/<string:keyword>')
    def codifica_morse(keyword):
        txt_mayus = keyword.upper()
        texto_codif = ""
        for letra in txt_mayus:
            if letra in datos["letters"]:
                texto_codif += datos["letters"][letra] + "+"

        return {'Mensaje en codigo morse': texto_codif}, 200

    # Ejercicio 12
    @app.route('/decode/<string:keyword>')
    def decodifica_morse(keyword):
        morse_split = keyword.split("+")
        texto_decod = ""
        for cod in morse_split:
            for letra, codigo_m in datos["letters"].items():
                if cod == codigo_m:
                    texto_decod += letra
        return {'Mensaje decodificado': texto_decod.capitalize()}, 200
    
    # Ejercicio 13

    # Ejercicio 14

    return app
