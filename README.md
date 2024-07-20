Reading data from IOT sensors and publishing it to the cloud using MQTT.

The following files are used :-
publish.py:- Reads temperature data and publishes it to an MQTT topic
server.py:- Exposes the latest sensor data through an HTTP endpoint using Flask.
subscriber.py :- Checks for temperature threshold, if exceeded, raises an alarm.

To run the project install the requirements mentioned in requirements.txt.
pip install -r requirements.txt
