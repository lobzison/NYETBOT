lng = {"from": "ru", "to": "pl"}
 
print('{}-{}'.format(lng["from"], lng["to"]))

lng_to = lng["to"]
lng_from = lng["from"]
lng["to"] = lng_from
lng["from"] = lng_to

print('{}-{}'.format(lng["from"], lng["to"]))
