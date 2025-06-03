# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_panel.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_ConfigPanelWidget(object):
    def setupUi(self, ConfigPanelWidget):
        if not ConfigPanelWidget.objectName():
            ConfigPanelWidget.setObjectName(u"ConfigPanelWidget")
        ConfigPanelWidget.resize(400, 800)
        self.mainVerticalLayout = QVBoxLayout(ConfigPanelWidget)
        self.mainVerticalLayout.setObjectName(u"mainVerticalLayout")
        self.titleLabel = QLabel(ConfigPanelWidget)
        self.titleLabel.setObjectName(u"titleLabel")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mainVerticalLayout.addWidget(self.titleLabel)

        self.functionGroup = QGroupBox(ConfigPanelWidget)
        self.functionGroup.setObjectName(u"functionGroup")
        self.verticalLayout_2 = QVBoxLayout(self.functionGroup)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.functionDisplayLabel = QLabel(self.functionGroup)
        self.functionDisplayLabel.setObjectName(u"functionDisplayLabel")
        self.functionDisplayLabel.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.functionDisplayLabel)

        self.editFunctionButton = QPushButton(self.functionGroup)
        self.editFunctionButton.setObjectName(u"editFunctionButton")

        self.verticalLayout_2.addWidget(self.editFunctionButton)


        self.mainVerticalLayout.addWidget(self.functionGroup)

        self.paramsGroup = QGroupBox(ConfigPanelWidget)
        self.paramsGroup.setObjectName(u"paramsGroup")
        self.gridLayout = QGridLayout(self.paramsGroup)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_interval_a = QLabel(self.paramsGroup)
        self.label_interval_a.setObjectName(u"label_interval_a")

        self.gridLayout.addWidget(self.label_interval_a, 0, 0, 1, 1)

        self.interval_a_spinbox = QDoubleSpinBox(self.paramsGroup)
        self.interval_a_spinbox.setObjectName(u"interval_a_spinbox")
        self.interval_a_spinbox.setDecimals(2)
        self.interval_a_spinbox.setMinimum(-10000.000000000000000)
        self.interval_a_spinbox.setMaximum(10000.000000000000000)

        self.gridLayout.addWidget(self.interval_a_spinbox, 0, 1, 1, 1)

        self.label_interval_b = QLabel(self.paramsGroup)
        self.label_interval_b.setObjectName(u"label_interval_b")

        self.gridLayout.addWidget(self.label_interval_b, 1, 0, 1, 1)

        self.interval_b_spinbox = QDoubleSpinBox(self.paramsGroup)
        self.interval_b_spinbox.setObjectName(u"interval_b_spinbox")
        self.interval_b_spinbox.setDecimals(2)
        self.interval_b_spinbox.setMinimum(-10000.000000000000000)
        self.interval_b_spinbox.setMaximum(10000.000000000000000)

        self.gridLayout.addWidget(self.interval_b_spinbox, 1, 1, 1, 1)

        self.label_delta_x = QLabel(self.paramsGroup)
        self.label_delta_x.setObjectName(u"label_delta_x")

        self.gridLayout.addWidget(self.label_delta_x, 2, 0, 1, 1)

        self.delta_x_spinbox = QDoubleSpinBox(self.paramsGroup)
        self.delta_x_spinbox.setObjectName(u"delta_x_spinbox")
        self.delta_x_spinbox.setDecimals(4)
        self.delta_x_spinbox.setMinimum(0.000100000000000)
        self.delta_x_spinbox.setMaximum(1000.000000000000000)

        self.gridLayout.addWidget(self.delta_x_spinbox, 2, 1, 1, 1)

        self.label_pop_size = QLabel(self.paramsGroup)
        self.label_pop_size.setObjectName(u"label_pop_size")

        self.gridLayout.addWidget(self.label_pop_size, 3, 0, 1, 1)

        self.pop_size_spinbox = QSpinBox(self.paramsGroup)
        self.pop_size_spinbox.setObjectName(u"pop_size_spinbox")
        self.pop_size_spinbox.setMinimum(1)
        self.pop_size_spinbox.setMaximum(1000)

        self.gridLayout.addWidget(self.pop_size_spinbox, 3, 1, 1, 1)

        self.label_num_generations = QLabel(self.paramsGroup)
        self.label_num_generations.setObjectName(u"label_num_generations")

        self.gridLayout.addWidget(self.label_num_generations, 4, 0, 1, 1)

        self.num_generations_spinbox = QSpinBox(self.paramsGroup)
        self.num_generations_spinbox.setObjectName(u"num_generations_spinbox")
        self.num_generations_spinbox.setMinimum(1)
        self.num_generations_spinbox.setMaximum(10000)

        self.gridLayout.addWidget(self.num_generations_spinbox, 4, 1, 1, 1)

        self.label_prob_crossover = QLabel(self.paramsGroup)
        self.label_prob_crossover.setObjectName(u"label_prob_crossover")

        self.gridLayout.addWidget(self.label_prob_crossover, 5, 0, 1, 1)

        self.prob_crossover_spinbox = QDoubleSpinBox(self.paramsGroup)
        self.prob_crossover_spinbox.setObjectName(u"prob_crossover_spinbox")
        self.prob_crossover_spinbox.setDecimals(2)
        self.prob_crossover_spinbox.setMaximum(1.000000000000000)
        self.prob_crossover_spinbox.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.prob_crossover_spinbox, 5, 1, 1, 1)

        self.label_prob_mutation_i = QLabel(self.paramsGroup)
        self.label_prob_mutation_i.setObjectName(u"label_prob_mutation_i")

        self.gridLayout.addWidget(self.label_prob_mutation_i, 6, 0, 1, 1)

        self.prob_mutation_i_spinbox = QDoubleSpinBox(self.paramsGroup)
        self.prob_mutation_i_spinbox.setObjectName(u"prob_mutation_i_spinbox")
        self.prob_mutation_i_spinbox.setDecimals(2)
        self.prob_mutation_i_spinbox.setMaximum(1.000000000000000)
        self.prob_mutation_i_spinbox.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.prob_mutation_i_spinbox, 6, 1, 1, 1)

        self.label_prob_mutation_g = QLabel(self.paramsGroup)
        self.label_prob_mutation_g.setObjectName(u"label_prob_mutation_g")

        self.gridLayout.addWidget(self.label_prob_mutation_g, 7, 0, 1, 1)

        self.prob_mutation_g_spinbox = QDoubleSpinBox(self.paramsGroup)
        self.prob_mutation_g_spinbox.setObjectName(u"prob_mutation_g_spinbox")
        self.prob_mutation_g_spinbox.setDecimals(2)
        self.prob_mutation_g_spinbox.setMaximum(1.000000000000000)
        self.prob_mutation_g_spinbox.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.prob_mutation_g_spinbox, 7, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_mode = QLabel(self.paramsGroup)
        self.label_mode.setObjectName(u"label_mode")

        self.horizontalLayout.addWidget(self.label_mode)

        self.minimize_radio = QRadioButton(self.paramsGroup)
        self.minimize_radio.setObjectName(u"minimize_radio")
        self.minimize_radio.setChecked(True)

        self.horizontalLayout.addWidget(self.minimize_radio)

        self.maximize_radio = QRadioButton(self.paramsGroup)
        self.maximize_radio.setObjectName(u"maximize_radio")

        self.horizontalLayout.addWidget(self.maximize_radio)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout, 8, 0, 1, 2)


        self.mainVerticalLayout.addWidget(self.paramsGroup)

        self.calculatedParamsGroup = QGroupBox(ConfigPanelWidget)
        self.calculatedParamsGroup.setObjectName(u"calculatedParamsGroup")
        self.gridLayout_2 = QGridLayout(self.calculatedParamsGroup)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_num_points = QLabel(self.calculatedParamsGroup)
        self.label_num_points.setObjectName(u"label_num_points")

        self.gridLayout_2.addWidget(self.label_num_points, 0, 0, 1, 1)

        self.num_points_label = QLabel(self.calculatedParamsGroup)
        self.num_points_label.setObjectName(u"num_points_label")

        self.gridLayout_2.addWidget(self.num_points_label, 0, 1, 1, 1)

        self.label_num_bits = QLabel(self.calculatedParamsGroup)
        self.label_num_bits.setObjectName(u"label_num_bits")

        self.gridLayout_2.addWidget(self.label_num_bits, 1, 0, 1, 1)

        self.num_bits_label = QLabel(self.calculatedParamsGroup)
        self.num_bits_label.setObjectName(u"num_bits_label")

        self.gridLayout_2.addWidget(self.num_bits_label, 1, 1, 1, 1)

        self.label_max_decimal = QLabel(self.calculatedParamsGroup)
        self.label_max_decimal.setObjectName(u"label_max_decimal")

        self.gridLayout_2.addWidget(self.label_max_decimal, 2, 0, 1, 1)

        self.max_decimal_label = QLabel(self.calculatedParamsGroup)
        self.max_decimal_label.setObjectName(u"max_decimal_label")

        self.gridLayout_2.addWidget(self.max_decimal_label, 2, 1, 1, 1)


        self.mainVerticalLayout.addWidget(self.calculatedParamsGroup)

        self.execute_ag_btn = QPushButton(ConfigPanelWidget)
        self.execute_ag_btn.setObjectName(u"execute_ag_btn")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.execute_ag_btn.setFont(font1)

        self.mainVerticalLayout.addWidget(self.execute_ag_btn)

        self.graphSelectionGroup = QGroupBox(ConfigPanelWidget)
        self.graphSelectionGroup.setObjectName(u"graphSelectionGroup")
        self.verticalLayout_graphs = QVBoxLayout(self.graphSelectionGroup)
        self.verticalLayout_graphs.setObjectName(u"verticalLayout_graphs")
        self.objectiveGraphButton = QPushButton(self.graphSelectionGroup)
        self.objectiveGraphButton.setObjectName(u"objectiveGraphButton")

        self.verticalLayout_graphs.addWidget(self.objectiveGraphButton)

        self.bestEvolutionGraphButton = QPushButton(self.graphSelectionGroup)
        self.bestEvolutionGraphButton.setObjectName(u"bestEvolutionGraphButton")

        self.verticalLayout_graphs.addWidget(self.bestEvolutionGraphButton)

        self.allEvolutionGraphButton = QPushButton(self.graphSelectionGroup)
        self.allEvolutionGraphButton.setObjectName(u"allEvolutionGraphButton")

        self.verticalLayout_graphs.addWidget(self.allEvolutionGraphButton)

        self.animatedEvolutionButton = QPushButton(self.graphSelectionGroup)
        self.animatedEvolutionButton.setObjectName(u"animatedEvolutionButton")

        self.verticalLayout_graphs.addWidget(self.animatedEvolutionButton)


        self.mainVerticalLayout.addWidget(self.graphSelectionGroup)

        self.actionsGroup = QGroupBox(ConfigPanelWidget)
        self.actionsGroup.setObjectName(u"actionsGroup")
        self.verticalLayout_actions = QVBoxLayout(self.actionsGroup)
        self.verticalLayout_actions.setObjectName(u"verticalLayout_actions")
        self.generateReportButton = QPushButton(self.actionsGroup)
        self.generateReportButton.setObjectName(u"generateReportButton")

        self.verticalLayout_actions.addWidget(self.generateReportButton)

        self.downloadAnimationButton = QPushButton(self.actionsGroup)
        self.downloadAnimationButton.setObjectName(u"downloadAnimationButton")

        self.verticalLayout_actions.addWidget(self.downloadAnimationButton)

        self.clearResultsButton = QPushButton(self.actionsGroup)
        self.clearResultsButton.setObjectName(u"clearResultsButton")

        self.verticalLayout_actions.addWidget(self.clearResultsButton)


        self.mainVerticalLayout.addWidget(self.actionsGroup)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainVerticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(ConfigPanelWidget)

        QMetaObject.connectSlotsByName(ConfigPanelWidget)
    # setupUi

    def retranslateUi(self, ConfigPanelWidget):
        ConfigPanelWidget.setWindowTitle(QCoreApplication.translate("ConfigPanelWidget", u"Config Panel Content", None))
        self.titleLabel.setText(QCoreApplication.translate("ConfigPanelWidget", u"Configuraci\u00f3n", None))
        self.functionGroup.setTitle(QCoreApplication.translate("ConfigPanelWidget", u"Funci\u00f3n Objetivo (AG de Ejemplo y Visualizador)", None))
        self.functionDisplayLabel.setText(QCoreApplication.translate("ConfigPanelWidget", u"f(x) = ...", None))
        self.editFunctionButton.setText(QCoreApplication.translate("ConfigPanelWidget", u"Editar Funci\u00f3n", None))
        self.paramsGroup.setTitle(QCoreApplication.translate("ConfigPanelWidget", u"Par\u00e1metros (para AG de Ejemplo)", None))
        self.label_interval_a.setText(QCoreApplication.translate("ConfigPanelWidget", u"Intervalo A:", None))
        self.label_interval_b.setText(QCoreApplication.translate("ConfigPanelWidget", u"Intervalo B:", None))
        self.label_delta_x.setText(QCoreApplication.translate("ConfigPanelWidget", u"\u0394x:", None))
        self.label_pop_size.setText(QCoreApplication.translate("ConfigPanelWidget", u"Poblaci\u00f3n:", None))
        self.label_num_generations.setText(QCoreApplication.translate("ConfigPanelWidget", u"Generaciones:", None))
        self.label_prob_crossover.setText(QCoreApplication.translate("ConfigPanelWidget", u"Prob. Cruzamiento:", None))
        self.label_prob_mutation_i.setText(QCoreApplication.translate("ConfigPanelWidget", u"PMI (Individuo):", None))
        self.label_prob_mutation_g.setText(QCoreApplication.translate("ConfigPanelWidget", u"PMG (Gen):", None))
        self.label_mode.setText(QCoreApplication.translate("ConfigPanelWidget", u"Modo:", None))
        self.minimize_radio.setText(QCoreApplication.translate("ConfigPanelWidget", u"Minimizar", None))
        self.maximize_radio.setText(QCoreApplication.translate("ConfigPanelWidget", u"Maximizar", None))
        self.calculatedParamsGroup.setTitle(QCoreApplication.translate("ConfigPanelWidget", u"Par\u00e1metros Calculados", None))
        self.label_num_points.setText(QCoreApplication.translate("ConfigPanelWidget", u"# Puntos:", None))
        self.num_points_label.setText(QCoreApplication.translate("ConfigPanelWidget", u"...", None))
        self.label_num_bits.setText(QCoreApplication.translate("ConfigPanelWidget", u"# Bits:", None))
        self.num_bits_label.setText(QCoreApplication.translate("ConfigPanelWidget", u"...", None))
        self.label_max_decimal.setText(QCoreApplication.translate("ConfigPanelWidget", u"M\u00e1x. Decimal:", None))
        self.max_decimal_label.setText(QCoreApplication.translate("ConfigPanelWidget", u"...", None))
        self.execute_ag_btn.setText(QCoreApplication.translate("ConfigPanelWidget", u"EJECUTAR AG DE EJEMPLO", None))
        self.graphSelectionGroup.setTitle(QCoreApplication.translate("ConfigPanelWidget", u"Seleccionar Gr\u00e1fica", None))
        self.objectiveGraphButton.setText(QCoreApplication.translate("ConfigPanelWidget", u"Funci\u00f3n Objetivo", None))
        self.bestEvolutionGraphButton.setText(QCoreApplication.translate("ConfigPanelWidget", u"Evoluci\u00f3n Mejor", None))
        self.allEvolutionGraphButton.setText(QCoreApplication.translate("ConfigPanelWidget", u"Evoluci\u00f3n Poblaci\u00f3n", None))
        self.animatedEvolutionButton.setText(QCoreApplication.translate("ConfigPanelWidget", u"Evoluci\u00f3n Animada", None))
        self.actionsGroup.setTitle(QCoreApplication.translate("ConfigPanelWidget", u"Acciones", None))
        self.generateReportButton.setText(QCoreApplication.translate("ConfigPanelWidget", u"Generar Reporte", None))
        self.downloadAnimationButton.setText(QCoreApplication.translate("ConfigPanelWidget", u"Descargar Animaci\u00f3n", None))
        self.clearResultsButton.setText(QCoreApplication.translate("ConfigPanelWidget", u"Limpiar Resultados", None))
    # retranslateUi

