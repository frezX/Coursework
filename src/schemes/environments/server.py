from env_attributes import EnvTypes


class EnvTypesDB(EnvTypes):
    host: str
    port: int
    url: str


class EnvTypesApp(EnvTypes):
    host: str
    port: int
    domen: str
    url: str
