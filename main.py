from fastapi import FastAPI, HTTPException
import Ice
import Murmur
import settings
from utils import get_all_users_count, get_server_conf, get_server_port
from datetime import timedelta

_props = Ice.createProperties()
_props.setProperty("Ice.ImplicitContext", "Shared")
_props.setProperty("Ice.Default.EncodingVersion", "1.0")
_props.setProperty("Ice.Default.InvocationTimeout", str(30 * 1000))
_props.setProperty("Ice.MessageSizeMax", str(settings.ICE_MESSAGE_SIZE))
_data = Ice.InitializationData()
_data.properties = _props
communicator = Ice.initialize(_data)
proxy = communicator.stringToProxy(settings.ICE_HOST)

meta = Murmur.MetaPrx.checkedCast(proxy)
if not meta:
    del communicator
    raise RuntimeError("Invalid proxy")


app: FastAPI = FastAPI(
    title="Mumble server rest api",
    version="0.0.1",  # docs_url=None, redoc_url=None
)


@app.get("/")
def root():
    try:
        version = meta.getVersion()
        return {"detail": f"app version : {app.version}, murmur ice version: {version}"}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/getAllServers")
def getAllServer():
    servers = []
    for s in meta.getAllServers():
        host = get_server_conf(meta, s, "host")
        port = get_server_port(meta, s)
        is_running = s.isRunning()
        uptime = s.getUptime() if is_running else 0

        servers.append(
            {
                "id": s.id(),
                "name": get_server_conf(meta, s, "registername"),
                "address": "%s:%s" % (host, port),
                "host": host,
                "port": port,
                "running": is_running,
                "users": (is_running and len(s.getUsers())) or 0,
                "maxusers": get_server_conf(meta, s, "users") or 0,
                "channels": (is_running and len(s.getChannels())) or 0,
                "uptime_seconds": uptime if is_running else 0,
                "uptime": str(timedelta(seconds=uptime) if is_running else ""),
                "log_length": s.getLogLen(),
            }
        )

    return {"servers": servers}
