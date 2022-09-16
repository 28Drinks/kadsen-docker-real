import json

calculated_dict = {}

with open('valueShares.json') as f:
    value = json.load(f)

with open('totalShares.json') as f:
    quantity = json.load(f)

for key in quantity:
    q = quantity[key]
    v = float(value[key])
    v2 = float("{:.2f}".format(v))

    calculated_dict[key] = round((q * v), 2)

print(calculated_dict)

total = 0
for x in calculated_dict:
    total += float(calculated_dict[x])
