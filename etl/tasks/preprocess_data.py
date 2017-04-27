# coding: utf-8

import os
from os import path
import logging
import logging.config
import json

import luigi
from luigi import configuration, WrapperTask

from tasks.prepdata_talentos import *
from tasks.prepdata_proyectos import *

logging_conf = configuration.get_config().get("core", "logging_conf_file")
custom_cf = path.join(os.getcwd(), logging_conf)
logging.config.fileConfig(custom_cf, disable_existing_loggers=True)
logger = logging.getLogger("fdc_pipeline")


class PreprocessData(luigi.Task):
    """
    Primer paso del pipeline. Recibe los metadatos, que se encuentran en:
    /src/pot/data/
    Preprocesa texto para homologacion, convierte a jsons y aplanada datos
    para regresar csvs listos para cargar a Neo4j
    """

    conf = configuration.get_config()
    logging_path = conf.get('etl', 'logging_path')

    def requires(self):
        """
        Primer paso del pipeline, no requiere mas que la existencia de archivos "sucios"
        Los pasos base que se realizan son:

        * Mergear distintos orígenes de datos
        * Quitar acentos
        * Todo lowercase
        * Poner guiones bajos a conjuntos de palabras (e.g. Ciencia de Datos -> Ciencia_de_Datos)

        Crear una estructura de tabla para quitar duplicados más fácilmente
        input: JSON con toda la información de un talento
        output: renglones "planos". Puede tener valores separados por comas
        en las columnas, ejemplo:
        empresa        | requisitos
        ---------------|------------------------------------------------
        empresita inc. | lic. economía, lic. relaciones internacionales

        No es necesario deduplicar porque existen restricciones en la carga a Neo4j para asegurar unicidad
        No es necesario homologar pues los datos de universidades, estudios y skills provienen de listas
        """
        # Carpeta en la que se encuentra todo el raw data
        raw_data_location = "/src/data"

        if self.trigger_source == 'talentos':
            return PreprocessTalentos()
        else:
            return PreprocessProyectos()

    def run(self):

        # Crear un archivo (vacío) para crear el log de limpieza de tablas
        output_path = "%s_data_preprocessed.log" % (
            self.logging_path
        )
        open(output_path, "a").close()

    def output(self):
        output_path = "%s_data_preprocessed.log" % (
            self.logging_path
        )
        return luigi.LocalTarget(output_path)


class PreprocessTalentos(luigi.Task):
    """
    input: tsv obtenido directamente de la fuente de datos
    output: csv listo para carga en neo4j
    """
    conf = configuration.get_config()
    logging_path = conf.get('etl', 'logging_path')
    raw_data_location = conf.get('etl', 'raw_data_location')
    out_data_location = conf.get('etl', 'out_data_location')
    data_talentos = path.join(out_data_location, 'talentos1.csv')

    def run(self):
        # Lee tsv de metadatos
        ed_data=pd.read_csv("%s/educacion.tsv" % self.raw_data_location, sep='\t',na_values=None, keep_default_na=False)
        ha_data=pd.read_csv("%s/habilidades.tsv" % self.raw_data_location, sep='\t',na_values=None, keep_default_na=False)
        la_data=pd.read_csv("%s/idioma.tsv" % self.raw_data_location, sep='\t',na_values=None, keep_default_na=False)
        ot_data=pd.read_csv("%s/otros.tsv" % self.raw_data_location, sep='\t',na_values=None, keep_default_na=False)
        pe_data=pd.read_csv("%s/person.tsv" % self.raw_data_location, sep='\t',na_values=None, keep_default_na=False)
        tr_data=pd.read_csv("%s/trabajo.tsv" % self.raw_data_location, sep='\t',na_values=None, keep_default_na=False)
        pem_data = ot_data.merge(pe_data, on='uid')

        # Hace match entre tsv y json, utilizando las clases definidas en prepdata-talentos
        talentos_data = []
        for pem in pem_data.itertuples():
            data = talento(pem.uid,pem.nombre,pem.ubicacion,pem.id)
            match_la = la_data['uid'] == data.uid
            match_ed = ed_data['uid'] == data.uid
            match_ha = ha_data['uid'] == data.uid
            match_tr = tr_data['uid'] == data.uid
            data.idiomas = [idiomas(idioma = lad.idioma, IDI_NIVEL_SP=lad.IDI_NIVEL_SP,
                                     IDI_NIVEL_TE=lad.IDI_NIVEL_TE, IDI_NIVEL_TR=lad.IDI_NIVEL_TR,
                                     IDI_NIVEL_WR=lad.IDI_NIVEL_WR ) for lad in la_data[match_la].itertuples()]
            data.educacion = [educacion(institucion = edu.institucion, area = edu.area_estudio, titulo = edu.titulo) for edu in ed_data[match_ed].itertuples()]
            data.habilidades = [habilidades(habilidades=hab.habilidades) for hab in ha_data[match_ha].itertuples() ]
            data.trabajos = [trabajos(titulo_posicion=tra.posicion,empresa=tra.empresa,
                                      area=tra.area, tipo=tra.tipo, voluntariado = tra.voluntariado,
                                      industria = tra.industria ) for tra in tr_data[match_tr].itertuples()]
            talentos_data.append(json.dumps(data, cls=MyEncoder))

        # Tiene como input el json output anterior. Define nombres técnicos y aplana el json
        jlArray = []
        for item in jsonlines.Reader(talentos_data).iter():
            preproc = {}
            preproc[u'ID'] = item[u'id']
            preproc[u'uid'] = item[u'uid']
            preproc[u'INF_UBICACION']=item[u'ubicacion']
            preproc[u'ID_NOMBRE']=item[u'nombre']
            preproc[u'IDI_NOMBRE'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'IDI_NOMBRE']) for cur in item[u'idiomas'] if cur != np.nan ]))
            preproc[u'IDI_NIVEL_SP'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'IDI_NIVEL_SP']) for cur in item[u'idiomas'] if cur != '']))
            preproc[u'IDI_NIVEL_WR'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'IDI_NIVEL_WR']) for cur in item[u'idiomas'] if cur != '']))
            preproc[u'IDI_NIVEL_TR'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'IDI_NIVEL_TR']) for cur in item[u'idiomas'] if cur != '']))
            preproc[u'IDI_NIVEL_TE'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'IDI_NIVEL_TE']) for cur in item[u'idiomas'] if cur != '']))
            preproc[u'EDU_INST'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'EDU_INST']) for cur in item['educacion'] if cur != 'NaN']))
            preproc[u'EDU_TITULO'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'EDU_TITULO']) for cur in item['educacion'] if cur != 'NaN']))
            preproc[u'EDU_AREA'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'EDU_AREA']) for cur in item['educacion'] if cur != 'NaN']))
            preproc['HAB_HABILIDAD'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'HAB_HABILIDAD']) for cur in item['habilidades'] if cur != 'NaN']))
            preproc[u'TRA_EMPRESA'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'TRA_EMPRESA']) for cur in item[u'trabajos'] if cur != 'NaN']))
            preproc[u'TRA_AREA'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'TRA_AREA']) for cur in item[u'trabajos'] if cur != 'NaN']))
            preproc[u'TRA_POSICION'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'TRA_POSICION']) for cur in item[u'trabajos'] if cur != 'NaN']))
            preproc[u'TRA_TIPO'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'TRA_TIPO']) for cur in item[u'trabajos'] if cur != 'NaN']))
            preproc[u'TRA_IND'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'TRA_IND']) for cur in item[u'trabajos'] if cur != 'NaN']))
            jlArray.append(preproc)

        dftalentos = pd.DataFrame(jlArray)
        # Escribe a carpeta import archivo listo para carga en Neo4j
        # TODO: para que todo corra desde cero, cambiar talentos1 -> talentos
        # Esto reescribirá las bases de juguete de Adrián
        dftalentos.to_csv(self.data_talentos)

        # Al final:
        # Crear un archivo (vacío) para crear el log de carga de talentos a Neo4j
        output_path = os.path.join(
            self.logging_path,
            "PreprocessedTalentos"
                )
        open(output_path, "a").close()

    def output(self):
        """
        Output es un log file indicando que se cargó correctamente a Neo4j
        """
        output_path = os.path.join(
            self.logging_path,
            "PreprocessedTalentos"
                )
        return luigi.LocalTarget(output_path)


class PreprocessProyectos(luigi.Task):
    """
    input: tsv obtenido directamente de la fuente de datos
    output: csv listo para carga en neo4j
    """
    conf = configuration.get_config()
    logging_path = conf.get('etl', 'logging_path')
    raw_data_location = conf.get('etl', 'raw_data_location')
    out_data_location = conf.get('etl', 'out_data_location')
    data_proyectos = path.join(out_data_location, 'proyectos1.csv')

    def run(self):
        # Lee tsv de metadatos
        proy_info_data=pd.read_csv("%s/proyecto_info.tsv" % self.raw_data_location, sep='\t',na_values=None, keep_default_na=False)
        proy_talentos_data=pd.read_csv("%s/proyecto_talentos.tsv" % self.raw_data_location, sep='\t',na_values=None, keep_default_na=False)

        # Hace match entre tsv y json, utilizando las clases definidas en prepdata-proyectos
        proyectos_data = []
        for i in proy_info_data.itertuples():
            data = proyecto(i.uid, i.numero, i.pais,i.nombre,
                            i.giro, i.descproyecto,i.objetivo,i.proyecto,i.entregable,
                            i.ubicacion, i.inicio, i.fin, i.pago)
            match_talentos = proy_talentos_data['uid'] == data.uid
            data.talentos = [talentos(grados=ta.grados, experiencia=ta.experiencia, funciones=ta.funciones,
                                      idiomas=ta.idiomas, almamater=ta.almamater, habilidades=ta.habilidades)
                             for ta in proy_talentos_data[match_talentos].itertuples()]
            proyectos_data.append(json.dumps(data, cls=MyEncoder))

        # Tiene como input el json output anterior. Define nombres técnicos y aplana el json
        jlArray = []
        for item in jsonlines.Reader(proyectos_data).iter():
            preproc = {}
            preproc[u'PRO_ID'] = item[u'numero']
            preproc[u'uid'] = item[u'uid']
            preproc[u'PRO_PAIS'] = item[u'pais']
            preproc[u'PRO_NOMBRE'] = item[u'nombre']
            preproc[u'PRO_PROY'] = item[u'proyecto']
            preproc[u'PRO_DESC'] = item[u'descproyecto']
            preproc[u'PRO_OBJ'] = item[u'objetivo']
            preproc[u'PRO_ENTR'] = item[u'entregable']
            preproc[u'PRO_UBIC'] = item[u'ubicacion']
            preproc[u'PRO_IND'] = item[u'giro']
            preproc[u'PRO_TITULO'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'PRO_TITULO']) for cur in item['talentos'] if cur != 'NaN']))
            preproc[u'PRO_EXP'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'PRO_EXP']) for cur in item['talentos'] if cur != 'NaN']))
            preproc[u'PRO_FUNCIONES'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'PRO_FUNCIONES']) for cur in item['talentos'] if cur != 'NaN']))
            preproc[u'PRO_IDIOMAS'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'PRO_IDIOMAS']) for cur in item['talentos'] if cur != 'NaN']))
            preproc[u'PRO_INST'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'PRO_INST']) for cur in item['talentos'] if cur != 'NaN']))
            preproc[u'PRO_HABILIDADES'] = parse_doc_list_plain(','.join([u'{0}'.format(cur[u'PRO_HABILIDADES']) for cur in item['talentos'] if cur != 'NaN']))
            jlArray.append(preproc)

        dfproyectos = pd.DataFrame(jlArray)
        # Escribe a carpeta import archivo listo para carga en Neo4j
        # TODO: para que todo corra desde cero, cambiar proyectos1 -> proyectos
        # Esto reescribirá las bases de juguete de Adrián
        dfproyectos.to_csv(self.data_proyectos)

        # Al final:
        # Crear un archivo (vacío) para crear el log de carga de talentos a Neo4j
        output_path = os.path.join(
            self.logging_path,
            "PreprocessedProyectos"
                )
        open(output_path, "a").close()

    def output(self):
        """
        Output es un log file indicando que se cargó correctamente a Neo4j
        """
        output_path = os.path.join(
            self.logging_path,
            "PreprocessedProyectos"
                )
        return luigi.LocalTarget(output_path)










