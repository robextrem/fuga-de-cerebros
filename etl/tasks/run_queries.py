# coding: utf-8

import ast
import logging
import logging.config
import json
import os
import pickle
import time

import luigi
from luigi import configuration

from py2neo import Graph

import tasks.general_functions.py as gen_func
from tasks.load_neo4j_data.py import LoadNeo4j
# from utils.load_elasticsearch_data.py import LoadElasticsearch

logging_conf = configuration.get_config().get("core", "logging_conf_file")
logging.config.fileConfig(logging_conf)
logger = logging.getLogger("fdc.pipeline")


class RunQueries(luigi.Task):
    """
    Corre queries a Neo4j para obtener match del proyecto
    """

    def requires(self):
        """
        Necesita que ambas bases de datos estén ya unidas y limpias
        """
        return LoadNeo4j()

    def run(self):
        """
        Correr, evaluar y cargar queries que se harán a la base, según lo requerido:
            * Especialidades (grados)
            * Experiencia Profesional
            * Habilidades
            * Todas las anteriores
        """
        g = Graph(password="pa$$w0rd")

        q_estudio = g.run("""
        MATCH (p:Proyecto {id: '2'} )
        WHERE (p.grados CONTAINS 'Matematicas' OR p.grados CONTAINS 'Economia')
        MATCH (p)-[:BUSCA_GRADO]->(g)<-[:EGRESADO_EN]-(t)
        RETURN t.nombre, g.grados
        """).data()

        print(q_estudio)

        q_especialidad = g.run("""
        MATCH (t: Talento)
        WHERE (t.area CONTAINS 'Antropologia')
        RETURN t.nombre, t.grados, t.area
        """).data()

        print(q_especialidad)

        q_sector = g.run("""
        MATCH (t: Talento)
        WHERE (t.sector CONTAINS 'Privada')
        RETURN t.nombre, t.sector
        """).data()

        print(q_sector)

        q_institucion = g.run("""
        MATCH (t: Talento)
        WHERE (t.empresa CONTAINS 'Secretaria')
        RETURN t.nombre, t.empresa
        """).data()

        print(q_institucion)

        q_cargo = g.run("""
        MATCH (t: Talento)
        WHERE (t.posicion CONTAINS 'Investigador')
        RETURN t.nombre, t.posicion
        """).data()

        print(q_cargo)

        q_habilidades = g.run("""
        MATCH (t: Talento)
        WHERE (t.habilidades CONTAINS 'R')
        RETURN t.nombre, t.habilidades
        """).data()

        print(q_habilidades)

        q_super = g.run("""
        MATCH (p:Proyecto) WHERE p.id = '2'
        MATCH (t:Talento)
        WHERE t.grados CONTAINS 'Ciencia de Datos' OR t.grados CONTAINS 'Computacion' OR t.grados CONTAINS 'Matematicas'
        MATCH (p)-[:DESEA_EGRESADOS_DE]->(a:AlmaMater {almaMater: 'ITAM'})<-[:EGRESADO_DE]-(t)
        WHERE t.area CONTAINS 'Ciencias Sociales' AND t.idiomas CONTAINS 'Frances' AND t.departamento CONTAINS 'Planeacion'
        RETURN t.nombre, t.nacimiento, t.lugar
        """).data()

        print(q_super)

        # Output? Regresa 4 listas. Las imprimiremos a pantalla porque nos sabemos en qué formato lo necesitan en end product

        # Al final
        # Crear un archivo (vacío) para que sea el output
        output_path = os.path.join(
            self.logging_path,
            "Neo4JQueriesRun"
                )
        open(output_path, "a").close()

    def output(self):
        """
        Output es un log file
        """
        output_path
        return luigi.LocalTarget(output_path)

