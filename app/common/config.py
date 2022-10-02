from dataclasses import dataclass
from functools import lru_cache
from os import path, environ
from os import error
import redis

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

@dataclass
class Config:
    """
    기본 Configuration
    """
    BASE_DIR: str = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DEBUG: bool = False
    TEST_MODE: bool = False

    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PW: str = "root123!"

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

def conf():
    """
    get config enviroments
    """

    return Config

def redis_config() :
	
    try:
        rd = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE)
		
    except:
        print("redis connection failure")
