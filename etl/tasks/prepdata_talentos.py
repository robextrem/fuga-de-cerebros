#from __future__ import absolute_import, division, print_function, unicode_literals
import pandas as pd
import json
import jsonlines
import re
import numpy as np

class persona(object):
    uid=""
    nombre=""
    ubicacion=""
    id=""


class idiomas(object):
    uid=""
    idioma=""
    IDI_NIVEL_SP=""
    IDI_NIVEL_WR=""
    IDI_NIVEL_TR=""
    IDI_NIVEL_TE=""

    def __init__(self, idioma, IDI_NIVEL_SP,IDI_NIVEL_WR,IDI_NIVEL_TR,IDI_NIVEL_TE):
        self.idioma = idioma
        self.IDI_NIVEL_SP=IDI_NIVEL_SP
        self.IDI_NIVEL_WR=IDI_NIVEL_WR
        self.IDI_NIVEL_TR=IDI_NIVEL_TR
        self.IDI_NIVEL_TE=IDI_NIVEL_TE



    def __json__(self):
        return {'IDI_NOMBRE':self.idioma, 'IDI_NIVEL_SP': self.IDI_NIVEL_SP,
                'IDI_NIVEL_WR':self.IDI_NIVEL_WR, 'IDI_NIVEL_TR':self.IDI_NIVEL_TR,
                'IDI_NIVEL_TE':self.IDI_NIVEL_TE }

class habilidades(object):
    ##tipo=""
    habilidades=""

    def __init__(self, habilidades):
        ##self.tipo = tipo
        self.habilidades = habilidades

    def __json__(self):
        return {'HAB_HABILIDAD':self.habilidades}


class educacion(object):
    uid=""
    institucion=""
    area=""
    fecha_inicio=""
    fecha_fin=""
    titulo=""
    extra_curriculares=""

    def __init__(self,institucion, area,  titulo):        #fecha_inicio, fecha_fin,
        self.institucion=institucion
        self.area=area
        #self.fecha_inicio=fecha_inicio
        #self.fecha_fin=fecha_fin
        self.titulo=titulo
        #self.extra_curriculares=extra_curriculares

    def __json__(self):
        return {'EDU_INST':self.institucion, 'EDU_AREA':self.area, 'EDU_TITULO':self.titulo}

class trabajos(object):
    uid=""
    titulo_posicion=""
    resumen=""
    fecha_inicio=""
    fecha_fin=""
    actual=""
    empresa=""
    area=""
    tipo=""
    industria=""
    voluntariado=""

    def __init__(self, titulo_posicion, empresa, area, tipo, industria, voluntariado):
        self.titulo_posicion=titulo_posicion
        #self.resumen=resumen
        #self.fecha_inicio=fecha_inicio
        #self.fecha_fin=fecha_fin
        #self.actual=actual
        self.empresa=empresa
        self.area=area
        self.tipo=tipo
        self.industria=industria
        #self.voluntariado=voluntariado

    def __json__(self):
        return {'TRA_POSICION': self.titulo_posicion, 'TRA_EMPRESA': self.empresa,
                'TRA_AREA':self.area, 'TRA_TIPO':self.tipo, 'TRA_IND':self.industria}

class talento(object):
    uid=''
    nombre=''
    ubicacion=''
    id=''
    trabajos=[]
    cursos = []
    educacion = []
    certificaciones = []
    habilidades = []
    idiomas = []
    patentes = []
    publicaciones = []

    def __init__(self, uid, nombre, ubicacion, id):
        self.uid = uid
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.id = np.uint32(id).item()

    def __json__(self):
        return {'uid': self.uid, 'nombre': self.nombre, 'ubicacion':self.ubicacion ,'id':self.id, 'trabajos':self.trabajos,
                'educacion':self.educacion, 'habilidades':self.habilidades,
               'idiomas':self.idiomas}


class MyEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that leverages an object's `__json__()` method,
    if available, to obtain its default JSON representation.

    """
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return json.JSONEncoder.default(self, obj)

def parse_doc_list_plain(doc):
    '''Preprocesing method, this code dont remove the character with graphic accent.'''
    red = r'[^,a-z\u00E7\u00F1\u00E1\u00E9\u00ED\u00F3\u00FA\u00E0\u00E8\u00EC\u00F2\u00F9\u00E4\u00EB\u00EF\u00F6\u00FC\u00E2\u00EA\u00EE\u00F4\u00FB ]'

    ##sandbox
    art_vect = re.sub(r' +',' ', re.sub(red,'',re.sub(r'\u201c',' ',re.sub('\n',' ',doc).lower()))) # Remove the most of the symbols.
    art_vect = re.sub(',+',',',art_vect) #
    art_vect = re.sub(', ',',',art_vect) # ,\s\+   remove space after comma, it could be improved
    art_vect = re.sub('^,','',art_vect) # ,\s\+   remove space after comma, it could be improved
    art_vect = re.sub(r' ','_',art_vect) # Replace the space by underscore.
    art_vect = re.sub(r',$','',art_vect)  # Remove the last comma character. just in case.
    return art_vect
