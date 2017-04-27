# coding: utf-8

import logging
import logging.config
import json

import luigi
from luigi import configuration, WrapperTask

from tasks.py2neo_proyectos import *
from tasks.py2neo_talentos import *
from tasks.preprocess_data import *

logging_conf = configuration.get_config().get("core", "logging_conf_file")
logging.config.fileConfig(logging_conf)
logger = logging.getLogger("fdc.pipeline")

class LoadNeo4j(luigi.WrapperTask):
    """
    Clase que crea la infraestructura de Neo4j para poder correr queries y modelos
    """

    conf = configuration.get_config()
    logging_path = conf.get('etl', 'logging_path')

    def requires(self):
        return LoadNeo4jTalentos(), LoadNeo4jProyectos()

    def run(self):

        # Al final:
        # Crear un archivo (vacío) para crear el log de carga de talentos a Neo4j       
        output_path = os.path.join(
            self.logging_path,
            "LoadedBothNeo4j"
                )
        open(output_path, "a").close()
    
    def output(self):
        """
        Output es un log file indicando que se cargaron correctamente ambas bases a Neo4j
        """
        output_path = os.path.join(
            self.logging_path,
            "LoadedBothNeo4j"
                )
        return luigi.LocalTarget(output_path)     

class LoadNeo4jTalentos(luigi.Task):
    """
    Carga Talentos a Neo4j con todas las relaciones (->) correctas
    """

    conf = configuration.get_config()
    logging_path = conf.get('etl', 'logging_path')

    def requires(self):
        return PreprocessTalentos()

    def run(self):
        # Necesario importar y correr archivo .py: base de talentos

        # exec(open("./py2neo_talentos.py").read())
        neodata = NeoTalentos()
        neodata.RunAll()

        # Al final:
        # Crear un archivo (vacío) para crear el log de carga de talentos a Neo4j       
        output_path = os.path.join(
            self.logging_path,
            "LoadedNeo4jTalentos"
                )
        open(output_path, "a").close()

    def output(self):
        """
        Output es un log file indicando que se cargó correctamente a Neo4j
        """
        output_path = os.path.join(
            self.logging_path,
            "LoadedNeo4jTalentos"
                )
        return luigi.LocalTarget(output_path) 

class LoadNeo4jProyectos(luigi.Task):
    """
    Carga Proyectos a Neo4j con todas las relaciones (->) correctas
    """

    conf = configuration.get_config()
    logging_path = conf.get('etl', 'logging_path')

    def requires(self):
        return PreprocessProyectos()

    def run(self):
        # Necesario importar y correr archivo .py: base de proyectos
        # exec(open("./py2neo_proyectos.py").read())
        neodata = NeoProyectos()
        neodata.RunAll()

        # Al final
        # Crear un archivo (vacío) para crear el log de carga de proyectos a Neo4j
        output_path = os.path.join(
            self.logging_path,
            "LoadedNeo4jProyectos"
                )
        open(output_path, "a").close()
    
    def output(self):
        """
        Output es un log file indicando que se cargó correctamente a Neo4j
        """
        output_path = os.path.join(
            self.logging_path,
            "LoadedNeo4jProyectos"
                )
        return luigi.LocalTarget(output_path) 


