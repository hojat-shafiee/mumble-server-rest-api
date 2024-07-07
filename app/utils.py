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

def obj_to_dict(obj):
    """
    Used for converting objects from Murmur.ice into python dict.
    """
    rv = {'_type': str(type(obj))}

    if isinstance(obj, (bool, int, float, str)):
        return obj

    if type(obj) in (list, tuple):
        return [obj_to_dict(item) for item in obj]

    if type(obj) == dict:
        return dict((str(k), obj_to_dict(v)) for k, v in obj.items())

    return obj_to_dict(obj.__dict__)
