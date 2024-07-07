import Murmur
import settings
import Ice

_props = Ice.createProperties()
_props.setProperty("Ice.ImplicitContext", "Shared")
_props.setProperty("Ice.Default.EncodingVersion", "1.0")
_props.setProperty("Ice.Default.InvocationTimeout", str(30 * 1000))
_props.setProperty("Ice.MessageSizeMax", str(settings.ICE_MESSAGE_SIZE))
_data = Ice.InitializationData()
_data.properties = _props
_communicator = Ice.initialize(_data)

_proxy = _communicator.stringToProxy(settings.ICE_HOST)
secret = settings.ICE_SECRET
if secret != '':
    _communicator.getImplicitContext().put("secret", secret)
meta = Murmur.MetaPrx.checkedCast(_proxy)
if not meta:
    raise RuntimeError("Invalid proxy")

from app import api
