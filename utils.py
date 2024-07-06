def get_server_conf(meta, server, key):
    """
    Gets the server configuration for given server/key.
    """
    val = server.getConf(key)
    if "" == val:
        val = meta.getDefaultConf().get(key, "")
    return val


def get_server_port(meta, server, val=None):
    """
    Gets the server port value from configuration.
    """
    val = server.getConf("port") if val is None else val

    if "" == val:
        val = meta.getDefaultConf().get("port", 0)
        val = int(val) + server.id() - 1
    return int(val)


def get_all_users_count(meta):
    """
    Gets the entire list of users online count by iterating through servers.
    """
    user_count = 0
    for s in meta.getAllServers():
        user_count += (s.isRunning() and len(s.getUsers())) or 0
    return user_count
