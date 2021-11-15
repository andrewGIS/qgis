from PyQt5.QtGui import QPainterPath, QFont
from qgis.gui import QgsMapTool

from qgis.PyQt.QtGui import (
    QColor,
)

from qgis.PyQt.QtCore import Qt, QRectF, QPoint

from qgis.core import (
    QgsVectorLayer,
    QgsPoint,
    QgsPointXY,
    QgsProject,
    QgsGeometry,
    QgsMapRendererJob,
)

from qgis.gui import (
    QgsMapCanvas,
    QgsMapCanvasItem,
    QgsRubberBand,
)


class QgsTextCanvasItem(QgsMapCanvasItem):

    def __init__(self, canvas, size=18, is_real_coords=False, font=None):
        QgsMapCanvasItem.__init__(self, canvas)
        self.__canvas = canvas
        self.__point = None
        self.__text = None
        self.angle = None
        self.size = size
        self.is_real_coords = is_real_coords
        self.font = font
        self.width = None
        self.height = None

    def paint(self, painter, option, widget):
        try:
            if ((self.__point is None) or (self.__text is None)):
                return
            font = painter.font()
            if (self.font is None):
                font = painter.font()
            else:
                font = self.font

            real_width = None
            real_height = None

            if self.is_real_coords:
                size = (self.size / self.__canvas.mapUnitsPerPixel()) * 72 / 96
                if (self.width is not None) and (self.height is not None):
                    real_width = (self.width / self.__canvas.mapUnitsPerPixel())
                    real_height = (self.height / self.__canvas.mapUnitsPerPixel())
            else:
                size = self.size

            font.setPointSize(size)
            painter.setFont(font)
            if (real_width is not None) and (real_height is not None):
                painter.drawText(QRectF(self.__point.x(), self.__point.y() - real_height, real_width, real_height),
                                     Qt.TextDontClip, self.__text)
            else:
                painter.drawText(self.__point, self.__text)

        except:
            pass

    def setText(self, text):
        self.__text = text
        self.update()

    def setTextRect(self, width, height):
        self.width = width
        self.height = height

    def Text(self):
        return self.__text

    def setPos(self, point):
        if self.is_real_coords:
            p = self.__canvas.getCoordinateTransform().transform(point)
            self.__point = QPoint(int(p.x()), int(p.y()))
        else:
            self.__point = point
        self.update()


class SquareMapTool(QgsMapTool):
    """Create cutom map tool
        with custom click and move event

        :param QgsMapTool: Basic qgis class
        :type QgsMapTool: Basic qgis class
        """

    def __init__(self, canvas):
        """Contstructor for custom class

        :param canvas: map canvas for class
        :type canvas: QgsMapCanvas
        :param labelElement: where circle area is showing
        :type labelElement: QLabel
        """
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas

        # custom attrs
        self.rubberBand = QgsRubberBand(self.canvas, True)  # for graphic storing
        self.circleCenterPoint = None

        # Graphic appereance
        self.rubberBand.setWidth(1)
        # Using the custom item:
        self.item = QgsTextCanvasItem(canvas, is_real_coords=True, font=QFont("Times", 10, QFont.Bold))
        self.geometry = None

    def canvasPressEvent(self, event):
        """Handle for move cursor
        if circleCenterPoint is set clear graphic and reset circle
        otherwise set clicked cursor coordinates

        :param event: basic type from QGIS
        :type event: QPoint?
        """
        self.clearRubberBand()
        if self.circleCenterPoint:
            self.circleCenterPoint = None
            self.clearRubberBand()
            self.item.setText(None)
            self.item.setEnabled(False)
        else:
            self.circleCenterPoint = self.toMapCoordinates(event.pos())
            self.item.setPos(self.toMapCoordinates(event.pos()))
            self.item.size = 5
            self.item.setEnabled(True)

    def canvasMoveEvent(self, event):
        """Handler for move event

        :param event: basic type from QGIS
        :type event: QPoint?
        """
        if self.circleCenterPoint:
            # convert moved cursor point to point
            # in geo-coordinates
            movedPoint = self.toMapCoordinates(event.pos())

            radius = self.circleCenterPoint.distance(movedPoint)

            # clear QgsBand for drawing new circle
            self.rubberBand.reset()  # False = not a polygon

            bboxGeometry = QgsGeometry.fromRect(QgsGeometry.fromPointXY(
                self.circleCenterPoint).buffer(radius, 50).boundingBox())

            # Show area of circle in text element
            # print(circleGeometry.area())

            # Display geometry of circle
            if bboxGeometry.area() <= 10000:
                self.rubberBand.setToGeometry(
                    bboxGeometry, None)
                self.item.setText(f"{bboxGeometry.area():.2f} м2")
                self.geometry = bboxGeometry

            else:
                self.rubberBand.setToGeometry(QgsGeometry.fromRect(QgsGeometry.fromPointXY(
                    self.circleCenterPoint).buffer(50, 50).boundingBox()))
                self.geometry = QgsGeometry.fromRect(QgsGeometry.fromPointXY(
                    self.circleCenterPoint).buffer(50, 50).boundingBox())
                self.item.setText(None)

    def canvasReleaseEvent(self, e):
        if self.geometry:
            print(self.geometry.area())
            self.rubberBand.addGeometry(self.geometry)
            #self.geometry = None


    def clearRubberBand(self):
        """Clear all drawed graphics
        """
        self.rubberBand.reset()