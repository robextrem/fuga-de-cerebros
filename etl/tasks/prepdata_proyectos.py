#from __future__ import absolute_import, division, print_function, unicode_literals
import pandas as pd
import json
import jsonlines
import re
import numpy as np


class talentos(object):
    uid=""
    grados=""
    experiencia=""
    funciones=""
    idiomas=""
    almamater=""
    habilidades=""

    def __init__(self, grados, experiencia, funciones, idiomas, almamater, habilidades):
        self.grados=grados
        self.experiencia=experiencia
        self.funciones=funciones
        self.idiomas=idiomas
        self.almamater=almamater
        self.habilidades=habilidades

    def __json__(self):
        return {'PRO_TITULO':self.grados, 'PRO_EXP':self.experiencia, 'PRO_FUNCIONES':self.funciones,'PRO_IDIOMAS':self.idiomas,
               'PRO_INST':self.almamater, 'PRO_HABILIDADES':self.habilidades}

class proyecto(object):
    uid=""
    numero=""
    pais=""
    nombre=""
    giro=""
    proyecto=""
    descproyecto=""
    objetivo=""
    entregable=""
    ubicacion=""
    inicio=""
    fin=""
    pago=""
    talentos=[]

    def __init__(self, uid, numero, pais, nombre, giro, proyecto, descproyecto, objetivo, entregable, ubicacion, inicio, fin, pago):
        self.uid = uid
        self.numero = np.uint(numero).item()
        self.pais = pais
        self.nombre = nombre
        self.giro = giro
        self.proyecto = proyecto
        self.descproyecto = descproyecto
        self.objetivo = objetivo
        self.entregable = entregable
        self.ubicacion = ubicacion
        self.inicio = inicio
        self.fin = fin
        self.pago = np.float32(pago).item()

    def __json__(self):
        return {'uid': self.uid, 'numero': self.numero, 'pais':self.pais ,'nombre':self.nombre,
                'giro':self.giro, 'proyecto':self.proyecto, 'descproyecto':self.descproyecto,
                'objetivo':self.objetivo,'entregable':self.entregable, 'ubicacion':self.ubicacion,'inicio':self.inicio,
                'fin': self.fin, 'pago': self.pago, 'talentos': self.talentos}


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

    art_vect = re.sub(r' +', ' ', re.sub(red,'',re.sub(r'\u201c',' ',re.sub('\n',' ',doc).lower()))) # Remove the most of the symbols.
    art_vect = re.sub(',+', ',', art_vect) #
    art_vect = re.sub(', ', ',', art_vect) # ,\s\+   remove space after comma, it could be improved
    art_vect = re.sub('^,', '', art_vect) # ,\s\+   remove space after comma, it could be improved
    art_vect = re.sub(r' ', '_', art_vect) # Replace the space by underscore.
    art_vect = re.sub(r',$', '', art_vect)  # Remove the last comma character. just in case.
    return art_vect


