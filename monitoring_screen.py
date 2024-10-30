# monitoring_screen.py

from kivy.uix.screenmanager import Screen
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.properties import ObjectProperty
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from excel_handler import ExcelHandler  # Assuming excel_handler.py has a class named ExcelHandler for data access

class MonitoringScreen(Screen):
    sensor_spinner = ObjectProperty(None)
    time_spinner = ObjectProperty(None)
    graph_area = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.excel_handler = ExcelHandler()  # Initialize excel handler to retrieve sensor data
        self.selected_sensor = None
        self.selected_time = None

    def on_sensor_selected(self, sensor_name):
        """Called when a sensor is selected from the dropdown."""
        self.selected_sensor = sensor_name

    def on_time_selected(self, time_period):
        """Called when a time period is selected from the dropdown."""
        self.selected_time = time_period

    def plot_data(self):
        """Fetches data for the selected sensor and plots it."""
        if not self.selected_sensor:
            print("Please select a sensor.")
            return
        if not self.selected_time:
            print("Please select a time period.")
            return

        # Retrieve sensor data from the Excel file
        data = self.excel_handler.get_sensor_data(self.selected_sensor, self.selected_time)
        
        # Extracting time and value lists for plotting
        times = [entry['time'] for entry in data]
        values = [entry['value'] for entry in data]

        # Create Matplotlib figure
        self.graph_area.clear_widgets()  # Clear previous plot
        fig = Figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        ax.plot(times, values, label=f"{self.selected_sensor} Data")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.set_title(f"{self.selected_sensor} Sensor Data")
        ax.legend()

        # Embed Matplotlib figure in Kivy
        self.graph_area.add_widget(FigureCanvasKivyAgg(fig))
