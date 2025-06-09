import psutil, time, redis, json

r = redis.Redis(host='localhost', port=6379, db=0)

while True:
    data = {
        "time": time.time(),
        "cpu": psutil.cpu_percent(interval=1),
        "mem": psutil.virtual_memory().percent
    }
    r.rpush("metrics", json.dumps(data))
    print(f"Pushed: {data}")
    time.sleep(10)
