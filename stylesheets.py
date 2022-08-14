class StyleSheetsManager(object):
    def __init__(self, parent):
        self.parent = parent
        self.dark_theme = None
        self.light_theme = '''
                #MainWindow {
                    color : black; 
                    background : rgba(255, 255, 255, 255);
                    }
                    
                #CameraLabel {
                    border : 2px solid rgba(0, 0, 0, 0);
                    alignment : center;
                    background : rgba(60, 60, 60, 250);
                    color : rgba(80, 80, 80, 255);
                    font-size : 25px;
                    font-family : Behavior;
                    text-align : center;
                }

                #RightLabel {
                    margin-top : 80px;
                    alignment : center;
                    border-radius : 20px;
                    font-size : 49px;
                    font-family : Behavior;
                    margin-right : 50px;
                    width : 720;
                    height : 480;
                    margin-top : 0px;
                    background : rgba(235, 235, 235, 250);
                    color : rgba(50, 110, 170, 235);
                }
                #RightLabel:hover {
                    background : rgba(80, 80, 80, 150);
                }
                #DropLabel {
                    padding : 100px;
                    alignment : center;
                    line-height : 10;
                    border : 5px solid rgba(0, 0, 0, 0);
                    border-radius : 20px;
                    width : 720;
                    height : 480;
                    font-size : 25px;
                    font-family : Behavior;

                    color : rgba(50, 110, 170, 255);
                    background : rgba(255, 255, 255, 50);
                }
                #DropLabel:hover {
                    background : rgba(80, 80, 80, 150);
                }

                #MenuButton {
                    border : 3px solid rgba(50, 110, 170, 255);
                    border-right : 3px solid rgba(255, 205, 0, 0);
                    border-left :3px solid rgba(255, 205, 0, 0);
                    font-size : 20px;
                    height : 30px;
                    color : rgba(120, 120, 120, 255);
                    font-family : Behavior;
                    text-align : center;
                    background : rgba(255, 255, 255, 0);
                    ToolTip.visible: hovered;
                    ToolTip.text: qsTr("выкройка");
                }
                #MenuButton:hover {
                    border : 3px solid rgba(0, 0, 0, 255);
                    border-right : 3px solid rgba(0, 255, 255, 0);
                    border-left :3px solid rgba(0, 255, 255, 0);
                }
                #MenuButton:focus{
                    border : 0px solid rgba(0, 0, 0, 255);
                    background : rgba(50, 110, 170, 255);
                    border-radius : 5px;
                    color : rgba(255, 255, 255, 255);
                }
                #MenuButton:hover:pressed{
                    background-color : rgba(40, 40, 40, 100);
                    border-radius : 5px;
                }
                #LogoLabel{
                    font-weight : bold;
                    font-size : 24px;
                    font-family : Behavior;
                    color : rgba(0, 0, 0, 150);
                    margin-left : 45px;
                    margin-right : 30px;
                }
                #LeftArea {
                    margin-left : 100px;
                }
                #LeftHistoryMessage{
                    font-weight : bold;
                    font-size : 16px;
                    padding : 5px;
                    font-family : Behavior;
                    color : rgba(255, 255, 255, 255);
                    background : rgba(50, 110, 170, 255);
                    margin-left : 35px;
                    border-radius : 10px;
                    width : 100px;
                }
                #LeftHistoryMessage:hover{
                    color : rgba(10, 70, 130, 235);
                }

                #RightHistoryMessage{
                    font-weight : bold;
                    font-size : 16px;
                    font-family : Behavior;
                    color : rgba(50, 110, 170, 235);
                    margin-top : 20px;
                    border-right : 3px solid rgba(255, 205, 0, 0);
                    border-left :3px solid rgba(255, 205, 0, 0);
                    margin-left : 50px;
                }
                #HistoryTitle{
                    font-weight : bold;
                    font-size : 24px;
                    font-family : Behavior;
                    color : rgba(0, 0, 0, 200);
                    margin-left : 30px;
                }

                #ScrollArea {
                    background : rgba(0, 0, 0, 0);
                    border-left : 0px solid rgba(0, 0, 0, 0);
                    border-right : 0px solid rgba(0, 0, 0, 0);
                    border-top : 1px solid rgba(0, 0, 0, 0);
                    
                }
                #ScrollWidget {
                    background : rgba(0, 0, 0, 0);
                    border-left : 0px solid rgba(0, 0, 0, 0);
                    border-right : 0px solid rgba(0, 0, 0, 0);
                    border-top : 3px solid rgba(0, 0, 0, 0);
                    
                }
                #HistoryTitleToolLeft{
                    font-weight : bold;
                    font-size : 18px;
                    font-family : Behavior;
                    color : rgba(0, 0, 0, 255);
                    margin-left : 35px;
                }
                #HistoryTitleToolRight{
                    font-weight : bold;
                    font-size : 18px;
                    font-family : Behavior;
                    color : rgba(0, 0, 0, 255);
                    margin-right : 250px;
                    margin-left : 40px;
                }
                #PlayButton{
                    background : rgba(0, 0, 0, 0);
                    border-radius : 5px;
                }
                #InfoTitle {
                    margin-top : 10px;
                    font-size : 15px;
                    color : rgba(0, 0, 0, 120);
                    font-family : Behavior;
                    font-weight: bold;
                }
        '''

    def setStyle(self, mode):
        if mode:
            self.parent.setStyleSheet(self.light_theme)
        else:
            self.parent.setStyleSheet(self.dark_theme)
