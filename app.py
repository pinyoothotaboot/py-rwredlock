from configs.config import REDIS_HOST, REDIS_PORT
from libs.exceptions.connect_exception import ConnectionException
from adapter.redis import Broker

print("REDIS HOST", REDIS_HOST)
print("REDIS PORT", REDIS_PORT)

ID = "1234"
broker = Broker()
broker.set(ID, "Hello Wolrd", 10)
resp = broker.get(ID)
print("OK ", resp)
res = broker.get("12345")
print("FAILED ", res)

print("INC ", broker.increase(f"COUNT:{ID}"))

print("PUB ", broker.publish(ID, "HELLO PUBLISH"))

print("SUB", broker.subscribe(ID))

print("DEL ", broker.delete(ID))
