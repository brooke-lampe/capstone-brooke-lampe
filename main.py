from kivy.app import App
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.properties import StringProperty
from openmrs import RESTConnection

class RestApp(App):
    recent_username = StringProperty("")

    def __init__(self, **kwargs):
        super(RestApp, self).__init__(**kwargs)

    def connect(self):
        self.openmrs_connection = RESTConnection('localhost', 8080, self.root.ids.username.text, self.root.ids.password.text)
        self.root.ids.password.text = ""

    def load_locations(self):
        self.root.ids.results.clear_widgets()
        self.openmrs_connection.send_request('location', None, self.on_locations_loaded,
                                             self.on_locations_not_loaded, self.on_locations_not_loaded)

    def on_locations_loaded(self, request, response):
        results_layout = self.root.ids.results
        for result in response['results']:
            results_layout.add_widget(Label(text=result['display']))
        recent_username = self.root.ids.username.text
        #Do I need the above line?  Username should remain in the TextInput
        #Later on, this will become a confirmation that the login was successful and will not be shown

    def on_locations_not_loaded(self, request, error):
        self.root.ids.results.add_widget(Label(text='[Failed to load locations]'))
        Logger.error('RestApp: {error}'.format(error=error))
        #Later on, this will become an error that the login was not successful and will not be shown

    def load_patient(self):
        self.root.ids.patient.clear_widgets()
        print(self.root.ids.openmrs_id.text)
        self.openmrs_connection.send_request('patient', None, self.on_patient_loaded,
                                             self.on_patient_not_loaded, self.on_patient_not_loaded)

    def on_patient_loaded(self, request, response):
        patient_layout = self.root.ids.patient
        for patient in response['patient']:
            patient_layout.add_widget(Label(text=patient['display']))

    def on_patient_not_loaded(self, request, error):
        self.root.ids.patient.add_widget(Label(text='[Failed to load patient information.  Please try again.]'))
        Logger.error('RestApp: {error}'.format(error=error))


if __name__ == "__main__":
    app = RestApp()
    app.run()
