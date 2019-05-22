from paho.mqtt import client as mqtt
from threading import Lock


class Mqtt:
    __instance = None
    __active_mqtt_clients = []
    lock = Lock()

    @staticmethod
    def get_manager():
        if Mqtt.__instance is None:
            Mqtt()
        return Mqtt.__instance

    def __init__(self):
        if Mqtt.__instance is not None:
            raise Exception("The Mqtt manager has been already instantiated")
        else:
            Mqtt.__instance = self

    def get_client(self):
        self.lock.acquire()
        client = self._generate_client()
        self.lock.release()
        return client

    def _generate_client(self):
        new_client = mqtt.Client()
        self.__active_mqtt_clients.append(new_client)
        return new_client

    def del_clients(self):
        self.lock.acquire()
        for client in self.__active_mqtt_clients:
            client.disconnect()
            self.__active_mqtt_clients.remove(client)
            del client
        self.lock.release()
