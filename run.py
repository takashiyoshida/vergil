from EchoLayer import EchoLayer
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks import YowAckProtocolLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.coder import YowCoderLayer
from yowsup.stacks import YowStack
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS
from yowsup import env

import json

#
# getCredentials
# - Get login information from a JSON file
#
def getCredentials(configFile):
    credentials = None
    with open(configFile, 'r') as config:
        data = json.load(config)
        credentials = (data['phone'].encode('ascii'), data['password'].encode('ascii'))
    return credentials

if __name__ == "__main__":
    CREDENTIALS = getCredentials("vergil.conf")
    
    layers = (
        EchoLayer,
        (YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer)
    ) + YOWSUP_CORE_LAYERS
    
    stack = YowStack(layers)
    # Setting credentials
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)
    # WhatsApp server address
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
    # Information about us as WhatsApp client
    stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())
    
    # Send connect signal
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
    
    # Program's main loop
    stack.loop()
