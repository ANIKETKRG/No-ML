from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from node_graphics_socket import *
from node_graphics_edge import *
from node_edge import *
from node_graphics_cutline import *





MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3


EDGE_DRAG_START_THRESHOLD = 10

DEBUG = True


class QDMGraphicsView ( QGraphicsView ) :
    def __init__ ( self , grScene , parent = None ) :
        super().__init__ ( parent )
        self.grScene = grScene

        self.initUI()

        self.setScene ( self.grScene )
        
        self.mode = MODE_NOOP
        
        self.editingFlag = False

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomSteps = 1
        self.zoomRange = [ 0 , 10 ]



        # CutLine
        self.cutline = QDMCutLine ()
        self.grScene.addItem ( self.cutline )



    def initUI ( self ) :
        self.setRenderHints ( QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform )

        self.setViewportUpdateMode ( QGraphicsView.FullViewportUpdate )

        self.setHorizontalScrollBarPolicy ( Qt.ScrollBarAlwaysOff )
        self.setVerticalScrollBarPolicy ( Qt.ScrollBarAlwaysOff )
        
        self.setTransformationAnchor ( QGraphicsView.AnchorUnderMouse )
        self.setDragMode ( QGraphicsView.RubberBandDrag )
    
    
    def mousePressEvent ( self , event ) :
        if event.button() == Qt.MiddleButton :
            self.middleMouseButtonPress ( event )
        elif event.button() == Qt.LeftButton :
            self.leftMouseButtonPress ( event )
        elif event.button() == Qt.RightButton :
            self.rightMouseButtonPress ( event )
        else :
            super().mousePressEvent ( event )
    
    
    
    def mouseReleaseEvent ( self , event ) :
        if event.button() == Qt.MiddleButton :
            self.middleMouseButtonRelease ( event )
        elif event.button() == Qt.LeftButton :
            self.leftMouseButtonRelease ( event )
        elif event.button() == Qt.RightButton :
            self.rightMouseButtonRelease ( event )
        else :
            super().mouseReleaseEvent ( event )
         
            
            
            
    def middleMouseButtonPress ( self , event ) :
        releaseEvent = QMouseEvent ( QEvent.MouseButtonRelease , event.localPos () , event.screenPos () , 
                                    Qt.LeftButton , Qt.NoButton , event.modifiers () )
        super().mouseReleaseEvent ( releaseEvent )
        self.setDragMode ( QGraphicsView.ScrollHandDrag ) 
        fakeEvent = QMouseEvent ( event.type() , event.localPos() , event.screenPos() ,
                                Qt.LeftButton , event.buttons() | Qt.LeftButton , event.modifiers() )
        super().mousePressEvent ( fakeEvent )



        
    def middleMouseButtonRelease ( self , event ) :
        fakeEvent = QMouseEvent ( event.type() , event.localPos() , event.screenPos() ,
                                Qt.LeftButton , event.buttons() & ~Qt.LeftButton , event.modifiers() )
        super().mouseReleaseEvent ( fakeEvent )
        self.setDragMode ( QGraphicsView.NoDrag )
 
 
 
 
 
    def leftMouseButtonPress ( self , event ) :
        # Get Item Which Be Clicked On        
        item = self.getItemAtClick ( event )
        # print ( item )
        
        #  We Store The position Of The Last LMB Click In Scene
        
        self.last_lmb_click_scene_pos = self.mapToScene ( event.pos() )
        
        
        # if DEBUG : print ( " LMB + Shift On " , item )
        if DEBUG : print ( " LMB Click On " , item , self.debug_modifiers ( event ) )
        
        # Logic
        if hasattr ( item , "node" ) or isinstance ( item , QDMGraphicsEdge ) or item is None :
            if event.modifiers() & Qt.ShiftModifier :
                event.ignore()
                # fakeEvent = QMouseEvent ( QEvent.MouseButtonPress , event.localPos() , event.screenPos() , 
                #                          Qt.LeftButton , event.buttons() | Qt.LeftButton , event.modifiers() ,
                #                          Qt.ControlModifier )
                # super().mousePressEvent ( fakeEvent )
                return
            
            
        if type ( item ) is QDMGraphicsSocket :
            # print ( " Socket Was Clicked. " )
            if self.mode == MODE_NOOP :
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart ( item )
                return
            
            
        if self.mode == MODE_EDGE_DRAG :
            res = self.edgeDragEnd ( item )
            
            if res :
                return
            
            
        if item is None :   
            if event.modifiers() & Qt.ControlModifier :
                self.mode = MODE_EDGE_CUT
                # fakeEvent = QMouseEvent ( QMouseEvent.MouseButtoRelease , event.localPos() , event.screenPos() ,
                #                          Qt.LeftButton , event.NoButton , event.modifiers() )
                # super().mouseReleaseEvent ( fakeEvent )
                QApplication.setOverrideCursor ( Qt.CrossCursor )
                return
                
                
                
                 
        super().mousePressEvent ( event )
                
    
                

    def leftMouseButtonRelease ( self , event ) : 
        # Get Item Which Be Released Mouse Button On
        item = self.getItemAtClick ( event )
        
        # Logic
        if hasattr ( item , "node" ) or isinstance ( item , QDMGraphicsEdge ) or item is None :
            if event.modifiers() & Qt.ShiftModifier :
                # if DEBUG : print ( " LMB Release + Shift On " , item )
                event.ignore()
                # fakeEvent = QMouseEvent ( event.type() , event.localPos() , event.screenPos() , 
                #                          Qt.LeftButton , Qt.NoButton , event.modifiers() ,
                #                          Qt.ControlModifier )
                # super().mouseReleaseEvent ( fakeEvent )
                return
            
        if self.mode == MODE_EDGE_DRAG :
            
            # print ( " Distance On Clicked & Release : " , dist_scene_pos )
                   
            if self.distanceBetweenClickAndReleaseIsOff ( event ) :
                res = self.edgeDragEnd ( item )
                if res : return 
           
            if self.mode == MODE_EDGE_CUT :
                self.cutIntersectingEdges ()
                self.cutline.line_points = []
                self.cutline.update ()
                QApplication.setOverrideCursor ( Qt.ArrowCursor )
                self.mode = MODE_NOOP
                return
                    
  
                
                # self.mode == MODE_EDGE_DRAG
                # self.mode = MODE_NOOP
                # print ( " End Dragging Edge " )
                
                # if type ( item ) is QDMGraphicsSocket :
                #     print ( " Assign End Socket " )
                #     return
        
        
        
        super().mouseReleaseEvent ( event )




    def rightMouseButtonPress ( self , event ) :
        super().mousePressEvent ( event )
        
        item = self.getItemAtClick ( event )
        
        if DEBUG : 
            # print ( " RMB DEBUG " , item )
            if isinstance ( item , QDMGraphicsEdge ) :
                print ( " RMB DEBUG : " , item.edge , " Connecting Sockets : " , item.edge.start_socket , "<-->" , item.edge.end_socket )
            if type ( item ) is QDMGraphicsSocket :
                print ( " RMB DEBUG : " , item.socket , " Has Edge : " , item.socket.edge )
            
            
            if item is None :
                print ( " SCENE : " )
                print ( " Nodes : " )
                for node in self.grScene.scene.nodes :
                    print ( "     " , node )
                print ( " Edges : " )   
                for edge in self.grScene.scene.edges :
                    print ( "     " , edge )

    def rightMouseButtonRelease ( self , event ) :
        super().mouseReleaseEvent ( event )
    
    
    
    
    def mouseMoveEvent ( self , event ) :
        if self.mode == MODE_EDGE_DRAG :
            pos = self.mapToScene ( event.pos() )
            self.dragEdge.grEdge.setDestination ( pos.x() , pos.y() )
            self.dragEdge.grEdge.update ()
        
        
        if self.mode == MODE_EDGE_CUT :
            pos = self.mapToScene ( event.pos() )
            self.cutline.line_points.append ( pos )
            self.cutline.update ()
        
        super().mouseMoveEvent ( event )    
        
    
    def keyPressEvent ( self , event ) -> None :
        # print ( " grView :: Key Press : " )
        if event.key() == Qt.Key_Delete :
            if not self.editingFlag :
                self.deleteSelected ()
            else :
                super().keyPressEvent ( event )
                
        else :
            super().keyPressEvent ( event )
    
    
    
    
    
    def cutIntersectingEdges ( self ) :
        
        for ix in range ( len ( self.cutline.line_points ) - 1 ) :
            p1 = self.cutline.line_points [ ix ]
            p2 = self.cutline.line_points [ ix + 1 ]
            
            for edge in self.grScene.scene.edges :
                if edge.grEdge.intersectsWith ( p1 ,  p2 ) :
                    edge.remove ()    
                
                
        
    def deleteSelected ( self ) :
        for item in self.grScene.selectedItems() :
            if isinstance ( item , QDMGraphicsEdge ) :
                item.edge.remove ()
            elif hasattr ( item , "node" ) :
                item.node.remove ()

    
    
    
    def debug_modifiers ( self , event ) :
        out = "MODS : "
        if event.modifiers() & Qt.ShiftModifier : out += "SHIFT "
        if event.modifiers() & Qt.ControlModifier : out += "CTRL "
        if event.modifiers() & Qt.AltModifier : out += "ALT "
        # if event.modifiers() & Qt.MetaModifier : out += "META "
        # if event.modifiers() & Qt.KeypadModifier : out += "KEYPAD "
        # if event.modifiers() & Qt.GroupSwitchModifier : out += "GROUP "
        # if event.modifiers() & Qt.KeyboardModifier : out += "KB "
        # if event.modifiers() & Qt.MouseButtonModifier : out += "MOUSE "
        return out
        
        
        
        
           
       
        
    def getItemAtClick ( self , event ) :
        """ Return The Object Which Be Clicked On / Release On """
        pos = event.pos()
        obj = self.itemAt ( pos )
        return obj
     
     
        
    def edgeDragStart ( self , item ) :
        if DEBUG : print ( " View :: EdgeDragStart ~ Start Dragging Edge " )
        if DEBUG : print ( " View :: EdgeDragStart ~ Assign Start Socket To : " , item.socket )
        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge ( self.grScene.scene , item.socket , None , EDGE_TYPE_BEZIER )    
        if DEBUG : print ( " View :: EdgeDragStart ~ DragEdge : " , self.dragEdge )
        
        
        
        
        
    def edgeDragEnd ( self , item ) :
        """ Return True If Skip The Rest Of The Code """
        self.mode = MODE_NOOP 
        if type ( item ) is QDMGraphicsSocket :
            if item.socket != self.last_start_socket :
                if DEBUG : print ( " View :: EdgeDragEnd ~ Previous Edge : " , self.previousEdge )
                if item.socket.hasEdge () :
                    item.socket.edge.remove ()
                if DEBUG : print ( " View :: EdgeDragStart ~ Assign End Socket " , item.socket )
                if self.previousEdge is not None :
                    self.previousEdge.remove()
                if DEBUG : print ( " View :: EdgeDragEnd ~ Previous Edge Removed " )
                self.dragEdge.start_socket = self.last_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge ( self.dragEdge )
                self.dragEdge.end_socket.setConnectedEdge ( self.dragEdge )
                if DEBUG : print ( " View :: EdgeDragEnd ~ Reassign Start & End Sockets To Drag Edge " )
                self.dragEdge.updatePositions ()
                return True
        
        if DEBUG : print ( " View :: EdgeDragEnd ~ End Dragging Edge " )
        self.dragEdge.remove ()
        self.dragEdge = None
        if DEBUG : print ( " View :: EdgeDragEnd ~ About To Set Socket To Previous Edge : " , self.previousEdge )
        if self.previousEdge is not None :
            self.previousEdge.start_socket.edge = self.previousEdge 
        if DEBUG : print ( " View :: EdgeDragEnd ~ EveryThing Done. " )
        
        return False
         
         
         
                       
    
    def distanceBetweenClickAndReleaseIsOff ( self , event ) :
        """ Measures If We Are Too Far From The Last LMB Click Scene Position """
        new_lmb_release_scene_pos = self.mapToScene ( event.pos() )
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_aq = EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
        return ( dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y() ) < edge_drag_threshold_aq
    
    
    
        
    def wheelEvent ( self , event ) :
        # Calculate Out Room Factor
        zoomOutFactor = 1 / self.zoomInFactor
        
        # Store Our Acene Position
        # oldPos = self.mapToScene ( event.pos() )
        
        # Calculate Zoom
        if event.angleDelta().y() > 0 :
            zoomFactor = self.zoomInFactor
            self.zoom == self.zoomSteps
        else :
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomSteps
        
        clamped = False
        if self.zoom < self.zoomRange [ 0 ] : self.zoom , clamped = self.zoomRange [ 0 ] , True
        if self.zoom > self.zoomRange[ 1 ] : self.zoom , clamped = self.zoomRange [ 1 ] , True
        
        
        # Set Acene Scale 
        if not clamped or self.zoomClamp is False :
            self.scale ( zoomFactor , zoomFactor )
            
            
            
        # self.scale ( 1.1 , 1.1 )        
               
        # Translate Our View
        # return super().wheelEvent ( event )
        
        # newPos = self.mapToScene( event.pos() )
        # delts = newPos - oldPos
        # self.translate ( delts.x() , delts.y() ) 
        
        # self.translate ( 100.0 , 100.0 )
        
        
         