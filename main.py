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

    def load_session(self):
        self.root.ids.session.clear_widgets()
        self.openmrs_connection.send_request('session', None, self.on_session_loaded,
                                             self.on_session_not_loaded, self.on_session_not_loaded)

    def on_session_loaded(self, request, response):
        if response['authenticated']:
            self.root.ids.session2.text = 'Welcome, {user}, you have logged in successfully.'.format(user=response['user']['display'])
            self.root.current = 'selection'
        else:
            self.root.ids.session.text = 'Unable to authenticate.  Invalid username or password.'
            self.root.ids.session2.text = 'Please verify credentials and try again.'
            self.root.ids.password.text = ''

    def on_session_not_loaded(self, request, error):
        self.root.ids.session.text = 'Unable to connect.'
        self.root.ids.session2.text = 'Please verify internet connection and try again.'
        Logger.error('RestApp: {error}'.format(error=error))

    def load_patient(self):
        self.openmrs_connection.send_request('patient?q={openmrs_id}'.format(openmrs_id=self.root.ids.openmrs_id.text), None, self.on_patient_loaded,
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
        encounters_request = 'encounter?patient={patient_uuid}&limit=10&custom:(uuid,datatype:(uuid,name),conceptClass,names:ref)'.format(patient_uuid=patient_uuid)
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

    #The code below will ultimately be deleted
    def load_locations(self):
        self.root.ids.results.clear_widgets()
        self.openmrs_connection.send_request('location', None, self.on_locations_loaded,
                                             self.on_locations_not_loaded, self.on_locations_not_loaded)

    def on_locations_loaded(self, request, response):
        results_layout = self.root.ids.results
        for result in response['results']:
            results_layout.add_widget(Label(text=result['display']))
        print(str(response))

    def on_locations_not_loaded(self, request, error):
        self.root.ids.results.add_widget(Label(text='[Failed to load locations]'))
        Logger.error('RestApp: {error}'.format(error=error))


if __name__ == "__main__":
    app = RestApp()
    app.run()
