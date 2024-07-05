from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

print(similar("Jogging du Floc et du souvenir","Jogginge du Floc et du souvenir"))