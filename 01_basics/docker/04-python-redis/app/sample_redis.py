import time
import redis

print("[INFO] Waiting for Redis to be ready...")
# Redis起動を待つ
time.sleep(3)

"""
depends_onは「起動を始める順番」のみ保証。起動完了は保証しない
まだRedisプロセスが立ち上がって準備中の場合もある
"""
try:
    print("[INFO] Connecting to Redis...")
    r = redis.Redis(host='redis', port=6379, db=0)
    r.ping()
    print("[INFO] Connected!")

    # データ書込
    data = {
        "果物": "りんご",
        "値段": "120円",
        "生産地": "青森",
        "糖度": "10度"
    }

    r.hset("りんご", mapping=data)
    print("[INFO] Data inserted.")

except redis.exceptions.ConnectionError as e:
    print("[ERROR] Could not connect to Redis:", e)
    exit(1)

except Exception as e:
    print("[ERROR] Unexpected error:", e)
    exit(1)
