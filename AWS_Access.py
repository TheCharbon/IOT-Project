from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import config

def init():
    global myMQTTClient
    myMQTTClient = AWSIoTMQTTClient(config.CLIENT_ID)
    myMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
    myMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)
    myMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
    myMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)
    if myMQTTClient.connect():
        print('AWS connection succeeded')

def pub(message):
    myMQTTClient.publish(config.TOPIC, message, 1)
    print(f"send {message} to ${config.TOPIC}")