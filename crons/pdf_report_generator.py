__author__ = 'christian'
# coding=utf-8
"""Views for layers"""
import glob
import os


from qgis.core import (
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
    QObject,
    QVariant,
    QFileInfo,
    QUrl,
    QSize,
    Qt,
    QTranslator
)
from PyQt4.QtXml import QDomDocument


def render_map():
    """This is the 'do it all' method to render a pdf.

    :param force_flag: (Optional). Whether to force the
            regeneration of map product. Defaults to False.
    :type force_flag: bool

    :raise Propagates any exceptions.
    """
    reports_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        os.path.pardir,
        os.path.pardir,
        'reports',
    ))
    shp_file = os.path.join(
        reports_dir,
        'shp',
        '6h',
        '2015-01-13-12.shp'
    )
    pdf_file = os.path.join(
        reports_dir,
        'pdf',
        '6h',
        '2015-01-13-12.pdf'
    )

    # Make sure the map layers have all been removed before we
    # start otherwise in batch mode we will get overdraws.
    # noinspection PyArgumentList
    QgsMapLayerRegistry.instance().removeAllMapLayers()

    layer = QgsVectorLayer(
        shp_file,
        'mmi-cities', "ogr")
    if not layer.isValid():
        raise ImportError

    project_path = os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        'data',
        'jakarta_background.qgs')

    # Load our project
    QgsProject.instance().setFileName(project_path)
    # noinspection PyArgumentList
    QgsProject.instance().read()

    # noinspection PyArgumentList
    QgsMapLayerRegistry.instance().addMapLayers([layer])

    # Load our template
    template_path = os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        'data',
        'realtime-template.qpt')

    template_file = file(template_path)
    template_content = template_file.read()
    template_file.close()
    document = QDomDocument()
    document.setContent(template_content)

    # Now set up the composition
    composition = QgsComposition(QgsMapSettings())

    # You can use this to replace any string like this [key]
    # in the template with a new value. e.g. to replace
    # [date] pass a map like this {'date': '1 Jan 2012'}
    substitution_map = {
        'this': 'that',
        'here': 'there'}

    composition.loadFromTemplate(document, substitution_map)

    # Get the main map canvas on the composition and set
    # its extents to the event.
    map_canvas = composition.getComposerItemById('main-map')
    # map_canvas.setNewExtent(extent)
    map_canvas.renderModeUpdateCachedImage()

    # Save a pdf.
    composition.exportAsPDF(pdf_file)


if __name__ == "__main__":
    render_map()
