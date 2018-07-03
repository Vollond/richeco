from collections import defaultdict
_default_data = lambda: defaultdict(_default_data)
data = _default_data()
import json
data["server"]["host"] = "127.0.0.1"
data["server"]["port"] = "22"

data["configuration"]["ssh"]["access"] = "true"
data["configuration"]["ssh"]["login"] = "some"
data["configuration"]["ssh"]["password"] = "some"


stats = _default_data()
stats["health"]["hp"] = 11
stats["health"]["mana"] = 22
stats["health"]["mana"] = stats["health"]["mana"] + 1
stats["exempls"]["head"] = "w"
stats["exempls"]["legs"] = "l"
stats["exempls"]["loolz"] = "123"

stats = json.dumps(stats)
stats = json.loads(stats)

print (stats["health"]["hp"])


print (json.dumps(data, indent=2))
print (json.dumps(stats, indent=5))
print (stats["exempls"]["head"])


