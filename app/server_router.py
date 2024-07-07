from fastapi import APIRouter, HTTPException
from app import meta
from app.models import ServerModel
from app.utils import get_all_users_count, get_server_conf, get_server_port, obj_to_dict
from datetime import timedelta


router = APIRouter()


@router.get("/murmur-version")
async def murmurVersion():
    try:
        version = meta.getVersion()
        return {"version": f"{version}"}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/getAllServers")
async def getAllServer():
    """
    Lists all servers
    """
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

    return servers


@router.get("/getServerDetail")
async def getServerDetail(id: int):
    """
    return server's detail
    """
    server = meta.getServer(id)
    if server is None:
        raise HTTPException(404, f"Server with id: {id} not found")

    tree = obj_to_dict(server.getTree()) if server.isRunning() else None
    json_data = {
        "id": server.id(),
        "name": get_server_conf(meta, server, "registername"),
        "host": get_server_conf(meta, server, "host"),
        "port": get_server_port(meta, server),
        "address": "%s:%s"
        % (
            get_server_conf(meta, server, "host"),
            get_server_port(meta, server),
        ),
        "password": get_server_conf(meta, server, "password"),
        "welcometext": get_server_conf(meta, server, "welcometext"),
        "user_count": (server.isRunning() and len(server.getUsers())) or 0,
        "maxusers": get_server_conf(meta, server, "users") or 0,
        "running": server.isRunning(),
        "uptime": server.getUptime() if server.isRunning() else 0,
        "humanize_uptime": str(
            timedelta(seconds=server.getUptime()) if server.isRunning() else ""
        ),
        "parent_channel": tree["c"] if server.isRunning() else None,
        "sub_channels": tree["children"] if server.isRunning() else None,
        "users": tree["users"] if server.isRunning() else None,
        "registered_users": (
            server.getRegisteredUsers("") if server.isRunning() else None
        ),
        "log_length": server.getLogLen(),
    }
    return json_data


@router.post("/createServer")
async def createServer(model: ServerModel):
    """
    Creates a server, starts server, and return server detail
    """
    server = meta.newServer()
    # Set conf if provided
    server.setConf("password", model.password) if model.password else None
    server.setConf("port", model.port) if model.port else None
    server.setConf("timeout", model.timeout) if model.timeout else None
    server.setConf("bandwidth", model.bandwidth) if model.bandwidth else None
    server.setConf("users", model.users) if model.users else None
    server.setConf("welcometext", model.welcomeText) if model.welcomeText else None
    server.setConf("registername", model.registerName) if model.registerName else None

    # Start server
    server.start()
    return await getServerDetail(server.id())


@router.delete("/deleteServer")
async def deleteServer(id: int):
    """
    Shuts down and deletes a server
    """

    server = meta.getServer(id)

    if server is None:
        raise HTTPException(404, f"Server with id: {id} not found")

    # Stop server first if it is running
    if server.isRunning():
        server.stop()

    # Delete server instance
    server.delete()
    return {"detail": f"server with id {id} deleted successfully"}


@router.delete("/deleteServers")
async def deleteServers(id_list: list[int]):
    deletedServers: list[int] = []
    for id in id_list:
        server = meta.getServer(id)

        if not server:
            continue

        if server.isRunning():
            server.stop()

        server.delete()
        deletedServers.append(id)
    return {"deleted servers": deletedServers}


@router.delete("/deleteAllServers")
async def deleteAllServers():
    deletedServers: list[int] = []
    for s in meta.getAllServers():
        id = s.id()
        await deleteServer(id)
        deletedServers.append(id)
    return {"deleted servers": deletedServers}


@router.post("/{id}/start")
def start(id: int):
    """Starts server"""
    server = meta.getServer(id)
    if server is None:
        raise HTTPException(404, f"Server with id: {id} not found")

    if server.isRunning():
        raise HTTPException(403, "Server already running.")
    server.start()
    return {"message": f"server {id} started"}


@router.post("/{id}/stop")
def start(id: int):
    """Stop server"""
    server = meta.getServer(id)
    if server is None:
        raise HTTPException(404, f"Server with id: {id} not found")

    if not server.isRunning():
        raise HTTPException(403, "Server already stopped.")
    server.stop()
    return {"message": f"server {id} stopped"}

def sortLogs(item):
    return item["timestamp"]

@router.get("/{id}/logs")
def logs(id: int):
    """Gets all server logs by server ID"""
    server = meta.getServer(id)
    if server is None:
        raise HTTPException(404, f"Server with id: {id} not found")
    logs = []

    first = 0
    last = -1
    for log in server.getLog(first, last):
        logs.append(
            {
                "message": log.txt,
                "timestamp": log.timestamp,
            }
        )
    logs.sort(key=sortLogs)
    return logs
