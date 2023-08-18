from flask import render_template, request, Flask, jsonify
from datetime import datetime
import json
import os
from config import Config
from .static.Clases.clases import Stack

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

        return jsonify({"formatted_word": formatted_word}), 200

    # Ejercicio 9
    def formatear_dni(dni):
        dni = dni.replace(".", "").replace("-", "")
        if dni.isdigit() and dni[0] != "0" and len(dni) == 8:
            return int(dni)
        return None

    @app.route('/formatted/<string:dni>')
    def dar_formato_dni(dni):
        dni_formateado = formatear_dni(dni)
        if dni_formateado is not None:
            return jsonify({"formatted_dni": dni_formateado}), 200
        return jsonify({'Error': 'Ha ocurrido un error'}), 400

    # Ejercicio 10
    def format_firstname(firstname):
        return firstname.capitalize()

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
        if dni.isdigit() and dni[0] != "0" and len(dni) == 8:
            return int(dni)
        return None

    @app.route('/format')
    def persona_dat():
        firstname = format_firstname(request.args.get('firstname'))
        lastname = format_lastname(request.args.get('lastname'))
        age = format_dob(request.args.get('dob'))
        dni = format_dni(request.args.get('dni'))
        if dni is None:
            return jsonify({'error': 'El DNI no es válido'}), 400
        if age <= 0:
            return jsonify({'error': 'La fecha de nacimiento no es valida'}), 400

        return jsonify({'firstname': firstname, 'lastname': lastname, 'age': age, 'dni': dni}), 200

    # Apertura del json para ejercicio 11 y 12
    with open(json_dir, 'r', encoding="utf-8") as data:
        datos = json.load(data)

    # Ejercicio 11
    @app.route('/encode/<string:keyword>')
    def codifica_morse(keyword):
        txt_mayus = keyword.upper()
        reemplazado = txt_mayus.replace("+", " ")
        texto_codif = ""
        if len(reemplazado) < 101:
            for letra in reemplazado:
                if letra in datos["letters"]:
                    texto_codif += datos["letters"][letra] + "+"
            return jsonify({'Mensaje en codigo morse': texto_codif}), 200
        else:
            return jsonify({'error': 'Las palabras clave exceden los 100 caracteres'}), 400

    # Ejercicio 12
    @app.route('/decode/<string:keyword>')
    def decodifica_morse(keyword):
        morse_split = keyword.split("+")
        texto_decod = ""
        for cod in morse_split:
            for letra, codigo_m in datos["letters"].items():
                if cod == codigo_m:
                    texto_decod += letra
        return jsonify({'Mensaje decodificado': texto_decod.upper()}), 200

    # Ejercicio 13
    @app.route('/convert/binary/<string:num>')
    def conversor_binario(num):
        decimal = 0
        potencia = len(num) - 1
        if num.isdigit() and all(i == "0" or i == "1" for i in num):
            for n in num:
                decimal += int(n) * (2 ** potencia)
                potencia -= 1
            return jsonify({'Numero decimal': decimal}), 200
        else:
            return jsonify({'Error': 'Solo debe ingresar un numero binario'}), 400

    # Ejercicio 14
    def balance(expresion):
        stack = Stack()
        limiters = {')': '(', '}': '{', ']': '['}

        for character in expresion:
            if character in '([{':
                stack.push(character)
            elif character in ')]}':
                if stack.is_empty() or stack.top() != limiters[character]:
                    return False
                stack.pop()
        return stack.is_empty()

    @app.route('/balance/<string:inputt>')
    def ver_balance(inputt):
        result_balance = balance(inputt)
        if result_balance:
            return jsonify({'balanced': result_balance}), 200
        else:
            return jsonify({'balanced': result_balance}), 200

    return app
