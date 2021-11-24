from qgis.core import (
    QgsMessageLog,
    QgsGeometry,
)

from qgis.gui import (
    QgsMessageBar,
)

from qgis.PyQt.QtWidgets import (
    QSizePolicy,
    QPushButton,
    QDialog,
    QGridLayout,
    QDialogButtonBox,
)

# БАЗОВЫЙ ВЫВОД В ОКНО СООБЩЕНИЙ
from qgis.core import Qgis
iface.messageBar().pushMessage("Error", "I'm sorry Dave, I'm afraid I can't do that", level=Qgis.Critical)

# АВТОСКРЫТИЕ
iface.messageBar().pushMessage("Ooops", "The plugin is not working as it should", level=Qgis.Critical, duration=3)

# МОЖНО ДОБАВЛЯТЬ В ОКОШКО СООБЩЕНИЙ ЕЩЕ КАКИЕ-ТО ВИДЖЕТЫ
def showError():
    pass
widget = iface.messageBar().createMessage("Missing Layers", "Show Me")
button = QPushButton(widget)
button.setText("Show Me")
button.pressed.connect(showError)
widget.layout().addWidget(button)
iface.messageBar().pushWidget(widget, Qgis.Warning)

# МОЖНО ОТПРАВЛЯТЬ С ЛОГ


# Взаимодействие через окно статуса
for i, feature in enumerate(range(1000)):
    # do something time-consuming here
    print('.') # printing should give enough time to present the progress

    percent = i / float(1000) * 100
    # iface.mainWindow().statusBar().showMessage("Processed {} %".format(int(percent)))
    iface.statusBarIface().showMessage("Processed {} %".format(int(percent)))

iface.statusBarIface().clearMessage()


# ВЫЧИСЛЕНИЕ ПОЛЕЙ
from qgis.core import *
scope = QgsExpressionContextUtils.globalScope()
scope.setVariable("start",0)
@qgsfunction(args = 'auto', group='Custom')
def my_numers(feature, parent,context):
    value = scope.variable("start")
    scope.setVariable("start",value +1)
    return value