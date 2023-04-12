import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QTimer

class RealTimePlot(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up the GUI window
        self.setWindowTitle("Real-Time Plot with PyQt")
        self.setGeometry(100, 100, 800, 600)
        
        # Create a vertical layout for the GUI
        layout = QVBoxLayout()
        
        # Create a label to display the current random number
        self.label = QLabel()
        layout.addWidget(self.label)
        
        # Create a Figure object for the plot
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Set the layout for the window
        self.setLayout(layout)
        
        # Create a QTimer to update the plot at regular intervals
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)
        
        # Initialize the plot
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")
        self.ax.set_title("Real-Time Plot")
        self.line, = self.ax.plot([], [], 'r-')  # Create an empty line for the plot
        self.x_data = []
        self.y_data = []
    
    def update_plot(self):
        # Generate random data
        x = len(self.x_data)
        y = random.randint(0, 100)
        
        # Append the new data to the existing data
        self.x_data.append(x)
        self.y_data.append(y)
        
        # Update the plot
        self.line.set_data(self.x_data, self.y_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
        
        # Update the label with the current random number
        self.label.setText(f"Current Random Number: {y}")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RealTimePlot()
    window.show()
    sys.exit(app.exec_())
