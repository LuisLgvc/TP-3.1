from flask import render_template, request, Flask
from datetime import date, datetime
from config import Config


def ej_10_app():
    """Crea y configura la aplicación Flask"""

    app = Flask(__name__, static_folder=Config.STATIC_FOLDER,
                template_folder=Config.TEMPLATE_FOLDER)

    app.config.from_object(Config)

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
    def titulo():
        firstname = format_name(request.args.get('firstname'))
        lastname = format_lastname(request.args.get('lastname'))
        age = format_dob(request.args.get('dob'))
        dni = format_dni(request.args.get('dni'))
        if dni is None:
            return {'error': 'El DNI no es válido'}, 400
        if age <= 0:
            return {'error': 'La fecha de nacimiento no es valida'}, 400

        return {'firstname': firstname, 'lastname': lastname, 'age': age, 'dni': dni}, 200

    return app
