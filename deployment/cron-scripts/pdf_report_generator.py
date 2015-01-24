# coding=utf-8

# A simple demonstration of how to print
# This code is public domain, use if for any purpose you see fit.
# Tim Sutton 2015

import sys

from qgis.core import (
    QgsMapLayerRegistry,
    QgsProject,
    QgsComposition,
    QgsApplication,
    QgsProviderRegistry,
    QgsVectorLayer,
    QgsRasterLayer)

from qgis.gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge
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

        self.project_path = project_path
        self.template_path = template_path

    def __del__(self):
        """Destructor."""
        del self.app

    def _load_project(self):
        """Load the QGIS project."""
        QgsLayerTreeMapCanvasBridge(
            QgsProject.instance().layerTreeRoot(), self.canvas)
        QgsProject.instance().read(QFileInfo(self.project_path))

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

    def load_layers(self):
        """Manually load all the layers listed in the given project.

        This is an alternative to load_project which does not reliably
        add all layers into the project.

        :return: A list of QgsMapLayer instances.
        :rtype: list
        """
        layers = []
        for layer in self._iterate_layers('maplayer'):
            layer_type = self._getAttr(layer, 'type').value()
            if layer_type == 'vector':
                qgsLayer = QgsVectorLayer()
            elif layer_type == 'raster':
                qgsLayer = QgsRasterLayer()

            # read layer from XML
            element = layer.toElement()
            if not(qgsLayer.readLayerXML(element)):
                raise RuntimeError(
                    'Layer is not readable: {}'.format(
                        layer.firstChildElement('id').text()
                    )
                )
            layers.append(qgsLayer)
        return layers

    def _iterate_layers(self, tag):
        """Iterator for all layers ina QGIS project file.

        :param tag: Tag to search for.
        :type tag: str
        """
        project_file = file(self.project_path)
        project_content = project_file.read()
        project_file.close()
        document = QDomDocument()
        document.setContent(project_content)
        elements = document.elementsByTagName(tag)
        for i in xrange(elements.size()):
            print elements.at(1)
            yield elements.at(i)

    def _getAttr(self, obj, attr):
        """Get an attribute from a document."""
        if not(obj):
            raise RuntimeError('XML Object must exist!')

        attrs = obj.attributes()
        return attrs.namedItem(attr).toAttr()

    def make_pdf(self, pdf_path):
        """Generate a pdf for the given project and template files.

        :param pdf_path: Absolute path for the output PDF file.
        :type pdf_path: str

        """
        self._load_project()
        layers = self.load_layers()
        for item in layers:
            print item.source()

        for item in QgsMapLayerRegistry.instance().mapLayers():
            print item.source()

        if self.canvas.layerCount() < 1:
            print 'No layers loaded from this project, exiting.'
            return
        print self.canvas.mapSettings().extent().toString()
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


maker = PdfMaker(project_path='test.qgs', template_path='test.qpt')
maker.make_pdf('/tmp/test.pdf')
maker.make_pdf('/tmp/test.pdf')


