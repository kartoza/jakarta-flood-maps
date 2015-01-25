# coding=utf-8

# A simple demonstration of how to print
# This code is public domain, use if for any purpose you see fit.
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
    QgsRasterLayer)

from qgis.gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge, QgsMapCanvasLayer
from PyQt4.QtCore import QFileInfo
from PyQt4.QtXml import QDomDocument


class PdfMaker(object):
    """A generator that takes a QGIS project file and a layout template and makes a pdf."""

    def __init__(self, project_path, template_path, debug=False):
        """Constructor.

        :param project_path: Absolute path to a QGIS project file.
        :type project_path: str

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

        self.project_path = project_path
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

    def _iterate_layer_elements(self):
        """Iterator for all layers in a QGIS project file.
        """
        tag = 'maplayer'
        print 'Searching for tag: %s' % tag
        project_file = file(self.project_path)
        project_content = project_file.read()
        project_file.close()
        document = QDomDocument()
        result = document.setContent(project_content)
        if not result:
            raise Exception('DOM loading failed')

        elements = document.elementsByTagName(tag)
        print 'Found %i layers' % elements.size()

        for i in xrange(elements.size()):
            print 'Element: %s' % elements.item(i).toDocument().toString()
            layer = elements.item(i)
            print 'ID: %s' % layer.firstChildElement('id').text()
            print 'DataSource: %s' % layer.firstChildElement('datasource').text()
            yield layer

    def _getAttr(self, obj, attr):
        """Get an attribute from a document."""
        if not(obj):
            raise RuntimeError('XML Object must exist!')

        attrs = obj.attributes()
        return attrs.namedItem(attr).toAttr()


    def _load_layers(self):
        """Manually load all the layers listed in the given project.

        This is an alternative to load_project which does not reliably
        add all layers into the project.

        :return: A list of QgsMapLayer instances.
        :rtype: list
        """
        layers = []
        project_dir = os.path.abspath(
                os.path.dirname(self.project_path))
        for item in self._iterate_layer_elements():
            layer_type = self._getAttr(item, 'type').value()
            source = item.firstChildElement('datasource').text()
            source = os.path.abspath(
                os.path.join(
                    project_dir,
                    source
                )
            )
            provider = item.firstChildElement('provider').text()
            title = item.firstChildElement('title').text()
            if layer_type == 'vector':
                layer = QgsVectorLayer(source, title, provider)

            if not layer.isValid():
                raise Exception('Loaded layer is not valid: %s' % source)
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


maker = PdfMaker(project_path='./projects/test.qgs', template_path='./templates/test.qpt')
maker.make_pdf('test.pdf')


