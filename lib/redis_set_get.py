import redis

def set(key, value, expired):
    #use None if don't want to use expired time
    try:
        r = redis.Redis()
        r.set(name=key, value=value, ex=expired)
        return True, None
    except Exception as e:
        return False, f'{e}'

def get(key):
    #key to get value
    r = redis.Redis()
    result=r.get(key)
    if result:
        return result.decode('utf-8')
    else:
        return None

def cekRedisToken(key):
    if get(key) is not None:
        return True
    else:
        return False