from PyQt5.QtWidgets import QDialogButtonBox, QPushButton


class CustomEdit:

    mDialog = None


    @classmethod
    def open(cls, dialog, layer, feature):
        print(layer, feature)
        cls.mDialog = dialog
        cls.editedLayer = layer
        cls.editedFeature = feature
        cls.createContent()

    @classmethod
    def createContent(cls):
        buttonBox = cls.mDialog.findChild(QDialogButtonBox, "buttonBox")
        bnOk = buttonBox.button(QDialogButtonBox.Ok)
        bnOk.clicked.disconnect()
        bnOk.clicked.connect(cls.accept)
        bnOk.setEnabled(True)

        bntCancel = buttonBox.button(QDialogButtonBox.Cancel)
        bntCancel.clicked.disconnect()
        bntCancel.clicked.connect(cls.cancel)


    @classmethod
    def cancel(cls):
        print("Cancel")

    @classmethod
    def accept(cls):
        print("Ok")


def open(dialog, layer, feature):
    CustomEdit.open(dialog, layer, feature)