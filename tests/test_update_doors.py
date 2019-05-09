from django.test import client, TestCase
from django.urls import reverse
from tests.data_base_test_utils import setup_db_for_test, security_door_result, storage_door_result, hall_door_result
import paho.mqtt.client as mqtt
import time
import json

C = client.Client()


class UpdateDoorsTest(TestCase):
    def setUp(self):
        setup_db_for_test()
        self.setup_door_clients()

    def setup_door_clients(self):
        self.security_door_mqtt_client = mqtt.Client()
        self.security_door_mqtt_client.connect(host="127.0.0.1", port=1883)
        self.security_door_mqtt_client.subscribe(topic="sc_2")
        self.security_door_mqtt_client.on_message = lambda client, userdata, message: self.assertSecurityUsersUpdated(
            message)
        self.security_door_mqtt_client.loop_start()
        self.security_door_sentinel = False

        self.storage_door_mqtt_client = mqtt.Client()
        self.storage_door_mqtt_client.connect(host="127.0.0.1", port=1883)
        self.storage_door_mqtt_client.subscribe(topic="st_72")
        self.storage_door_mqtt_client.on_message = lambda client, userdata, message: self.assertStorageUsersUpdated(
            message)
        self.storage_door_mqtt_client.loop_start()
        self.storage_door_sentinel = False

        self.hall_door_mqtt_client = mqtt.Client()
        self.hall_door_mqtt_client.connect(host="127.0.0.1", port=1883)
        self.hall_door_mqtt_client.subscribe(topic="hl-19")
        self.hall_door_mqtt_client.on_message = lambda client, userdata, message: self.assertHallUsersUpdated(
            message)
        self.hall_door_mqtt_client.loop_start()
        self.hall_door_sentinel = False

    def assertSecurityUsersUpdated(self, message):
        data = json.loads(message.payload)
        self.assertDictEqual(data, security_door_result)
        self.security_door_sentinel = True

    def assertStorageUsersUpdated(self, message):
        data = json.loads(message.payload)
        self.assertDictEqual(data, storage_door_result)
        self.storage_door_sentinel = True

    def assertHallUsersUpdated(self, message):
        data = json.loads(message.payload)
        self.assertDictEqual(data, hall_door_result)
        self.hall_door_sentinel = True

    def test_update_doors(self):
        C.get(path=reverse('update_doors'))
        print("waiting for mqtt publishing ...")
        time.sleep(3)
        self.assertTrue(self.security_door_sentinel)
        self.assertTrue(self.storage_door_sentinel)
        self.assertTrue(self.hall_door_sentinel)
