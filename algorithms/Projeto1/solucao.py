# -*- coding: utf-8 -*-

"""
/***************************************************************************
 ProgramacaoAplicadaGrupo4
                                 A QGIS plugin
 Solução do Grupo 4
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-03-25
        copyright            : (C) 2024 by Grupo 4
        email                : alexprocopio323@ime.eb.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Grupo 4'
__date__ = '2024-03-25'
__copyright__ = '(C) 2024 by Grupo 4'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterDistance,
                       QgsFields,
                       QgsField,
                       QgsFeature,
                       QgsWkbTypes)

from qgis import processing
from PyQt5.QtCore import QVariant

class Projeto1Solucao(QgsProcessingAlgorithm):

    VDESLOC = 'VDESLOC'
    BUFF_VDESLOC = 'BUFF_VDESLOC'
    VEG = 'VEG'
    MAGUA = 'MAGUA'
    DREN = 'DREN'
    BUFF_DREN = 'BUFF_DREN'
    BUFF_CIL = 'BUFF_CIL'
    ED = 'ED'
    VAZIO = 'VAZIO'
    TP = 'TP'
    TOLERANCE = 'TOLERANCE'
    MDT = 'MDT'
    OUTPUT = 'OUTPUT'
    OUTPUT2 = 'OUTPUT2'


    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CartaTrafegabilidade()

    #Esse é o nome que eu vou puxar no python
    def name(self):
        return 'cartatrafegabilidade'

    #Esse é o nome que vai aparecer na interface
    def displayName(self):
        return self.tr('Carta de Trafegabilidade')

    #Esse é o nome do grupo no qual vai ficar o nome
    def group(self):
        return self.tr('Aula')

    #Esse será uma string fixa 
    def groupId(self):

        return 'examplescripts'

    #Esse é o que aparece do lado 
    def shortHelpString(self):
        return self.tr("Example algorithm short description")

    def initAlgorithm(self, config=None):
        #Parameter Feature Source recebe elementos, isso me deixa aplicar só em algumas feições
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.VDESLOC,
                self.tr('Via de Deslocamento'),
                [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.VEG,
                self.tr('Vegetação'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.MAGUA,
                self.tr('Massa Água'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.DREN,
                self.tr('Drenagem'),
                [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.ED,
                self.tr('Edifícios'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.VAZIO,
                self.tr('Área Vazia'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter (
            QgsProcessingParameterDistance (
                self.BUFF_VDESLOC,
                self.tr('Buffer Trecho de deslocamento' ),
                parentParameterName =self.VDESLOC ,
                minValue=0,
                defaultValue =1.0
            ))
        self.addParameter (
            QgsProcessingParameterDistance (
                self.BUFF_CIL,
                self.tr('Buffer Ciliar' ),
                parentParameterName =self.VEG ,
                minValue=0,
                defaultValue =1.0
            ))
        self.addParameter (
            QgsProcessingParameterDistance (
                self.BUFF_DREN,
                self.tr('Buffer Drenagem' ),
                parentParameterName =self.DREN ,
                minValue=0,
                defaultValue =1.0
            ))


        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT2,
                self.tr('Output2 layer')
            )
        )
    #context -> carregar cadama de saída, feedback -> comunicar com a interface do QGIS
    def processAlgorithm(self, parameters, context, feedback):

        VDESLOC = self.parameterAsSource(parameters,
                                         self.VDESLOC,
                                         context)
        BUFF_VDESLOC = self.parameterAsSource(parameters,
                                              self.BUFF_VDESLOC,
                                              context)
        VEG = self.parameterAsVectorLayer(parameters,
                                     self.VEG,
                                     context)
        
        MAGUA = self.parameterAsVectorLayer(parameters,
                                       self.MAGUA,
                                       context)
        DREN = self.parameterAsVectorLayer(parameters,
                                      self.DREN,
                                      context)
        buff_dren_value = self.parameterAsDouble(parameters, self.BUFF_DREN, context)

        buff_cil_value = self.parameterAsDouble(parameters, self.BUFF_CIL, context)

        ED = self.parameterAsSource(parameters,
                                    self.ED,
                                    context)
        VAZIO = self.parameterAsSource(parameters,
                                       self.VAZIO,
                                       context)

        #Ele recebe uma fonte
        your_fields = QgsFields()
        your_fields.append(QgsField('id', QVariant.String))
        your_fields.append(QgsField('Trafeg', QVariant.Int))

        if MAGUA is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        #É assim que você prepara a saída
        #a saida do processo é o feature sink
        #Publica uma saída
        (sink_line, dest_id) = self.parameterAsSink(
    parameters,
    self.OUTPUT,
    context,
    your_fields,
    VDESLOC.wkbType(),
    VDESLOC.sourceCrs()
)
        (sink_pol, dest_id2) = self.parameterAsSink(
    parameters,
    self.OUTPUT2,
    context,
    your_fields,
    MAGUA.wkbType(),
    MAGUA.sourceCrs()
)

        #Asim eu me comunico com o usuário
        feedback.pushInfo('CRS is {}'.format(MAGUA.sourceCrs().authid()))

        if sink_line is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        total = 100.0 / MAGUA.featureCount() if MAGUA.featureCount() else 0
        features = MAGUA.getFeatures()
        #O enumerate vai gerar um dicionário com as features e o número que corresponde a elas enumerando-as , dess forma, enumerate(features) devolte uma tupla 
        for current, feature in enumerate(features):
            #Esse é o passo q permite que você cancele a execução            
            if feedback.isCanceled():
                break

            geometry = feature.geometry()
            feat = QgsFeature()
            feat.setGeometry(geometry)
            id = feature["id"]
            Trafeg = 3
            feat.setAttributes([id,Trafeg])
            sink_pol.addFeature(feat, QgsFeatureSink.FastInsert)

            feedback.setProgress(int(current * total))
        total = 100.0 / VDESLOC.featureCount() if VDESLOC.featureCount() else 0
        features = VDESLOC.getFeatures()
        #O enumerate vai gerar um dicionário com as features e o número que corresponde a elas enumerando-as , dess forma, enumerate(features) devolte uma tupla 
        for current, feature in enumerate(features):
            #Esse é o passo q permite que você cancele a execução            
            if feedback.isCanceled():
                break

            geometry = feature.geometry()
            feat = QgsFeature()
            feat.setGeometry(geometry)
            id = feature["id"]
            if (feature["jurisdicao"] == 1) or (feature['jurisdicao'] == 2):
                Trafeg = 3
            else:
                Trafeg = 1
                
            feat.setAttributes([id,Trafeg])
            sink_line.addFeature(feat, QgsFeatureSink.FastInsert)

            feedback.setProgress(int(current * total)) 

        total = 100.0 / VAZIO.featureCount() if VAZIO.featureCount() else 0
        features = VAZIO.getFeatures()
        #O enumerate vai gerar um dicionário com as features e o número que corresponde a elas enumerando-as , dess forma, enumerate(features) devolte uma tupla 
        for current, feature in enumerate(features):
            #Esse é o passo q permite que você cancele a execução            
            if feedback.isCanceled():
                break

            geometry = feature.geometry()
            feat = QgsFeature()
            feat.setGeometry(geometry)
            id = feature["id"]
            Trafeg = 0
                
            feat.setAttributes([id,Trafeg])
            sink_pol.addFeature(feat, QgsFeatureSink.FastInsert)

            feedback.setProgress(int(current * total))
        total = 100.0 / ED.featureCount() if ED.featureCount() else 0
        features = ED.getFeatures()
        #O enumerate vai gerar um dicionário com as features e o número que corresponde a elas enumerando-as , dess forma, enumerate(features) devolte uma tupla 
        for current, feature in enumerate(features):
            #Esse é o passo q permite que você cancele a execução            
            if feedback.isCanceled():
                break

            geometry = feature.geometry()
            feat = QgsFeature()
            feat.setGeometry(geometry)
            id = feature["id"]
            Trafeg = 2
                
            feat.setAttributes([id,Trafeg])
            sink_pol.addFeature(feat, QgsFeatureSink.FastInsert)

            feedback.setProgress(int(current * total))
        total = 100.0 / VEG.featureCount() if VEG.featureCount() else 0
        features = VEG.getFeatures()
        #O enumerate vai gerar um dicionário com as features e o número que corresponde a elas enumerando-as , dess forma, enumerate(features) devolte uma tupla 
        for current, feature in enumerate(features):
            #Esse é o passo q permite que você cancele a execução            
            if feedback.isCanceled():
                break

            geometry = feature.geometry()
            feat = QgsFeature()
            feat.setGeometry(geometry)
            id = feature["id"]
            if feature["tipo"] == 601 or feature["tipo"] == 602:
                Trafeg = 3
            elif feature["tipo"] in [1000,1001,1002,1003]:
                Trafeg = 1
            else:
                Trafeg = 2
            feat.setAttributes([id,Trafeg])
            sink_pol.addFeature(feat, QgsFeatureSink.FastInsert)

            feedback.setProgress(int(current * total))
                
            feat.setAttributes([id,Trafeg])
            sink_pol.addFeature(feat, QgsFeatureSink.FastInsert)

            feedback.setProgress(int(current * total))
        
        
        buffer_cil = processing.run("native:buffer", {'INPUT':MAGUA,'DISTANCE':buff_cil_value,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
        blink = processing.run("native:selectbylocation", {'INPUT':VEG,'PREDICATE':[0],'INTERSECT':buffer_cil,'METHOD':0})['OUTPUT']
        for feat in blink.getFeatures():
            geom = feat.geometry()
            feat2 = QgsFeature()
            feat2.setGeometry(geometry)
            id = feat["id"]
            Trafeg = 3
            feat.setAttributes([id,Trafeg])
            if geom.wkbType() == QgsWkbTypes.PolygonGeometry:
                sink_pol.addFeature(feat, QgsFeatureSink.EditModeUpdateGeometry)
            elif geom.wkbType() == QgsWkbTypes.LineString:
                sink_line.addFeature(feat, QgsFeatureSink.EditModeUpdateGeometry)
        buffer_dren = processing.run("native:buffer", {'INPUT':DREN,'DISTANCE':buff_dren_value,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
        blink = processing.run("native:selectbylocation", {'INPUT':VEG,'PREDICATE':[0],'INTERSECT':buffer_dren,'METHOD':0})['OUTPUT']
        for feat in blink.getFeatures():
            geom = feat.geometry()
            feat2 = QgsFeature()
            feat2.setGeometry(geometry)
            id = feat["id"]
            Trafeg = 3
            feat.setAttributes([id,Trafeg])
            if geom.wkbType() == QgsWkbTypes.PolygonGeometry:
                sink_pol.addFeature(feat, QgsFeatureSink.EditModeUpdateGeometry)
            elif geom.wkbType() == QgsWkbTypes.LineString:
                sink_line.addFeature(feat, QgsFeatureSink.EditModeUpdateGeometry)

        if False:
            buffered_layer = processing.run("native:buffer", {
                'INPUT': dest_id,
                'DISTANCE': 1.5,
                'SEGMENTS': 5,
                'END_CAP_STYLE': 0,
                'JOIN_STYLE': 0,
                'MITER_LIMIT': 2,
                'DISSOLVE': False,
                'OUTPUT': 'memory:'
            }, context=context, feedback=feedback)['OUTPUT']

        return {self.OUTPUT: dest_id, self.OUTPUT2: dest_id2}
