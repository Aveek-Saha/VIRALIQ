import sys
import json
data = {
    'array': [
        ["vid1", 0.02],
        ["vid2", 0.90],
        ["vid3", 0.01]
    ]
}
# array = 
print(json.dumps(data))
sys.stdout.flush()
