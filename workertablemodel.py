from PyQt5 import Qt, QtCore

# Classi riguardanti i modelli delle tabelle utilizzate cambia solamente il titolo delle colonne

class TableModelBoss(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModelBoss, self).__init__()
        self._data = data
        self.columns = ["Username", "Age", "Type", "Salary"]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Qt.Horizontal and role == Qt.Qt.ItemDataRole.DisplayRole:
            return self.columns[col]
        if orientation == Qt.Qt.Vertical and role == Qt.Qt.ItemDataRole.DisplayRole:
            return f"{col + 1}"

    def data(self, index, role):
        if role == Qt.Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def setData(self, index, value, role=Qt.Qt.EditRole):
        if role == Qt.Qt.EditRole:
            row = index.row()
            col = index.column()
            self._data[row][col] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class TableModelOperator(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModelOperator, self).__init__()
        self._data = data
        self.columns = ["Type", "Color", "Quantity", "Optionals"]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Qt.Horizontal and role == Qt.Qt.ItemDataRole.DisplayRole:
            return self.columns[col]
        if orientation == Qt.Qt.Vertical and role == Qt.Qt.ItemDataRole.DisplayRole:
            return f"{col + 1}"

    def data(self, index, role):
        if role == Qt.Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def setData(self, index, value, role=Qt.Qt.EditRole):
        if role == Qt.Qt.EditRole:
            row = index.row()
            col = index.column()
            self._data[row][col] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class TableModelImpiegato(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModelImpiegato, self).__init__()
        self._data = data
        self.columns = ["Business Name", "Investment", "Order's number"]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Qt.Horizontal and role == Qt.Qt.ItemDataRole.DisplayRole:
            return self.columns[col]
        if orientation == Qt.Qt.Vertical and role == Qt.Qt.ItemDataRole.DisplayRole:
            return f"{col + 1}"

    def data(self, index, role):
        if role == Qt.Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def setData(self, index, value, role=Qt.Qt.EditRole):
        if role == Qt.Qt.EditRole:
            row = index.row()
            col = index.column()
            self._data[row][col] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])
