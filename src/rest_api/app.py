from flask import Flask
from flask_restful import reqparse, Resource, Api
from api.talento.talentos import BlTalentos
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
neoserver='neo4j'

@app.route('/')
def project_name():
    return '{"project_name":"Proyecto Fuga de Cerebros"}'


@app.route('/api')
def api_version():
    return '{"version":"Version 0.99 - 2016"}'


class Talentos_Grados(Resource):

    g = ''

    def __init__(self):
        self.g = BlTalentos(host=neoserver, password="password")

    def get(self, lista_grados):

        grados = self.g.get_talentos_grados(lista_grados)
        return grados


class Talentos_Especialidades(Resource):

    g = ''

    def __init__(self):
        self.g = BlTalentos(host=neoserver, password="password")

    def get(self, lista_especialidades ):
        grados = self.g.get_talentos_especialidades(lista_especialidades)
        return grados


class Talentos_Habilidades(Resource):

    g = ''

    def __init__(self):
        self.g = BlTalentos(host=neoserver, password="password")

    def get(self, lista_habilidades):
        grados = self.g.get_habilidades(lista_habilidades)
        return grados



class Talentos_Multiparm(Resource):

    g = ''

    def __init__(self):
        self.g = BlTalentos(host=neoserver, password="password")

    def get(self, lista_grados, lista_especialidades, lista_habilidades):
        grados = self.g.get_multiquery(lista_grados, lista_especialidades, lista_habilidades)
        return grados



api.add_resource(Talentos_Grados, '/api/talentos/grados/<string:lista_grados>')
api.add_resource(Talentos_Especialidades, '/api/talentos/especialidades/<string:lista_especialidades>')
api.add_resource(Talentos_Habilidades, '/api/talentos/habilidades/<string:lista_habilidades>')
api.add_resource(Talentos_Multiparm, '/api/talentos/grados/<string:lista_grados>/especialidades/<string:lista_especialidades>/habilidades/<string:lista_habilidades>')



#/talentos/grados/{}
#/talentos/especialidades/{}
#/talentos/habilidades/{}
#/talentos/grado/{}/especialidades/{}/habilidades


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

