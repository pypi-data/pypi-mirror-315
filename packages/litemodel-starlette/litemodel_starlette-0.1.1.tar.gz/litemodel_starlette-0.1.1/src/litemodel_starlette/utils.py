def tables() -> str:
    return """SELECT name FROM sqlite_master where type='table' order by name GLOB '[A-Za-z]*' DESC, name;"""
