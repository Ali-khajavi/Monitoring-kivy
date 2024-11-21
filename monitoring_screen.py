from kivy.uix.screenmanager import Screen
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.app import App
from kivy.properties import ObjectProperty
from matplotlib.figure import Figure
from excel_handler import ExcelHandler
import influxdb_client
import pandas as pd
from kivy.core.window import Window
from kivy.properties import StringProperty

from secrets_server import get_influxdb_token, get_organization, get_bucket, get_server_address

# Access values via the functions
INFLUXDB_TOKEN = get_influxdb_token()
ORGANIZATION = get_organization()
BUCKET = get_bucket()
SERVER_ADDRESS = get_server_address()

import os, sys

def resource_path(relative_path):
        """Get absolute path to resource, works for dev and PyInstaller"""
        try:
            # PyInstaller temporary folder
            base_path = sys._MEIPASS
        except AttributeError:
            # Development environment
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


token = INFLUXDB_TOKEN
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
    background_image = StringProperty(resource_path('assets/BG1.jpg'))
    background_normal = StringProperty(resource_path('assets/PNG/Button_1/b2.png'))
    background_down = StringProperty(resource_path('assets/PNG/Button_1/b4.png'))

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        
        self.customers = []

        self.excel_handler = ExcelHandler(resource_path('customers_data.xlsx'))  # Initialize Excel handler

    def on_enter(self):
            self.load_customers()
            self.reset_charts_values()
            #self.create_empty_graphs()


#-----------------------------------------Customers Update, Selection Functions----------------------------#          
    def update_customer_list(self):
        # Remove all children from the customer list
        self.customer_list.clear_widgets()
        self.selected_customer = None

        # Sort customers list in case the list is not empty!
        if self.customers is not None:  
            sorted_customers = sorted(self.customers, key=lambda customer: customer['last_name'].lower())
            for customer in sorted_customers:
                # Create a layout to hold the toggle button and label
                layout = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=30,
                    padding=(0, 0, 10, 0)  # Add padding (left, top, right, bottom)
                )
                # Create a label for the customer's name
                customer_label = Label(
                    text=f"{customer['first_name']} {customer['last_name']}",
                    size_hint_y=None,
                    height=30,
                    padding= (10,0,0,0),
                    halign="left",
                    valign="middle",
                    font_size= 14,
                    text_size=(self.width * 0.7, None)
                )

                customer_label.bind(
                size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)),
                width=lambda instance, value: setattr(instance, 'font_size', value * 0.08)  # Adjust font size dynamically
                )

                # Create a ToggleButton for selection
                toggle_button = ToggleButton(
                    group='customer_selection', 
                    size_hint_x=None,
                    width=30,  
                    on_press=lambda instance, cust=customer: self.on_customer_selected(cust)
                )
                layout.add_widget(customer_label)
                layout.add_widget(toggle_button)
                self.customer_list.add_widget(layout)
                
    def load_customers(self):
        self.customers = App.get_running_app().excel_handler.load_customers()
        self.update_customer_list()

    def on_customer_selected(self, customer):
        self.reset_charts_values()
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
        
        self.ids.sensor_channel_1.values.append("None")
        self.ids.sensor_channel_2.values.append("None")
        self.ids.sensor_channel_3.values.append("None")
        self.ids.sensor_channel_4.values.append("None")

        #spinner_list = [self.sensor_channel_1, self.sensor_channel_2, self.sensor_channel_3, self.sensor_channel_4]
        for i in range(len(sensors_code)): 
            self.ids.sensor_channel_1.values.append(f"{sensors_code[i]}")
            self.ids.sensor_channel_2.values.append(f"{sensors_code[i]}")
            self.ids.sensor_channel_3.values.append(f"{sensors_code[i]}")
            self.ids.sensor_channel_4.values.append(f"{sensors_code[i]}")
        
        self.update_font_size()

    def update_font_size(self, *args):
        font_scale = min(Window.width / 1200, Window.height / 700)  # Adjust the base scaling factors as needed
        new_font_size = 20 * font_scale  # Adjust '20' as needed for base font size
        # Update font size for each spinner
        self.ids.sensor_channel_1.font_size = new_font_size
        self.ids.sensor_channel_2.font_size = new_font_size
        self.ids.sensor_channel_3.font_size = new_font_size
        self.ids.sensor_channel_4.font_size = new_font_size



#------------------------------------------Sensors and Time Selection Functions ----------------------------#
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
            elif name == 'sensor_channel_2':
                self.sensor_ch2 = self.sensor
            elif name == 'sensor_channel_3':
                self.sensor_ch3 = self.sensor
            elif name == 'sensor_channel_4':
                self.sensor_ch4 = self.sensor
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
            print("Halllllllo")
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


#---------------------------------------- Quary Functions and Ploting data -----------------------------------------------#
    def check_quary(self, channel):
        # This Function Will Check If Both of The Range Spinner(Timer) and Sensor Spinner(Sensor) Act By Press Update Button!
        # Has Valued by The User Not Defult! Then Call the "Plot_data()" Function with Correct Channel Input! 
        print(f"this is the channel in check_quary : {channel}")
        if channel == 1:
            channel_id = 'channel_1'
            print(self.range_ch1)
            print(self.sensor_ch1)
            if self.sensor_ch1 != 'Sensor!' and self.range_ch1 != 'Time!':
                self.plot_data(self.sensor_ch1, self.range_ch1, channel_id)
            else:
                self.clear_chart(channel_id)

        elif channel == 2:
            channel_id = 'channel_2'
            if (self.sensor_ch2 != 'Sensor!') and self.range_ch2 != 'Time!':
                self.plot_data(self.sensor_ch2, self.range_ch2, channel_id)
            else:
                self.clear_chart(channel_id)

        elif channel == 3:
            channel_id = 'channel_3'
            if (self.sensor_ch3 != 'Sensor!') and self.range_ch3 != 'Time!':
                self.plot_data(self.sensor_ch3, self.range_ch3, channel_id)
            else:
                self.clear_chart(channel_id)

        elif channel == 4:
            channel_id = 'channel_4'
            if (self.sensor_ch4 != 'Sensor!') and self.range_ch4 != 'Time!':
                    self.plot_data(self.sensor_ch4, self.range_ch4, channel_id)
            else:
                self.clear_chart(channel_id)
            
    def plot_data(self, sensor, time, channel_id):
        # Code the sensor time sheet for the database query using "time_coding" function
        time = self.time_coding(time)
        print("we are here")
        if sensor and time:
            # Query data from InfluxDB using the selected sensor and time
            data = self.query_data(sensor, time)
            if data.empty:
                self.show_error_popup("No data found for the selected sensor!")
                return

        times = data["time"]
        values = data["value"]
        #print(data)

        sensor_channel = self.ids[channel_id]
        sensor_channel.clear_widgets()

        # Create a new plot
        fig = Figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        ax.plot(times, values, label=f"{sensor} Data")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.set_title(f"{sensor} Sensor Data of {self.time_decoding(time)}")
        ax.legend()

        # Create a canvas for the plot
        plot_canvas = FigureCanvasKivyAgg(fig)

        # Bind the touch event to show the popup
        def on_canvas_touch(instance, touch):
            # Check if the touch is within the canvas bounds
            if plot_canvas.collide_point(*touch.pos):
                self.popup_plot(times, values, sensor, time)
                return True  # Consume the event to stop further propagation
            return False  # Let the event propagate if not in the canvas

        plot_canvas.bind(on_touch_down=on_canvas_touch)

        # Add the new plot to the specified channel
        sensor_channel.add_widget(plot_canvas)

    def query_data(self, sensor, time):
        query_api = write_client.query_api()
        print(f"Querying data for sensor: {sensor}, time range: {time}")
        query = f"""
        from(bucket: "{bucket}")
        |> range(start: {time})
        |> filter(fn: (r) => r.DEVICE == "{sensor}")
        """

        try:
            tables = query_api.query(query, org=org)

            # Convert results to a DataFrame
            return pd.DataFrame(
                [(record.get_time(), record.get_value()) for table in tables for record in table.records],
                columns=["time", "value"]
            )
        except Exception as e:
            # Log the error (optional)
            print(f"Error occurred during query: {e}")

            # Show the error popup
            self.show_error_popup(f"Query failed: {e}")
            return pd.DataFrame(columns=["time", "value"])  # Return an empty DataFrame

    def popup_plot(self, times, values, sensor, time):
        # Layout for the popup
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        close_button = Button(text="Close", size_hint=(1, 0.1))

        # Larger figure for the popup
        popup_fig = Figure(figsize=(8, 6))
        popup_ax = popup_fig.add_subplot(111)
        popup_ax.plot(times, values, label=f"{sensor} Data")
        popup_ax.set_xlabel("Time")
        popup_ax.set_ylabel("Value")
        popup_ax.set_title(f"{sensor} Sensor Data of {self.time_decoding(time)}")
        popup_ax.legend()

        popup_canvas = FigureCanvasKivyAgg(popup_fig)

        popup_layout.add_widget(popup_canvas)
        popup_layout.add_widget(close_button)

        # Create and open the popup
        popup = Popup(
            title="Sensor",
            content=popup_layout,
            size_hint=(0.9, 0.9),
        )
        close_button.bind(on_release=popup.dismiss)
        popup.open()



#---------------------------------------Monitoring Charts Operations----------------------#
    def create_empty_graphs(self):
        for i in range(1, 5):  # Loop through channels 1 to 4
            fig = Figure(figsize=(1, 1))  # Create a figure
            ax = fig.add_subplot(111)  # Add a subplot
            ax.set_title(f"Channel {i}")  # Set title

            # Clear previous widgets and add the figure
            sensor_channel = self.ids[f'channel_{i}']
            sensor_channel.clear_widgets()
            sensor_canvas = FigureCanvasKivyAgg(fig)
            sensor_channel.add_widget(sensor_canvas)

    def clear_chart(self, chart):
        self.ids[chart].clear_widgets()

        self.ids[f"sensor_{chart}"].text = 'Sensor!'

    def reset_charts_values(self):
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

    def time_decoding(self, time):
        decode_time = {
            '-30m': '30 Minute',
            '-1h' : '1 Hour',
            '-3h' : '3 Hours',
            '-6h' : '6 Hours',
            '-12h': '12 Hours',
            '-1d' : '1 Day',
            '-2d' : '2 Days',
            '-7d' : '7 Days',
            '-30d': '1 Month' 
        }
        return decode_time[time]
    
    def show_error_popup(self, message):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Create a label with wrapped text
        label = Label(
            text=message, 
            halign="center", 
            valign="middle",
            size_hint=(1, 1),
            #text_size=(400, None)  # Adjust width for text wrapping
        )
        label.bind(size=lambda *args: label.setter('text_size')(label, (label.width, None)))

        # Add a close button
        close_button = Button(text="Close", size_hint=(0.5, None), height=40)
        layout.add_widget(label)
        layout.add_widget(close_button)
        
        # Create the popup
        popup = Popup(title="Error", content=layout, size_hint=(0.4, 0.3))
        close_button.bind(on_release=popup.dismiss)
        popup.open()