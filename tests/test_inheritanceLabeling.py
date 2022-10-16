# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 18:09:02 2022

@author: akrual
"""

import sys
import os


def getParentalWKD(level):
    
    cwd = os.getcwd()
    
    for i in range(level):
        cwd = os.path.dirname(cwd)
        
    return cwd


path = getParentalWKD(1)

sys.path.insert(0, path)

from diagrams import Cluster, Diagram, DiagramManager
from diagrams.programming.flowchart import Action

RESULTDIR = os.path.join(os.getcwd(), "DiagramGeneratorResults")


class DiagramGenerator(DiagramManager):
    def __init__(self,
                 *args,
                 **kwargs):
        DiagramManager.__init__(self, *args, **kwargs)
        
    def generateDiagram(self):

        with Diagram(name = self.diagramName,
                     filename = os.path.join(RESULTDIR, self.diagramFileName),
                     show=True):

            A0 = Action("Tipos de cálculo de PU", 
                        diagramManager = self,
                        level="1")
        
            with Cluster("Tipo de ICM") as TipoICMCluster:
                a = Action("Mensal", diagramManager = self)
                b = Action("Diário", diagramManager = self)
                TipoICMNodes = [a,b]
                [TipoICMCluster.insertElementToDigraph(x) for x in TipoICMNodes]
            
            subClusters = []
            
            for iid, node in enumerate(TipoICMCluster.dot.nodes, start=1):
                
                subCluster = self._generateFJCluster(".{0}".format(iid))
                
                subClusters.append(subCluster)
        
        
            A0 >> TipoICMCluster
            
            TipoICMCluster.level()
            
            [TipoICMCluster >> subCluster for subCluster in subClusters]

    def _generateFJCluster(self, label):
        
        with Cluster("Tipo De Fator de Juros ({0})".format(label)) as FJCluster:
            FJGregoriano = Action("Gregoriano", diagramManager = self)
            FJJuliano = Action("Juliano", diagramManager = self)
            FJNodes = [FJGregoriano, FJJuliano]
            [FJCluster.insertElementToDigraph(x) for x in FJNodes]
            
        return FJCluster


if "__main__" == __name__:
    gen = DiagramGenerator()
    
    gen.generateDiagram()