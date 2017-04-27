from py2neo import Graph


class BlTalentos():

    g = ''

    def __init__(self, host, password):
        self.g = Graph(host=host, password=password)

    def get_talentos_grados(self, grados):

        cond = self.__create_qry('p.grados', 'CONTAINS', grados, 'OR')
        qry = '''MATCH(p:Proyecto)
        WHERE {0}
        MATCH (p)-[:BUSCA_GRADO]->(g)<-[:EGRESADO_EN]-(t)
        RETURN t.nombre, t.grados'''.format(cond)
        q_estudio = self.g.run(qry).data()
        return q_estudio

    def get_talentos_especialidades(self, especialidades):

        cond = self.__create_qry('t.area', 'CONTAINS', especialidades, 'OR')
        qry = '''MATCH (t: Talento)
        WHERE {0}
        RETURN t.nombre, t.grados, t.area'''.format(cond)

        q_estudio = self.g.run(qry).data()
        return q_estudio

    def get_habilidades(self, habilidades):

        cond = self.__create_qry('t.habilidades', 'CONTAINS', habilidades, 'OR')
        qry = '''MATCH (t: Talento)
        WHERE {0}
        RETURN t.nombre, t.habilidades'''.format(cond)

        q_estudio = self.g.run(qry).data()
        return q_estudio


    def get_multiquery(self, grados, especialidades, habilidades):

        grd = self.__create_qry('t.grados', 'CONTAINS', grados, 'OR')
        esp = self.__create_qry('t.area', 'CONTAINS', especialidades, 'OR')
        hab = self.__create_qry('t.habilidades', 'CONTAINS', habilidades, 'OR')

        qry = '''MATCH (p:Proyecto)
        MATCH (t:Talento)
        WHERE {0}
        MATCH (p)-[:DESEA_EGRESADOS_DE]->(a:AlmaMater)<-[:EGRESADO_DE]-(t)
        WHERE {1} AND {2}
        RETURN t.nombre, t.nacimiento, t.lugar
        '''.format(grd, esp, hab)

        q_estudio = self.g.run(qry).data()
        return q_estudio


    def __create_qry(self, param, reserved, values, logic):
        list_values = values.split(',')
        preqry = [' {0} {1} "{2}" '.format(param, reserved, value) for value in list_values]
        return '({0})'.format('{0}'.format(logic).join(preqry))

'''
MATCH (p:Proyecto) WHERE p.id = '2'
MATCH (t:Talento)
WHERE t.grados CONTAINS 'Ciencia de Datos' OR t.grados CONTAINS 'Computacion' OR t.grados CONTAINS 'Matematicas'
MATCH (p)-[:DESEA_EGRESADOS_DE]->(a:AlmaMater {almaMater: 'ITAM'})<-[:EGRESADO_DE]-(t)
WHERE t.area CONTAINS 'Ciencias Sociales' AND t.idiomas CONTAINS 'Frances' AND t.departamento CONTAINS 'Planeacion'
RETURN t.nombre, t.nacimiento, t.lugar
'''