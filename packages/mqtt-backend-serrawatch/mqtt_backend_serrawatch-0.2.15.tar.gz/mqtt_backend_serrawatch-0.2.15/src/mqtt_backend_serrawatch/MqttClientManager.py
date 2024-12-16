import paho.mqtt.client as mqtt
from .data import TopicsConfig, BrokerConfig

from SerraWatchLogger.backend import LoggerSerraWatch
Logger = LoggerSerraWatch.LoggerSerraWatch.get_instance("SerraWatch")

class MQTTClientManager:
    def __init__(self, broker_config: BrokerConfig, topics_config: TopicsConfig, on_message_callback):
        """
        Initializes the MQTTClientManager with broker and topic configurations.
        :param broker_config: Configuration for the MQTT broker (address and port).
        :param topics_config: Configuration for the topics to subscribe to.
        """
        self.broker_config = broker_config
        self.topics_config = topics_config
        self.on_message_callback = on_message_callback
        self.client = mqtt.Client()

        # Assign callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        Logger.debug(self=Logger, message="[SUBSCRIBERS] MQTTClientManager initialized.")

    def on_connect(self, client, userdata, flags, rc):
        """
        Handles the connection to the MQTT broker.
        :param client: The MQTT client instance.
        :param userdata: User-defined data of any type.
        :param flags: Response flags sent by the broker.
        :param rc: The connection result.
        """
        if rc == 0:
            Logger.info(self=Logger, message="[SUBSCRIBERS] Connected to MQTT Broker successfully.")
            # Subscribe to multiple topics
            for topic in self.topics_config.subscribers:
                self.client.subscribe(topic)
                Logger.debug(self=Logger, message=f"[SUBSCRIBERS] Subscribed to topic: {topic}")
        else:
            Logger.error(self=Logger, message=f"[SUBSCRIBERS] Failed to connect to MQTT Broker. Return code: {rc}")

    def on_message(self, client, userdata, msg):
        """
        Handles incoming messages from subscribed topics.
        :param client: The MQTT client instance.
        :param userdata: User-defined data of any type.
        :param msg: The received MQTT message.
        """
        if "log" in msg.topic:
            Logger.info(self=Logger,
                        message=f"[SUBSCRIBERS] Message received: Topic: {msg.topic}")
            Logger.add_topic_log(self=Logger, topic=msg.topic,
                                 message=f"[SUBSCRIBERS] Message received: Topic: {msg.topic}")
        else:
            Logger.info(self=Logger,
                        message=f"[SUBSCRIBERS] Message received: Topic: {msg.topic}, Payload: {msg.payload.decode()}")
            Logger.add_topic_log(self=Logger, topic=msg.topic,
                                 message=f"[SUBSCRIBERS] Message received: Topic: {msg.topic}, Payload: {msg.payload.decode()}")

        # Appelle le callback défini dans l'interface
        self.on_message_callback(msg.topic, msg.payload.decode())

    def connect_and_listen(self):
        """
        Connects to the MQTT broker and starts listening for messages indefinitely.
        """
        try:
            Logger.debug(self=Logger, message=f"[SUBSCRIBERS] Connecting to broker at {self.broker_config.address}:{self.broker_config.port}")
            if self.broker_config.port == 8883:
                if not hasattr(self, "tls_configured") or not self.tls_configured:
                    self.client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
                    self.tls_configured = True  # Marquer TLS comme configuré
                    Logger.debug(self=Logger, message=f"[SUBSCRIBERS] SSL Establish")
            self.client.connect(self.broker_config.address, self.broker_config.port, 60)
            # Start listening (blocking loop)
            self.client.loop_forever()
        except Exception as e:
            Logger.error(self=Logger, message=f"[SUBSCRIBERS] Error while connecting to MQTT broker: {e}")

    def disconnect_and_stop(self):
        """
        Disconnects from the MQTT broker and stops the network loop.
        """
        try:
            Logger.debug(self=Logger, message="[SUBSCRIBERS] Disconnecting from MQTT Broker and stopping the loop.")
            self.client.disconnect()  # Disconnect the client from the broker
            self.client.loop_stop()  # Stop the listening loop
            Logger.info(self=Logger, message="[SUBSCRIBERS] Disconnected from MQTT Broker successfully.")
        except Exception as e:
            Logger.error(self=Logger, message=f"[SUBSCRIBERS] Error while disconnecting from MQTT broker: {e}")