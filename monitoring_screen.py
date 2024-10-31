from kivy.uix.screenmanager import Screen
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.app import App
from kivy.properties import ObjectProperty
from matplotlib.figure import Figure
from excel_handler import ExcelHandler  # Assuming excel_handler.py has a class named ExcelHandler for data access
from secrets_server import INFLUXDB_TOKEN, ORGANIZATION, BUCKET, SERVER_ADDRESS
import influxdb_client
import pandas as pd

token = INFLUXDB_TOKEN  # replace with your token
org = ORGANIZATION
url = SERVER_ADDRESS
bucket = BUCKET
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=influxdb_client.client.write_api.SYNCHRONOUS)


class MonitoringScreen(Screen):
    customer_list = ObjectProperty(None)

    

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.Flag_Sensor = False
        self.Flag_Time = False
        self.Flag_Quary= False
        self.customers = []
        self.excel_handler = ExcelHandler('customers_data.xlsx')  # Initialize Excel handler
        self.load_customers()

        #self.create_empty_graphs()  # Create empty graphs

    def ready_quary(self, Sensor):
        pass

    def sensor_selected(self, Spinner_id):
        # Take Spinner ID and Selected Sensor
        _spinner = self.ids.Spinner_id
        _spinner_sensor = _spinner.text
        # Check if the Sensor is Correct
        if _spinner_sensor != 'Sensor!':
            self.Flag_Sensor = True
        else:
            self.Flag_Sensor = False
        
        ready_quary(_spinner_sensor)

    def update_customer_list(self):
        """Refresh the customer list display."""
        self.customer_list.clear_widgets()  # Remove all children from the customer list

        # Sort customers by last name
        sorted_customers = sorted(self.customers, key=lambda customer: customer['last_name'].lower())
        self.selected_customer = None

        for customer in sorted_customers:
            # Create a layout to hold the toggle button and label
            layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=40,
                padding=(0, 0, 10, 0)  # Add padding (left, top, right, bottom)
            )
            # Create a label for the customer's name
            customer_label = Label(
                text= f"{customer['first_name']} {customer['last_name']}",
                color= (0, 0, 0),
                size_hint_y= None,
                height= 40,
                halign= "left",
                font_size= 16,
                pos_hint= {"x":.25}
            )
            
            # Create a ToggleButton for selection
            toggle_button = ToggleButton(
                group='customer_selection',  # Group name to ensure only one can be selected
                size_hint_x=None,
                width=40,  # Width of the toggle button
                on_state=lambda instance, state, cust=customer: self.on_customer_selected(cust, state)
            )

            # Add the toggle button and label to the layout
            layout.add_widget(customer_label)
            layout.add_widget(toggle_button)


            # Dynamically update padding based on the label width
            def update_padding(instance, value):
                padding = instance.width * 0.4  # Set padding to 5% of the label width
                instance.text_size = (instance.width - padding, None)
            
            # Bind the width change to the padding adjustment
            customer_label.bind(size=update_padding)  # Use 'size' instead of 'width' for binding

            self.customer_list.add_widget(layout)

    def create_empty_graphs(self):
        """Creates empty Matplotlib graphs for sensor channels."""
        for i in range(1, 5):  # Loop through channels 1 to 4
            fig = Figure(figsize=(5, 4))  # Create a figure
            ax = fig.add_subplot(111)  # Add a subplot
            ax.set_title(f"Channel {i}")  # Set title

            # Clear previous widgets and add the figure
            sensor_channel = self.ids[f'sensor_channel_{i}']
            sensor_channel.clear_widgets()
            sensor_canvas = FigureCanvasKivyAgg(fig)
            sensor_channel.add_widget(sensor_canvas)

    def on_sensor_selected(self, sensor_name):
        """Called when a sensor is selected from the dropdown."""
        self.selected_sensor = sensor_name

    def on_time_selected(self, time_period):
        """Called when a time period is selected from the dropdown."""
        self.selected_time = time_period

    def load_customers(self):
        """Load customer data from Excel and update the customer list."""
        self.customers = App.get_running_app().excel_handler.load_customers()

        #print("Loaded customers:", self.customers)
        self.update_customer_list()

    def plot_data(self):
        """Fetches data for the selected sensor and plots it."""
        if not self.selected_sensor:
            print("Please select a sensor.")
            return
        if not self.selected_time:
            print("Please select a time period.")
            return

        data = self.excel_handler.get_sensor_data(self.selected_sensor, self.selected_time)
        times = [entry['time'] for entry in data]
        values = [entry['value'] for entry in data]

        self.graph_area.clear_widgets()  # Clear previous plot
        fig = Figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        ax.plot(times, values, label=f"{self.selected_sensor} Data")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.set_title(f"{self.selected_sensor} Sensor Data")
        ax.legend()

        self.graph_area.add_widget(FigureCanvasKivyAgg(fig))

    def query_data(self, customer, sensor, time):
        query_api = write_client.query_api()
        print(sensor)
        query =  f"""from(bucket: "Sensors")
        |> range(start: {time})
        |> filter(fn: (r) => r._measurement == "{customer}" and r.DEVICE == "{sensor}")"""
        tables = query_api.query(query, org="Pillipp_1")
        print(tables)
        return pd.DataFrame([(r.get_time(), r.get_value()) for t in tables for r in t.records], columns=["time", "value"])
