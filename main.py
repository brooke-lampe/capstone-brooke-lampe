from kivy.app import App
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.properties import StringProperty
from openmrs import RESTConnection

class RestApp(App):
    recent_username = StringProperty("")
    patient_uuid = StringProperty("")
    encounters_request = StringProperty("")

    def __init__(self, **kwargs):
        super(RestApp, self).__init__(**kwargs)

    def connect(self):
        self.openmrs_connection = RESTConnection('localhost', 8080, self.root.ids.username.text, self.root.ids.password.text)
        self.root.ids.password.text = ""

    def verify(self):
        self.root.ids.verify.clear_widgets()
        self.openmrs_connection.send_request('session', None, self.on_session_loaded,
                                             self.on_session_not_loaded, self.on_session_not_loaded)

    def on_session_loaded(self, request, response):
        verify_layout = self.root.ids.verify
        #for result in response['results']:
        verify_layout.add_widget(Label(text=str(response)))
        print("Success")
        self.root.current = 'location'

    def on_session_not_loaded(self, request, error):
        self.root.ids.verify.add_widget(Label(text='[Failed to connect.  Invalid username or password]'))
        Logger.error('RestApp: {error}'.format(error=error))
        print("Failure")

    def load_locations(self):
        self.root.ids.results.clear_widgets()
        self.openmrs_connection.send_request('location', None, self.on_locations_loaded,
                                             self.on_locations_not_loaded, self.on_locations_not_loaded)

    def on_locations_loaded(self, request, response):
        results_layout = self.root.ids.results
        for result in response['results']:
            results_layout.add_widget(Label(text=result['display']))
        print(str(response))
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
        self.openmrs_connection.send_request('patient?q=10002T', None, self.on_patient_loaded,
                                             self.on_patient_not_loaded, self.on_patient_not_loaded)

    def on_patient_loaded(self, request, response):
        patient_layout = self.root.ids.patient
        #patient_layout.add_widget(Label(text=str(response)))
        print(str(response))
        for result in response['results']:
            patient_layout.add_widget(Label(text=result['display']))
            patient_uuid = result['uuid']
        print(patient_uuid)
        self.load_encounters(patient_uuid)

    def on_patient_not_loaded(self, request, error):
        self.root.ids.patient.add_widget(Label(text='[Failed to load patient information.  Please try again.]'))
        Logger.error('RestApp: {error}'.format(error=error))

    def load_encounters(self, patient_uuid):
        self.root.ids.patient.clear_widgets()
        print(self.root.ids.openmrs_id.text)
        print(patient_uuid)
        encounters_request = 'encounter?patient={patient_uuid}&limit=10'.format(patient_uuid=patient_uuid)
        print(encounters_request)
        self.openmrs_connection.send_request(encounters_request, None, self.on_encounters_loaded,
                                             self.on_encounters_not_loaded, self.on_encounters_not_loaded)

    def on_encounters_loaded(self, request, response):
        patient_layout = self.root.ids.patient
        #patient_layout.add_widget(Label(text=str(response)))
        print(str(response))
        for result in response['results']:
            patient_layout.add_widget(Label(text=result['display']))

    def on_encounters_not_loaded(self, request, error):
        self.root.ids.patient.add_widget(Label(text='[Failed to load patient information.  Please try again.]'))
        Logger.error('RestApp: {error}'.format(error=error))

    #functions for load_encounters
    #Try full to get more information about vitals

if __name__ == "__main__":
    app = RestApp()
    app.run()
