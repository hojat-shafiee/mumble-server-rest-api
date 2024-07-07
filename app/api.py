from fastapi import APIRouter, HTTPException
from app import meta
from app.utils import get_all_users_count, get_server_conf, get_server_port
from datetime import timedelta


router = APIRouter()


@router.get("/murmur-version")
async def murmur_version():
    try:
        version = meta.getVersion()
        return {"version": f"{version}"}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/getAllServers")
async def getAllServer():
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
