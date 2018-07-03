from collections import defaultdict
_default_data = lambda: defaultdict(_default_data)
data = _default_data()
import json




jonew=[({'build': {'n': 1}},)]

jonew = jonew[0][0]
jonew["build"]["n"] = jonew["build"]["n"] +1

print(jonew)