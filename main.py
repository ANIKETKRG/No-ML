import sys
from PyQt5.QtWidgets import *
from node_editor_wnd import NodeEditorWnd

if __name__ == "__main__" :
    # print ( " Hello Python " )
    app = QApplication ( sys.argv )
    # label = QLabel ( " Helllo, PyQt5! " )
    # label.show()
    wnd = NodeEditorWnd()
    sys.exit ( app.exec_() )    