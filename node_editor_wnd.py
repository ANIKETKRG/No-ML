from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# from node_graphics_scene import QDMGraphicsScene
from node_graphics_view import QDMGraphicsView
from node_scene import Scene
from node_node import Node
# from node_socket import Socket
from node_edge import *


class NodeEditorWnd ( QWidget ) :
    def __init__ ( self , parent = None ) :
        super().__init__( parent )
        
        self.stylesheet_filename = "qss/nodestyle.qss"
        self.loadStylesheet ( self.stylesheet_filename )
        
        self.initUI()
             
    def initUI ( self ) :
        self.setGeometry ( 200 , 200 , 800 , 600 )
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins ( 0 , 0 , 0 , 0 )
        self.setLayout ( self.layout )
        
        # Create Graphics Scene
        # self.grScene = QDMGraphicsScene()
        self.scene = Scene()
                                                                                                           
        # self.grScene = self.scene.grScene
        # node = Node( self.scene , " My Awesome Node " , inputs = [ Socket() , Socket() , Socket() ] , 
        #             outputs = [ Socket() ] )
        
        


        self.addNodes()


        
          
        # Create Graphics View
        # self.view = QGraphicsView ( self )
        # self.view = QDMGraphicsView ( self.grScene , self )
        self.view = QDMGraphicsView ( self.scene.grScene , self )
        # self.view.setScene ( self.scene.grScene )
        self.layout.addWidget ( self.view )
        
        self.setWindowTitle ( " Aniket " )
        self.show()      
        
        
        
    def addNodes ( self ) :
        # node = Node ( self.scene , "My Awesome Node" )
        node1 = Node ( self.scene , "My Awesome Node 1" , inputs = [ 0 , 0 , 0 ] , outputs = [ 1 ] )
        node2 = Node ( self.scene , "My Awesome Node 2" , inputs = [ 3 , 3 , 3 ] , outputs = [ 1 ] )
        node3 = Node ( self.scene , "My Awesome Node 3" , inputs = [ 2 , 2 , 2 ] , outputs = [ 1 ] )
         
        node1.setPos ( -350 , -250 )
        node2.setPos ( -75 , -0 )
        node3.setPos ( 200 , -150 )
        
        
        edge1 = Edge ( self.scene , node1.outputs [0] , node2.inputs [0] , edge_type = EDGE_TYPE_BEZIER )      
        edge2 = Edge ( self.scene , node2.outputs [0] , node3.inputs [2] , edge_type = EDGE_TYPE_BEZIER )      
        
        
        # self.addDebugContent()
    
    def addDebugContent( self ) :
        greenBrush = QBrush ( Qt.red )
        outlinePen = QPen ( Qt.black )
        outlinePen.setWidth ( 2 )
        
        rect = self.grScene.addRect ( -80 , -80 , 80 , 80 , outlinePen , greenBrush )
        rect.setFlag ( QGraphicsItem.ItemIsMovable )
        
        text = self.grScene.addText ( " Hello World " , QFont ( " Ubuntu " , 20 ) )
        text.setFlag ( QGraphicsItem.ItemIsMovable )
        text.setFlag ( QGraphicsItem.ItemIsSelectable )
        text.setPos ( -50 , -50 )
        text.setDefaultTextColor ( QColor.fromRgbF ( 255 , 255 , 255 ) )
        
        
        widget1 = QPushButton ( " Button 1 " )
        proxy1 = self.grScene.addWidget ( widget1 )
        proxy1.setFlag ( QGraphicsItem.ItemIsMovable )
        proxy1.setPos ( 0 , 50 )
        
        
        # widget2 = QTextEdit()
        # proxy2 = self.grScene.addWidget(widget2)
        # proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        # proxy2.setPos(0, 60)
        # proxy2.setFlag ( QGraphicsItem.ItemIsMovable )
        
        line = self.grScene.addLine ( -200 , -200 , 400 , -100 , outlinePen )
        line.setFlag ( QGraphicsItem.ItemIsMovable )
        line.setFlag ( QGraphicsItem.ItemIsSelectable )


    def loadStylesheet ( self , filename ) :
        print ( " STYLE LOADING : " , filename ) 
        file = QFile ( filename )
        file.open ( QFile.ReadOnly | QFile.Text )
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet ( str ( stylesheet , encoding = 'utf-8' ) )   
      
      
       