# coding=utf-8

# A simple demonstration of how to print
# This code is public domain, use if for any purpose you see fit.
# 
# See also pdf_report_generator.py which loads state from a project file rather
# This version manually constructs layers and loads them.
#
# Tim Sutton 2015
import os
import sys
from qgis.core import (
    QgsMapLayerRegistry,
    QgsProject,
    QgsComposition,
    QgsApplication,
    QgsProviderRegistry,
    QgsCoordinateReferenceSystem,
    QgsVectorLayer,
    QgsDataSourceURI)
from qgis.gui import QgsMapCanvas, QgsMapCanvasLayer

from PyQt4.QtXml import QDomDocument


class PdfMaker(object):
    """A generator that takes a QGIS project file and a layout template and makes a pdf."""

    def __init__(self, template_path, debug=False):
        """Constructor.

        :param template_path: Absolute path to a QGIS composer template file.
        :type template_path: str
        """
        gui_flag = True
        self.app = QgsApplication(sys.argv, gui_flag)

        # Make sure QGIS_PREFIX_PATH is set in your env if needed!
        self.app.initQgis()

        if debug:
            print QgsProviderRegistry.instance().pluginList()

        self.canvas = QgsMapCanvas()
        self.canvas.enableAntiAliasing(True)

        self.template_path = template_path

    def __del__(self):
        """Destructor."""
        del self.app

    def _load_template(self):
        """Load the template.

        :return: QgsComposition containing the loaded template.
        :rtype: QgsComposition
        """
        template_file = file(self.template_path)
        template_content = template_file.read()
        template_file.close()
        document = QDomDocument()
        document.setContent(template_content)
        composition = QgsComposition(self.canvas.mapSettings())
        # You can use this to replace any string like this [key]
        # in the template with a new value. e.g. to replace
        # [date] pass a map like this {'date': '1 Jan 2012'}
        substitution_map = {
            'DATE_TIME_START': 'foo',
            'DATE_TIME_END': 'bar'}
        composition.loadFromTemplate(document, substitution_map)
        return composition

    def _load_layers(self):
        """Manually load all the layers for our project.

        :return: A list of QgsMapLayer instances.
        :rtype: list
        """
        layers = []

        # First the RW layer

        host = 'db'
        port = '5432'
        user = 'docker'
        password = 'docker'
        dbname = 'gis'
        uri = QgsDataSourceURI()
        uri.setConnection(host, port, dbname, user, password)

        schema = 'public'
        table = 'flood_mapper_rw'
        geometry_column = 'geometry'
        where_clause = ''
        title = 'RW'
        uri.setDataSource(schema, table, geometry_column, where_clause)
        layer = QgsVectorLayer(uri.uri(), title, 'postgres')

        QgsMapLayerRegistry.instance().addMapLayer(layer, False)
        canvas_layer = QgsMapCanvasLayer(layer)
        layers.append(canvas_layer)

        # Now the JK layer
        path = './data/jk.shp'
        title = 'JK'
        layer = QgsVectorLayer(path, title, 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(layer, False)
        canvas_layer = QgsMapCanvasLayer(layer)
        layers.append(canvas_layer)

        return layers

    def make_pdf(self, pdf_path):
        """Generate a pdf for the given project and template files.

        :param pdf_path: Absolute path for the output PDF file.
        :type pdf_path: str

        """

        layers = self._load_layers()
        self.canvas.setLayerSet(layers)

        if self.canvas.layerCount() < 1:
            print 'No layers loaded from this project, exiting.'
            return
        self.canvas.setDestinationCrs(QgsCoordinateReferenceSystem('EPSG:3857'))
        self.canvas.setCrsTransformEnabled(True)
        self.canvas.zoomToFullExtent()

        print 'Extent: %s' % self.canvas.mapSettings().extent().toString()
        # self._load_project()
        composition = self._load_template()
        # You must set the id in the template
        map_item = composition.getComposerItemById('map')
        map_item.setMapCanvas(self.canvas)
        map_item.zoomToExtent(self.canvas.extent())
        # You must set the id in the template
        legend_item = composition.getComposerItemById('legend')
        legend_item.updateLegend()
        composition.refreshItems()
        composition.exportAsPDF(pdf_path)
        QgsProject.instance().clear()


maker = PdfMaker(template_path='./templates/test.qpt')
maker.make_pdf('test.pdf')



