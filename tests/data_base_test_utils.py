from mqtt_rules.models import WeekRules
from mqtt_groups.models import MqttGroup
from custom_users.models import User
from cards.models import Card
from doors.models import Door
from mqtt_brokers.models import Broker
import datetime

security_door_result = {
    'groups': {
        'security': {
            'time_table': {
                'L': [['14:00', '24:00']],
                'M': [['14:00', '24:00']],
                'X': [['14:00', '24:00']],
                'J': [['14:00', '24:00']],
                'V': [['14:00', '24:00']],
                'S': [['14:00', '24:00']],
                'D': [['14:00', '24:00']]
            },
            'init_date': '2019-01-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        },
    },
    'cards': {
        '2121': {
            'groups': ['security'],
            'init_date': '2018-10-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        },
        '333': {
            'groups': ['security'],
            'init_date': '2018-10-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        },
        '4444': {
            'groups': ['security'],
            'init_date': '2018-10-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        }
    }
}

storage_door_result = {
    'groups': {
        'housekeeping': {
            'time_table': {
                'L': [['05:00', '11:00']],
                'M': [['14:00', '18:00']],
                'X': [['05:00', '11:00'], ['14:00', '18:00']],
                'J': [['14:00', '18:00']],
                'V': [['05:00', '11:00']],
                'S': [['14:00', '18:00']],
                'D': [['05:00', '11:00']]
            },
            'init_date': '2019-01-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        },
    },
    'cards': {
        '1234': {
            'groups': ['housekeeping'],
            'init_date': '2018-10-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        },
        '2222': {
            'groups': ['housekeeping'],
            'init_date': '2018-10-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        },
    }
}

hall_door_result = {
    'groups': {
        'security': {
            'time_table': {
                'L': [['14:00', '24:00']],
                'M': [['14:00', '24:00']],
                'X': [['14:00', '24:00']],
                'J': [['14:00', '24:00']],
                'V': [['14:00', '24:00']],
                'S': [['14:00', '24:00']],
                'D': [['14:00', '24:00']]
            },
            'init_date': '2019-01-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        },
        'housekeeping': {
            'time_table': {
                'L': [['05:00', '11:00']],
                'M': [['14:00', '18:00']],
                'X': [['05:00', '11:00'], ['14:00', '18:00']],
                'J': [['14:00', '18:00']],
                'V': [['05:00', '11:00']],
                'S': [['14:00', '18:00']],
                'D': [['05:00', '11:00']]
            },
            'init_date': '2019-01-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        },
    },
    'cards': {
        '2121': {
            'groups': ['security'],
            'init_date': '2018-10-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        },
        '333': {
            'groups': ['security'],
            'init_date': '2018-10-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        },
        '4444': {
            'groups': ['security'],
            'init_date': '2018-10-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        },
        '1234': {
            'groups': ['housekeeping'],
            'init_date': '2018-10-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        },
        '2222': {
            'groups': ['housekeeping'],
            'init_date': '2018-10-23T00:00:00.000000Z',
            'exp_date': '2020-10-23T00:00:00.000000Z'
        },
    }
}


def setup_db_for_test():
    current_rule_1 = WeekRules.objects.create(
        identf="current_rule_1",
        initial_hour_access="05:00",
        duration=datetime.timedelta(hours=6),
        days_per_week=[1, 3, 5, 7],
    )
    current_rule_2 = WeekRules.objects.create(
        identf="current_rule_2",
        initial_hour_access="14:00",
        duration=datetime.timedelta(hours=4),
        days_per_week=[2, 3, 4, 6],
    )
    current_rule_3 = WeekRules.objects.create(
        identf="current_rule_3",
        initial_hour_access="14:00",
        duration=datetime.timedelta(hours=10),
        days_per_week=[1, 2, 3, 4, 5, 6, 7],
    )
    old_rule = WeekRules.objects.create(
        identf="old_rule",
        initial_hour_access="07:00",
        duration=datetime.timedelta(hours=5),
        days_per_week=[3, 6, 7],
    )

    housekeeping = MqttGroup.objects.create(
        name="housekeeping",
        initial_date="2019-01-23",
        expiration_date="2020-01-23",
    )
    security = MqttGroup.objects.create(
        name="security",
        initial_date="2019-01-23",
        expiration_date="2020-01-23",
    )
    old_residents = MqttGroup.objects.create(
        name="old_residents",
        initial_date="2014-01-23",
        expiration_date="2025-01-23",
    )

    gilbert = User.objects.create(username="Gilbert")
    anna = User.objects.create(username="Anna")
    maria = User.objects.create(username="Maria")
    marta = User.objects.create(username="Marta")
    mr_misterius = User.objects.create(username="Mr_Misterius")

    gilberts_card = Card.objects.create(
        hash="1234",
        initial_date="2018-10-23",
        expiration_date="2020-10-23",
    )
    annas_card = Card.objects.create(
        hash="2222",
        initial_date="2018-10-23",
        expiration_date="2020-10-23",
    )
    marias_card_1 = Card.objects.create(
        hash="2121",
        initial_date="2018-10-23",
        expiration_date="2020-10-23",
    )
    marias_card_2 = Card.objects.create(
        hash="333",
        initial_date="2018-10-23",
        expiration_date="2020-10-23",
    )
    martas_card = Card.objects.create(
        hash="4444",
        initial_date="2018-10-23",
        expiration_date="2020-10-23",
    )
    mr_misterius_card = Card.objects.create(
        hash="4343",
        initial_date="2018-10-23",
        expiration_date="2020-10-23",
    )

    storage_room_door = Door.objects.create(
        id="st-door",
        manage_topic="st_72"
    )
    security_room_door = Door.objects.create(
        id="sc-door",
        manage_topic="sc_2"
    )
    hall_door = Door.objects.create(
        id="hl-door",
        manage_topic="hl_19"
    )

    server_A = Broker.objects.create(
        ip="127.0.0.1",
        port=1883,
        duty="logs"
    )
    server_B = Broker.objects.create(
        ip='127.0.0.1',
        port=1883,
        duty="management"
    )

    current_rule_1.save()
    current_rule_2.save()
    current_rule_3.save()
    old_rule.save()

    housekeeping.save()
    old_residents.save()
    security.save()

    housekeeping.rules.add(current_rule_1, current_rule_2)
    housekeeping.save()
    security.rules.add(current_rule_3)
    security.save()
    old_residents.rules.add(old_rule)
    old_residents.save()

    gilbert.save()
    anna.save()
    maria.save()
    marta.save()
    mr_misterius.save()

    gilbert.mqtt_groups.add(housekeeping)
    gilbert.save()
    anna.mqtt_groups.add(housekeeping)
    anna.save()
    maria.mqtt_groups.add(security)
    maria.save()
    marta.mqtt_groups.add(security)
    marta.save()
    mr_misterius.mqtt_groups.add(old_residents)
    mr_misterius.save()

    gilberts_card.user = gilbert
    gilberts_card.save()
    annas_card.user = anna
    annas_card.save()
    marias_card_1.user = maria
    marias_card_1.save()
    marias_card_2.user = maria
    marias_card_2.save()
    martas_card.user = marta
    martas_card.save()
    mr_misterius_card.user = mr_misterius
    mr_misterius_card.save()

    server_A.save()
    server_B.save()

    storage_room_door.save()
    security_room_door.save()
    hall_door.save()

    storage_room_door.logs_broker = server_A
    storage_room_door.manage_broker = server_B
    storage_room_door.groups.add(housekeeping)
    storage_room_door.save()
    security_room_door.logs_broker = server_A
    security_room_door.logs_broker = server_B
    security_room_door.groups.add(security)
    security_room_door.save()
    hall_door.logs_broker = server_A
    hall_door.manage_broker = server_B
    hall_door.groups.add(security, housekeeping)
    hall_door.save()


