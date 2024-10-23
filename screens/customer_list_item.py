from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty
from kivy.app import App

class CustomerListItem(BoxLayout):
    customer = DictProperty({})

    def __init__(self, customer, **kwargs):
        super().__init__(**kwargs)

        self.customer = customer  # Store the passed customer data
        self.bind(customer=self.update_display)
        self.update_display()
        self.is_selected = False

    def update_display(self, *args):
        """Update the label text based on the customer data."""
        self.ids.customer_label.text = f"{self.customer.get('first_name', 'Unknown')} {self.customer.get('last_name', 'Unknown')}"

    def on_select(self, is_active):
        """Triggered when the checkbox is selected or deselected."""
        self.is_selected = is_active
        if is_active:
            App.get_running_app().root.get_screen('customer_setup').on_customer_selected(self.customer)
        print(f"Displaying details for {self.customer['first_name']} {self.customer['last_name']}")

    def on_name_click(self):
        """Triggered when the customer's name is clicked, showing the popup."""
        App.get_running_app().root.get_screen('customer_setup').show_customer_info(self.customer)
        if self.is_selected:
            print(f"Selected {self.customer['first_name']} {self.customer['last_name']} for sensor setup")
