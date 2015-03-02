# coding=utf-8

# A simple demonstration of how to load a QGIS project and then
# show it in a widget.
# This code is public domain, use if for any purpose you see fit.
# Tim Sutton 2015

import os
import sys
from qgis.core import (
    QgsProject, QgsComposition, QgsApplication, QgsProviderRegistry)
from qgis.gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge
from PyQt4.QtCore import QFileInfo
from PyQt4.QtXml import QDomDocument


gui_flag = True
app = QgsApplication(sys.argv, gui_flag)

# Make sure QGIS_PREFIX_PATH is set in your env if needed!
app.initQgis()

print 'Available providers:'
print QgsProviderRegistry.instance().pluginList()


project_path = os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    'maps',
    'jk-floods.qgs')
template_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    'maps',
    'templates',
    'jakarta_flooded_rw.qpt'
))

TIME_SLICE = sys.argv[1]
TIME_START = sys.argv[2]
TIME_STOP = sys.argv[3]
LABEL = sys.argv[4]


def make_pdf():
    canvas = QgsMapCanvas()
    # Load our project
    QgsProject.instance().read(QFileInfo(project_path))
    bridge = QgsLayerTreeMapCanvasBridge(
        QgsProject.instance().layerTreeRoot(), canvas)
    bridge.setCanvasLayers()
    if canvas.layerCount() < 1:
        print 'No layers loaded from this project, exiting.'
        return
    print canvas.mapSettings().extent().toString()
    template_file = file(template_path)
    template_content = template_file.read()
    template_file.close()
    document = QDomDocument()
    document.setContent(template_content)
    composition = QgsComposition(canvas.mapSettings())
    # You can use this to replace any string like this [key]
    # in the template with a new value. e.g. to replace
    # [date] pass a map like this {'date': '1 Jan 2012'}
    substitution_map = {
        'DATE_TIME_START': TIME_START,
        'DATE_TIME_END': TIME_STOP}
    composition.loadFromTemplate(document, substitution_map)
    # You must set the id in the template
    map_item = composition.getComposerItemById('map')
    map_item.setMapCanvas(canvas)
    map_item.zoomToExtent(canvas.extent())
    # You must set the id in the template
    legend_item = composition.getComposerItemById('legend')
    legend_item.updateLegend()
    composition.refreshItems()
    composition.exportAsPDF(
        '/home/web/reports/pdf/%s/%s.pdf' % (TIME_SLICE, LABEL))
    QgsProject.instance().clear()


make_pdf()


