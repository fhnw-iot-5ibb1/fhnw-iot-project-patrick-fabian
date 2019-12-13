import requests

class ThingSpeakService():

        def __init__(self):
            self.url = 'https://api.thingspeak.com/channels/'
            self.channel = 935198
            self.apikey = '81SYGRV7PHQU25C8'
            self.co2field = 'field1'
            self.tempfield = 'field2'
            self.humfield = 'field3'



        def get_readings_json(self, nrReadings):
            req = self.url + str(self.channel) + '/feeds.json?api_key=' + self.apikey + '&results=' + str(nrReadings)
            response = requests.get(req)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return 'error'

        def get_field(self, fieldName, numReadings):
            json = self.get_readings_json(numReadings)
            feeds = json.get('feeds')
            if numReadings == 1:
                return feeds[0].get(fieldName)
            else:
                readings = []
                for i in range(numReadings):
                    readings.append(feeds[i].get(fieldName))
                return readings

        def get_co2(self, nr = 1):
            return self.get_field(self.co2field, nr)

        def get_temp(self, nr=1):
            return self.get_field(self.tempfield, nr)

        def get_hum(self, nr=1):
            return self.get_field(self.humfield, nr)
