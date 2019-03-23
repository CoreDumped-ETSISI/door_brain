# door_brain

An API REST full to manage a mqtt communication between an escalable numbers of doors with RFID/NFC access.


## requirements

 - python3
 - virtualenv
 - Django
 - djangoresfrmework
 - paho-mqtt
 - django-rest-swagger
 
 
 ## Setup
 
Init a virtual environment:

```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Init the data base:

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
sudo apt-get istall mosquitto
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
First, run the server with `python3 manage.py runserver`. Then, open the admin interface to create a new `Broker` instance with the ip `127.0.0.1` .

Now start the MQTT communication with a GET request http://127.0.0.1:8000/mqtt/listenLogs.
Use `mosquitto_pub -h 127.0.0.1 -t "logs" -m "hi there, brain!"` command to publish a message. 

A new log must be created in the database. To be sure, in the admin site must be the new `Log` instance with the published message. 
Also you can check it with the request http://127.0.0.1:8000/logs, which should return this JSON response:

```
[
    {
        "date_time": "YYYY-MM-DDThh:mm:ss.000000Z",
        "message": "hi there, brain"
    },
]
```
