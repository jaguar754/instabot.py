#!/usr/bin/env python
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import parameters_ui
import mainTela_ui
import login_ui
import random
import time
from src import InstaBot
from src import boostversion
from src.check_status import check_status

class MainWindow(QMainWindow, login_ui.Ui_Echo):

    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        uiLogin.setupUi(LoginQW)
        LoginQW.show()
        uiLogin.confirmarButton.clicked.connect(self.login)

    def login(self):
        self.usuario = uiLogin.loginEdit.text()
        self.senha = uiLogin.senhaEdit.text()

        #if r.text.find("batata") and self.usuario == "usuariobeta" and self.senha == "usuariobeta":
        uiParam.setupUi(ParamQW)
        uiParam.startButton.clicked.connect(self.startMain)
        ParamQW.show()
        LoginQW.hide()
        #else:
         #   QMessageBox.critical(self, "Login", "Wrong User or password", QMessageBox.Ok)

    def startMain(self):
        uiParam.label_10.setText("Verificando...")
        self.rodarThread = RodarThread()
        self.rodarThread.loggedSignal.connect(self.logarInsta)
        self.rodarThread.start()


    def logarInsta(self,boolLogging):
        if boolLogging:
            uiMain.setupUi(MainQW)
            uiMain.sairButton.clicked.connect(self.sair)
            MainQW.show()
            ParamQW.hide()
        else:
            QMessageBox.critical(self, "Login", "Wrong User or password!!", QMessageBox.Ok)
            uiParam.label_10.setText("")

    def sair(self):
        #loggof
        self.rodarThread.loggout()
        time.sleep(2)
        LoginQW.close()
        ParamQW.close()
        MainQW.close()
        self.rodarThread.terminate()

class RodarThread(QThread):
    infoBot = pyqtSignal(str)
    loggedSignal = pyqtSignal(bool)

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        # funcao pra validar os dados
        # desabilitar o botao de ok e colocar um load
        self.bot = InstaBot(
            login=uiParam.lineEdit.text(),
            password=uiParam.lineEdit_2.text(),
            like_per_day=int(uiParam.lineEdit_3.text()),
            comments_per_day=0,#int(uiParam.lineEdit_4.text()),
            tag_list=uiParam.textEdit.toPlainText().strip()[1:].replace(" ","").split("#"),
            tag_blacklist=['compras', 'promocao'],
            user_blacklist={},
            max_like_for_one_tag=26,
            follow_per_day=int(uiParam.lineEdit_5.text()),
            follow_time=1 * 60,
            unfollow_per_day=int(uiParam.lineEdit_6.text()),
            unfollow_break_min=15,
            unfollow_break_max=30,
            log_mod=0,
            proxy='',
            # List of list of words, each of which will be used to generate comment
            # For example: "This shot feels wow!"
            comment_list=[["this", "the", "your"],
                          ["photo", "picture", "pic", "shot", "snapshot"],
                          ["is", "looks", "feels", "is really"],
                          ["great", "super", "good", "very good", "good", "wow",
                           "WOW", "cool", "GREAT", "magnificent", "magical",
                           "very cool", "stylish", "beautiful", "so beautiful",
                           "so stylish", "so professional", "lovely",
                           "so lovely", "very lovely", "glorious", "so glorious",
                           "very glorious", "adorable", "excellent", "amazing"],
                          [".", "..", "...", "!", "!!", "!!!"]],
            # Use unwanted_username_list to block usernames containing a string
            ## Will do partial matches; i.e. 'mozart' will block 'legend_mozart'
            ### 'free_followers' will be blocked because it contains 'free'
            unwanted_username_list=[],
            unfollow_whitelist=[],
            UI=True)

        if self.bot.login_status:
            self.loggedSignal.emit(True)
            self.Rodar()
        else:
            self.loggedSignal.emit(False)

    def Rodar(self):
        ultimaMsg = ""
        check_status(self.bot)
        if self.bot.boostUpdated != True:
            self.bot.mandamsg = '< \n<< \n<<< \n THIS SOFTWARE MUST BE UPDATED,\n PLEASE, UPDATE YOUR INSTABOOST IN \n "https://github.com/andrewsegas/instaboost" !\n>>> \n>> \n>'
            ultimaMsg = self.mostraMsg(ultimaMsg)

        while True:

            uiMain.labelNome.setText(self.bot.user_login)
            uiMain.labelSeguindo.setText(str(self.bot.self_following))
            uiMain.labelSeguidores.setText(str(self.bot.self_follower))
            uiMain.labelLikes.setText(str(self.bot.like_counter))
            uiMain.labelComent.setText(str(self.bot.comments_counter))
            uiMain.labelFollow.setText(str(self.bot.follow_counter))
            uiMain.labelUnfollow.setText(str(self.bot.unfollow_counter))

            # ------------------- Get media_id -------------------
            if len(self.bot.media_by_tag) == 0:
                self.bot.get_media_id_by_tag(random.choice(self.bot.tag_list))
                self.bot.this_tag_like_count = 0
                self.bot.max_tag_like_count = random.randint(
                    1, self.bot.max_like_for_one_tag)
                self.bot.remove_already_liked()
            ultimaMsg = self.mostraMsg(ultimaMsg)
            # ------------------- Like -------------------
            self.bot.new_auto_mod_like()
            ultimaMsg = self.mostraMsg(ultimaMsg)
            # ------------------- Follow -------------------
            self.bot.new_auto_mod_follow()
            ultimaMsg = self.mostraMsg(ultimaMsg)
            # ------------------- Unfollow -------------------
            self.bot.new_auto_mod_unfollow()
            ultimaMsg = self.mostraMsg(ultimaMsg)
            # ------------------- Comment -------------------
            self.bot.new_auto_mod_comments()
            ultimaMsg = self.mostraMsg(ultimaMsg)

            # Bot iteration in 2 sec
            time.sleep(2 * random.random())
            # print("Tic!")
    def mostraMsg(self,ultimaMsg):

        if ultimaMsg != self.bot.mandamsg:
            uiMain.listWidget.addItem(self.bot.mandamsg,)
            ultimaMsg = self.bot.mandamsg
            #1 - like, 2- follow, 3- comentario, 4-unfollow

        return ultimaMsg
    def loggout(self):
        self.bot.logout()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    LoginQW = QWidget()
    ParamQW = QWidget()
    MainQW = QWidget()

    uiLogin = login_ui.Ui_Echo()
    uiParam = parameters_ui.Ui_Echo()
    uiMain = mainTela_ui.Ui_mainTela()

    main_window = MainWindow()
    sys.exit(app.exec_())

