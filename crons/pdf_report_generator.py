# coding=utf-8

import os
import sys
from qgis.core import (
    QgsRectangle,
    QgsApplication,
    QgsMapRenderer,
    QgsPoint,
    QgsField,
    QgsFeature,
    QgsGeometry,
    QgsVectorLayer,
    QgsRaster,
    QgsRasterLayer,
    QgsDataSourceURI,
    QgsVectorFileWriter,
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsComposition,
    QgsMapLayerRegistry,
    QgsPalLabeling,
    QgsProviderRegistry,
    QgsFeatureRequest,
    QgsVectorDataProvider,
    QgsMapSettings
)
from PyQt4.QtCore import (
    QCoreApplication,
    QSizeF,
    QObject,
    QVariant,
    QFileInfo,
    QUrl,
    QSize,
    Qt,
    QTranslator
)
from PyQt4.QtGui import QPrinter, QPainter

from PyQt4.QtXml import QDomDocument


QCoreApplication.setOrganizationName('JakartaFloodMaps')
QCoreApplication.setOrganizationDomain('kartoza.com')
QCoreApplication.setApplicationName('JakartaFloodMaps')

#noinspection PyPep8Naming
gui_flag = True
# app = QApplication([], gui_flag)
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

# Make sure the map layers have all been removed before we
# start otherwise in batch mode we will get overdraws.
# noinspection PyArgumentList

project_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    'maps',
    'projects',
    'jakarta_flood_maps.qgs'
))

# Load our project
QgsProject.instance().setFileName(project_path)
# noinspection PyArgumentList
# QgsProject.instance().read()

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

label_engine = QgsPalLabeling()
renderer = QgsMapRenderer()
renderer.setLabelingEngine(label_engine)

crs = QgsCoordinateReferenceSystem('EPSG:4326')
extent = QgsRectangle(1, 1, 10, 10)
map_settings = QgsMapSettings()
map_settings.setDestinationCrs(crs)
map_settings.setCrsTransformEnabled(True)
map_settings.setExtent(extent)
map_settings.setOutputSize(QSize(1000, 1000))
# Now set up the composition
composition = QgsComposition(map_settings)
# You can use this to replace any string like this [key]
# in the template with a new value. e.g. to replace
# [date] pass a map like this {'date': '1 Jan 2012'}
substitution_map = {
    'DATE_TIME_START': 'foo',
    'DATE_TIME_END': 'bar'}
composition.loadFromTemplate(document, substitution_map)

printer = QPrinter()
printer.setOutputFormat(QPrinter.PdfFormat)
printer.setOutputFileName(pdf_file)
printer.setPaperSize(
    QSizeF(composition.paperWidth(), composition.paperHeight()),
    QPrinter.Millimeter)
printer.setFullPage(True)
printer.setColorMode(QPrinter.Color)
printer.setResolution(composition.printResolution())

pdfPainter = QPainter(printer)
paperRectMM = printer.pageRect(QPrinter.Millimeter)
paperRectPixel = printer.pageRect(QPrinter.DevicePixel)
composition.render(pdfPainter, paperRectPixel, paperRectMM)
pdfPainter.end()




# Get the main map canvas on the composition and set
# its extents to the event.
map_canvas = composition.getComposerItemById('main-map')
# map_canvas.setNewExtent(extent)
map_canvas.renderModeUpdateCachedImage()

# Save a pdf.
composition.exportAsPDF(pdf_file)


