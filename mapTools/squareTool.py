from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import QgsGeometry


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

    def canvasPressEvent(self, event):
        """Handle for move cursor
        if circleCenterPoint is set clear graphic and reset circle
        otherwise set clicked cursor coordinates

        :param event: basic type from QGIS
        :type event: QPoint?
        """
        if self.circleCenterPoint:
            self.circleCenterPoint = None
            self.clearRubberBand()
        else:
            self.circleCenterPoint = self.toMapCoordinates(event.pos())

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
            self.rubberBand.setToGeometry(
                bboxGeometry, None)

    def clearRubberBand(self):
        """Clear all drawed graphics
        """
        self.rubberBand.reset()