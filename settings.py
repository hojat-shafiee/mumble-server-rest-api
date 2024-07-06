import os

# Ice connectivity
ICE_HOST_HOST = os.environ.get("MURMUR_ICE_HOST", "localhost")
ICE_HOST_PORT = os.environ.get("MURMUR_ICE_PORT", "6502")
ICE_HOST = "Meta:tcp -h " + ICE_HOST_HOST + " -p " + ICE_HOST_PORT

ICE_MESSAGE_SIZE = 1024
