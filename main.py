from kivy.app import App
from kivy.uix.label import Label

from kivy.logger import Logger

from openmrs import RESTConnection


__app_package__ = 'edu.unl.cse.soft161.rest'
__app__ = 'Rest'
__version__ = '0.1'
__flags__ = ['--bootstrap=sdl2', '--requirements=python2,kivy', '--permission=INTERNET', '--orientation=landscape']


class RestApp(App):
    def __init__(self, **kwargs):
        super(RestApp, self).__init__(**kwargs)
        self.openmrs_connection = RESTConnection('localhost', 8080, 'admin', 'Admin123')

    def load_locations(self):
        results_layout = self.root.ids.results
        for moribund in tuple(results_layout.children):
            results_layout.remove_widget(moribund)
        self.openmrs_connection.send_request('location', None, self.on_locations_loaded,
                                             self.on_locations_not_loaded, self.on_locations_not_loaded)

    def on_locations_loaded(self, request, response):
        results_layout = self.root.ids.results
        for result in response['results']:
            results_layout.add_widget(Label(text=result['display']))

    def on_locations_not_loaded(self, request, error):
        results_layout = self.root.ids.results
        results_layout.add_widget(Label(text='[Failed to load locations]'))
        Logger.error('RestApp: {error}'.format(error=error))


if __name__ == "__main__":
    app = RestApp()
    app.run()
