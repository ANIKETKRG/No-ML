import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QDMGraphicsScene ( QGraphicsScene ) :
    
    def __init__( self , scene , parent = None ) :
        super().__init__( parent )
        
        self.scene = scene
        
        self.gridSize = 20
        self.gridSquares = 5
        
        self._color_background = QColor( "#393939" )
        self._color_light = QColor( "#2f2f2f" )
        self._color_dark = QColor( "292929" )
        
        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(1)
        
        # self.scene_width , self.scene_height = 64000 , 64000
        # self.setSceneRect ( -self.scene_width//2 , -self.scene_height//2 , self.scene_width , self.scene_height )
        
        
        
        
        self.setBackgroundBrush( self._color_background )
        
    # def setBackgroundBrush(self, brush: QBrush | QColor | GlobalColor | QGradient) -> None:
    #     return super().setBackgroundBrush(brush) 
    
    def setGrScene ( self , vidth , heigth ) :
        self.setSceneRect ( -vidth//2 , -heigth//2 , vidth , heigth )
         
        
    def drawBackground( self , painter , rect ) :
        super().drawBackground( painter , rect )
        # Here We Create Our Grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))
        
        first_left = left - ( left % self.gridSize )
        first_top = top - ( top % self.gridSize )
            
            
            
                
        # Compute All Lines To Be Drawn
        lines_light , lines_dark = [] , []
        for x in range ( first_left , right , self.gridSize ) :
            if (x % (self.gridSize*self.gridSquares) != 0 ) :
                lines_light.append(QLine(x, top , x , bottom ))
            else :
                lines_dark.append(QLine(x, top , x , bottom ))
            
        for y in range ( first_top , bottom , self.gridSize ) :
            if (y % (self.gridSize*self.gridSquares) != 0 ) :
                lines_light.append(QLine(left, y , right , y ))
            else :
                lines_dark.append(QLine(left, y , right , y ))
        
        
        
        
        
        # lines_light.append(QLine(0,0,100,100))
        
        
        
        
        # Draw The Line 
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)
        
        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)