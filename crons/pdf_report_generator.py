# coding=utf-8

import os
import sys
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsComposition,
    QgsMapLayerRegistry,
    QgsPalLabeling,
    QgsMapSettings,
)
from qgis.gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge
from PyQt4.QtCore import (
    QCoreApplication,
    QFileInfo,
    QSize,
)
from PyQt4.QtGui import QPrinter, QPainter, QWidget, QVBoxLayout
from PyQt4.QtXml import QDomDocument

QCoreApplication.setOrganizationName('JakartaFloodMaps')
QCoreApplication.setOrganizationDomain('kartoza.com')
QCoreApplication.setApplicationName('JakartaFloodMaps')

gui_flag = True
app = QgsApplication(sys.argv, gui_flag)

# Make sure QGIS_PREFIX_PATH is set in your env if needed!
app.initQgis()

reports_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    'reports',
))

pdf_file = os.path.abspath(os.path.join(
    reports_dir,
    'pdf',
    '6h',
    '2015-01-13-12.pdf'
))

project_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    'maps',
    'projects',
    'jakarta_flood_maps.qgs'
))

widget = QWidget()
canvas = QgsMapCanvas(widget)
canvas.resize(QSize(400, 400))

print 'Canvas extent before loading project: %s' % canvas.extent().toString()
# Load our project
bridge = QgsLayerTreeMapCanvasBridge(
    QgsProject.instance().layerTreeRoot(), canvas)
QgsProject.instance().read(QFileInfo(project_path))
canvas.zoomToFullExtent()
print 'Canvas extent after loading project: %s' % canvas.extent().toString()
# Load our template
template_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    'maps',
    'templates',
    'jakarta_flooded_rw.qpt'
))

template_file = file(template_path)
template_content = template_file.read()
template_file.close()
document = QDomDocument()
document.setContent(template_content)

#
#label_engine = QgsPalLabeling()
#renderer = QgsMapRenderer()
#renderer.setLabelingEngine(label_engine)
# Now set up the composition
composition = QgsComposition(canvas.mapSettings())
# You can use this to replace any string like this [key]
# in the template with a new value. e.g. to replace
# [date] pass a map like this {'date': '1 Jan 2012'}
substitution_map = {
    'DATE_TIME_START': 'foo',
    'DATE_TIME_END': 'bar'}
composition.loadFromTemplate(document, substitution_map)

# Get the main map canvas on the composition and set
# its extents to the event.
map_canvas = composition.getComposerItemById('main-map')
# Save a pdf.
composition.exportAsPDF(pdf_file)


