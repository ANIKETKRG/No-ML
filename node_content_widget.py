from PyQt5 import QtGui
from PyQt5.QtWidgets import *


class QDMNodeContentWidget ( QWidget ) :
    def __init__ ( self , node , parent = None ) :
        self.node = node
        super().__init__( parent )

        self.initUI()

    def initUI ( self ) :
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins ( 0 , 0 , 0 , 0 )
        self.setLayout ( self.layout )

        self.wdg_label = QLabel ( "Some Title" )
        self.layout.addWidget ( self.wdg_label )
        # self.layout.addWidget ( QTextEdit ( "foo" ) )
        self.layout.addWidget ( QDMTextEdit ( "foo" ) )

    
    
    
    
    def setEditingFlag ( self , value ) :
        self.node.scene.grScene.views()[0].editingFlag = value
        self.wdg_label.setVisible ( not value )

        # print ("QDMNodeContentWidget::setEditingFlag", self._editing_flag)
        # print ("QDMNodeContentWidget::setEditingFlag", self.wdg_label.isVisible())


class QDMTextEdit ( QTextEdit ) :
    # def keyPressEvent ( self , event ) :
    #     print ( " QDMTextEdit -- KEY PRESS " )
    #     # event.ignore()
    #     super().keyPressEvent ( event )


    def focusInEvent ( self , event ) :
        # print ( " FOCUS IN EVENT " )
        self.parentWidget().setEditingFlag ( True )
        super().focusInEvent ( event )
        
        
    def focusOutEvent ( self , event ) :
        # print ( " FOCUS OUT EVENT " )
        self.parentWidget().setEditingFlag ( False )
        super().focusOutEvent ( event )     