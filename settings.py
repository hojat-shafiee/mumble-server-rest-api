import os

# Ice connectivity
ICE_HOST_ADDRESS = os.environ.get("MURMUR_ICE_HOST", "localhost")
ICE_HOST_PORT = os.environ.get("MURMUR_ICE_PORT", "6502")
ICE_HOST = f"Meta:tcp -h {ICE_HOST_ADDRESS} -p {ICE_HOST_PORT} -t 1000"

ICE_MESSAGE_SIZE = 1024
