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
from kivy.core.window import Window


token = INFLUXDB_TOKEN  # replace with your token
org = ORGANIZATION
url = SERVER_ADDRESS
bucket = BUCKET
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=influxdb_client.client.write_api.SYNCHRONOUS)

class MonitoringScreen(Screen):
    customer_list = ObjectProperty(None)
    sensor_channel_1 = ObjectProperty(None)
    sensor_channel_2 = ObjectProperty(None)
    sensor_channel_3 = ObjectProperty(None)
    sensor_channel_4 = ObjectProperty(None)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        
        self.customers = []
        self.excel_handler = ExcelHandler('customers_data.xlsx')  # Initialize Excel handler

    def on_enter(self):
            """Load customer data from Excel when the screen is opened."""
            self.load_customers()
            self.reset_charts()
            self.create_empty_graphs()


#-----------------------------------------Customers Operations----------------------------#          
    def update_customer_list(self):
        """Refresh the customer list display."""
        self.customer_list.clear_widgets()  # Remove all children from the customer list
        self.selected_customer = None
       
        if self.customers != None:  # Sort customers list in case the list is not empty!
            sorted_customers = sorted(self.customers, key=lambda customer: customer['last_name'].lower())
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
                    font_size= 14.5,
                    pos_hint= {"x":.25}
                ) 
                # Create a ToggleButton for selection
                toggle_button = ToggleButton(
                    group='customer_selection',  # Group name to ensure only one can be selected
                    size_hint_x=None,
                    width=40,  # Width of the toggle button
                    on_press = lambda instance, cust=customer: self.on_customer_selected(cust)
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

    def load_customers(self):
        """Load customer data from Excel and update the customer list."""
        self.customers = App.get_running_app().excel_handler.load_customers()

        #print("Loaded customers:", self.customers)
        self.update_customer_list()

    def on_customer_selected(self, customer):
        self.reset_charts()
        self.selected_customer = f"{customer['last_name']};{customer['first_name']}"
        print(self.selected_customer)
        #Take sensors data from customer
        sensors_code = customer['sensors_code']
        sensors_type = customer['sensors_type']

        # Keep Program Alive Even if The Customer Has no Sensor Setuped yet :D
        if sensors_code: pass
        else:
            return None
        
        for i in range(9):
            self.ids.range_channel_1.values.append(self.time_decode(i))
            self.ids.range_channel_2.values.append(self.time_decode(i))
            self.ids.range_channel_3.values.append(self.time_decode(i))
            self.ids.range_channel_4.values.append(self.time_decode(i))
        
        if sensors_code is not None:
            sensors_code = sensors_code.split(';')
        if sensors_type is not None:
            sensors_type = sensors_type.split(';')
        sensors_name= list(zip(sensors_code, sensors_type))
        

        #spinner_list = [self.sensor_channel_1, self.sensor_channel_2, self.sensor_channel_3, self.sensor_channel_4]
        for name in sensors_name: 
            self.ids.sensor_channel_1.values.append(f"{name[0]}.{name[1]}")
            self.ids.sensor_channel_2.values.append(f"{name[0]}.{name[1]}")
            self.ids.sensor_channel_3.values.append(f"{name[0]}.{name[1]}")
            self.ids.sensor_channel_4.values.append(f"{name[0]}.{name[1]}")
        self.update_font_size()

    def update_font_size(self, *args):
        """Dynamically update the font size of each spinner based on window size."""
        font_scale = min(Window.width / 1200, Window.height / 700)  # Adjust the base scaling factors as needed
        new_font_size = 20 * font_scale  # Adjust '20' as needed for base font size
        # Update font size for each spinner
        self.ids.sensor_channel_1.font_size = new_font_size
        self.ids.sensor_channel_2.font_size = new_font_size
        self.ids.sensor_channel_3.font_size = new_font_size
        self.ids.sensor_channel_4.font_size = new_font_size


#------------------------------------------Sensors Operations----------------------------#
    def sensor_selected(self, sensor, name):
        self.sensor_ch1 = 'Sensor!'
        self.sensor_ch2 = 'Sensor!'
        self.sensor_ch3 = 'Sensor!'
        self.sensor_ch4 = 'Sensor!'
        if sensor != 'Sensor!': 
            # Decodeing the sensor Code!
            sensor = sensor.split('.') # Take sensor code and name
            self.sensor = sensor[0] # Take sensor code
            if name == 'sensor_channel_1':
                self.sensor_ch1 = self.sensor
                return self.check_quary(1)
            elif name == 'sensor_channel_2':
                self.sensor_ch2 = self.sensor
                return self.check_quary(2)
            elif name == 'sensor_channel_3':
                self.sensor_ch3 = self.sensor
                return self.check_quary(3)
            elif name == 'sensor_channel_4':
                self.sensor_ch4 = self.sensor
                return self.check_quary(4)
        else:
            print("Please Select Sensor!")
            return None

    def time_selected(self, time, name):
        self.range_ch1 = 'Time!'
        self.range_ch2 = 'Time!'
        self.range_ch3 = 'Time!'
        self.range_ch4 = 'Time!'
        if time != 'Time!':
            print(time)
            self.time = time
            if name == 'range_channel_1':
                self.range_ch1 = self.time
                return self.check_quary(1)
            elif name == 'range_channel_2':
                self.range_ch2 = self.time
                return self.check_quary(2)
            elif name == 'range_channel_3':
                self.range_ch3 = self.time
                return self.check_quary(3)
            elif name == 'range_channel_4':
                self.range_ch4 = self.time
                return self.check_quary(4)
        else:
            print('Select time!')
            return None


#---------------------------------------Monitoring Charts Operations----------------------#
    def create_empty_graphs(self):
        """Creates empty Matplotlib graphs for sensor channels."""
        for i in range(1, 5):  # Loop through channels 1 to 4
            fig = Figure(figsize=(1, 1))  # Create a figure
            ax = fig.add_subplot(111)  # Add a subplot
            ax.set_title(f"Channel {i}")  # Set title

            # Clear previous widgets and add the figure
            sensor_channel = self.ids[f'sensor_channel_{i}']
            sensor_channel.clear_widgets()
            sensor_canvas = FigureCanvasKivyAgg(fig)
            sensor_channel.add_widget(sensor_canvas)

    def check_quary(self, channel):
        # This Function Will Check If Both of The Range Spinner(Timer) and Sensor Spinner(Sensor)
        # Has Valued by The User Not Defult! Then Call the "Plot_data()" Function with Correct Channel Input! 
        if channel == 1:
            channel_id = 'sensor_channel_1'
            print(self.range_ch1)
            print(self.sensor_ch1)
            if self.sensor_ch1 != 'Sensor!' and self.range_ch1 != 'Time!':
                self.plot_data(self.sensor_ch1, self.range_ch1, channel_id)
        elif channel == 2:
            channel_id = 'sensor_channel_2'
            if (self.sensor_ch2 != 'Sensor!') and self.range_ch2 != 'Time!':
                self.plot_data(self.sensor_ch2, self.range_ch2, channel_id)
        elif channel == 3:
            channel_id = 'sensor_channel_3'
            if (self.sensor_ch3 != 'Sensor!') and self.range_ch3 != 'Time!':
                self.plot_data(self.sensor_ch3, self.range_ch3, channel_id)
        elif channel == 4:
            channel_id = 'sensor_channel_4'
            if (self.sensor_ch4 != 'Sensor!') and self.range_ch4 != 'Time!':
                    self.plot_data(self.sensor_ch4, self.range_ch4, channel_id)

    def plot_data(self, sensor, time, channel_id):
        # Code the sensor time sheet for the database quary using "time_coding" function
        time = self.time_coding(time)
        print(f"we are here")
        if sensor and time : 
            # Query data from InfluxDB using the selected sensor and time
            data = self.query_data(sensor, time)
            if data.empty:
                print("No data found for the selected sensor and time.")
                return

        times = data["time"]
        values = data["value"]
        print(data)

        sensor_channel = self.ids[channel_id]
        sensor_channel.clear_widgets()
        
        # Create a new plot
        fig = Figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        ax.plot(times, values, label=f"{sensor} Data")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.set_title(f"{sensor} Sensor Data")
        ax.legend()

        # Add the new plot to the specified channel
        sensor_channel.add_widget(FigureCanvasKivyAgg(fig))

    def query_data(self, sensor, time):
        """Queries data from InfluxDB for the specified sensor and time."""
        query_api = write_client.query_api()
        print(f"Querying data for sensor: {sensor}, time range: {time}")
        query = f"""
        from(bucket: "{bucket}")
        |> range(start: {time})
        |> filter(fn: (r) => r.DEVICE == "{sensor}")
        """
        
        tables = query_api.query(query, org=org)
        
        # Convert results to a DataFrame
        return pd.DataFrame(
            [(record.get_time(), record.get_value()) for table in tables for record in table.records],
            columns=["time", "value"]
        )

    def reset_charts(self):
        self.sensor_ch1 = 'Sensor!'
        self.sensor_ch2 = 'Sensor!'
        self.sensor_ch3 = 'Sensor!'
        self.sensor_ch4 = 'Sensor!'
        self.range_ch1 =  'Time!'
        self.range_ch2 =  'Time!'
        self.range_ch3 =  'Time!'
        self.range_ch4 =  'Time!'

        self.ids.range_channel_1.values.clear()
        self.ids.range_channel_2.values.clear()
        self.ids.range_channel_3.values.clear()
        self.ids.range_channel_4.values.clear()

        self.ids.sensor_channel_1.values.clear()
        self.ids.sensor_channel_2.values.clear()
        self.ids.sensor_channel_3.values.clear()
        self.ids.sensor_channel_4.values.clear()

    def time_decode(self, i):
        time = {
            0 : '30 m',
            1 : '1 h',
            2 : '3 h',
            3 : '6 h',
            4 : '12 h',
            5 : '1 d',
            6 : '2 d',
            7 : '7 d',
            8 : '30 d'
        }
        return time[i]

    def time_coding(self, time):
        code_time = {
            '30 m': '-30m',
            '1 h' : '-1h',
            '3 h' : '-3h',
            '6 h' : '-6h',
            '12 h': '-12h',
            '1 d' : '-1d',
            '2 d' : '-2d',
            '7 d' : '-7d',
            '30 d': '-30d'
        }
        return code_time[time]