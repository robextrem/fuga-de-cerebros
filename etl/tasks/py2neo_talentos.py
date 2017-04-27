from py2neo import Graph


class NeoTalentos():
    file_loc = ''
    g = ''

    def __init__(self):
        self.file_location = "file:///talentos1.csv"
        self.g = Graph("http://neo4j:7474/db/data/")

    def RunAll(self):
        self.g.run("CREATE CONSTRAINT ON (t:Talento) ASSERT t.nombre IS UNIQUE")
        self.g.run("CREATE CONSTRAINT ON (u:Ubicacion) ASSERT u.lugar IS UNIQUE")
        self.g.run("CREATE CONSTRAINT ON (g:Grado) ASSERT g.grados IS UNIQUE")
        self.g.run("CREATE CONSTRAINT ON (h:Habilidad) ASSERT h.habilidades IS UNIQUE")
        self.g.run("CREATE CONSTRAINT ON (a:AlmaMater) ASSERT a.almaMater IS UNIQUE")
        self.g.run("CREATE CONSTRAINT ON (i:Idioma) ASSERT i.idiomas IS UNIQUE")

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            MERGE (t:Talento {id: row.ID, nombre: row.ID_NOMBRE})
            ON CREATE SET t.idiomas = row.IDI_NOMBRE, t.habilidades = row.HAB_HABILIDAD,
            t.almaMater = row.EDU_INST, t.area = row.EDU_AREA, t.grados = row.EDU_TITULO,
            t.posicion = row.TRA_POSICION, t.empresa = row.TRA_EMPRESA, t.departamento = row.TRA_AREA,
            t.sector = row.TRA_TIPO, t.industria = row.TRA_IND, t.nacimiento = row.INF_FECHNAC,
            t.lugar = row.INF_UBICACION
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            UNWIND split(row.IDI_NOMBRE, ",") AS idiomasId
            WITH DISTINCT idiomasId
            MERGE (i:Idioma {idiomas: idiomasId})
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            WITH split(row.IDI_NOMBRE, ",") AS idiomas, row.ID_NOMBRE AS Nombre
            UNWIND idiomas AS idiomasId
            WITH DISTINCT idiomasId, Nombre
            MATCH (t:Talento {nombre: Nombre})
            MATCH (i:Idioma {idiomas: idiomasId})
            MERGE (t)-[:FLUYENTES_EN]->(i)
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            UNWIND split(row.HAB_HABILIDAD, ",") AS habilidadesId
            WITH DISTINCT habilidadesId
            MERGE (h:Habilidad {habilidades: habilidadesId})
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            WITH split(row.HAB_HABILIDAD, ",") AS habilidades, row.ID AS proyectoNo
            UNWIND habilidades AS habilidadesId
            WITH DISTINCT habilidadesId, proyectoNo
            MATCH (t:Talento {id: proyectoNo})
            MATCH (h:Habilidad {habilidades: habilidadesId})
            MERGE (t)-[:TIENE_HABILIDADES]->(h)

            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            UNWIND split(row.EDU_INST, ",") AS almaMaters
            WITH DISTINCT almaMaters
            MERGE (:AlmaMater {almaMater: almaMaters})
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            WITH split(row.EDU_INST, ",") AS almas, row.ID AS No
            UNWIND almas AS almasId
            WITH DISTINCT almasId, No
            MATCH (t:Talento {id: No})
            MATCH (a:AlmaMater {almaMater: almasId})
            MERGE (t)-[:EGRESADO_DE]->(a)
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            UNWIND split(row.EDU_TITULO, ",") AS Grado
            WITH DISTINCT Grado
            MERGE (:Grado {grados: Grado})
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            WITH split(row.EDU_TITULO, ",") AS grados, row.ID AS proyectoNo
            UNWIND grados AS gradosId
            WITH DISTINCT gradosId, proyectoNo
            MATCH (t:Talento {id: proyectoNo})
            MATCH (g:Grado {grados: gradosId})
            MERGE (t)-[:EGRESADO_EN]->(g)
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            MERGE (u:Ubicacion {lugar: row.INF_UBICACION})
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            MATCH (t:Talento {id: row.ID})
            MATCH (u:Ubicacion {lugar: row.INF_UBICACION})
            MERGE (t)-[:UBICADO_EN]->(u)
            """ % self.file_location)
