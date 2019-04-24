from django.test import client, TestCase
import datetime

from mqtt_brokers.models import Broker
from doors.models import Door
from mqtt_groups.models import MqttGroup
from mqtt_rules.models import WeekRules
from custom_users.models import CustomUser
from cards.models import Card

C = client.Client()


class UpdateDoorsTest(TestCase):
    def setUp(self):
        curent_rule_hk = WeekRules(
            indentf="current_rule",
            initial_hour_access="05:00",
            duration=datetime.timedelta(hours=5),
            days_per_week=[1, 5, 7],
            permission_level=1,
            initial_date="2019-01-23T00:00:00.000000Z",
            expiration_date="2020-01-23T00:00:00.000000Z",
        )
        curent_rule_s = WeekRules(
            indentf="current_rule",
            initial_hour_access="05:00",
            duration=datetime.timedelta(hours=5),
            days_per_week=[1, 5, 7],
            permission_level=1,
            initial_date="2019-01-23T00:00:00.000000Z",
            expiration_date="2020-01-23T00:00:00.000000Z",
        )
        old_rule = WeekRules(
            identf="old_rule",
            initial_hour_access="05:00",
            duration=datetime.timedelta(hours=5),
            days_per_week=[1, 5, 7],
            permission_level=1,
            initial_date="2014-01-23T00:00:00.000000Z",
            expiration_date="2025-01-23T00:00:00.000000Z",
        )

        housekeeping = MqttGroup(name="housekeeping",)
        security = MqttGroup(name="security")
        old_residents = MqttGroup(name="old_residents")

        gilbert = CustomUser(username="Gilbert")
        anna = CustomUser(username="Anna")
        maria = CustomUser(username="Maria")
        marta = CustomUser(username="Marta")
        mr_misterius = CustomUser(username="Mr_Misterius")

        gilberts_card = Card(hash="1234", user="")
        annas_card = Card(hash="2222")
        marias_card_1 = Card(hash="2121")
        marias_card_2 = Card(hash="333")
        martas_card = Card(hash="4444")
        mr_misterius_card = Card(hash="4343")

        curent_rule_hk.save()
        curent_rule_s.save()
        old_rule.save()

        housekeeping.save()
        old_residents.save()
        security.save()

        housekeeping.rules.add(curent_rule_hk)
        housekeeping.save()
        security.rules.add(curent_rule_s)
        security.save()
        old_residents.rules.add(old_rule)
        old_residents.save()

        gilbert.save()
        anna.save()
        maria.save()
        marta.save()
        mr_misterius.save()

        gilbert.groups.add(housekeeping)
        gilbert.save()
        anna.groups.add(housekeeping)
        anna.save()
        maria.groups.add(security)
        maria.save()
        marta.groups.add(security)
        marta.save()
        mr_misterius.groups.add(old_residents)
        mr_misterius_card.save()

        gilberts_card.user = "Gilbert"
        gilberts_card.save()
        annas_card.user = "Anna"
        annas_card.save()
        marias_card_1.user = "Maria"
        marias_card_1.save()
        marias_card_2.user = "Maria"
        marias_card_2.save()
        martas_card.user = "Marta"
        martas_card.save()
        mr_misterius_card.user = "Mr_Misterius"
        mr_misterius_card.save()

