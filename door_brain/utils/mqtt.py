from paho.mqtt import client as mqtt
from threading import Lock


class Mqtt:
    __instance = None
    __active_mqtt_clients = []
    __sleep_mqtt_clients = []
    lock = Lock()

    @staticmethod
    def get_manager():
        if Mqtt.__instance is None:
            Mqtt()
        return Mqtt.__instance

    def __init__(self):
        if self.__instance is not None:
            raise Exception("The Mqtt manager has been already instantiated")
        else:
            self.__instance = self

    def get_client(self):
        self.lock.acquire()
        client = self._generate_client()
        self.lock.release()
        return client

    def _generate_client(self):
        if self.__sleep_mqtt_clients:
            new_client = self.__sleep_mqtt_clients[0]
            self.__sleep_mqtt_clients.pop(0)
        else:
            new_client = mqtt.Client()
            self.__active_mqtt_clients.append(new_client)
        return new_client

    def lull_client(self, client):
        self.lock.acquire()
        if client not in self.__active_mqtt_clients:
            raise Exception("The client is not active")
        else:
            self.__active_mqtt_clients.remove(client)
            client.reinitialise()
            self.__sleep_mqtt_clients.append(client)
        self.lock.release()

    def lull_clients(self):
        self.lock.acquire()
        for client in self.__sleep_mqtt_clients:
            self.__active_mqtt_clients.remove(client)
            client.reinitialise()
            self.__sleep_mqtt_clients.append(client)
        self.lock.release()


Mqtt()