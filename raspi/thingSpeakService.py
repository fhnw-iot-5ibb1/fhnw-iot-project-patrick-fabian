import requests
from time import time, sleep

class ThingSpeakService:

    def __init__(self):
        self.url = 'https://api.thingspeak.com/channels/'
        self.channel = 935198
        self.api_key = '81SYGRV7PHQU25C8'
        self.co2_field = 'field1'
        self.temp_field = 'field2'
        self.hum_field = 'field3'
        self.read_delay = 10
        self.last_read_time = 0
        self.last_reading = ""
        

    def get_readings_json(self, nr_readings):
        current_time = time()
        if current_time - self.last_read_time > self.read_delay:
            self.last_read_time = current_time
            req = self.url + str(self.channel) + '/feeds.json?api_key=' + self.api_key + '&results=' + str(nr_readings)
            response = requests.get(req)
            if response.status_code == 200:
                self.last_reading = response.json()
                return response.json()
            elif response.status_code == 404:
                raise Exception('bad response ' + str(response.status_code))
        else:
            return self.last_reading

    def get_field(self, field_name, num_readings):
        json = self.get_readings_json(num_readings)
        feeds = json.get('feeds')
        if num_readings == 1:
            return feeds[0].get(field_name)
        else:
            readings = []
            for i in range(num_readings):
                readings.append(feeds[i].get(field_name))
            return readings

    def get_co2(self, nr=1):
        return self.get_field(self.co2_field, nr)

    def get_temp(self, nr=1):
        return self.get_field(self.temp_field, nr)

    def get_hum(self, nr=1):
        return self.get_field(self.hum_field, nr)