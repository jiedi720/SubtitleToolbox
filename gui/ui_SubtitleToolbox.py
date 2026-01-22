# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SubtitleToolboxYvbWzn.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPlainTextEdit,
    QProgressBar, QPushButton, QSizePolicy, QTabWidget,
    QToolButton, QVBoxLayout, QWidget)

class Ui_SubtitleToolbox(object):
    def setupUi(self, SubtitleToolbox):
        if not SubtitleToolbox.objectName():
            SubtitleToolbox.setObjectName(u"SubtitleToolbox")
        SubtitleToolbox.resize(606, 605)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SubtitleToolbox.sizePolicy().hasHeightForWidth())
        SubtitleToolbox.setSizePolicy(sizePolicy)
        SubtitleToolbox.setMinimumSize(QSize(606, 605))
        SubtitleToolbox.setMaximumSize(QSize(606, 605))
        font = QFont()
        font.setHintingPreference(QFont.PreferDefaultHinting)
        SubtitleToolbox.setFont(font)
        SubtitleToolbox.setMouseTracking(False)
        SubtitleToolbox.setToolTipDuration(-1)
        SubtitleToolbox.setStyleSheet(u"/* \u6d45\u8272\u6a21\u5f0f */\n"
"[theme=\"light\"] QToolTip {\n"
"    background-color: #ffffff;\n"
"    color: #333333;\n"
"    border: 1px solid #cccccc;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"/* \u6df1\u8272\u6a21\u5f0f */\n"
"[theme=\"dark\"] QToolTip {\n"
"    background-color: #333333;\n"
"    color: #eeeeee;\n"
"    border: 1px solid #555555;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"}")
        SubtitleToolbox.setAnimated(True)
        self.actionLight = QAction(SubtitleToolbox)
        self.actionLight.setObjectName(u"actionLight")
        self.actionDark = QAction(SubtitleToolbox)
        self.actionDark.setObjectName(u"actionDark")
        self.actionOpenSettings = QAction(SubtitleToolbox)
        self.actionOpenSettings.setObjectName(u"actionOpenSettings")
        icon = QIcon(QIcon.fromTheme(u"document-open"))
        self.actionOpenSettings.setIcon(icon)
        font1 = QFont()
        self.actionOpenSettings.setFont(font1)
        self.actionSaveSettings = QAction(SubtitleToolbox)
        self.actionSaveSettings.setObjectName(u"actionSaveSettings")
        icon1 = QIcon(QIcon.fromTheme(u"document-save"))
        self.actionSaveSettings.setIcon(icon1)
        self.actionReadSettings = QAction(SubtitleToolbox)
        self.actionReadSettings.setObjectName(u"actionReadSettings")
        icon2 = QIcon(QIcon.fromTheme(u"document-save-as"))
        self.actionReadSettings.setIcon(icon2)
        self.centralwidget = QWidget(SubtitleToolbox)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"/* 2. \u5173\u952e\uff1a\u5c06 TabWidget \u5185\u90e8\u76f4\u63a5\u5d4c\u5957\u7684 QWidget \u8bbe\u4e3a\u900f\u660e */\n"
"/* \u53ea\u6709\u8fd9\u6837\uff0c\u9762\u677f\u7684\u989c\u8272\u624d\u80fd\u900f\u51fa\u6765 */\n"
"QTabWidget > QWidget {\n"
"    background-color: transparent;\n"
"}")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.PathLayout = QHBoxLayout()
        self.PathLayout.setSpacing(1)
        self.PathLayout.setObjectName(u"PathLayout")
        self.PathLayout.setContentsMargins(7, -1, 10, -1)
        self.PathLabel = QVBoxLayout()
        self.PathLabel.setSpacing(5)
        self.PathLabel.setObjectName(u"PathLabel")
        self.PathLabel.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.PathLabel.setContentsMargins(5, 0, 5, -1)
        self.ReadPath = QLabel(self.centralwidget)
        self.ReadPath.setObjectName(u"ReadPath")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ReadPath.sizePolicy().hasHeightForWidth())
        self.ReadPath.setSizePolicy(sizePolicy1)
        self.ReadPath.setMinimumSize(QSize(55, 30))
        self.ReadPath.setMaximumSize(QSize(55, 30))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setHintingPreference(QFont.PreferNoHinting)
        self.ReadPath.setFont(font2)
        self.ReadPath.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.PathLabel.addWidget(self.ReadPath)

        self.SavePath = QLabel(self.centralwidget)
        self.SavePath.setObjectName(u"SavePath")
        sizePolicy1.setHeightForWidth(self.SavePath.sizePolicy().hasHeightForWidth())
        self.SavePath.setSizePolicy(sizePolicy1)
        self.SavePath.setMinimumSize(QSize(55, 30))
        self.SavePath.setMaximumSize(QSize(55, 30))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setWeight(QFont.Medium)
        font3.setHintingPreference(QFont.PreferNoHinting)
        self.SavePath.setFont(font3)
        self.SavePath.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.PathLabel.addWidget(self.SavePath)


        self.PathLayout.addLayout(self.PathLabel)

        self.PathInput = QVBoxLayout()
        self.PathInput.setSpacing(5)
        self.PathInput.setObjectName(u"PathInput")
        self.ReadPathInput = QLineEdit(self.centralwidget)
        self.ReadPathInput.setObjectName(u"ReadPathInput")
        sizePolicy.setHeightForWidth(self.ReadPathInput.sizePolicy().hasHeightForWidth())
        self.ReadPathInput.setSizePolicy(sizePolicy)
        self.ReadPathInput.setMinimumSize(QSize(400, 30))
        self.ReadPathInput.setMaximumSize(QSize(400, 30))
        palette = QPalette()
        self.ReadPathInput.setPalette(palette)
        self.ReadPathInput.setAutoFillBackground(False)
        self.ReadPathInput.setStyleSheet(u"border-radius: 7px;\n"
"padding-left: 5px;")

        self.PathInput.addWidget(self.ReadPathInput)

        self.SavePathInput = QLineEdit(self.centralwidget)
        self.SavePathInput.setObjectName(u"SavePathInput")
        sizePolicy.setHeightForWidth(self.SavePathInput.sizePolicy().hasHeightForWidth())
        self.SavePathInput.setSizePolicy(sizePolicy)
        self.SavePathInput.setMinimumSize(QSize(400, 30))
        self.SavePathInput.setMaximumSize(QSize(400, 30))
        palette1 = QPalette()
        self.SavePathInput.setPalette(palette1)
        self.SavePathInput.setStyleSheet(u"border-radius: 7px;\n"
"padding-left: 5px;")

        self.PathInput.addWidget(self.SavePathInput)


        self.PathLayout.addLayout(self.PathInput)

        self.PathButton = QGridLayout()
        self.PathButton.setSpacing(5)
        self.PathButton.setObjectName(u"PathButton")
        self.PathButton.setContentsMargins(5, -1, -1, -1)
        self.ReadPathOpen = QPushButton(self.centralwidget)
        self.ReadPathOpen.setObjectName(u"ReadPathOpen")
        sizePolicy.setHeightForWidth(self.ReadPathOpen.sizePolicy().hasHeightForWidth())
        self.ReadPathOpen.setSizePolicy(sizePolicy)
        self.ReadPathOpen.setMinimumSize(QSize(30, 30))
        self.ReadPathOpen.setMaximumSize(QSize(30, 30))
        self.ReadPathOpen.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: 1px solid #bfc1c8; \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548 */\n"
"QPushButton[theme=\"light\"]:hover {\n"
"    background-color: #a0a0a0; /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton[theme=\"dark\"]:hover {\n"
"    background-color: #DEDEDE;  /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 4px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u"icons/open-folder2.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ReadPathOpen.setIcon(icon3)
        self.ReadPathOpen.setIconSize(QSize(20, 20))

        self.PathButton.addWidget(self.ReadPathOpen, 0, 3, 1, 1)

        self.ReadPathSelect = QPushButton(self.centralwidget)
        self.ReadPathSelect.setObjectName(u"ReadPathSelect")
        sizePolicy.setHeightForWidth(self.ReadPathSelect.sizePolicy().hasHeightForWidth())
        self.ReadPathSelect.setSizePolicy(sizePolicy)
        self.ReadPathSelect.setMinimumSize(QSize(30, 30))
        self.ReadPathSelect.setMaximumSize(QSize(30, 30))
        self.ReadPathSelect.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: 1px solid #bfc1c8; \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548 */\n"
"QPushButton[theme=\"light\"]:hover {\n"
"    background-color: #a0a0a0; /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton[theme=\"dark\"]:hover {\n"
"    background-color: #DEDEDE;  /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 4px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u"icons/search2.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ReadPathSelect.setIcon(icon4)
        self.ReadPathSelect.setIconSize(QSize(20, 20))

        self.PathButton.addWidget(self.ReadPathSelect, 0, 1, 1, 1)

        self.ReadPathSet = QPushButton(self.centralwidget)
        self.ReadPathSet.setObjectName(u"ReadPathSet")
        self.ReadPathSet.setEnabled(True)
        sizePolicy.setHeightForWidth(self.ReadPathSet.sizePolicy().hasHeightForWidth())
        self.ReadPathSet.setSizePolicy(sizePolicy)
        self.ReadPathSet.setMinimumSize(QSize(30, 30))
        self.ReadPathSet.setMaximumSize(QSize(30, 30))
        self.ReadPathSet.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: 1px solid #bfc1c8; \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548 */\n"
"QPushButton[theme=\"light\"]:hover {\n"
"    background-color: #a0a0a0; /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton[theme=\"dark\"]:hover {\n"
"    background-color: #DEDEDE;  /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 4px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u"icons/refresh.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ReadPathSet.setIcon(icon5)
        self.ReadPathSet.setIconSize(QSize(20, 20))

        self.PathButton.addWidget(self.ReadPathSet, 0, 0, 1, 1)

        self.SavePathOpen = QPushButton(self.centralwidget)
        self.SavePathOpen.setObjectName(u"SavePathOpen")
        sizePolicy.setHeightForWidth(self.SavePathOpen.sizePolicy().hasHeightForWidth())
        self.SavePathOpen.setSizePolicy(sizePolicy)
        self.SavePathOpen.setMinimumSize(QSize(30, 30))
        self.SavePathOpen.setMaximumSize(QSize(30, 30))
        self.SavePathOpen.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: 1px solid #bfc1c8; \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548 */\n"
"QPushButton[theme=\"light\"]:hover {\n"
"    background-color: #a0a0a0; /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton[theme=\"dark\"]:hover {\n"
"    background-color: #DEDEDE;  /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 4px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        self.SavePathOpen.setIcon(icon3)
        self.SavePathOpen.setIconSize(QSize(20, 20))

        self.PathButton.addWidget(self.SavePathOpen, 1, 3, 1, 1)

        self.SavePathSelect = QPushButton(self.centralwidget)
        self.SavePathSelect.setObjectName(u"SavePathSelect")
        sizePolicy.setHeightForWidth(self.SavePathSelect.sizePolicy().hasHeightForWidth())
        self.SavePathSelect.setSizePolicy(sizePolicy)
        self.SavePathSelect.setMinimumSize(QSize(30, 30))
        self.SavePathSelect.setMaximumSize(QSize(30, 30))
        self.SavePathSelect.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: 1px solid #bfc1c8; \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548 */\n"
"QPushButton[theme=\"light\"]:hover {\n"
"    background-color: #a0a0a0; /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton[theme=\"dark\"]:hover {\n"
"    background-color: #DEDEDE;  /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 4px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        self.SavePathSelect.setIcon(icon4)
        self.SavePathSelect.setIconSize(QSize(20, 20))

        self.PathButton.addWidget(self.SavePathSelect, 1, 1, 1, 1)

        self.SavePathSet = QPushButton(self.centralwidget)
        self.SavePathSet.setObjectName(u"SavePathSet")
        sizePolicy.setHeightForWidth(self.SavePathSet.sizePolicy().hasHeightForWidth())
        self.SavePathSet.setSizePolicy(sizePolicy)
        self.SavePathSet.setMinimumSize(QSize(30, 30))
        self.SavePathSet.setMaximumSize(QSize(30, 30))
        self.SavePathSet.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: 1px solid #bfc1c8; \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548 */\n"
"QPushButton[theme=\"light\"]:hover {\n"
"    background-color: #a0a0a0; /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton[theme=\"dark\"]:hover {\n"
"    background-color: #DEDEDE;  /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 4px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        self.SavePathSet.setIcon(icon5)
        self.SavePathSet.setIconSize(QSize(20, 20))

        self.PathButton.addWidget(self.SavePathSet, 1, 0, 1, 1)


        self.PathLayout.addLayout(self.PathButton)


        self.verticalLayout_5.addLayout(self.PathLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(11, -1, 11, -1)
        self.Function = QTabWidget(self.centralwidget)
        self.Function.setObjectName(u"Function")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.Function.sizePolicy().hasHeightForWidth())
        self.Function.setSizePolicy(sizePolicy2)
        self.Function.setMinimumSize(QSize(348, 0))
        self.Function.setMaximumSize(QSize(348, 120))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setHintingPreference(QFont.PreferDefaultHinting)
        self.Function.setFont(font4)
        self.Function.setStyleSheet(u"/* \u6574\u4f53\u5bb9\u5668\u7f8e\u5316 */\n"
"QTabWidget[theme=\"light\"]::pane {\n"
"    background-color: #DEDEDE;   \n"
"    border-radius: 9px;            \n"
"    border-top-left-radius: 0px;   \n"
"    border-top-right-radius: 0px;  \n"
"    top: 0px;                     \n"
"}\n"
"\n"
"QTabWidget[theme=\"dark\"]::pane {\n"
"    background-color: #9e9e9e;    \n"
"    border-radius: 9px;            \n"
"    border-top-left-radius: 0px;   \n"
"    border-top-right-radius: 0px;  \n"
"    top: 0px;                     \n"
"}\n"
"\n"
"/* \u6240\u6709\u6807\u7b7e\uff08\u9ed8\u8ba4\u8272\uff09\uff1a\u9ec4\u8272 */\n"
"/* \u6ce8\u610f\uff1a\u8fd9\u91cc\u4f5c\u4e3a\u9ed8\u8ba4\u503c\uff0c\u4f1a\u88ab first \u548c last \u8986\u76d6 */\n"
"QTabBar::tab { \n"
"    color: rgb(0, 0, 0);\n"
"    background-color: #FFC209;\n"
"    padding: 2px 1px;/*\u8bbe\u7f6e\u6807\u7b7e\u6587\u5b57\u4e0e\u6807\u7b7e\u8fb9\u6846\u4e4b\u95f4\u7684\u7559\u767d\u533a\u57df */\n"
"    min-width: 84px; /*\u8bbe\u7f6e\u6807\u7b7e\u7684\u6700"
                        "\u5c0f\u5bbd\u5ea6 */\n"
"    margin-right: 1px; /* \u9ed8\u8ba4\u4fdd\u7559\u8fb9\u8ddd\u7528\u4e8e\u91cd\u53e0 */\n"
"    /* \u6838\u5fc3\u4fee\u6539\uff1a\u5206\u522b\u8bbe\u7f6e\u56db\u4e2a\u89d2\u7684\u5f27\u5ea6 \u987a\u5e8f\u4e3a\uff1a\u5de6\u4e0a, \u53f3\u4e0a, \u53f3\u4e0b, \u5de6\u4e0b */\n"
"    border-top-left-radius: 9px;  \n"
"    border-top-right-radius: 9px; \n"
"    border-bottom-left-radius: 1px;\n"
"    border-bottom-right-radius: 1px;\n"
"}\n"
"\n"
"/* \u9009\u4e2d\u72b6\u6001 */\n"
"QTabBar::tab:selected {\n"
"    font-weight: bold;\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: #7953B1;\n"
"    /* 3. \u8fd9\u91cc\u7684 margin-top \u8bbe\u4e3a 0\uff0c\u914d\u5408\u57fa\u7840\u6001\u7684 2px\uff0c\u5b9e\u73b0\u76f8\u5bf9\u5347\u8d77\u6548\u679c */\n"
"    margin-top: 0px; \n"
"    /* \u518d\u6b21\u660e\u786e\u5706\u89d2\uff0c\u786e\u4fdd\u4e0d\u88ab\u9ed8\u8ba4\u6837\u5f0f\u8986\u76d6 */\n"
"    border-top-left-radius: 9px;\n"
"    border-top-right-radius: 9px;\n"
"}")
        self.Function.setElideMode(Qt.TextElideMode.ElideNone)
        self.Function.setDocumentMode(False)
        self.Function.setTabsClosable(False)
        self.Function.setMovable(False)
        self.Script = QWidget()
        self.Script.setObjectName(u"Script")
        font5 = QFont()
        font5.setHintingPreference(QFont.PreferNoHinting)
        self.Script.setFont(font5)
        self.verticalLayout_4 = QVBoxLayout(self.Script)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(5, -1, 2, -1)
        self.Output2PDF = QToolButton(self.Script)
        self.Output2PDF.setObjectName(u"Output2PDF")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.Output2PDF.sizePolicy().hasHeightForWidth())
        self.Output2PDF.setSizePolicy(sizePolicy3)
        self.Output2PDF.setMinimumSize(QSize(50, 50))
        self.Output2PDF.setMaximumSize(QSize(50, 50))
        font6 = QFont()
        font6.setPointSize(9)
        font6.setHintingPreference(QFont.PreferDefaultHinting)
        self.Output2PDF.setFont(font6)
        self.Output2PDF.setAutoFillBackground(False)
        self.Output2PDF.setStyleSheet(u"QToolButton {\n"
"    /* \u5373\u4f7f\u4e0d\u8bbe\u7f6e\u80cc\u666f\u548c\u8fb9\u6846\uff0c\u4e5f\u8981\u5728\u8fd9\u91cc\u58f0\u660e\u5706\u89d2 */\n"
"    border-radius: 9px;\n"
"    border: 1px solid #b4b7bc;     \n"
"    /* \u57fa\u7840\u5185\u8fb9\u8ddd\u548c\u5b57\u4f53 */\n"
"    padding: 4px;\n"
"    background-color: transparent; /* \u6216\u8005\u8bbe\u7f6e\u4f60\u60f3\u8981\u7684\u9ed8\u8ba4\u80cc\u666f\u8272 */\n"
"}\n"
"\n"
"/* 2. \u4f60\u539f\u672c\u7684\u60ac\u6d6e\u72b6\u6001 */\n"
"QToolButton:hover {\n"
"    background-color: #e5f1fb;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 3. \u4f60\u539f\u672c\u7684\u6309\u4e0b\u72b6\u6001 */\n"
"QToolButton:pressed {\n"
"    background-color: #cce4f7;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 4. \u4f60\u539f\u672c\u7684\u9009\u4e2d\u72b6\u6001 */\n"
"QToolButton:checked {\n"
"    background-color: #9b6be3;\n"
"    color: white;\n"
"    border: 1px solid #9b6be3;\n"
"    border-r"
                        "adius: 9px;\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u"icons/PDF.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Output2PDF.setIcon(icon6)
        self.Output2PDF.setIconSize(QSize(35, 35))
        self.Output2PDF.setCheckable(True)
        self.Output2PDF.setChecked(False)

        self.horizontalLayout_5.addWidget(self.Output2PDF)

        self.Output2Word = QToolButton(self.Script)
        self.Output2Word.setObjectName(u"Output2Word")
        sizePolicy3.setHeightForWidth(self.Output2Word.sizePolicy().hasHeightForWidth())
        self.Output2Word.setSizePolicy(sizePolicy3)
        self.Output2Word.setMinimumSize(QSize(50, 50))
        self.Output2Word.setMaximumSize(QSize(50, 50))
        font7 = QFont()
        font7.setPointSize(9)
        self.Output2Word.setFont(font7)
        self.Output2Word.setStyleSheet(u"QToolButton {\n"
"    /* \u5373\u4f7f\u4e0d\u8bbe\u7f6e\u80cc\u666f\u548c\u8fb9\u6846\uff0c\u4e5f\u8981\u5728\u8fd9\u91cc\u58f0\u660e\u5706\u89d2 */\n"
"    border-radius: 9px;\n"
"    border: 1px solid #b4b7bc;     \n"
"    /* \u57fa\u7840\u5185\u8fb9\u8ddd\u548c\u5b57\u4f53 */\n"
"    padding: 4px;\n"
"    background-color: transparent; /* \u6216\u8005\u8bbe\u7f6e\u4f60\u60f3\u8981\u7684\u9ed8\u8ba4\u80cc\u666f\u8272 */\n"
"}\n"
"\n"
"/* 2. \u4f60\u539f\u672c\u7684\u60ac\u6d6e\u72b6\u6001 */\n"
"QToolButton:hover {\n"
"    background-color: #e5f1fb;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 3. \u4f60\u539f\u672c\u7684\u6309\u4e0b\u72b6\u6001 */\n"
"QToolButton:pressed {\n"
"    background-color: #cce4f7;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 4. \u4f60\u539f\u672c\u7684\u9009\u4e2d\u72b6\u6001 */\n"
"QToolButton:checked {\n"
"    background-color: #9b6be3;\n"
"    color: white;\n"
"    border: 1px solid #9b6be3;\n"
"    border-r"
                        "adius: 9px;\n"
"}")
        icon7 = QIcon()
        icon7.addFile(u"icons/Word.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Output2Word.setIcon(icon7)
        self.Output2Word.setIconSize(QSize(35, 35))
        self.Output2Word.setCheckable(True)
        self.Output2Word.setChecked(False)

        self.horizontalLayout_5.addWidget(self.Output2Word)

        self.Output2Txt = QToolButton(self.Script)
        self.Output2Txt.setObjectName(u"Output2Txt")
        sizePolicy3.setHeightForWidth(self.Output2Txt.sizePolicy().hasHeightForWidth())
        self.Output2Txt.setSizePolicy(sizePolicy3)
        self.Output2Txt.setMinimumSize(QSize(50, 50))
        self.Output2Txt.setMaximumSize(QSize(50, 50))
        self.Output2Txt.setFont(font7)
        self.Output2Txt.setStyleSheet(u"QToolButton {\n"
"    /* \u5373\u4f7f\u4e0d\u8bbe\u7f6e\u80cc\u666f\u548c\u8fb9\u6846\uff0c\u4e5f\u8981\u5728\u8fd9\u91cc\u58f0\u660e\u5706\u89d2 */\n"
"    border-radius: 9px;\n"
"    border: 1px solid #b4b7bc;     \n"
"    /* \u57fa\u7840\u5185\u8fb9\u8ddd\u548c\u5b57\u4f53 */\n"
"    padding: 4px;\n"
"    background-color: transparent; /* \u6216\u8005\u8bbe\u7f6e\u4f60\u60f3\u8981\u7684\u9ed8\u8ba4\u80cc\u666f\u8272 */\n"
"}\n"
"\n"
"/* 2. \u4f60\u539f\u672c\u7684\u60ac\u6d6e\u72b6\u6001 */\n"
"QToolButton:hover {\n"
"    background-color: #e5f1fb;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 3. \u4f60\u539f\u672c\u7684\u6309\u4e0b\u72b6\u6001 */\n"
"QToolButton:pressed {\n"
"    background-color: #cce4f7;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 4. \u4f60\u539f\u672c\u7684\u9009\u4e2d\u72b6\u6001 */\n"
"QToolButton:checked {\n"
"    background-color: #9b6be3;\n"
"    color: white;\n"
"    border: 1px solid #9b6be3;\n"
"    border-r"
                        "adius: 9px;\n"
"}")
        icon8 = QIcon()
        icon8.addFile(u"icons/txt.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Output2Txt.setIcon(icon8)
        self.Output2Txt.setIconSize(QSize(35, 35))
        self.Output2Txt.setCheckable(True)
        self.Output2Txt.setChecked(False)

        self.horizontalLayout_5.addWidget(self.Output2Txt)

        self.Output2Md = QToolButton(self.Script)
        self.Output2Md.setObjectName(u"Output2Md")
        sizePolicy3.setHeightForWidth(self.Output2Md.sizePolicy().hasHeightForWidth())
        self.Output2Md.setSizePolicy(sizePolicy3)
        self.Output2Md.setMinimumSize(QSize(50, 50))
        self.Output2Md.setMaximumSize(QSize(50, 50))
        self.Output2Md.setFont(font7)
        self.Output2Md.setStyleSheet(u"QToolButton {\n"
"    /* \u5373\u4f7f\u4e0d\u8bbe\u7f6e\u80cc\u666f\u548c\u8fb9\u6846\uff0c\u4e5f\u8981\u5728\u8fd9\u91cc\u58f0\u660e\u5706\u89d2 */\n"
"    border-radius: 9px;\n"
"    border: 1px solid #b4b7bc;     \n"
"    /* \u57fa\u7840\u5185\u8fb9\u8ddd\u548c\u5b57\u4f53 */\n"
"    padding: 4px;\n"
"    background-color: transparent; /* \u6216\u8005\u8bbe\u7f6e\u4f60\u60f3\u8981\u7684\u9ed8\u8ba4\u80cc\u666f\u8272 */\n"
"}\n"
"\n"
"/* 2. \u4f60\u539f\u672c\u7684\u60ac\u6d6e\u72b6\u6001 */\n"
"QToolButton:hover {\n"
"    background-color: #e5f1fb;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 3. \u4f60\u539f\u672c\u7684\u6309\u4e0b\u72b6\u6001 */\n"
"QToolButton:pressed {\n"
"    background-color: #cce4f7;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 4. \u4f60\u539f\u672c\u7684\u9009\u4e2d\u72b6\u6001 */\n"
"QToolButton:checked {\n"
"    background-color: #9b6be3;\n"
"    color: white;\n"
"    border: 1px solid #9b6be3;\n"
"    border-r"
                        "adius: 9px;\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u"Icons/Markdown.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Output2Md.setIcon(icon9)
        self.Output2Md.setIconSize(QSize(35, 35))
        self.Output2Md.setCheckable(True)
        self.Output2Md.setChecked(False)

        self.horizontalLayout_5.addWidget(self.Output2Md)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(10, -1, -1, -1)
        self.DividingLine = QFrame(self.Script)
        self.DividingLine.setObjectName(u"DividingLine")
        self.DividingLine.setMinimumSize(QSize(10, 0))
        self.DividingLine.setMaximumSize(QSize(10, 70))
        self.DividingLine.setStyleSheet(u"/* \u9488\u5bf9\u6240\u6709\u7ad6\u76f4\u5206\u5272\u7ebf\u8fdb\u884c\u7f8e\u5316 */\n"
"QFrame[frameShape=\"4\"] {\n"
"    /* \u53bb\u9664\u9ed8\u8ba4\u7684 3D \u9634\u5f71 */\n"
"    border: none;\n"
"    /* \u6838\u5fc3\uff1a\u8bbe\u7f6e\u5bbd\u5ea6\u4e3a 1px */\n"
"    width: 1px;\n"
"    max-width: 1px;\n"
"    /* \u8bbe\u7f6e\u989c\u8272\uff1a\u5efa\u8bae\u4f7f\u7528\u534a\u900f\u660e\uff0c\u4f7f\u5176\u770b\u8d77\u6765\u66f4\u7ec6 */\n"
"    background-color: rgba(0, 0, 0, 50);\n"
"    /* \u5efa\u8bae\u4e0a\u4e0b\u7559\u767d\uff0c\u4e0d\u8981\u9876\u6ee1\u5e03\u5c40\uff0c\u4f1a\u66f4\u6709\u547c\u5438\u611f */\n"
"    margin-top: 5px;\n"
"    margin-bottom: 5px;\n"
"}")
        self.DividingLine.setFrameShape(QFrame.Shape.VLine)
        self.DividingLine.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_6.addWidget(self.DividingLine)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 5, -1, 10)
        self.VolumeLabel = QLabel(self.Script)
        self.VolumeLabel.setObjectName(u"VolumeLabel")
        self.VolumeLabel.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(60)
        sizePolicy4.setVerticalStretch(30)
        sizePolicy4.setHeightForWidth(self.VolumeLabel.sizePolicy().hasHeightForWidth())
        self.VolumeLabel.setSizePolicy(sizePolicy4)
        self.VolumeLabel.setMinimumSize(QSize(0, 0))
        self.VolumeLabel.setMaximumSize(QSize(50, 16777215))
        font8 = QFont()
        font8.setPointSize(11)
        font8.setBold(True)
        font8.setHintingPreference(QFont.PreferNoHinting)
        self.VolumeLabel.setFont(font8)
        self.VolumeLabel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.VolumeLabel.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.VolumeLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.VolumeLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.VolumeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.VolumeLabel.setWordWrap(False)

        self.verticalLayout_6.addWidget(self.VolumeLabel, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.VolumePatternSelect = QComboBox(self.Script)
        self.VolumePatternSelect.addItem("")
        self.VolumePatternSelect.addItem("")
        self.VolumePatternSelect.addItem("")
        self.VolumePatternSelect.setObjectName(u"VolumePatternSelect")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.VolumePatternSelect.sizePolicy().hasHeightForWidth())
        self.VolumePatternSelect.setSizePolicy(sizePolicy5)
        self.VolumePatternSelect.setMinimumSize(QSize(50, 0))
        self.VolumePatternSelect.setMaximumSize(QSize(50, 30))
        font9 = QFont()
        font9.setPointSize(10)
        font9.setBold(False)
        font9.setHintingPreference(QFont.PreferDefaultHinting)
        self.VolumePatternSelect.setFont(font9)
        self.VolumePatternSelect.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.VolumePatternSelect.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.VolumePatternSelect.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.VolumePatternSelect.setStyleSheet(u"/* 1. \u4e0b\u62c9\u6846\u4e3b\u4f53\uff08\u4fdd\u6301\u4f60\u539f\u6765\u7684\uff09 */\n"
"QComboBox {\n"
"    color: #333333;\n"
"    background-color: #F2F2F2;        \n"
"    border: 1px solid #B5B5B5;\n"
"    border-radius: 9px;\n"
"    padding: 1px 10px;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u4e0e\u6fc0\u6d3b\u72b6\u6001 */\n"
"QComboBox:hover {\n"
"    border: 2px solid #7953B1;       \n"
"}\n"
"\n"
"/* 2. \u4e0b\u62c9\u5217\u8868\u5bb9\u5668 */\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #7953B1;\n"
"    border-radius: 9px;\n"
"    background-color: #F2F2F2;\n"
"    outline: 0px;  /* \u79fb\u9664\u865a\u7ebf\u6846 */\n"
"}\n"
"\n"
"/* 3. \u6bcf\u4e00\u4e2a\u9009\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item {\n"
"    color: black;\n"
"    height: 30px; /* \u589e\u52a0\u9ad8\u5ea6\uff0c\u5706\u89d2\u624d\u597d\u770b */\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"/* 4. \u9009\u4e2d\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-co"
                        "lor: #7953B1;\n"
"    color: white;\n"
"    /* \u5982\u679c\u60f3\u8ba9\u9009\u4e2d\u7684\u9ad8\u4eae\u5757\u4e5f\u6709\u5706\u89d2\uff0c\u53ef\u4ee5\u52a0\u4e0b\u9762\u8fd9\u53e5 */\n"
"    border-radius: 5px; \n"
"}\n"
"\n"
"/*\u79fb\u9664\u4e0b\u62c9\u7bad\u5934 */\n"
"QComboBox::drop-down {\n"
"    width: 0px;                         /* \u5c06\u4e0b\u62c9\u533a\u57df\u5bbd\u5ea6\u8bbe\u4e3a0 */\n"
"    border: none;                       /* \u79fb\u9664\u53ef\u80fd\u5b58\u5728\u7684\u5206\u5272\u7ebf */\n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: none;                        /* \u660e\u786e\u4e0d\u663e\u793a\u4efb\u4f55\u56fe\u6807 */\n"
"}")
        self.VolumePatternSelect.setEditable(False)
        self.VolumePatternSelect.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        self.VolumePatternSelect.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.VolumePatternSelect.setFrame(True)

        self.verticalLayout_6.addWidget(self.VolumePatternSelect, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_6.setStretch(0, 1)
        self.verticalLayout_6.setStretch(1, 1)

        self.horizontalLayout_6.addLayout(self.verticalLayout_6)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.Function.addTab(self.Script, "")
        self.Merge = QWidget()
        self.Merge.setObjectName(u"Merge")
        self.Merge.setFont(font5)
        self.verticalLayout_2 = QVBoxLayout(self.Merge)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(20, -1, 20, -1)
        self.MergePDF = QToolButton(self.Merge)
        self.MergePDF.setObjectName(u"MergePDF")
        sizePolicy.setHeightForWidth(self.MergePDF.sizePolicy().hasHeightForWidth())
        self.MergePDF.setSizePolicy(sizePolicy)
        self.MergePDF.setMinimumSize(QSize(50, 50))
        self.MergePDF.setMaximumSize(QSize(50, 50))
        self.MergePDF.setFont(font6)
        self.MergePDF.setAutoFillBackground(False)
        self.MergePDF.setStyleSheet(u"QToolButton {\n"
"    /* \u5373\u4f7f\u4e0d\u8bbe\u7f6e\u80cc\u666f\u548c\u8fb9\u6846\uff0c\u4e5f\u8981\u5728\u8fd9\u91cc\u58f0\u660e\u5706\u89d2 */\n"
"    border-radius: 9px;\n"
"    border: 1px solid #b4b7bc;     \n"
"    /* \u57fa\u7840\u5185\u8fb9\u8ddd\u548c\u5b57\u4f53 */\n"
"    padding: 4px;\n"
"    background-color: transparent; /* \u6216\u8005\u8bbe\u7f6e\u4f60\u60f3\u8981\u7684\u9ed8\u8ba4\u80cc\u666f\u8272 */\n"
"}\n"
"\n"
"/* 2. \u4f60\u539f\u672c\u7684\u60ac\u6d6e\u72b6\u6001 */\n"
"QToolButton:hover {\n"
"    background-color: #e5f1fb;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 3. \u4f60\u539f\u672c\u7684\u6309\u4e0b\u72b6\u6001 */\n"
"QToolButton:pressed {\n"
"    background-color: #cce4f7;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 4. \u4f60\u539f\u672c\u7684\u9009\u4e2d\u72b6\u6001 */\n"
"QToolButton:checked {\n"
"    background-color: #9b6be3;\n"
"    color: white;\n"
"    border: 1px solid #9b6be3;\n"
"    border-r"
                        "adius: 9px;\n"
"}\n"
"\n"
"/* \u8fd9\u6bb5\u4ee3\u7801\u7684\u4f5c\u7528\u662f\uff1a\n"
"1. \u4e3a\u63a7\u4ef6\u63d0\u4f9b\u4e00\u4e2a\u201c\u5e95\u8272\u201d\u548c\u201c\u57fa\u7840\u5f62\u72b6\u201d\u3002\u5728\u57fa\u7840\u9009\u62e9\u5668\u4e2d\u8bbe\u7f6e border-radius \u540e\uff0c\u63a7\u4ef6\u5728\u4efb\u4f55\u65f6\u5019\u90fd\u4f1a\u4fdd\u6301\u5706\u89d2\u3002\n"
"2. \u901a\u8fc7\u8bbe\u7f6e border: 1px solid transparent\uff08\u900f\u660e\u8fb9\u6846\uff09\uff0c\u9884\u7559\u51fa\u8fb9\u6846\u5360\u4f4d\u3002\u8fd9\u6837\u5f53\u9f20\u6807\u60ac\u6d6e\u5207\u6362\u5230\u6709\u989c\u8272\u7684\u8fb9\u6846\u65f6\uff0c\u6309\u94ae\u7684\u5185\u5bb9\u4e0d\u4f1a\u56e0\u4e3a\u8fb9\u6846\u539a\u5ea6\u7684\u589e\u52a0\u800c\u53d1\u751f\u4f4d\u79fb\uff08\u907f\u514d\u95ea\u70c1\uff09\u3002")
        self.MergePDF.setIcon(icon6)
        self.MergePDF.setIconSize(QSize(35, 35))
        self.MergePDF.setCheckable(True)
        self.MergePDF.setChecked(False)

        self.horizontalLayout_2.addWidget(self.MergePDF)

        self.MergeWord = QToolButton(self.Merge)
        self.MergeWord.setObjectName(u"MergeWord")
        sizePolicy.setHeightForWidth(self.MergeWord.sizePolicy().hasHeightForWidth())
        self.MergeWord.setSizePolicy(sizePolicy)
        self.MergeWord.setMinimumSize(QSize(50, 50))
        self.MergeWord.setMaximumSize(QSize(50, 50))
        self.MergeWord.setFont(font7)
        self.MergeWord.setStyleSheet(u"QToolButton {\n"
"    /* \u5373\u4f7f\u4e0d\u8bbe\u7f6e\u80cc\u666f\u548c\u8fb9\u6846\uff0c\u4e5f\u8981\u5728\u8fd9\u91cc\u58f0\u660e\u5706\u89d2 */\n"
"    border-radius: 9px;\n"
"    border: 1px solid #b4b7bc;     \n"
"    /* \u57fa\u7840\u5185\u8fb9\u8ddd\u548c\u5b57\u4f53 */\n"
"    padding: 4px;\n"
"    background-color: transparent; /* \u6216\u8005\u8bbe\u7f6e\u4f60\u60f3\u8981\u7684\u9ed8\u8ba4\u80cc\u666f\u8272 */\n"
"}\n"
"\n"
"/* 2. \u4f60\u539f\u672c\u7684\u60ac\u6d6e\u72b6\u6001 */\n"
"QToolButton:hover {\n"
"    background-color: #e5f1fb;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 3. \u4f60\u539f\u672c\u7684\u6309\u4e0b\u72b6\u6001 */\n"
"QToolButton:pressed {\n"
"    background-color: #cce4f7;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 4. \u4f60\u539f\u672c\u7684\u9009\u4e2d\u72b6\u6001 */\n"
"QToolButton:checked {\n"
"    background-color: #9b6be3;\n"
"    color: white;\n"
"    border: 1px solid #9b6be3;\n"
"    border-r"
                        "adius: 9px;\n"
"}\n"
"\n"
"/* \u8fd9\u6bb5\u4ee3\u7801\u7684\u4f5c\u7528\u662f\uff1a\n"
"1. \u4e3a\u63a7\u4ef6\u63d0\u4f9b\u4e00\u4e2a\u201c\u5e95\u8272\u201d\u548c\u201c\u57fa\u7840\u5f62\u72b6\u201d\u3002\u5728\u57fa\u7840\u9009\u62e9\u5668\u4e2d\u8bbe\u7f6e border-radius \u540e\uff0c\u63a7\u4ef6\u5728\u4efb\u4f55\u65f6\u5019\u90fd\u4f1a\u4fdd\u6301\u5706\u89d2\u3002\n"
"2. \u901a\u8fc7\u8bbe\u7f6e border: 1px solid transparent\uff08\u900f\u660e\u8fb9\u6846\uff09\uff0c\u9884\u7559\u51fa\u8fb9\u6846\u5360\u4f4d\u3002\u8fd9\u6837\u5f53\u9f20\u6807\u60ac\u6d6e\u5207\u6362\u5230\u6709\u989c\u8272\u7684\u8fb9\u6846\u65f6\uff0c\u6309\u94ae\u7684\u5185\u5bb9\u4e0d\u4f1a\u56e0\u4e3a\u8fb9\u6846\u539a\u5ea6\u7684\u589e\u52a0\u800c\u53d1\u751f\u4f4d\u79fb\uff08\u907f\u514d\u95ea\u70c1\uff09\u3002")
        self.MergeWord.setIcon(icon7)
        self.MergeWord.setIconSize(QSize(35, 35))
        self.MergeWord.setCheckable(True)
        self.MergeWord.setChecked(False)

        self.horizontalLayout_2.addWidget(self.MergeWord)

        self.MergeTxt = QToolButton(self.Merge)
        self.MergeTxt.setObjectName(u"MergeTxt")
        sizePolicy.setHeightForWidth(self.MergeTxt.sizePolicy().hasHeightForWidth())
        self.MergeTxt.setSizePolicy(sizePolicy)
        self.MergeTxt.setMinimumSize(QSize(50, 50))
        self.MergeTxt.setMaximumSize(QSize(50, 50))
        self.MergeTxt.setFont(font7)
        self.MergeTxt.setStyleSheet(u"QToolButton {\n"
"    /* \u5373\u4f7f\u4e0d\u8bbe\u7f6e\u80cc\u666f\u548c\u8fb9\u6846\uff0c\u4e5f\u8981\u5728\u8fd9\u91cc\u58f0\u660e\u5706\u89d2 */\n"
"    border-radius: 9px;\n"
"    border: 1px solid #b4b7bc;     \n"
"    /* \u57fa\u7840\u5185\u8fb9\u8ddd\u548c\u5b57\u4f53 */\n"
"    padding: 4px;\n"
"    background-color: transparent; /* \u6216\u8005\u8bbe\u7f6e\u4f60\u60f3\u8981\u7684\u9ed8\u8ba4\u80cc\u666f\u8272 */\n"
"}\n"
"\n"
"/* 2. \u4f60\u539f\u672c\u7684\u60ac\u6d6e\u72b6\u6001 */\n"
"QToolButton:hover {\n"
"    background-color: #e5f1fb;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 3. \u4f60\u539f\u672c\u7684\u6309\u4e0b\u72b6\u6001 */\n"
"QToolButton:pressed {\n"
"    background-color: #cce4f7;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 4. \u4f60\u539f\u672c\u7684\u9009\u4e2d\u72b6\u6001 */\n"
"QToolButton:checked {\n"
"    background-color: #9b6be3;\n"
"    color: white;\n"
"    border: 1px solid #9b6be3;\n"
"    border-r"
                        "adius: 9px;\n"
"}")
        self.MergeTxt.setIcon(icon8)
        self.MergeTxt.setIconSize(QSize(35, 35))
        self.MergeTxt.setCheckable(True)
        self.MergeTxt.setChecked(False)

        self.horizontalLayout_2.addWidget(self.MergeTxt)

        self.MergeMd = QToolButton(self.Merge)
        self.MergeMd.setObjectName(u"MergeMd")
        sizePolicy3.setHeightForWidth(self.MergeMd.sizePolicy().hasHeightForWidth())
        self.MergeMd.setSizePolicy(sizePolicy3)
        self.MergeMd.setMinimumSize(QSize(50, 50))
        self.MergeMd.setMaximumSize(QSize(50, 50))
        self.MergeMd.setFont(font7)
        self.MergeMd.setStyleSheet(u"QToolButton {\n"
"    /* \u5373\u4f7f\u4e0d\u8bbe\u7f6e\u80cc\u666f\u548c\u8fb9\u6846\uff0c\u4e5f\u8981\u5728\u8fd9\u91cc\u58f0\u660e\u5706\u89d2 */\n"
"    border-radius: 9px;\n"
"    border: 1px solid #b4b7bc;     \n"
"    /* \u57fa\u7840\u5185\u8fb9\u8ddd\u548c\u5b57\u4f53 */\n"
"    padding: 4px;\n"
"    background-color: transparent; /* \u6216\u8005\u8bbe\u7f6e\u4f60\u60f3\u8981\u7684\u9ed8\u8ba4\u80cc\u666f\u8272 */\n"
"}\n"
"\n"
"/* 2. \u4f60\u539f\u672c\u7684\u60ac\u6d6e\u72b6\u6001 */\n"
"QToolButton:hover {\n"
"    background-color: #e5f1fb;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 3. \u4f60\u539f\u672c\u7684\u6309\u4e0b\u72b6\u6001 */\n"
"QToolButton:pressed {\n"
"    background-color: #cce4f7;\n"
"    border: 1px solid #9b6be3;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* 4. \u4f60\u539f\u672c\u7684\u9009\u4e2d\u72b6\u6001 */\n"
"QToolButton:checked {\n"
"    background-color: #9b6be3;\n"
"    color: white;\n"
"    border: 1px solid #9b6be3;\n"
"    border-r"
                        "adius: 9px;\n"
"}")
        self.MergeMd.setIcon(icon9)
        self.MergeMd.setIconSize(QSize(35, 35))
        self.MergeMd.setCheckable(True)
        self.MergeMd.setChecked(False)

        self.horizontalLayout_2.addWidget(self.MergeMd)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.Function.addTab(self.Merge, "")
        self.Srt2Ass = QWidget()
        self.Srt2Ass.setObjectName(u"Srt2Ass")
        self.Srt2Ass.setFont(font5)
        self.verticalLayout_9 = QVBoxLayout(self.Srt2Ass)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(8)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, 5, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.AssPatternLabel = QLabel(self.Srt2Ass)
        self.AssPatternLabel.setObjectName(u"AssPatternLabel")
        sizePolicy.setHeightForWidth(self.AssPatternLabel.sizePolicy().hasHeightForWidth())
        self.AssPatternLabel.setSizePolicy(sizePolicy)
        self.AssPatternLabel.setMinimumSize(QSize(0, 30))
        self.AssPatternLabel.setMaximumSize(QSize(16777215, 30))
        font10 = QFont()
        font10.setPointSize(11)
        font10.setWeight(QFont.DemiBold)
        font10.setHintingPreference(QFont.PreferNoHinting)
        self.AssPatternLabel.setFont(font10)
        self.AssPatternLabel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.AssPatternLabel.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.AssPatternLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.AssPatternLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.AssPatternLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.AssPatternLabel.setWordWrap(False)

        self.verticalLayout.addWidget(self.AssPatternLabel, 0, Qt.AlignmentFlag.AlignHCenter)

        self.AssPatternSelect = QComboBox(self.Srt2Ass)
        self.AssPatternSelect.addItem("")
        self.AssPatternSelect.addItem("")
        self.AssPatternSelect.addItem("")
        self.AssPatternSelect.addItem("")
        self.AssPatternSelect.setObjectName(u"AssPatternSelect")
        sizePolicy.setHeightForWidth(self.AssPatternSelect.sizePolicy().hasHeightForWidth())
        self.AssPatternSelect.setSizePolicy(sizePolicy)
        self.AssPatternSelect.setMinimumSize(QSize(80, 30))
        self.AssPatternSelect.setMaximumSize(QSize(80, 30))
        font11 = QFont()
        font11.setPointSize(10)
        self.AssPatternSelect.setFont(font11)
        self.AssPatternSelect.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.AssPatternSelect.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.AssPatternSelect.setStyleSheet(u"/* 1. \u4e0b\u62c9\u6846\u4e3b\u4f53\uff08\u4fdd\u6301\u4f60\u539f\u6765\u7684\uff09 */\n"
"QComboBox {\n"
"    color: #333333;\n"
"    background-color: #F2F2F2;        \n"
"    border: 1px solid #B5B5B5;\n"
"    border-radius: 9px;\n"
"    padding: 1px 10px;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u4e0e\u6fc0\u6d3b\u72b6\u6001 */\n"
"QComboBox:hover {\n"
"    border: 2px solid #7953B1;       \n"
"}\n"
"\n"
"/* 2. \u4e0b\u62c9\u5217\u8868\u5bb9\u5668 */\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #7953B1;\n"
"    border-radius: 9px;\n"
"    background-color: #F2F2F2;\n"
"    outline: 0px;  /* \u79fb\u9664\u865a\u7ebf\u6846 */\n"
"}\n"
"\n"
"/* 3. \u6bcf\u4e00\u4e2a\u9009\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item {\n"
"    color: black;\n"
"    height: 30px; /* \u589e\u52a0\u9ad8\u5ea6\uff0c\u5706\u89d2\u624d\u597d\u770b */\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"/* 4. \u9009\u4e2d\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-co"
                        "lor: #7953B1;\n"
"    color: white;\n"
"    /* \u5982\u679c\u60f3\u8ba9\u9009\u4e2d\u7684\u9ad8\u4eae\u5757\u4e5f\u6709\u5706\u89d2\uff0c\u53ef\u4ee5\u52a0\u4e0b\u9762\u8fd9\u53e5 */\n"
"    border-radius: 5px; \n"
"}\n"
"\n"
"/*\u79fb\u9664\u4e0b\u62c9\u7bad\u5934 */\n"
"QComboBox::drop-down {\n"
"    width: 0px;                         /* \u5c06\u4e0b\u62c9\u533a\u57df\u5bbd\u5ea6\u8bbe\u4e3a0 */\n"
"    border: none;                       /* \u79fb\u9664\u53ef\u80fd\u5b58\u5728\u7684\u5206\u5272\u7ebf */\n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: none;                        /* \u660e\u786e\u4e0d\u663e\u793a\u4efb\u4f55\u56fe\u6807 */\n"
"}")
        self.AssPatternSelect.setEditable(False)

        self.verticalLayout.addWidget(self.AssPatternSelect, 0, Qt.AlignmentFlag.AlignHCenter)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.DividingLine_2 = QFrame(self.Srt2Ass)
        self.DividingLine_2.setObjectName(u"DividingLine_2")
        self.DividingLine_2.setMinimumSize(QSize(10, 0))
        self.DividingLine_2.setMaximumSize(QSize(10, 70))
        self.DividingLine_2.setStyleSheet(u"/* \u9488\u5bf9\u6240\u6709\u7ad6\u76f4\u5206\u5272\u7ebf\u8fdb\u884c\u7f8e\u5316 */\n"
"QFrame[frameShape=\"4\"] {\n"
"    /* \u53bb\u9664\u9ed8\u8ba4\u7684 3D \u9634\u5f71 */\n"
"    border: none;\n"
"    /* \u6838\u5fc3\uff1a\u8bbe\u7f6e\u5bbd\u5ea6\u4e3a 1px */\n"
"    width: 1px;\n"
"    max-width: 1px;\n"
"    /* \u8bbe\u7f6e\u989c\u8272\uff1a\u5efa\u8bae\u4f7f\u7528\u534a\u900f\u660e\uff0c\u4f7f\u5176\u770b\u8d77\u6765\u66f4\u7ec6 */\n"
"    background-color: rgba(0, 0, 0, 50);\n"
"    /* \u5efa\u8bae\u4e0a\u4e0b\u7559\u767d\uff0c\u4e0d\u8981\u9876\u6ee1\u5e03\u5c40\uff0c\u4f1a\u66f4\u6709\u547c\u5438\u611f */\n"
"    margin-top: 5px;\n"
"    margin-bottom: 5px;\n"
"}")
        self.DividingLine_2.setFrameShape(QFrame.Shape.VLine)
        self.DividingLine_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.DividingLine_2)

        self.Vtt2SrtDrop = QLabel(self.Srt2Ass)
        self.Vtt2SrtDrop.setObjectName(u"Vtt2SrtDrop")
        sizePolicy.setHeightForWidth(self.Vtt2SrtDrop.sizePolicy().hasHeightForWidth())
        self.Vtt2SrtDrop.setSizePolicy(sizePolicy)
        self.Vtt2SrtDrop.setMinimumSize(QSize(0, 70))
        self.Vtt2SrtDrop.setMaximumSize(QSize(180, 70))
        font12 = QFont()
        font12.setPointSize(11)
        font12.setBold(False)
        font12.setHintingPreference(QFont.PreferNoHinting)
        self.Vtt2SrtDrop.setFont(font12)
        self.Vtt2SrtDrop.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.Vtt2SrtDrop.setStyleSheet(u"/* \u9ed8\u8ba4\u6837\u5f0f (\u4f60\u7684\u57fa\u7840\u6837\u5f0f) */\n"
"QFrame {\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: #f0f0f0;\n"
"    border: 2px solid #7953B1;\n"
"    border-radius: 9px;\n"
"    padding: 5px 15px;\n"
"}\n"
"\n"
"/* \u62d6\u62fd\u60ac\u6d6e\u65f6\u7684\u7279\u6548\u6837\u5f0f */\n"
"QFrame[active=\"true\"] {\n"
"    background-color: #e0d4f7;  /* \u80cc\u666f\u53d8\u6210\u6d45\u7d2b\u8272\uff0c\u6697\u793a\u53ef\u653e\u5165 */\n"
"    border: 3px solid #9b72cf;  /* \u8fb9\u6846\u52a0\u7c97\u5e76\u4eae\u5316 */\n"
"}")
        self.Vtt2SrtDrop.setFrameShape(QFrame.Shape.NoFrame)
        self.Vtt2SrtDrop.setTextFormat(Qt.TextFormat.PlainText)
        self.Vtt2SrtDrop.setScaledContents(False)
        self.Vtt2SrtDrop.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Vtt2SrtDrop.setWordWrap(True)

        self.horizontalLayout_3.addWidget(self.Vtt2SrtDrop)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(2, 3)

        self.verticalLayout_9.addLayout(self.horizontalLayout_3)

        self.Function.addTab(self.Srt2Ass, "")
        self.AutoSub = QWidget()
        self.AutoSub.setObjectName(u"AutoSub")
        self.verticalLayout_8 = QVBoxLayout(self.AutoSub)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(10)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(10, -1, -1, -1)
        self.WhisperModelLabel = QLabel(self.AutoSub)
        self.WhisperModelLabel.setObjectName(u"WhisperModelLabel")
        sizePolicy.setHeightForWidth(self.WhisperModelLabel.sizePolicy().hasHeightForWidth())
        self.WhisperModelLabel.setSizePolicy(sizePolicy)
        self.WhisperModelLabel.setMinimumSize(QSize(0, 30))
        self.WhisperModelLabel.setMaximumSize(QSize(16777215, 30))
        self.WhisperModelLabel.setFont(font10)
        self.WhisperModelLabel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.WhisperModelLabel.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.WhisperModelLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.WhisperModelLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.WhisperModelLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.WhisperModelLabel)

        self.SelectWhisperModel = QPushButton(self.AutoSub)
        self.SelectWhisperModel.setObjectName(u"SelectWhisperModel")
        self.SelectWhisperModel.setMinimumSize(QSize(30, 30))
        self.SelectWhisperModel.setMaximumSize(QSize(30, 30))
        self.SelectWhisperModel.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: 1px solid #bfc1c8; \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548 */\n"
"QPushButton[theme=\"light\"]:hover {\n"
"    background-color: #a0a0a0; /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton[theme=\"dark\"]:hover {\n"
"    background-color: #DEDEDE;  /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 4px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        self.SelectWhisperModel.setIcon(icon4)
        self.SelectWhisperModel.setIconSize(QSize(20, 20))

        self.horizontalLayout_8.addWidget(self.SelectWhisperModel, 0, Qt.AlignmentFlag.AlignLeft)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.WhisperModelSelect = QComboBox(self.AutoSub)
        self.WhisperModelSelect.addItem("")
        self.WhisperModelSelect.addItem("")
        self.WhisperModelSelect.addItem("")
        self.WhisperModelSelect.setObjectName(u"WhisperModelSelect")
        sizePolicy.setHeightForWidth(self.WhisperModelSelect.sizePolicy().hasHeightForWidth())
        self.WhisperModelSelect.setSizePolicy(sizePolicy)
        self.WhisperModelSelect.setMinimumSize(QSize(208, 30))
        self.WhisperModelSelect.setMaximumSize(QSize(208, 30))
        self.WhisperModelSelect.setFont(font11)
        self.WhisperModelSelect.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.WhisperModelSelect.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.WhisperModelSelect.setStyleSheet(u"/* 1. \u4e0b\u62c9\u6846\u4e3b\u4f53\uff08\u4fdd\u6301\u4f60\u539f\u6765\u7684\uff09 */\n"
"QComboBox {\n"
"    color: #333333;\n"
"    background-color: #F2F2F2;        \n"
"    border: 1px solid #B5B5B5;\n"
"    border-radius: 9px;\n"
"    padding: 1px 10px;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u4e0e\u6fc0\u6d3b\u72b6\u6001 */\n"
"QComboBox:hover {\n"
"    border: 2px solid #7953B1;       \n"
"}\n"
"\n"
"/* 2. \u4e0b\u62c9\u5217\u8868\u5bb9\u5668 */\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #7953B1;\n"
"    border-radius: 9px;\n"
"    background-color: #F2F2F2;\n"
"    outline: 0px;  /* \u79fb\u9664\u865a\u7ebf\u6846 */\n"
"}\n"
"\n"
"/* 3. \u6bcf\u4e00\u4e2a\u9009\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item {\n"
"    color: black;\n"
"    height: 30px; /* \u589e\u52a0\u9ad8\u5ea6\uff0c\u5706\u89d2\u624d\u597d\u770b */\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"/* 4. \u9009\u4e2d\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-co"
                        "lor: #7953B1;\n"
"    color: white;\n"
"    /* \u5982\u679c\u60f3\u8ba9\u9009\u4e2d\u7684\u9ad8\u4eae\u5757\u4e5f\u6709\u5706\u89d2\uff0c\u53ef\u4ee5\u52a0\u4e0b\u9762\u8fd9\u53e5 */\n"
"    border-radius: 5px; \n"
"}\n"
"\n"
"/*\u79fb\u9664\u4e0b\u62c9\u7bad\u5934 */\n"
"QComboBox::drop-down {\n"
"    width: 0px;                         /* \u5c06\u4e0b\u62c9\u533a\u57df\u5bbd\u5ea6\u8bbe\u4e3a0 */\n"
"    border: none;                       /* \u79fb\u9664\u53ef\u80fd\u5b58\u5728\u7684\u5206\u5272\u7ebf */\n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: none;                        /* \u660e\u786e\u4e0d\u663e\u793a\u4efb\u4f55\u56fe\u6807 */\n"
"}")
        self.WhisperModelSelect.setEditable(False)

        self.verticalLayout_3.addWidget(self.WhisperModelSelect)


        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 2, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(10)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.WhisperEngineLabel = QLabel(self.AutoSub)
        self.WhisperEngineLabel.setObjectName(u"WhisperEngineLabel")
        sizePolicy.setHeightForWidth(self.WhisperEngineLabel.sizePolicy().hasHeightForWidth())
        self.WhisperEngineLabel.setSizePolicy(sizePolicy)
        self.WhisperEngineLabel.setMinimumSize(QSize(0, 30))
        self.WhisperEngineLabel.setMaximumSize(QSize(16777215, 30))
        self.WhisperEngineLabel.setFont(font10)
        self.WhisperEngineLabel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.WhisperEngineLabel.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.WhisperEngineLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.WhisperEngineLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.WhisperEngineLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.WhisperEngineLabel)

        self.WhisperEngineSelect = QComboBox(self.AutoSub)
        self.WhisperEngineSelect.addItem("")
        self.WhisperEngineSelect.addItem("")
        self.WhisperEngineSelect.setObjectName(u"WhisperEngineSelect")
        sizePolicy.setHeightForWidth(self.WhisperEngineSelect.sizePolicy().hasHeightForWidth())
        self.WhisperEngineSelect.setSizePolicy(sizePolicy)
        self.WhisperEngineSelect.setMinimumSize(QSize(50, 30))
        self.WhisperEngineSelect.setMaximumSize(QSize(50, 30))
        self.WhisperEngineSelect.setFont(font11)
        self.WhisperEngineSelect.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.WhisperEngineSelect.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.WhisperEngineSelect.setStyleSheet(u"/* 1. \u4e0b\u62c9\u6846\u4e3b\u4f53\uff08\u4fdd\u6301\u4f60\u539f\u6765\u7684\uff09 */\n"
"QComboBox {\n"
"    color: #333333;\n"
"    background-color: #F2F2F2;        \n"
"    border: 1px solid #B5B5B5;\n"
"    border-radius: 9px;\n"
"    padding: 1px 10px;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u4e0e\u6fc0\u6d3b\u72b6\u6001 */\n"
"QComboBox:hover {\n"
"    border: 2px solid #7953B1;       \n"
"}\n"
"\n"
"/* 2. \u4e0b\u62c9\u5217\u8868\u5bb9\u5668 */\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #7953B1;\n"
"    border-radius: 9px;\n"
"    background-color: #F2F2F2;\n"
"    outline: 0px;  /* \u79fb\u9664\u865a\u7ebf\u6846 */\n"
"}\n"
"\n"
"/* 3. \u6bcf\u4e00\u4e2a\u9009\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item {\n"
"    color: black;\n"
"    height: 30px; /* \u589e\u52a0\u9ad8\u5ea6\uff0c\u5706\u89d2\u624d\u597d\u770b */\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"/* 4. \u9009\u4e2d\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-co"
                        "lor: #7953B1;\n"
"    color: white;\n"
"    /* \u5982\u679c\u60f3\u8ba9\u9009\u4e2d\u7684\u9ad8\u4eae\u5757\u4e5f\u6709\u5706\u89d2\uff0c\u53ef\u4ee5\u52a0\u4e0b\u9762\u8fd9\u53e5 */\n"
"    border-radius: 5px; \n"
"}\n"
"\n"
"/*\u79fb\u9664\u4e0b\u62c9\u7bad\u5934 */\n"
"QComboBox::drop-down {\n"
"    width: 0px;                         /* \u5c06\u4e0b\u62c9\u533a\u57df\u5bbd\u5ea6\u8bbe\u4e3a0 */\n"
"    border: none;                       /* \u79fb\u9664\u53ef\u80fd\u5b58\u5728\u7684\u5206\u5272\u7ebf */\n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: none;                        /* \u660e\u786e\u4e0d\u663e\u793a\u4efb\u4f55\u56fe\u6807 */\n"
"}")
        self.WhisperEngineSelect.setEditable(False)

        self.horizontalLayout_9.addWidget(self.WhisperEngineSelect)


        self.gridLayout.addLayout(self.horizontalLayout_9, 0, 1, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.WhisperLanguageLabel = QLabel(self.AutoSub)
        self.WhisperLanguageLabel.setObjectName(u"WhisperLanguageLabel")
        sizePolicy.setHeightForWidth(self.WhisperLanguageLabel.sizePolicy().hasHeightForWidth())
        self.WhisperLanguageLabel.setSizePolicy(sizePolicy)
        self.WhisperLanguageLabel.setMinimumSize(QSize(0, 30))
        self.WhisperLanguageLabel.setMaximumSize(QSize(16777215, 30))
        self.WhisperLanguageLabel.setFont(font10)
        self.WhisperLanguageLabel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.WhisperLanguageLabel.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.WhisperLanguageLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.WhisperLanguageLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.WhisperLanguageLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.WhisperLanguageLabel)

        self.WhisperLanguageSelect = QComboBox(self.AutoSub)
        self.WhisperLanguageSelect.addItem("")
        self.WhisperLanguageSelect.addItem("")
        self.WhisperLanguageSelect.addItem("")
        self.WhisperLanguageSelect.addItem("")
        self.WhisperLanguageSelect.addItem("")
        self.WhisperLanguageSelect.setObjectName(u"WhisperLanguageSelect")
        sizePolicy.setHeightForWidth(self.WhisperLanguageSelect.sizePolicy().hasHeightForWidth())
        self.WhisperLanguageSelect.setSizePolicy(sizePolicy)
        self.WhisperLanguageSelect.setMinimumSize(QSize(50, 30))
        self.WhisperLanguageSelect.setMaximumSize(QSize(50, 30))
        self.WhisperLanguageSelect.setFont(font11)
        self.WhisperLanguageSelect.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.WhisperLanguageSelect.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.WhisperLanguageSelect.setStyleSheet(u"/* 1. \u4e0b\u62c9\u6846\u4e3b\u4f53\uff08\u4fdd\u6301\u4f60\u539f\u6765\u7684\uff09 */\n"
"QComboBox {\n"
"    color: #333333;\n"
"    background-color: #F2F2F2;        \n"
"    border: 1px solid #B5B5B5;\n"
"    border-radius: 9px;\n"
"    padding: 1px 10px;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u4e0e\u6fc0\u6d3b\u72b6\u6001 */\n"
"QComboBox:hover {\n"
"    border: 2px solid #7953B1;       \n"
"}\n"
"\n"
"/* 2. \u4e0b\u62c9\u5217\u8868\u5bb9\u5668 */\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #7953B1;\n"
"    border-radius: 9px;\n"
"    background-color: #F2F2F2;\n"
"    outline: 0px;  /* \u79fb\u9664\u865a\u7ebf\u6846 */\n"
"}\n"
"\n"
"/* 3. \u6bcf\u4e00\u4e2a\u9009\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item {\n"
"    color: black;\n"
"    height: 30px; /* \u589e\u52a0\u9ad8\u5ea6\uff0c\u5706\u89d2\u624d\u597d\u770b */\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"/* 4. \u9009\u4e2d\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-co"
                        "lor: #7953B1;\n"
"    color: white;\n"
"    /* \u5982\u679c\u60f3\u8ba9\u9009\u4e2d\u7684\u9ad8\u4eae\u5757\u4e5f\u6709\u5706\u89d2\uff0c\u53ef\u4ee5\u52a0\u4e0b\u9762\u8fd9\u53e5 */\n"
"    border-radius: 5px; \n"
"}\n"
"\n"
"/*\u79fb\u9664\u4e0b\u62c9\u7bad\u5934 */\n"
"QComboBox::drop-down {\n"
"    width: 0px;                         /* \u5c06\u4e0b\u62c9\u533a\u57df\u5bbd\u5ea6\u8bbe\u4e3a0 */\n"
"    border: none;                       /* \u79fb\u9664\u53ef\u80fd\u5b58\u5728\u7684\u5206\u5272\u7ebf */\n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: none;                        /* \u660e\u786e\u4e0d\u663e\u793a\u4efb\u4f55\u56fe\u6807 */\n"
"}")
        self.WhisperLanguageSelect.setEditable(False)

        self.horizontalLayout_4.addWidget(self.WhisperLanguageSelect)


        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)


        self.verticalLayout_8.addLayout(self.gridLayout)

        self.Function.addTab(self.AutoSub, "")

        self.horizontalLayout.addWidget(self.Function)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.Stop = QPushButton(self.centralwidget)
        self.Stop.setObjectName(u"Stop")
        sizePolicy2.setHeightForWidth(self.Stop.sizePolicy().hasHeightForWidth())
        self.Stop.setSizePolicy(sizePolicy2)
        self.Stop.setMinimumSize(QSize(0, 55))
        self.Stop.setMaximumSize(QSize(16777215, 55))
        font13 = QFont()
        font13.setPointSize(12)
        font13.setWeight(QFont.DemiBold)
        font13.setKerning(True)
        font13.setHintingPreference(QFont.PreferNoHinting)
        self.Stop.setFont(font13)
        self.Stop.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"color: rgb(0, 0, 0);\n"
"background-color: #f6416c;\n"
"border-radius: 9px;\n"
"padding: 5px 15px;\n"
"border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"background-color: rgb(255, 102, 117);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 5px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u"Icons/stop.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Stop.setIcon(icon10)
        self.Stop.setIconSize(QSize(30, 30))
        self.Stop.setCheckable(False)
        self.Stop.setChecked(False)

        self.gridLayout_2.addWidget(self.Stop, 0, 1, 1, 1)

        self.Start = QPushButton(self.centralwidget)
        self.Start.setObjectName(u"Start")
        sizePolicy2.setHeightForWidth(self.Start.sizePolicy().hasHeightForWidth())
        self.Start.setSizePolicy(sizePolicy2)
        self.Start.setMinimumSize(QSize(0, 55))
        self.Start.setMaximumSize(QSize(16777215, 55))
        self.Start.setFont(font13)
        self.Start.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: rgb(0, 0, 0);\n"
"    background-color:#00b8a9;\n"
"    border-radius: 9px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(0, 214, 196); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 5px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        icon11 = QIcon()
        icon11.addFile(u"icons/shuttle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Start.setIcon(icon11)
        self.Start.setIconSize(QSize(30, 30))
        self.Start.setCheckable(False)
        self.Start.setChecked(False)

        self.gridLayout_2.addWidget(self.Start, 0, 0, 1, 1)

        self.ClearLogs = QPushButton(self.centralwidget)
        self.ClearLogs.setObjectName(u"ClearLogs")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.ClearLogs.sizePolicy().hasHeightForWidth())
        self.ClearLogs.setSizePolicy(sizePolicy6)
        self.ClearLogs.setMinimumSize(QSize(0, 55))
        self.ClearLogs.setMaximumSize(QSize(16777215, 55))
        self.ClearLogs.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: #f8f3d4;\n"
"    border-radius: 9px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(218, 213, 186); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 8px;\n"
"}\n"
"\n"
"")
        icon12 = QIcon()
        icon12.addFile(u"icons/broom.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ClearLogs.setIcon(icon12)
        self.ClearLogs.setIconSize(QSize(40, 40))

        self.gridLayout_2.addWidget(self.ClearLogs, 1, 0, 1, 1)

        self.DeleteFiles = QPushButton(self.centralwidget)
        self.DeleteFiles.setObjectName(u"DeleteFiles")
        sizePolicy6.setHeightForWidth(self.DeleteFiles.sizePolicy().hasHeightForWidth())
        self.DeleteFiles.setSizePolicy(sizePolicy6)
        self.DeleteFiles.setMinimumSize(QSize(0, 55))
        self.DeleteFiles.setMaximumSize(QSize(16777215, 55))
        self.DeleteFiles.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: #ffde7d;\n"
"    border-radius: 9px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(255, 234, 152); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 8px;\n"
"}\n"
"\n"
"\n"
"")
        icon13 = QIcon()
        icon13.addFile(u"icons/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.DeleteFiles.setIcon(icon13)
        self.DeleteFiles.setIconSize(QSize(30, 30))

        self.gridLayout_2.addWidget(self.DeleteFiles, 1, 1, 1, 1)

        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setColumnStretch(0, 1)

        self.horizontalLayout.addLayout(self.gridLayout_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.verticalLayout_Log = QVBoxLayout()
        self.verticalLayout_Log.setSpacing(10)
        self.verticalLayout_Log.setObjectName(u"verticalLayout_Log")
        self.verticalLayout_Log.setContentsMargins(11, 0, 11, 11)
        self.ProgressBar = QProgressBar(self.centralwidget)
        self.ProgressBar.setObjectName(u"ProgressBar")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.ProgressBar.sizePolicy().hasHeightForWidth())
        self.ProgressBar.setSizePolicy(sizePolicy7)
        self.ProgressBar.setMinimumSize(QSize(400, 15))
        self.ProgressBar.setMaximumSize(QSize(16777215, 15))
        self.ProgressBar.setStyleSheet(u"/* \u8fdb\u5ea6\u6761\u80cc\u666f\u69fd */\n"
"QProgressBar {\n"
"    border: none;                /* \u53bb\u6389\u8fb9\u6846 */\n"
"    color: white;                /* \u767e\u5206\u6bd4\u6587\u5b57\u989c\u8272 */\n"
"    text-align: center;          /* \u6587\u5b57\u5c45\u4e2d */\n"
"    background: #e0e0e0;         /* \u69fd\u7684\u80cc\u666f\u8272 */\n"
"    border-radius: 7px;          /* \u5706\u89d2\u9ad8\u5ea6\u7684\u4e00\u534a\u901a\u5e38\u770b\u8d77\u6765\u5f88\u8212\u670d */\n"
"    height: 10px;                /* \u8fd9\u91cc\u7684 height \u4f1a\u5f71\u54cd\u69fd\u7684\u7c97\u7ec6 */\n"
"}\n"
"\n"
"/* \u5df2\u586b\u5145\u7684\u8fdb\u5ea6\u90e8\u5206 */\n"
"QProgressBar::chunk {\n"
"    background-color: #05B8CC;   /* \u8fdb\u5ea6\u6761\u989c\u8272\uff1a\u9752\u84dd\u8272 */\n"
"    border-radius: 7px;          /* \u8fdb\u5ea6\u6761\u7684\u5706\u89d2 */\n"
"}")
        self.ProgressBar.setValue(24)
        self.ProgressBar.setTextVisible(False)
        self.ProgressBar.setOrientation(Qt.Orientation.Horizontal)
        self.ProgressBar.setInvertedAppearance(False)

        self.verticalLayout_Log.addWidget(self.ProgressBar)

        self.Log = QPlainTextEdit(self.centralwidget)
        self.Log.setObjectName(u"Log")
        self.Log.setMinimumSize(QSize(400, 300))
        self.Log.setMaximumSize(QSize(16777215, 600))
        self.Log.setStyleSheet(u"QPlainTextEdit {\n"
"    /* 1. \u5fc5\u987b\u6709\u8fb9\u6846\uff0c\u900f\u660e\u5373\u53ef */\n"
"    border: 1px solid transparent;\n"
"    border-radius: 9px;\n"
"    /* 1. \u663e\u5f0f\u58f0\u660e background\uff0c\u4e0d\u8981\u53ea\u7528 background-color */\n"
"    background: palette(base);\n"
"    /* 3. \u6838\u5fc3\uff1a\u5fc5\u987b\u5b9a\u4e49\u80cc\u666f\u8272\uff0c\u5706\u89d2\u624d\u80fd\u88ab\u201c\u586b\u5145\u201d\u51fa\u6765 */\n"
"    /* palette(base) \u4f1a\u81ea\u52a8\u8ddf\u968f\u4e3b\u9898\uff1a\u6d45\u8272\u65f6\u662f\u767d\u8272\uff0c\u6df1\u8272\u65f6\u662f\u6df1\u7070 */\n"
"    background-color: palette(base);\n"
"    \n"
"    /* 4. \u6587\u5b57\u989c\u8272\u4e5f\u8ddf\u968f\u4e3b\u9898 */\n"
"    color: palette(text);\n"
"    \n"
"    /* \u5efa\u8bae\u52a0\u70b9\u5185\u8fb9\u8ddd\uff0c\u5426\u5219\u5b57\u4f1a\u8d34\u5230\u5706\u89d2\u8fb9\u4e0a */\n"
"    padding: 3px;\n"
"}\n"
"\n"
"/* \u57fa\u7840\u83dc\u5355\u6837\u5f0f  */\n"
"QMenu {\n"
"    border: 1px solid #dcdcdc; /*\u589e\u52a0"
                        "\u8fb9\u6846\uff0c\u9632\u6b62\u83dc\u5355\u4e0e\u80cc\u666f\u878d\u4e3a\u4e00\u4f53 */\n"
"    padding: 4px;              /* \u83dc\u5355\u5185\u90e8\u56db\u5468\u7559\u767d */\n"
" }  \n"
"\n"
"/* \u6df1\u8272\u6a21\u5f0f\u7ec6\u5316 */\n"
"[theme=\"dark\"] QMenu {\n"
"    color: #eeeeee;\n"
"    background-color: #2b2b2b; /* \u4f7f\u7528\u6df1\u7070\u8272\u6bd4\u7eaf\u9ed1\u66f4\u5177\u9ad8\u7ea7\u611f */\n"
"    border-color: #555555; \n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* \u6d45\u8272\u6a21\u5f0f\u7ec6\u5316 */\n"
"[theme=\"light\"] QMenu {\n"
"    color: #333333;\n"
"    background-color: #ffffff;\n"
"    border-color: #cccccc;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* \u83dc\u5355\u9879\u6574\u4f53\u6837\u5f0f */\n"
"QMenu::item {\n"
"    padding: 6px 25px 6px 20px; /* \u589e\u52a0\u70b9\u51fb\u533a\u57df\u5927\u5c0f */\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"/* \u9009\u4e2d/\u60ac\u505c\u72b6\u6001 */\n"
"QMenu::item:selected {\n"
"    background-color: #FFC209; /* \u9ec4\u8272\u9009\u4e2d"
                        "\u6548\u679c\uff0c\u66f4\u7b26\u5408\u4e3b\u6d41\u5ba1\u7f8e */\n"
"    color: black;              /* \u786e\u4fdd\u9009\u4e2d\u65f6\u6587\u5b57\u4f9d\u7136\u6e05\u6670 */\n"
"}\n"
"\n"
"/* \u7981\u7528\u72b6\u6001\uff08\u6bd4\u5982\u6ca1\u6709\u5185\u5bb9\u53ef\u7c98\u8d34\u65f6\uff09 */\n"
"QMenu::item:disabled {\n"
"    color: #888888;\n"
"}")

        self.verticalLayout_Log.addWidget(self.Log)


        self.verticalLayout_5.addLayout(self.verticalLayout_Log)

        SubtitleToolbox.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(SubtitleToolbox)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 606, 29))
        self.menuBar.setStyleSheet(u"/* \u7edf\u4e00\u8bbe\u7f6e\u6240\u6709\u9879\u7684\u9ed8\u8ba4\u72b6\u6001 */\n"
"QMenuBar::item {\n"
"    padding-left: 20px;\n"
"    padding-right: 20px;\n"
"    padding-top: 5px;\n"
"    padding-bottom: 5px;\n"
"    /* \u5173\u952e\uff1a\u9ed8\u8ba4\u4e5f\u7ed91px\u8fb9\u6846\uff0c\u4f46\u989c\u8272\u8bbe\u4e3a\u900f\u660e\uff0c\u9632\u6b62\u70b9\u51fb\u65f6\u6587\u5b57\u6296\u52a8 */\n"
"    border: 1px solid transparent; \n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"/* \u83dc\u5355\u680f\u6574\u4f53\u6837\u5f0f */\n"
"QMenuBar {\n"
"    border-bottom: 1px solid #dcdcdc; /* \u8fd9\u5c31\u662f\u90a3\u6761\u6d45\u7070\u8272\u7684\u7ebf */\n"
"    padding: 0px; /* \u589e\u52a0\u4e00\u70b9\u5185\u8fb9\u8ddd\uff0c\u8ba9\u83dc\u5355\u9879\u4e0d\u7d27\u8d34\u8fb9\u6846 */\n"
"}\n"
"\n"
"/* \u6d45\u8272\u4e3b\u9898\u4e0b\u7684\u6309\u4e0b\u6548\u679c */\n"
"QMenuBar[theme=\"light\"]::item:pressed {\n"
"    background: #e0e0e0; \n"
"    border: 1px solid transparent;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"/* \u6df1"
                        "\u8272\u4e3b\u9898\u4e0b\u7684\u6309\u4e0b\u6548\u679c */\n"
"QMenuBar[theme=\"dark\"]::item:pressed {\n"
"	color: rgb(255, 255, 255);\n"
"    background: #989898; \n"
"    border: 1px solid transparent;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"/* \u4e0b\u62c9\u83dc\u5355\u6837\u5f0f */\n"
"QMenu {\n"
"    padding-left: 2px;\n"
"    padding-right: 2px;\n"
"    padding-top: 2px;\n"
"    border: 1px solid #e0e0e0;\n"
"    border-radius: 9px;  \n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"    background-color: #FFC209;\n"
"    color: black; /* \u663e\u5f0f\u8bbe\u7f6e\u6587\u5b57\u989c\u8272\uff0c\u9632\u6b62\u88ab\u539f\u751f\u53cd\u8272\u8986\u76d6 */\n"
"    border: 1px solid #FFC209; /* \u5173\u952e\uff1a\u52a0\u4e0a\u8fb9\u6846\uff0c\u54ea\u6015\u989c\u8272\u548c\u80cc\u666f\u4e00\u6837 */\n"
"    border-radius: 4px; /* \u8ba9\u9009\u4e2d\u7684\u9ad8\u4eae\u5757\u4e5f\u6709\u5706\u89d2\uff0c\u770b\u8d77\u6765\u66f4\u73b0\u4ee3 */\n"
"}")
        self.Theme = QMenu(self.menuBar)
        self.Theme.setObjectName(u"Theme")
        self.Settings = QMenu(self.menuBar)
        self.Settings.setObjectName(u"Settings")
        SubtitleToolbox.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.Theme.menuAction())
        self.menuBar.addAction(self.Settings.menuAction())
        self.Theme.addAction(self.actionLight)
        self.Theme.addAction(self.actionDark)
        self.Settings.addAction(self.actionOpenSettings)
        self.Settings.addAction(self.actionSaveSettings)
        self.Settings.addAction(self.actionReadSettings)

        self.retranslateUi(SubtitleToolbox)

        self.Function.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SubtitleToolbox)
    # setupUi

    def retranslateUi(self, SubtitleToolbox):
        SubtitleToolbox.setWindowTitle(QCoreApplication.translate("SubtitleToolbox", u"SubtitleToolbox", None))
        self.actionLight.setText(QCoreApplication.translate("SubtitleToolbox", u"Light", None))
#if QT_CONFIG(tooltip)
        self.actionLight.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"Light\u4e3b\u9898", None))
#endif // QT_CONFIG(tooltip)
        self.actionDark.setText(QCoreApplication.translate("SubtitleToolbox", u"Dark", None))
#if QT_CONFIG(tooltip)
        self.actionDark.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"Dark\u4e3b\u9898", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpenSettings.setText(QCoreApplication.translate("SubtitleToolbox", u"\u6253\u5f00\u914d\u7f6e", None))
        self.actionSaveSettings.setText(QCoreApplication.translate("SubtitleToolbox", u"\u4fdd\u5b58\u914d\u7f6e", None))
        self.actionReadSettings.setText(QCoreApplication.translate("SubtitleToolbox", u"\u8bfb\u53d6\u914d\u7f6e", None))
        self.ReadPath.setText(QCoreApplication.translate("SubtitleToolbox", u"\u8bfb\u53d6\u76ee\u5f55", None))
        self.SavePath.setText(QCoreApplication.translate("SubtitleToolbox", u"\u4fdd\u5b58\u76ee\u5f55", None))
        self.ReadPathInput.setPlaceholderText(QCoreApplication.translate("SubtitleToolbox", u"\u9009\u62e9\u5f85\u5904\u7406\u6587\u4ef6\u76ee\u5f55", None))
        self.SavePathInput.setPlaceholderText(QCoreApplication.translate("SubtitleToolbox", u"\u9009\u62e9\u4fdd\u5b58\u76ee\u5f55", None))
#if QT_CONFIG(tooltip)
        self.ReadPathOpen.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u6253\u5f00\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.ReadPathOpen.setText("")
#if QT_CONFIG(tooltip)
        self.ReadPathSelect.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u9009\u62e9\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.ReadPathSelect.setText("")
#if QT_CONFIG(tooltip)
        self.ReadPathSet.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u66f4\u65b0\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.ReadPathSet.setText("")
#if QT_CONFIG(tooltip)
        self.SavePathOpen.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u6253\u5f00\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.SavePathOpen.setText("")
#if QT_CONFIG(tooltip)
        self.SavePathSelect.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u9009\u62e9\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.SavePathSelect.setText("")
#if QT_CONFIG(tooltip)
        self.SavePathSet.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u66f4\u65b0\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.SavePathSet.setText("")
#if QT_CONFIG(tooltip)
        self.Output2PDF.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u4fdd\u5b58\u4e3aPDF", None))
#endif // QT_CONFIG(tooltip)
        self.Output2PDF.setText("")
#if QT_CONFIG(tooltip)
        self.Output2Word.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u4fdd\u5b58\u4e3aword", None))
#endif // QT_CONFIG(tooltip)
        self.Output2Word.setText("")
#if QT_CONFIG(tooltip)
        self.Output2Txt.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u4fdd\u5b58\u4e3atxt", None))
#endif // QT_CONFIG(tooltip)
        self.Output2Txt.setText("")
#if QT_CONFIG(tooltip)
        self.Output2Md.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u4fdd\u5b58\u4e3aMarkdown", None))
#endif // QT_CONFIG(tooltip)
        self.Output2Md.setText("")
        self.VolumeLabel.setText(QCoreApplication.translate("SubtitleToolbox", u"\u5206\u5377", None))
        self.VolumePatternSelect.setItemText(0, QCoreApplication.translate("SubtitleToolbox", u"\u6574\u5b63", None))
        self.VolumePatternSelect.setItemText(1, QCoreApplication.translate("SubtitleToolbox", u"\u667a\u80fd", None))
        self.VolumePatternSelect.setItemText(2, QCoreApplication.translate("SubtitleToolbox", u"\u5355\u96c6", None))

        self.Function.setTabText(self.Function.indexOf(self.Script), QCoreApplication.translate("SubtitleToolbox", u"Script", None))
#if QT_CONFIG(tooltip)
        self.MergePDF.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u5408\u5e76PDF", None))
#endif // QT_CONFIG(tooltip)
        self.MergePDF.setText("")
#if QT_CONFIG(tooltip)
        self.MergeWord.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u5408\u5e76word", None))
#endif // QT_CONFIG(tooltip)
        self.MergeWord.setText("")
#if QT_CONFIG(tooltip)
        self.MergeTxt.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u5408\u5e76txt", None))
#endif // QT_CONFIG(tooltip)
        self.MergeTxt.setText("")
#if QT_CONFIG(tooltip)
        self.MergeMd.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u5408\u5e76Markdown", None))
#endif // QT_CONFIG(tooltip)
        self.MergeMd.setText("")
        self.Function.setTabText(self.Function.indexOf(self.Merge), QCoreApplication.translate("SubtitleToolbox", u"Merge", None))
        self.AssPatternLabel.setText(QCoreApplication.translate("SubtitleToolbox", u"\u5b57\u4f53\u65b9\u6848", None))
        self.AssPatternSelect.setItemText(0, QCoreApplication.translate("SubtitleToolbox", u"\u97e9\u4e0a\u4e2d\u4e0b", None))
        self.AssPatternSelect.setItemText(1, QCoreApplication.translate("SubtitleToolbox", u"\u65e5\u4e0a\u4e2d\u4e0b", None))
        self.AssPatternSelect.setItemText(2, QCoreApplication.translate("SubtitleToolbox", u"\u82f1\u4e0a\u4e2d\u4e0b", None))
        self.AssPatternSelect.setItemText(3, QCoreApplication.translate("SubtitleToolbox", u"\u97e9\u4e0a\u65e5\u4e0b", None))

#if QT_CONFIG(tooltip)
        self.Vtt2SrtDrop.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.Vtt2SrtDrop.setText(QCoreApplication.translate("SubtitleToolbox", u"Drop .vtt files\n"
"here to convert", None))
        self.Function.setTabText(self.Function.indexOf(self.Srt2Ass), QCoreApplication.translate("SubtitleToolbox", u"Srt2Ass", None))
        self.WhisperModelLabel.setText(QCoreApplication.translate("SubtitleToolbox", u"\u5f53\u524d\u6a21\u578b", None))
#if QT_CONFIG(tooltip)
        self.SelectWhisperModel.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u9009\u62e9Whisper\u6a21\u578b\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.SelectWhisperModel.setText("")
        self.WhisperModelSelect.setItemText(0, QCoreApplication.translate("SubtitleToolbox", u"faster-whisper-large-v3-turbo", None))
        self.WhisperModelSelect.setItemText(1, QCoreApplication.translate("SubtitleToolbox", u"faster-whisper-large-v3", None))
        self.WhisperModelSelect.setItemText(2, QCoreApplication.translate("SubtitleToolbox", u"faster-whisper-large-v2", None))

        self.WhisperEngineLabel.setText(QCoreApplication.translate("SubtitleToolbox", u"\u6a21\u5f0f", None))
        self.WhisperEngineSelect.setItemText(0, QCoreApplication.translate("SubtitleToolbox", u"GPU", None))
        self.WhisperEngineSelect.setItemText(1, QCoreApplication.translate("SubtitleToolbox", u"CPU", None))

        self.WhisperLanguageLabel.setText(QCoreApplication.translate("SubtitleToolbox", u"\u8bed\u8a00", None))
        self.WhisperLanguageSelect.setItemText(0, QCoreApplication.translate("SubtitleToolbox", u"\u81ea\u52a8", None))
        self.WhisperLanguageSelect.setItemText(1, QCoreApplication.translate("SubtitleToolbox", u"\u97e9\u8bed", None))
        self.WhisperLanguageSelect.setItemText(2, QCoreApplication.translate("SubtitleToolbox", u"\u65e5\u8bed", None))
        self.WhisperLanguageSelect.setItemText(3, QCoreApplication.translate("SubtitleToolbox", u"\u82f1\u8bed", None))
        self.WhisperLanguageSelect.setItemText(4, QCoreApplication.translate("SubtitleToolbox", u"\u4e2d\u6587", None))

        self.Function.setTabText(self.Function.indexOf(self.AutoSub), QCoreApplication.translate("SubtitleToolbox", u"AutoSub", None))
#if QT_CONFIG(tooltip)
        self.Stop.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u505c\u6b62\u5904\u7406", None))
#endif // QT_CONFIG(tooltip)
        self.Stop.setText("")
#if QT_CONFIG(tooltip)
        self.Start.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u5f00\u59cb\u5904\u7406", None))
#endif // QT_CONFIG(tooltip)
        self.Start.setText("")
#if QT_CONFIG(tooltip)
        self.ClearLogs.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u6e05\u7a7a\u65e5\u5fd7", None))
#endif // QT_CONFIG(tooltip)
        self.ClearLogs.setText("")
#if QT_CONFIG(tooltip)
        self.DeleteFiles.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u6e05\u7a7a\u6587\u4ef6\u5939", None))
#endif // QT_CONFIG(tooltip)
        self.DeleteFiles.setText("")
        self.Theme.setTitle(QCoreApplication.translate("SubtitleToolbox", u"\u4e3b\u9898", None))
        self.Settings.setTitle(QCoreApplication.translate("SubtitleToolbox", u"\u914d\u7f6e", None))
    # retranslateUi

