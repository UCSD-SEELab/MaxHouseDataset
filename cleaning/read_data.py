import sys
sys.path.append('../')

from preliminaries.preliminaries import *

def toDateTime(s):
    dt = parser.parse(s)
    return dt

# **** Processing procedure for raw data ****
class RawDataDigester(object):
    def __init__(self, data_path, label_path):
        with open(data_path) as fh:
            lines = fh.readlines()

        with open(label_path) as fh:
            self.labels = fh.readlines()

        self.data = defaultdict(list)

        curr_timestamp = None
        for line in lines:
            line = eval(line.strip())
            topic = line['Topic']
            if topic == 'watch':
                curr_timestamp = line['TimeStamp']

            if curr_timestamp is not None:
                break

        for line in lines:
            try:
                line = eval(line.strip())
                topic = line['Topic']

                message = line['Payload']

                if topic == 'watch':
                    curr_timestamp = line['TimeStamp']
                    message = {"timestamp": curr_timestamp, "message": message}
                else:
                    message = {"timestamp": curr_timestamp, "message": message}

                self.data[topic].append(message)
            except SyntaxError:
                continue

    def get_watch_data(self):
        return self.data['watch']

    def get_pir_data(self):
        return self.data['pir/raw/1'], self.data['pir/raw/2']

    def get_plugs_data(self):
        return self.data['plug1'], self.data['plug2'], self.data['plug3']

    def get_ble_data(self):
        return self.data['rssi1'], self.data['rssi2'], self.data['rssi3']

    def get_smartthings_data(self):
        return self.data['smartthings']

    def get_bulb_data(self):
        return self.data["bulb"], self.data["kitchen_bulb"]

    def get_pressuremat_data(self):
        return self.data['PressureMat/raw']

    def list_topics(self):
        return self.data.keys()

    def get_labels(self):

        for line in self.labels:
            message = line.strip().split(" ", 2)
            curr_timestamp = message[0] + " " + message[1]
            print message
            message = {"timestamp": curr_timestamp, "message": message[2]}
            self.data["labels"].append(message)

        return self.data["labels"]

if __name__ == '__main__':
    data_file = "../data/subject1_data/MQTT_Messages.txt"
    labels_file = "../data/subject1_data/labels.txt"

    p = RawDataDigester(data_file, labels_file)

    print p.list_topics()

