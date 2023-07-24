# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'layerUathFQ.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QVBoxLayout,
    QWidget)

from photoeditor.image_preview import ImagePreview

class Ui_Layer(object):
    def setupUi(self, Layer):
        if not Layer.objectName():
            Layer.setObjectName(u"Layer")
        Layer.resize(286, 181)
        self.verticalLayout_2 = QVBoxLayout(Layer)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.name_edit = QLineEdit(Layer)
        self.name_edit.setObjectName(u"name_edit")

        self.verticalLayout_2.addWidget(self.name_edit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.preview = ImagePreview(Layer)
        self.preview.setObjectName(u"preview")

        self.horizontalLayout.addWidget(self.preview)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.enable_button = QPushButton(Layer)
        self.enable_button.setObjectName(u"enable_button")

        self.verticalLayout.addWidget(self.enable_button)

        self.delete_button = QPushButton(Layer)
        self.delete_button.setObjectName(u"delete_button")

        self.verticalLayout.addWidget(self.delete_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.alpha_slider = QSlider(Layer)
        self.alpha_slider.setObjectName(u"alpha_slider")
        self.alpha_slider.setMaximum(1000)
        self.alpha_slider.setValue(1000)
        self.alpha_slider.setOrientation(Qt.Horizontal)

        self.verticalLayout_2.addWidget(self.alpha_slider)


        self.retranslateUi(Layer)

        QMetaObject.connectSlotsByName(Layer)
    # setupUi

    def retranslateUi(self, Layer):
        Layer.setWindowTitle(QCoreApplication.translate("Layer", u"Form", None))
        self.name_edit.setText(QCoreApplication.translate("Layer", u"Layer", None))
        self.enable_button.setText(QCoreApplication.translate("Layer", u"disable", None))
        self.delete_button.setText(QCoreApplication.translate("Layer", u"delete", None))
    # retranslateUi

