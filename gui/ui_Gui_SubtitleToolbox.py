# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Gui_SubtitleToolboxdlAgeL.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QProgressBar, QPushButton, QSizePolicy,
    QTabWidget, QVBoxLayout, QWidget)
from . import Icons_rc

class Ui_SubtitleToolbox(object):
    def setupUi(self, SubtitleToolbox):
        if not SubtitleToolbox.objectName():
            SubtitleToolbox.setObjectName(u"SubtitleToolbox")
        SubtitleToolbox.resize(628, 605)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SubtitleToolbox.sizePolicy().hasHeightForWidth())
        SubtitleToolbox.setSizePolicy(sizePolicy)
        SubtitleToolbox.setMinimumSize(QSize(628, 605))
        SubtitleToolbox.setMaximumSize(QSize(628, 605))
        font = QFont()
        font.setHintingPreference(QFont.PreferDefaultHinting)
        SubtitleToolbox.setFont(font)
        SubtitleToolbox.setMouseTracking(False)
        SubtitleToolbox.setToolTipDuration(-1)
        SubtitleToolbox.setStyleSheet(u"")
        SubtitleToolbox.setAnimated(True)
        self.actionchn = QAction(SubtitleToolbox)
        self.actionchn.setObjectName(u"actionchn")
        self.actionkor = QAction(SubtitleToolbox)
        self.actionkor.setObjectName(u"actionkor")
        self.actionjpn = QAction(SubtitleToolbox)
        self.actionjpn.setObjectName(u"actionjpn")
        self.actioneng = QAction(SubtitleToolbox)
        self.actioneng.setObjectName(u"actioneng")
        self.actionLight = QAction(SubtitleToolbox)
        self.actionLight.setObjectName(u"actionLight")
        self.actionDark = QAction(SubtitleToolbox)
        self.actionDark.setObjectName(u"actionDark")
        self.OpenSettings_2 = QAction(SubtitleToolbox)
        self.OpenSettings_2.setObjectName(u"OpenSettings_2")
        self.SaveSettings_2 = QAction(SubtitleToolbox)
        self.SaveSettings_2.setObjectName(u"SaveSettings_2")
        self.centralwidget = QWidget(SubtitleToolbox)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"/* 2. \u5173\u952e\uff1a\u5c06 TabWidget \u5185\u90e8\u76f4\u63a5\u5d4c\u5957\u7684 QWidget \u8bbe\u4e3a\u900f\u660e */\n"
"/* \u53ea\u6709\u8fd9\u6837\uff0c\u9762\u677f\u7684\u989c\u8272\u624d\u80fd\u900f\u51fa\u6765 */\n"
"QTabWidget > QWidget {\n"
"    background-color: transparent;\n"
"}")
        self.Function = QTabWidget(self.centralwidget)
        self.Function.setObjectName(u"Function")
        self.Function.setGeometry(QRect(21, 90, 355, 120))
        self.Function.setMinimumSize(QSize(0, 120))
        self.Function.setMaximumSize(QSize(16777215, 120))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setHintingPreference(QFont.PreferDefaultHinting)
        self.Function.setFont(font1)
        self.Function.setStyleSheet(u"/* 1. \u6574\u4f53\u5bb9\u5668\u7f8e\u5316\uff1a\u53bb\u6389\u5185\u5bb9\u9762\u677f\u9876\u90e8\u7684\u7ebf\u6761\uff0c\u9632\u6b62\u4ea7\u751f\u4e0b\u5212\u7ebf\u611f */\n"
"QTabWidget::pane {\n"
"    /*border: 1px solid #dcdfe6;*/\n"
"    border-radius: 6px; /* \u5706\u89d2 */\n"
"    border-top-left-radius: 0px;  /* \u4e0a\u8fb9\u7f18\u5f27\u5ea6\u5927 */\n"
"    background-color: rgb(219, 219, 219); \n"
"}\n"
"\n"
"/* \u7b2c 1 \u4e2a\u6807\u7b7e\uff1a\u6d45\u7c89\u8272 */\n"
"QTabBar::tab:first {\n"
"    background-color: #FFB6C1;\n"
"}\n"
"\n"
"/* \u6240\u6709\u6807\u7b7e\uff08\u9ed8\u8ba4\u8272/\u7b2c 2 \u4e2a\uff09\uff1a\u6de1\u7eff\u8272 */\n"
"/* \u6ce8\u610f\uff1a\u8fd9\u91cc\u4f5c\u4e3a\u9ed8\u8ba4\u503c\uff0c\u4f1a\u88ab first \u548c last \u8986\u76d6 */\n"
"QTabBar::tab {\n"
"    padding: 2px 15px;\n"
"    min-width: 20px;\n"
"    background-color: #90EE90; \n"
"    /* \u6838\u5fc3\u4fee\u6539\uff1a\u5206\u522b\u8bbe\u7f6e\u56db\u4e2a\u89d2\u7684\u5f27\u5ea6 */\n"
"    /* \u987a\u5e8f\u4e3a\uff1a"
                        "\u5de6\u4e0a, \u53f3\u4e0a, \u53f3\u4e0b, \u5de6\u4e0b */\n"
"    border-top-left-radius: 6px;  /* \u4e0a\u8fb9\u7f18\u5f27\u5ea6\u5927 */\n"
"    border-top-right-radius: 6px; \n"
"    border-bottom-left-radius: 1px; /* \u4e0b\u8fb9\u7f18\u5f27\u5ea6\u5c0f\u6216\u8bbe\u4e3a 0 */\n"
"    border-bottom-right-radius: 1px;\n"
"}\n"
"\n"
"/* \u7b2c 3 \u4e2a\uff08\u6700\u540e\u4e00\u4e2a\uff09\u6807\u7b7e\uff1a\u5929\u84dd\u8272 */\n"
"QTabBar::tab:last {\n"
"    background-color: #87CEFA;\n"
"}\n"
"\n"
"/* \u9009\u4e2d\u72b6\u6001 */\n"
"QTabBar::tab:selected {\n"
"    font-weight: bold;\n"
"    background-color: #5555ff;\n"
"    color: white;\n"
"    /* 3. \u8fd9\u91cc\u7684 margin-top \u8bbe\u4e3a 0\uff0c\u914d\u5408\u57fa\u7840\u6001\u7684 2px\uff0c\u5b9e\u73b0\u76f8\u5bf9\u5347\u8d77\u6548\u679c */\n"
"    margin-top: 0px; \n"
"    /* \u518d\u6b21\u660e\u786e\u5706\u89d2\uff0c\u786e\u4fdd\u4e0d\u88ab\u9ed8\u8ba4\u6837\u5f0f\u8986\u76d6 */\n"
"    border-top-left-radius: 6px;\n"
"    border-top-right-radius: 6p"
                        "x;\n"
"}")
        self.Function.setElideMode(Qt.TextElideMode.ElideNone)
        self.Function.setDocumentMode(False)
        self.Function.setTabsClosable(False)
        self.Function.setMovable(False)
        self.Script = QWidget()
        self.Script.setObjectName(u"Script")
        font2 = QFont()
        font2.setHintingPreference(QFont.PreferNoHinting)
        self.Script.setFont(font2)
        self.horizontalLayout_3 = QHBoxLayout(self.Script)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, -1, 3, -1)
        self.OutputFormat = QHBoxLayout()
        self.OutputFormat.setObjectName(u"OutputFormat")
        self.Output2PDF = QCheckBox(self.Script)
        self.Output2PDF.setObjectName(u"Output2PDF")
        sizePolicy.setHeightForWidth(self.Output2PDF.sizePolicy().hasHeightForWidth())
        self.Output2PDF.setSizePolicy(sizePolicy)
        self.Output2PDF.setMinimumSize(QSize(75, 80))
        self.Output2PDF.setMaximumSize(QSize(75, 80))
        font3 = QFont()
        font3.setPointSize(9)
        font3.setHintingPreference(QFont.PreferDefaultHinting)
        self.Output2PDF.setFont(font3)
        self.Output2PDF.setAutoFillBackground(False)
        self.Output2PDF.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-radius: 5px; /* \u5706\u89d2 */\n"
"}\n"
"\n"
"/* \u672a\u9009\u4e2d\u72b6\u6001 */\n"
"QCheckBox::indicator:unchecked {\n"
"    border: 1px solid #999;\n"
"    background: white;\n"
"}\n"
"\n"
"/* \u9009\u4e2d\u72b6\u6001 */\n"
"QCheckBox::indicator:checked {\n"
"    border: 1px solid #2196F3; \n"
"    /* \u4fee\u6b63\u62fc\u5199\u9519\u8bef\uff1auurl -> url */\n"
"    image: url(:/resources/checkmark.png); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u72b6\u6001 */\n"
"QCheckBox::indicator:hover {\n"
"    border: 1px solid #2196F3;\n"
"    /* \u5efa\u8bae\uff1a\u60ac\u6d6e\u65f6\u80cc\u666f\u53ef\u4ee5\u6bd4\u9009\u4e2d\u65f6\u7a0d\u6d45\uff0c\u6216\u8005\u4fdd\u6301\u4e0d\u53d8 */\n"
"    background-color: #2196F3; \n"
"}")
        icon = QIcon()
        icon.addFile(u"../SubtitleToolbox/resources/PDF.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Output2PDF.setIcon(icon)
        self.Output2PDF.setIconSize(QSize(35, 35))
        self.Output2PDF.setCheckable(True)
        self.Output2PDF.setChecked(False)
        self.Output2PDF.setTristate(False)

        self.OutputFormat.addWidget(self.Output2PDF)

        self.Output2Word = QCheckBox(self.Script)
        self.Output2Word.setObjectName(u"Output2Word")
        sizePolicy.setHeightForWidth(self.Output2Word.sizePolicy().hasHeightForWidth())
        self.Output2Word.setSizePolicy(sizePolicy)
        self.Output2Word.setMinimumSize(QSize(75, 80))
        self.Output2Word.setMaximumSize(QSize(75, 80))
        font4 = QFont()
        font4.setPointSize(9)
        self.Output2Word.setFont(font4)
        self.Output2Word.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-radius: 5px; /* \u5706\u89d2 */\n"
"}\n"
"\n"
"/* \u672a\u9009\u4e2d\u72b6\u6001 */\n"
"QCheckBox::indicator:unchecked {\n"
"    border: 1px solid #999;\n"
"    background: white;\n"
"}\n"
"\n"
"/* \u9009\u4e2d\u72b6\u6001 */\n"
"QCheckBox::indicator:checked {\n"
"    border: 1px solid #2196F3; \n"
"    /* \u4fee\u6b63\u62fc\u5199\u9519\u8bef\uff1auurl -> url */\n"
"    image: url(:/resources/checkmark.png); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u72b6\u6001 */\n"
"QCheckBox::indicator:hover {\n"
"    border: 1px solid #2196F3;\n"
"    /* \u5efa\u8bae\uff1a\u60ac\u6d6e\u65f6\u80cc\u666f\u53ef\u4ee5\u6bd4\u9009\u4e2d\u65f6\u7a0d\u6d45\uff0c\u6216\u8005\u4fdd\u6301\u4e0d\u53d8 */\n"
"    background-color: #2196F3; \n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"../SubtitleToolbox/resources/Word.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Output2Word.setIcon(icon1)
        self.Output2Word.setIconSize(QSize(35, 35))
        self.Output2Word.setCheckable(True)
        self.Output2Word.setChecked(False)
        self.Output2Word.setTristate(False)

        self.OutputFormat.addWidget(self.Output2Word)

        self.Output2Txt = QCheckBox(self.Script)
        self.Output2Txt.setObjectName(u"Output2Txt")
        sizePolicy.setHeightForWidth(self.Output2Txt.sizePolicy().hasHeightForWidth())
        self.Output2Txt.setSizePolicy(sizePolicy)
        self.Output2Txt.setMinimumSize(QSize(75, 80))
        self.Output2Txt.setMaximumSize(QSize(75, 80))
        self.Output2Txt.setFont(font4)
        self.Output2Txt.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-radius: 5px; /* \u5706\u89d2 */\n"
"}\n"
"\n"
"/* \u672a\u9009\u4e2d\u72b6\u6001 */\n"
"QCheckBox::indicator:unchecked {\n"
"    border: 1px solid #999;\n"
"    background: white;\n"
"}\n"
"\n"
"/* \u9009\u4e2d\u72b6\u6001 */\n"
"QCheckBox::indicator:checked {\n"
"    border: 1px solid #2196F3; \n"
"    /* \u4fee\u6b63\u62fc\u5199\u9519\u8bef\uff1auurl -> url */\n"
"    image: url(:/resources/checkmark.png); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u72b6\u6001 */\n"
"QCheckBox::indicator:hover {\n"
"    border: 1px solid #2196F3;\n"
"    /* \u5efa\u8bae\uff1a\u60ac\u6d6e\u65f6\u80cc\u666f\u53ef\u4ee5\u6bd4\u9009\u4e2d\u65f6\u7a0d\u6d45\uff0c\u6216\u8005\u4fdd\u6301\u4e0d\u53d8 */\n"
"    background-color: #2196F3; \n"
"}")
        icon2 = QIcon()
        icon2.addFile(u"../SubtitleToolbox/resources/txt.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Output2Txt.setIcon(icon2)
        self.Output2Txt.setIconSize(QSize(35, 35))
        self.Output2Txt.setCheckable(True)
        self.Output2Txt.setChecked(False)
        self.Output2Txt.setTristate(False)

        self.OutputFormat.addWidget(self.Output2Txt)


        self.horizontalLayout.addLayout(self.OutputFormat)

        self.DividingLine = QFrame(self.Script)
        self.DividingLine.setObjectName(u"DividingLine")
        self.DividingLine.setMinimumSize(QSize(20, 0))
        self.DividingLine.setMaximumSize(QSize(20, 16777215))
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

        self.horizontalLayout.addWidget(self.DividingLine)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 5, 0, 5)
        self.VolumeLabel = QLabel(self.Script)
        self.VolumeLabel.setObjectName(u"VolumeLabel")
        self.VolumeLabel.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.VolumeLabel.sizePolicy().hasHeightForWidth())
        self.VolumeLabel.setSizePolicy(sizePolicy1)
        font5 = QFont()
        font5.setPointSize(11)
        font5.setBold(True)
        font5.setHintingPreference(QFont.PreferNoHinting)
        self.VolumeLabel.setFont(font5)
        self.VolumeLabel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.VolumeLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.VolumeLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.VolumeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.VolumeLabel.setWordWrap(False)

        self.verticalLayout.addWidget(self.VolumeLabel)

        self.VolumePatternSelect = QComboBox(self.Script)
        self.VolumePatternSelect.addItem("")
        self.VolumePatternSelect.addItem("")
        self.VolumePatternSelect.addItem("")
        self.VolumePatternSelect.setObjectName(u"VolumePatternSelect")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.VolumePatternSelect.sizePolicy().hasHeightForWidth())
        self.VolumePatternSelect.setSizePolicy(sizePolicy2)
        self.VolumePatternSelect.setMinimumSize(QSize(0, 30))
        self.VolumePatternSelect.setMaximumSize(QSize(9999, 30))
        font6 = QFont()
        font6.setPointSize(10)
        self.VolumePatternSelect.setFont(font6)
        self.VolumePatternSelect.setStyleSheet(u"")
        self.VolumePatternSelect.setEditable(False)

        self.verticalLayout.addWidget(self.VolumePatternSelect)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 10)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 5)

        self.horizontalLayout_3.addLayout(self.horizontalLayout)

        self.Function.addTab(self.Script, "")
        self.DividingLine.raise_()
        self.VolumePatternSelect.raise_()
        self.VolumeLabel.raise_()
        self.Merge = QWidget()
        self.Merge.setObjectName(u"Merge")
        self.Merge.setFont(font2)
        self.horizontalLayout_2 = QHBoxLayout(self.Merge)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.MergePDF = QCheckBox(self.Merge)
        self.MergePDF.setObjectName(u"MergePDF")
        sizePolicy.setHeightForWidth(self.MergePDF.sizePolicy().hasHeightForWidth())
        self.MergePDF.setSizePolicy(sizePolicy)
        self.MergePDF.setMinimumSize(QSize(75, 80))
        self.MergePDF.setMaximumSize(QSize(75, 80))
        self.MergePDF.setFont(font3)
        self.MergePDF.setAutoFillBackground(False)
        self.MergePDF.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-radius: 5px; /* \u5706\u89d2 */\n"
"}\n"
"\n"
"/* \u672a\u9009\u4e2d\u72b6\u6001 */\n"
"QCheckBox::indicator:unchecked {\n"
"    border: 1px solid #999;\n"
"    background: white;\n"
"}\n"
"\n"
"/* \u9009\u4e2d\u72b6\u6001 */\n"
"QCheckBox::indicator:checked {\n"
"    border: 1px solid #2196F3; \n"
"    /* \u4fee\u6b63\u62fc\u5199\u9519\u8bef\uff1auurl -> url */\n"
"    image: url(:/resources/checkmark.png); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u72b6\u6001 */\n"
"QCheckBox::indicator:hover {\n"
"    border: 1px solid #2196F3;\n"
"    /* \u5efa\u8bae\uff1a\u60ac\u6d6e\u65f6\u80cc\u666f\u53ef\u4ee5\u6bd4\u9009\u4e2d\u65f6\u7a0d\u6d45\uff0c\u6216\u8005\u4fdd\u6301\u4e0d\u53d8 */\n"
"    background-color: #2196F3; \n"
"}")
        self.MergePDF.setIcon(icon)
        self.MergePDF.setIconSize(QSize(35, 35))
        self.MergePDF.setCheckable(True)
        self.MergePDF.setChecked(False)
        self.MergePDF.setTristate(False)

        self.horizontalLayout_2.addWidget(self.MergePDF)

        self.MergeWord = QCheckBox(self.Merge)
        self.MergeWord.setObjectName(u"MergeWord")
        sizePolicy.setHeightForWidth(self.MergeWord.sizePolicy().hasHeightForWidth())
        self.MergeWord.setSizePolicy(sizePolicy)
        self.MergeWord.setMinimumSize(QSize(75, 80))
        self.MergeWord.setMaximumSize(QSize(75, 80))
        self.MergeWord.setFont(font4)
        self.MergeWord.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-radius: 5px; /* \u5706\u89d2 */\n"
"}\n"
"\n"
"/* \u672a\u9009\u4e2d\u72b6\u6001 */\n"
"QCheckBox::indicator:unchecked {\n"
"    border: 1px solid #999;\n"
"    background: white;\n"
"}\n"
"\n"
"/* \u9009\u4e2d\u72b6\u6001 */\n"
"QCheckBox::indicator:checked {\n"
"    border: 1px solid #2196F3; \n"
"    /* \u4fee\u6b63\u62fc\u5199\u9519\u8bef\uff1auurl -> url */\n"
"    image: url(:/resources/checkmark.png); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u72b6\u6001 */\n"
"QCheckBox::indicator:hover {\n"
"    border: 1px solid #2196F3;\n"
"    /* \u5efa\u8bae\uff1a\u60ac\u6d6e\u65f6\u80cc\u666f\u53ef\u4ee5\u6bd4\u9009\u4e2d\u65f6\u7a0d\u6d45\uff0c\u6216\u8005\u4fdd\u6301\u4e0d\u53d8 */\n"
"    background-color: #2196F3; \n"
"}")
        self.MergeWord.setIcon(icon1)
        self.MergeWord.setIconSize(QSize(35, 35))
        self.MergeWord.setCheckable(True)
        self.MergeWord.setChecked(False)
        self.MergeWord.setTristate(False)

        self.horizontalLayout_2.addWidget(self.MergeWord)

        self.MergeTxt = QCheckBox(self.Merge)
        self.MergeTxt.setObjectName(u"MergeTxt")
        sizePolicy.setHeightForWidth(self.MergeTxt.sizePolicy().hasHeightForWidth())
        self.MergeTxt.setSizePolicy(sizePolicy)
        self.MergeTxt.setMinimumSize(QSize(75, 80))
        self.MergeTxt.setMaximumSize(QSize(75, 80))
        self.MergeTxt.setFont(font4)
        self.MergeTxt.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-radius: 5px; /* \u5706\u89d2 */\n"
"}\n"
"\n"
"/* \u672a\u9009\u4e2d\u72b6\u6001 */\n"
"QCheckBox::indicator:unchecked {\n"
"    border: 1px solid #999;\n"
"    background: white;\n"
"}\n"
"\n"
"/* \u9009\u4e2d\u72b6\u6001 */\n"
"QCheckBox::indicator:checked {\n"
"    border: 1px solid #2196F3; \n"
"    /* \u4fee\u6b63\u62fc\u5199\u9519\u8bef\uff1auurl -> url */\n"
"    image: url(:/resources/checkmark.png); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u72b6\u6001 */\n"
"QCheckBox::indicator:hover {\n"
"    border: 1px solid #2196F3;\n"
"    /* \u5efa\u8bae\uff1a\u60ac\u6d6e\u65f6\u80cc\u666f\u53ef\u4ee5\u6bd4\u9009\u4e2d\u65f6\u7a0d\u6d45\uff0c\u6216\u8005\u4fdd\u6301\u4e0d\u53d8 */\n"
"    background-color: #2196F3; \n"
"}")
        self.MergeTxt.setIcon(icon2)
        self.MergeTxt.setIconSize(QSize(35, 35))
        self.MergeTxt.setCheckable(True)
        self.MergeTxt.setChecked(False)
        self.MergeTxt.setTristate(False)

        self.horizontalLayout_2.addWidget(self.MergeTxt)

        self.Function.addTab(self.Merge, "")
        self.Srt2Ass = QWidget()
        self.Srt2Ass.setObjectName(u"Srt2Ass")
        self.Srt2Ass.setFont(font2)
        self.verticalLayout_2 = QVBoxLayout(self.Srt2Ass)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.AssPattern = QHBoxLayout()
        self.AssPattern.setSpacing(0)
        self.AssPattern.setObjectName(u"AssPattern")
        self.AssPattern.setContentsMargins(0, 0, 0, 0)
        self.AssPatternLabel = QLabel(self.Srt2Ass)
        self.AssPatternLabel.setObjectName(u"AssPatternLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.AssPatternLabel.sizePolicy().hasHeightForWidth())
        self.AssPatternLabel.setSizePolicy(sizePolicy3)
        self.AssPatternLabel.setMinimumSize(QSize(0, 30))
        self.AssPatternLabel.setMaximumSize(QSize(16777215, 30))
        font7 = QFont()
        font7.setPointSize(11)
        font7.setWeight(QFont.DemiBold)
        font7.setHintingPreference(QFont.PreferNoHinting)
        self.AssPatternLabel.setFont(font7)
        self.AssPatternLabel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.AssPatternLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.AssPatternLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.AssPatternLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.AssPatternLabel.setWordWrap(False)

        self.AssPattern.addWidget(self.AssPatternLabel)

        self.AssPatternSelect = QComboBox(self.Srt2Ass)
        self.AssPatternSelect.addItem("")
        self.AssPatternSelect.setObjectName(u"AssPatternSelect")
        self.AssPatternSelect.setMinimumSize(QSize(80, 30))
        self.AssPatternSelect.setMaximumSize(QSize(80, 30))
        self.AssPatternSelect.setFont(font6)
        self.AssPatternSelect.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.AssPatternSelect.setStyleSheet(u"")
        self.AssPatternSelect.setEditable(False)

        self.AssPattern.addWidget(self.AssPatternSelect)


        self.horizontalLayout_4.addLayout(self.AssPattern)

        self.AssSettings = QHBoxLayout()
        self.AssSettings.setSpacing(10)
        self.AssSettings.setObjectName(u"AssSettings")
        self.RefreshSettings = QPushButton(self.Srt2Ass)
        self.RefreshSettings.setObjectName(u"RefreshSettings")
        self.RefreshSettings.setMinimumSize(QSize(45, 45))
        self.RefreshSettings.setMaximumSize(QSize(45, 45))
        self.RefreshSettings.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    background-color:rgb(238, 238, 0);\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color:rgb(208, 208, 0);\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 6px;\n"
"}\n"
"")
        icon3 = QIcon(QIcon.fromTheme(u"emblem-synchronized"))
        self.RefreshSettings.setIcon(icon3)
        self.RefreshSettings.setIconSize(QSize(30, 30))

        self.AssSettings.addWidget(self.RefreshSettings)

        self.OpenSettings = QPushButton(self.Srt2Ass)
        self.OpenSettings.setObjectName(u"OpenSettings")
        self.OpenSettings.setMinimumSize(QSize(45, 45))
        self.OpenSettings.setMaximumSize(QSize(45, 45))
        self.OpenSettings.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    background-color:rgb(167, 83, 250);\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color:rgb(127, 64, 191);\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 6px;\n"
"}\n"
"")
        icon4 = QIcon(QIcon.fromTheme(u"document-save-as"))
        self.OpenSettings.setIcon(icon4)
        self.OpenSettings.setIconSize(QSize(30, 30))

        self.AssSettings.addWidget(self.OpenSettings)


        self.horizontalLayout_4.addLayout(self.AssSettings)

        self.horizontalLayout_4.setStretch(0, 6)
        self.horizontalLayout_4.setStretch(1, 4)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.Function.addTab(self.Srt2Ass, "")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(22, 10, 589, 69))
        self.PathLayout = QHBoxLayout(self.layoutWidget)
        self.PathLayout.setSpacing(5)
        self.PathLayout.setObjectName(u"PathLayout")
        self.PathLayout.setContentsMargins(0, 0, 0, 0)
        self.PathLabel = QVBoxLayout()
        self.PathLabel.setSpacing(5)
        self.PathLabel.setObjectName(u"PathLabel")
        self.PathLabel.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.PathLabel.setContentsMargins(5, 0, 0, -1)
        self.ReadPath = QLabel(self.layoutWidget)
        self.ReadPath.setObjectName(u"ReadPath")
        sizePolicy3.setHeightForWidth(self.ReadPath.sizePolicy().hasHeightForWidth())
        self.ReadPath.setSizePolicy(sizePolicy3)
        self.ReadPath.setMinimumSize(QSize(65, 30))
        self.ReadPath.setMaximumSize(QSize(65, 30))
        font8 = QFont()
        font8.setPointSize(10)
        font8.setBold(False)
        font8.setHintingPreference(QFont.PreferNoHinting)
        self.ReadPath.setFont(font8)

        self.PathLabel.addWidget(self.ReadPath)

        self.SavePath = QLabel(self.layoutWidget)
        self.SavePath.setObjectName(u"SavePath")
        sizePolicy3.setHeightForWidth(self.SavePath.sizePolicy().hasHeightForWidth())
        self.SavePath.setSizePolicy(sizePolicy3)
        self.SavePath.setMinimumSize(QSize(65, 30))
        self.SavePath.setMaximumSize(QSize(65, 30))
        font9 = QFont()
        font9.setPointSize(10)
        font9.setWeight(QFont.Medium)
        font9.setHintingPreference(QFont.PreferNoHinting)
        self.SavePath.setFont(font9)

        self.PathLabel.addWidget(self.SavePath)


        self.PathLayout.addLayout(self.PathLabel)

        self.PathInput = QVBoxLayout()
        self.PathInput.setSpacing(5)
        self.PathInput.setObjectName(u"PathInput")
        self.ReadPathInput = QLineEdit(self.layoutWidget)
        self.ReadPathInput.setObjectName(u"ReadPathInput")
        sizePolicy.setHeightForWidth(self.ReadPathInput.sizePolicy().hasHeightForWidth())
        self.ReadPathInput.setSizePolicy(sizePolicy)
        self.ReadPathInput.setMinimumSize(QSize(400, 30))
        self.ReadPathInput.setMaximumSize(QSize(400, 30))
        palette = QPalette()
        self.ReadPathInput.setPalette(palette)
        self.ReadPathInput.setAutoFillBackground(False)
        self.ReadPathInput.setStyleSheet(u"border-radius: 6px;")

        self.PathInput.addWidget(self.ReadPathInput)

        self.SavePathInput = QLineEdit(self.layoutWidget)
        self.SavePathInput.setObjectName(u"SavePathInput")
        sizePolicy.setHeightForWidth(self.SavePathInput.sizePolicy().hasHeightForWidth())
        self.SavePathInput.setSizePolicy(sizePolicy)
        self.SavePathInput.setMinimumSize(QSize(400, 30))
        self.SavePathInput.setMaximumSize(QSize(400, 30))
        palette1 = QPalette()
        self.SavePathInput.setPalette(palette1)
        self.SavePathInput.setStyleSheet(u"border-radius: 6px;")

        self.PathInput.addWidget(self.SavePathInput)


        self.PathLayout.addLayout(self.PathInput)

        self.PathButton = QGridLayout()
        self.PathButton.setSpacing(5)
        self.PathButton.setObjectName(u"PathButton")
        self.ReadPathSet = QPushButton(self.layoutWidget)
        self.ReadPathSet.setObjectName(u"ReadPathSet")
        self.ReadPathSet.setEnabled(True)
        sizePolicy.setHeightForWidth(self.ReadPathSet.sizePolicy().hasHeightForWidth())
        self.ReadPathSet.setSizePolicy(sizePolicy)
        self.ReadPathSet.setMinimumSize(QSize(30, 30))
        self.ReadPathSet.setMaximumSize(QSize(30, 30))
        self.ReadPathSet.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(160, 160, 160); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(160, 160, 160); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 3px;\n"
"}\n"
"")
        self.ReadPathSet.setIcon(icon3)
        self.ReadPathSet.setIconSize(QSize(20, 20))

        self.PathButton.addWidget(self.ReadPathSet, 0, 0, 1, 1)

        self.SavePathOpen = QPushButton(self.layoutWidget)
        self.SavePathOpen.setObjectName(u"SavePathOpen")
        sizePolicy.setHeightForWidth(self.SavePathOpen.sizePolicy().hasHeightForWidth())
        self.SavePathOpen.setSizePolicy(sizePolicy)
        self.SavePathOpen.setMinimumSize(QSize(30, 30))
        self.SavePathOpen.setMaximumSize(QSize(30, 30))
        self.SavePathOpen.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(160, 160, 160); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(160, 160, 160); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 3px;\n"
"}\n"
"")
        icon5 = QIcon(QIcon.fromTheme(u"edit-find"))
        self.SavePathOpen.setIcon(icon5)
        self.SavePathOpen.setIconSize(QSize(20, 20))

        self.PathButton.addWidget(self.SavePathOpen, 1, 1, 1, 1)

        self.ReadPathOpen = QPushButton(self.layoutWidget)
        self.ReadPathOpen.setObjectName(u"ReadPathOpen")
        sizePolicy.setHeightForWidth(self.ReadPathOpen.sizePolicy().hasHeightForWidth())
        self.ReadPathOpen.setSizePolicy(sizePolicy)
        self.ReadPathOpen.setMinimumSize(QSize(30, 30))
        self.ReadPathOpen.setMaximumSize(QSize(30, 30))
        self.ReadPathOpen.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(160, 160, 160); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(160, 160, 160); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 3px;\n"
"}\n"
"")
        self.ReadPathOpen.setIcon(icon5)
        self.ReadPathOpen.setIconSize(QSize(20, 20))

        self.PathButton.addWidget(self.ReadPathOpen, 0, 1, 1, 1)

        self.SavePathSelect = QPushButton(self.layoutWidget)
        self.SavePathSelect.setObjectName(u"SavePathSelect")
        sizePolicy.setHeightForWidth(self.SavePathSelect.sizePolicy().hasHeightForWidth())
        self.SavePathSelect.setSizePolicy(sizePolicy)
        self.SavePathSelect.setMinimumSize(QSize(30, 30))
        self.SavePathSelect.setMaximumSize(QSize(30, 30))
        self.SavePathSelect.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(160, 160, 160); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(160, 160, 160); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 3px;\n"
"}\n"
"")
        icon6 = QIcon(QIcon.fromTheme(u"folder-open"))
        self.SavePathSelect.setIcon(icon6)
        self.SavePathSelect.setIconSize(QSize(20, 20))

        self.PathButton.addWidget(self.SavePathSelect, 1, 2, 1, 1)

        self.ReadPathSelect = QPushButton(self.layoutWidget)
        self.ReadPathSelect.setObjectName(u"ReadPathSelect")
        sizePolicy.setHeightForWidth(self.ReadPathSelect.sizePolicy().hasHeightForWidth())
        self.ReadPathSelect.setSizePolicy(sizePolicy)
        self.ReadPathSelect.setMinimumSize(QSize(30, 30))
        self.ReadPathSelect.setMaximumSize(QSize(30, 30))
        self.ReadPathSelect.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(160, 160, 160); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(160, 160, 160); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 3px;\n"
"}\n"
"")
        self.ReadPathSelect.setIcon(icon6)
        self.ReadPathSelect.setIconSize(QSize(20, 20))

        self.PathButton.addWidget(self.ReadPathSelect, 0, 2, 1, 1)

        self.SavePathSet = QPushButton(self.layoutWidget)
        self.SavePathSet.setObjectName(u"SavePathSet")
        sizePolicy.setHeightForWidth(self.SavePathSet.sizePolicy().hasHeightForWidth())
        self.SavePathSet.setSizePolicy(sizePolicy)
        self.SavePathSet.setMinimumSize(QSize(30, 30))
        self.SavePathSet.setMaximumSize(QSize(30, 30))
        self.SavePathSet.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(160, 160, 160); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(160, 160, 160); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 3px;\n"
"}\n"
"")
        self.SavePathSet.setIcon(icon3)
        self.SavePathSet.setIconSize(QSize(20, 20))

        self.PathButton.addWidget(self.SavePathSet, 1, 0, 1, 1)


        self.PathLayout.addLayout(self.PathButton)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(450, 110, 161, 102))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.DeleteFiles = QPushButton(self.widget)
        self.DeleteFiles.setObjectName(u"DeleteFiles")
        self.DeleteFiles.setMinimumSize(QSize(45, 45))
        self.DeleteFiles.setMaximumSize(QSize(45, 45))
        self.DeleteFiles.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    background-color: rgb(255, 160, 162);\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(255, 89, 92);\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 6px;\n"
"}\n"
"")
        icon7 = QIcon(QIcon.fromTheme(u"edit-delete"))
        self.DeleteFiles.setIcon(icon7)
        self.DeleteFiles.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.DeleteFiles, 0, 0, 1, 1)

        self.Start = QPushButton(self.widget)
        self.Start.setObjectName(u"Start")
        sizePolicy.setHeightForWidth(self.Start.sizePolicy().hasHeightForWidth())
        self.Start.setSizePolicy(sizePolicy)
        self.Start.setMinimumSize(QSize(100, 100))
        self.Start.setMaximumSize(QSize(100, 100))
        font10 = QFont()
        font10.setPointSize(12)
        font10.setWeight(QFont.DemiBold)
        font10.setKerning(True)
        font10.setHintingPreference(QFont.PreferNoHinting)
        self.Start.setFont(font10)
        self.Start.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    background-color:rgb(76, 229, 112);\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(0, 200, 0); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 6px;\n"
"}\n"
"")
        icon8 = QIcon(QIcon.fromTheme(u"media-playback-start"))
        self.Start.setIcon(icon8)
        self.Start.setIconSize(QSize(60, 60))
        self.Start.setCheckable(False)
        self.Start.setChecked(False)

        self.gridLayout.addWidget(self.Start, 0, 1, 2, 1)

        self.ClearLogs = QPushButton(self.widget)
        self.ClearLogs.setObjectName(u"ClearLogs")
        self.ClearLogs.setMinimumSize(QSize(45, 45))
        self.ClearLogs.setMaximumSize(QSize(45, 45))
        self.ClearLogs.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    background-color: rgb(250, 160, 0);\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(250, 120, 0); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 6px;\n"
"}\n"
"")
        icon9 = QIcon(QIcon.fromTheme(u"edit-clear"))
        self.ClearLogs.setIcon(icon9)
        self.ClearLogs.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.ClearLogs, 1, 0, 1, 1)

        self.widget1 = QWidget(self.centralwidget)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(20, 220, 591, 341))
        self.gridLayout_2 = QGridLayout(self.widget1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(10)
        self.gridLayout_2.setContentsMargins(1, 0, 4, 0)
        self.Log = QPlainTextEdit(self.widget1)
        self.Log.setObjectName(u"Log")
        self.Log.setStyleSheet(u"QPlainTextEdit {\n"
"    /* 1. \u5fc5\u987b\u6709\u8fb9\u6846\uff0c\u900f\u660e\u5373\u53ef */\n"
"    border: 1px solid transparent;\n"
"    \n"
"    /* 2. \u5b9a\u4e49\u5706\u89d2 */\n"
"    border-radius: 6px;\n"
"    \n"
"    /* 3. \u6838\u5fc3\uff1a\u5fc5\u987b\u5b9a\u4e49\u80cc\u666f\u8272\uff0c\u5706\u89d2\u624d\u80fd\u88ab\u201c\u586b\u5145\u201d\u51fa\u6765 */\n"
"    /* palette(base) \u4f1a\u81ea\u52a8\u8ddf\u968f\u4e3b\u9898\uff1a\u6d45\u8272\u65f6\u662f\u767d\u8272\uff0c\u6df1\u8272\u65f6\u662f\u6df1\u7070 */\n"
"    background-color: palette(base);\n"
"    \n"
"    /* \u5efa\u8bae\u52a0\u70b9\u5185\u8fb9\u8ddd\uff0c\u5426\u5219\u5b57\u4f1a\u8d34\u5230\u5706\u89d2\u8fb9\u4e0a */\n"
"    padding: 3px;\n"
"}")

        self.gridLayout_2.addWidget(self.Log, 1, 0, 1, 1)

        self.ProgressBar = QProgressBar(self.widget1)
        self.ProgressBar.setObjectName(u"ProgressBar")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.ProgressBar.sizePolicy().hasHeightForWidth())
        self.ProgressBar.setSizePolicy(sizePolicy4)
        self.ProgressBar.setStyleSheet(u"/* \u8fdb\u5ea6\u6761\u80cc\u666f\u69fd */\n"
"QProgressBar {\n"
"    border: none;                /* \u53bb\u6389\u8fb9\u6846 */\n"
"    color: white;                /* \u767e\u5206\u6bd4\u6587\u5b57\u989c\u8272 */\n"
"    text-align: center;          /* \u6587\u5b57\u5c45\u4e2d */\n"
"    background: #e0e0e0;         /* \u69fd\u7684\u80cc\u666f\u8272 */\n"
"    border-radius: 5px;          /* \u5706\u89d2\u9ad8\u5ea6\u7684\u4e00\u534a\u901a\u5e38\u770b\u8d77\u6765\u5f88\u8212\u670d */\n"
"    height: 10px;                /* \u8fd9\u91cc\u7684 height \u4f1a\u5f71\u54cd\u69fd\u7684\u7c97\u7ec6 */\n"
"}\n"
"\n"
"/* \u5df2\u586b\u5145\u7684\u8fdb\u5ea6\u90e8\u5206 */\n"
"QProgressBar::chunk {\n"
"    background-color: #05B8CC;   /* \u8fdb\u5ea6\u6761\u989c\u8272\uff1a\u9752\u84dd\u8272 */\n"
"    border-radius: 5px;          /* \u8fdb\u5ea6\u6761\u7684\u5706\u89d2 */\n"
"}")
        self.ProgressBar.setValue(0)
        self.ProgressBar.setTextVisible(False)
        self.ProgressBar.setOrientation(Qt.Orientation.Horizontal)
        self.ProgressBar.setInvertedAppearance(False)

        self.gridLayout_2.addWidget(self.ProgressBar, 0, 0, 1, 1)

        SubtitleToolbox.setCentralWidget(self.centralwidget)
        self.Start.raise_()
        self.Function.raise_()
        self.Log.raise_()
        self.widget.raise_()
        self.menuBar = QMenuBar(SubtitleToolbox)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 628, 22))
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName(u"menu")
        SubtitleToolbox.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionLight)
        self.menu.addAction(self.actionDark)

        self.retranslateUi(SubtitleToolbox)

        self.Function.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(SubtitleToolbox)
    # setupUi

    def retranslateUi(self, SubtitleToolbox):
        SubtitleToolbox.setWindowTitle(QCoreApplication.translate("SubtitleToolbox", u"MainWindow", None))
        self.actionchn.setText(QCoreApplication.translate("SubtitleToolbox", u"chn", None))
        self.actionkor.setText(QCoreApplication.translate("SubtitleToolbox", u"kor", None))
        self.actionjpn.setText(QCoreApplication.translate("SubtitleToolbox", u"jpn", None))
        self.actioneng.setText(QCoreApplication.translate("SubtitleToolbox", u"eng", None))
        self.actionLight.setText(QCoreApplication.translate("SubtitleToolbox", u"Light", None))
        self.actionDark.setText(QCoreApplication.translate("SubtitleToolbox", u"Dark", None))
        self.OpenSettings_2.setText(QCoreApplication.translate("SubtitleToolbox", u"\u6253\u5f00\u914d\u7f6e\u6587\u4ef6", None))
        self.SaveSettings_2.setText(QCoreApplication.translate("SubtitleToolbox", u"\u4fdd\u5b58\u914d\u7f6e", None))
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
        self.Function.setTabText(self.Function.indexOf(self.Merge), QCoreApplication.translate("SubtitleToolbox", u"Merge", None))
        self.AssPatternLabel.setText(QCoreApplication.translate("SubtitleToolbox", u"\u5b57\u4f53\u65b9\u6848\uff1a", None))
        self.AssPatternSelect.setItemText(0, QCoreApplication.translate("SubtitleToolbox", u"\u9ed8\u8ba4", None))

#if QT_CONFIG(tooltip)
        self.RefreshSettings.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u66f4\u65b0\u914d\u7f6e", None))
#endif // QT_CONFIG(tooltip)
        self.RefreshSettings.setText("")
#if QT_CONFIG(tooltip)
        self.OpenSettings.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u6253\u5f00\u914d\u7f6e", None))
#endif // QT_CONFIG(tooltip)
        self.OpenSettings.setText("")
        self.Function.setTabText(self.Function.indexOf(self.Srt2Ass), QCoreApplication.translate("SubtitleToolbox", u"Srt2Ass", None))
        self.ReadPath.setText(QCoreApplication.translate("SubtitleToolbox", u"\u8bfb\u53d6\u76ee\u5f55\uff1a", None))
        self.SavePath.setText(QCoreApplication.translate("SubtitleToolbox", u"\u4fdd\u5b58\u76ee\u5f55\uff1a", None))
#if QT_CONFIG(tooltip)
        self.ReadPathSet.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u66f4\u65b0\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.ReadPathSet.setText("")
#if QT_CONFIG(tooltip)
        self.SavePathOpen.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u6253\u5f00\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.SavePathOpen.setText("")
#if QT_CONFIG(tooltip)
        self.ReadPathOpen.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u6253\u5f00\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.ReadPathOpen.setText("")
#if QT_CONFIG(tooltip)
        self.SavePathSelect.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u9009\u62e9\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.SavePathSelect.setText("")
#if QT_CONFIG(tooltip)
        self.ReadPathSelect.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u9009\u62e9\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.ReadPathSelect.setText("")
#if QT_CONFIG(tooltip)
        self.SavePathSet.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u66f4\u65b0\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.SavePathSet.setText("")
#if QT_CONFIG(tooltip)
        self.DeleteFiles.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u6e05\u7a7a\u6587\u4ef6\u5939", None))
#endif // QT_CONFIG(tooltip)
        self.DeleteFiles.setText("")
#if QT_CONFIG(tooltip)
        self.Start.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u5f00\u59cb\u5904\u7406", None))
#endif // QT_CONFIG(tooltip)
        self.Start.setText("")
#if QT_CONFIG(tooltip)
        self.ClearLogs.setToolTip(QCoreApplication.translate("SubtitleToolbox", u"\u6e05\u7a7a\u65e5\u5fd7", None))
#endif // QT_CONFIG(tooltip)
        self.ClearLogs.setText("")
        self.menu.setTitle(QCoreApplication.translate("SubtitleToolbox", u"\u4e3b\u9898", None))
    # retranslateUi

