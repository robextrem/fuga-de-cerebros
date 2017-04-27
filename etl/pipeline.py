#z coding: utf-8

# Correr como: python pipeline.py FDCPipeline --local-scheduler

import logging
from logging import config
import luigi
import luigi.postgres
from luigi import configuration

from tasks.load_neo4j_data import *

logging_conf = configuration.get_config().get("core", "logging_conf_file")
logging.config.fileConfig(logging_conf)
logger = logging.getLogger('fdc_pipeline')


class FDCPipeline(luigi.WrapperTask):
    """
    Wrapper Task que ejecuta todo el pipeline
    """

    def requires(self):
        yield LoadNeo4j()

if __name__ == "__main__":
    luigi.run()
