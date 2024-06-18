import ubinascii
import machine
from umqtt.simple2 import MQTTClient import config

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_BROKER_SERVER = mqtt_config['server']
MQTT_BROKER_PORT = mqtt_config['port']
MQTT_BROKER_USERNAME = mqtt_config['username']
MQTT_BROKER_PASSWORD = mqtt_config['password']

class Mqtt:
    def __init__(self,
                 server: str = MQTT_BROKER_SERVER,
                 port: int = MQTT_BROKER_PORT,
                 username: str = MQTT_BROKER_USERNAME,
                 password: str = MQTT_BROKER_PASSWORD,
                 device_uuid: str = CLIENT_ID,
                 ) -> None:

        # Connection
        self._server = server
        self._port = port
        self._username = username
        self._password = password

        # Client
        self._client = None
        self._client_id: str = device_uuid

    def _connect(self):
        try:
            if self._client is None:
                self._client = MQTTClient(
                        self._client_id,
                        self._server,
                        port=self._port,
                        user=self._username,
                        password=self._password
                        )
                self._client.connect()
            else:
                # TODO: Reconnect here
            return True, {}
        except Exception as err:
            print(f"Error connecting device to message broker: {err}")
            return False, {'msg': err}

    def _disconnect(self) -> None:
        if self._client is not None:
            self._client.disconnect()

    def start(self) -> None:
        succ, resp = self._connect()
        if succ and self._client is not None:
            print("Started App MQTT Client")
        else:
            print(f"Can't start MQTT client - {resp['msg']}")

    def stop(self) -> None:
        if self._client is not None:
            self._client.disconnect()
            print("Stopped App MQTT Client")

    def publish(self, topic: str, message: str) -> None:
        if self._client is not None:
            self._client.publish(topic, message)
            print(f"Published message - {message[:20]")
