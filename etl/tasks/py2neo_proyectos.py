from py2neo import Graph


class NeoProyectos():
    file_location = ''
    g = ''

    def __init__(self):
        self.file_location = "file:///proyectos1.csv"
        self.g = Graph("http://neo4j:7474/db/data/")

    def RunAll(self):
        self.g.run("CREATE CONSTRAINT ON (x:Empresa) ASSERT x.nombre IS UNIQUE")
        self.g.run("CREATE CONSTRAINT ON (p:Proyecto) ASSERT p.id IS UNIQUE")
        self.g.run("CREATE CONSTRAINT ON (u:Ubicacion) ASSERT u.lugar IS UNIQUE")
        self.g.run("CREATE CONSTRAINT ON (g:Grado) ASSERT g.grados IS UNIQUE")
        self.g.run("CREATE CONSTRAINT ON (e:Experiencia) ASSERT e.experiencia IS UNIQUE")
        self.g.run("CREATE CONSTRAINT ON (h:Habilidad) ASSERT h.habilidades IS UNIQUE")
        self.g.run("CREATE CONSTRAINT ON (a:AlmaMater) ASSERT a.almaMater IS UNIQUE")
        self.g.run("CREATE CONSTRAINT ON (i:Idioma) ASSERT i.idiomas IS UNIQUE")

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            MERGE (:Empresa {id: row.PRO_ID, nombre: row.PRO_NOMBRE, giro: row.PRO_IND})
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            MERGE (p:Proyecto {id: row.PRO_ID})
            ON CREATE SET p.proyecto = row.PRO_PROY, p.descripcion = row.PRO_DESC,
            p.objetivoP = row.PRO_OBJ, p.entregable = row.PRO_ENTR, p.lugar = row.PRO_UBIC,
            p.grados = row.PRO_TITULO, p.experiencia = row.PRO_EXP, p.funciones = row.PRO_FUNCIONES,
            p.idiomas = row.PRO_IDIOMAS, p.almaMater = row.PRO_INST, p.habilidades = row.PRO_HABILIDADES,
            p.pago = row.PRO_PAGO
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            MATCH (p:Proyecto {id: row.PRO_ID})
            MATCH (e:Empresa {nombre: row.PRO_NOMBRE})
            MERGE (e)-[:TIENE_PROYECTO]->(p)
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            MERGE (u:Ubicacion {lugar: row.PRO_UBIC})
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            MATCH (p:Proyecto {id: row.PRO_ID})
            MATCH (u:Ubicacion {lugar: row.PRO_UBIC})
            MERGE (p)-[:UBICADO_EN]->(u)
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            UNWIND split(row.PRO_TITULO, ",") AS Grado
            WITH DISTINCT Grado
            MERGE (:Grado {grados: Grado})
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            WITH split(row.PRO_TITULO, ",") AS grados, row.PRO_ID AS proyectoNo
            UNWIND grados AS gradosId
            WITH DISTINCT gradosId, proyectoNo
            MATCH (p:Proyecto {id: proyectoNo})
            MATCH (g:Grado {grados: gradosId})
            MERGE (p)-[:BUSCA_GRADO]->(g)
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            UNWIND split(row.PRO_EXP, ",") AS experienciaId
            WITH DISTINCT experienciaId
            MERGE (:Experiencia {experiencia: experienciaId})
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            WITH split(row.PRO_EXP, ",") AS experiencia, row.PRO_ID AS proyectoNo
            UNWIND experiencia AS experienciaId
            WITH DISTINCT experienciaId, proyectoNo
            MATCH (p:Proyecto {id: proyectoNo})
            MATCH (e:Experiencia {experiencia: experienciaId})
            MERGE (p)-[:BUSCA_EXPERIENCIA]->(e)
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            UNWIND split(row.PRO_HABILIDADES, ",") AS habilidadesId
            WITH DISTINCT habilidadesId
            MERGE (h:Habilidad {habilidades: habilidadesId})
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            WITH split(row.PRO_HABILIDADES, ",") AS habilidades, row.PRO_ID AS proyectoNo
            UNWIND habilidades AS habilidadesId
            WITH DISTINCT habilidadesId, proyectoNo
            MATCH (p:Proyecto {id: proyectoNo})
            MATCH (h:Habilidad {habilidades: habilidadesId})
            MERGE (p)-[:BUSCA_HABILIDAD]->(h)
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            UNWIND split(row.PRO_INST, ",") AS almaMaters
            WITH DISTINCT almaMaters
            MERGE (:AlmaMater {almaMater: almaMaters})
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            WITH split(row.PRO_INST, ",") AS almas, row.PRO_ID AS No
            UNWIND almas AS almasId
            WITH DISTINCT almasId, No
            MATCH (p:Proyecto {id: No})
            MATCH (a:AlmaMater {almaMater: almasId})
            MERGE (p)-[:DESEA_EGRESADOS_DE]->(a)
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            UNWIND split(row.PRO_IDIOMAS, ",") AS idiomasId
            WITH DISTINCT idiomasId
            MERGE (i:Idioma {idiomas: idiomasId})
            """ % self.file_location)

        self.g.run("""
            LOAD CSV WITH HEADERS FROM '%s' AS row
            WITH split(row.PRO_IDIOMAS, ",") AS idiomas, row.PRO_ID AS No
            UNWIND idiomas AS idiomasId
            WITH DISTINCT idiomasId, No
            MATCH (p:Proyecto {id: No})
            MATCH (i:Idioma {idiomas: idiomasId})
            MERGE (p)-[:FLUYENTES_EN]->(i)
            """ % self.file_location)
