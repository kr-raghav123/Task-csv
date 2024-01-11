import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QWidget, QProgressBar, QMessageBox
import pyqtgraph as pg

class CSVViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('CSV Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.plot_widget = pg.PlotWidget(title='CSV Data Plot')
        self.plot_widget.setLabel('left', 'Values')
        self.plot_widget.setLabel('bottom', 'Sample Index')

        self.load_button = QPushButton('Load CSV', self)
        self.load_button.clicked.connect(self.loadCSV)

        self.progress_bar = QProgressBar(self)
        self.statusBar().addPermanentWidget(self.progress_bar)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.load_button)

    def loadCSV(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if not file_name:
            return

        try:
            with open(file_name, 'r') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)  # Assuming the first row is the header
                data = list(csv_reader)

                total_rows = len(data)

                # Extracting data columns
                x_data = [float(row[0]) for row in data]  # Assuming the first column is x-axis data
                y_data = [list(map(float, row[1:])) for row in data]  # Assuming the next five columns are y-axis data

                # Plotting the data
                self.plot_widget.clear()
                for i, y_values in enumerate(zip(*y_data)):
                    self.plot_widget.plot(x_data, y_values, pen=(i, 6), name=header[i + 1])

                self.plot_widget.addLegend()
                self.statusBar().showMessage(f'CSV File Loaded: {file_name}', 3000)

        except FileNotFoundError:
            self.showErrorMessage("File not found.")
        except IsADirectoryError:
            self.showErrorMessage("Selected path is a directory, not a file.")
        except csv.Error as e:
            self.showErrorMessage(f'Error reading CSV file: {str(e)}')
        except Exception as e:
            self.showErrorMessage(f'An unexpected error occurred: {str(e)}')
            return

        finally:
            self.progress_bar.setValue(100)  # Set progress to 100% on success

    def showErrorMessage(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = CSVViewer()
    viewer.show()
    sys.exit(app.exec_())


