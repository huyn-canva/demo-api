from configparser import ConfigParser
from dataclasses import dataclass

@dataclass
class Environment:
    base_connect_api_url: str
    client_id: str
    client_secret: str
    redirect_uri: str

def load_env(filename: str) -> Environment:
    parser = ConfigParser()
    with open(filename) as stream:
        parser.read_string("[top]\n" + stream.read())
        return Environment(**parser["top"])

