# door_brain

An API REST full to manage a mqtt communication between an escalable numbers of doors with RFID/NFC access.


## requirements

 - python3
 - pip3
 - Django
 - djangoresfrmework
 - paho-mqtt
 - django-rest-swagger
 
 
 ## Setup
Init the data base:

First, we need to install postgresql. In linux:
```
sudo apt-get install libpq-dev postgresql
```
Create the Database, the user and his password
```
createdb door-brain_DB
createuser lordmascachapas
psql
ALTER USER lordmascachapas WITH PASSWORD 'admin';
```

Then, install python requirements:
```
pip3 install -r requirements.txt
```
(Notice that is needed to install libpq-dev and postgresql to install psycopg2 with the python requirements)

Make the Django migrations:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

Create an admin user:
```
python3 manage.py createsuperuser
```

Run the server:
```
python3 manage.py runserver [ip:port]
```

The http://127.0.0.1:8000/ path will display a swagger doc with the API endpoints.

The http://127.0.0.1:8000/admin path will open an administration interface where login with super user credentials.

## Usage

This API generates MQTT clients lo listen and save other clients (Doors) messages as logs.

### Into the MQTT comunication

The MQTT protocol requires a broker, which will manage the clients messages. 
There are different ways to setup a MQTT broker. Here is an example with Mosquitto:

```
sudo apt-get update
sudo apt-get install mosquitto
```

**CONGRATULATIONS !!!**

Your MQTT broker is installed and operative. Now we need clients:
```
sudo apt-get install mosquitto-clients
```

MQTT clients need the broker ip to send and get messages. You can use `127.0.0.1` to test it.

To setup a *subscriber* type the next command:
```
mosquitto_sub -h 127.0.0.1 -t "some_topic"
```
A *subscriber* is a client which will wait for messages with `"some_topic"` as topic.

Now try to send a message from another command prompt. *Publishers* must send messages with the same topic:

```
mosquitto_pub -h 127.0.0.1 -t "some_topic" -m "some_message"
```

Your *publisher* sent a message and your *subscriber* has received that message

### The Brain listens

Now try the API to start listen other MQTT clients. In the `door_brain/settings.py` file are the topics which the API will use to manage the doors

 - "logs": To listen the doors and save their messages as logs in a database
 - "manager": Which will be use to send users data to the doors

To try the MQTT communication, is needed to tell the Brain to which brokers will send and listen messages.
First, run the server with `python3 manage.py runserver`. Then, open the admin interface to create a new `Broker` instance with the ip `127.0.0.1` and 'logs listener' as duty.
Also you will need to create a door instance, an mqtt_group and a week_rule (Relational databases :D). 

Now start the MQTT communication with a GET request http://127.0.0.1:8000/mqtt/listenLogs.

To save a log, the message should be a jsonized data like this:

```
{
	"card_authorized": false,
	"door": "1789339278014108", 
	"date_time": "2013-01-29T12:34:56.000000Z", 
	"card_hash": "982341", 
	"reason": "card does not exists"
}
``` 
Use `mosquitto_pub -h 127.0.0.1 -t "logs" -m '{"card_authorized": false, "door": "1789339278014108", "date_time": "2013-01-29T12:34:56.000000Z", "card_hash": "982341", "reason": "card does not exists"}'` command to publish the message. 

A new log must be created in the database. To be sure, in the admin site must be the new `Log` instance with the published message. 
Also you can check it with the request http://127.0.0.1:8000/logs, which should return this JSON response:

```
[
    {
        "id": 1,
        "card_authorized": false,
        "reason": "card does not exists",
        "date_time": "2013-01-29T12:34:56Z",
        "card_hash": "982341",
        "door": "1789339278014108"
    },
]
```

### The Brain talks

Remember to create a broker with 'management' as duty. Having two brokers with the same ip is not allowed, so you can update the broker `127.0.0.1` with the duty 'management'.

A message can be published with the GET request http://127.0.0.1:8000/mqtt/sendMessage/msg.
The last extension *msg* will be the message to publish.
Start a *subscriber* with `mosquitto_sub -h 127.0.0.1 -t "manager"` and make the request.
The command console will display the message.

http://127.0.0.1:8000/mqtt/sendMessage/Hello

http://127.0.0.1:8000/mqtt/sendMessage/Dude

http://127.0.0.1:8000/mqtt/sendMessage/ooooh

```
linux:~$ mosquitto_sub -h 127.0.0.1 -t "manager"
Hello
Dude
ooooh
```
