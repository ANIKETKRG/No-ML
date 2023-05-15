from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class QDMCutLine ( QGraphicsItem ) :
    def __init__ ( self , parent = None ) :
        super().__init__ ( parent )
        
        
        self.line_points = []
        
        self._pen = QPen ( Qt.white)
        self._pen.setWidthF ( 2.0 )
        self._pen.setDashPattern ( [ 3 , 3 ] )
        
        self.setZValue ( 2 )
        
        
    def boundingRect ( self ) -> QRectF :
        return QRectF ( 0 , 0 , 1 , 1 )
    
    def paint ( self , painter , QStyleOptionGraphicsItem , widget = None ) :
        painter.setRenderHint ( QPainter.Antialiasing )
        painter.setPen ( self._pen )    
        painter.setBrush ( Qt.NoBrush )
        
        
        poly = QPolygonF ( self.line_points )
        painter.drawPolyline ( poly )
        
        
        
        
        
        
        
        
        
        