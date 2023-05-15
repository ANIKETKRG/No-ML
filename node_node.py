from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget
from node_socket import *



DEBUG = False


class Node() :
    def __init__( self , scene , title = " Undefined Node " , inputs = [ ] , outputs = [ ] ) :
        self.scene = scene
        
        
        self.title = title
        
        self.content = QDMNodeContentWidget( self )
        # self.grNode = QDMGraphicsNode( self , self.title )
        # self.grNode = QDMGraphicsNode( self , self.content )
        self.grNode = QDMGraphicsNode ( self )

        
        self.scene.addNode ( self )
        self.scene.grScene.addItem ( self.grNode )
        self.socket_spacing = 22
        # self.initInputOutputs ( inputs , outputs )
        
        # self.grNode.title = " abcd "
        
        # self.inputs = []
        # self.outputs = []
     
    # def initInputOutputs ( self , inputs , outputs ) :  
    
    # Create Socket For Inputs And Outputs 
        self.inputs = []
        self.outputs = []
        
        counter = 0
        
        for item in inputs :
            socket = Socket ( node = self , index = counter , position = LEFT_BOTTOM , socket_type = item )
            counter += 1
            self.inputs.append ( socket ) 

        counter = 0
        
        for item in outputs :
            socket = Socket ( node = self , index = counter , position = RIGHT_TOP , socket_type = item )
            counter += 1
            self.outputs.append ( socket )




    def __str__ ( self ) :
        return " < Node %s..%s> " % ( hex ( id ( self ) ) [ 2 : 5 ] , hex ( id ( self ) ) [ -3 : ] )
    
    
    @property
    
    def pos ( self ) :
        return self.grNode.pos()           # QPointF
    
    def setPos ( self , x , y ) :
        self.grNode.setPos ( x , y )


    def getSocketPosition ( self , index , position ) :
        x = 0 if ( position in ( LEFT_TOP , LEFT_BOTTOM ) ) else self.grNode.width

        if position in ( LEFT_BOTTOM , RIGHT_BOTTOM ) :
            
            # start from bottom
            y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing
        else :
            # start from top
            y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing
            
        return [ x , y ]



    


    def updateConnectedEdges ( self ) :
        for socket in self.inputs + self.outputs :
            if socket.hasEdge ( ) :
                # print ( " Updating Edge : " , socket.edge )
                socket.edge.updatePositions ( )
            # else :
            #     print ( " Socket hasn't edge " )
    
    
    def remove ( self ) :
        if DEBUG : print ( " > Removing Node " , self ) 
        if DEBUG : print ( " - Remove All Edges From Sockets " ) 
        for socket in ( self.inputs + self.outputs ) :
            if socket.hasEdge() :
                if DEBUG : print ( "      - Removing From Sockets : " , socket , " Edge : " , socket.edge )
                socket.edge.remove()
        if DEBUG : print ( " - Removing grNode " ) 
        self.scene.grScene.removeItem ( self.grNode )
        self.grNode = None
        if DEBUG : print ( " - Removing Node From The scene " )
        self.scene.removeNode ( self )
        if DEBUG : print ( " - Everything Was Done. " )    