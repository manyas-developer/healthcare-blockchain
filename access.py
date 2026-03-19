roles = {
    "doctor":["read","write"],
    "nurse":["read"],
    "admin":["read"]
}

def check_access(role, action):
    return action in roles.get(role, [])