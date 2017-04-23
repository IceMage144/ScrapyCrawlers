import json
from pathlib import Path

def loadDatabase(name):
    fileName = f"conv_{name}_products.json"
    path = Path(fileName)
    dic = {}
    if path.is_file():
        print(Color("Loading database...", 33))
        dic = json.load(open(fileName))
        print(Color("Finish loading", 32))
        return dic
    else:
        print(Color("Database not found", 31))
    return dic

def convert(name):
    lines = []
    dic = {}
    original = f'{name}_products.jl'
    newName = "conv_" + original.replace(".jl", ".json")
    path = Path(newName)
    if path.is_file():
        print(Color("Loading database...", 33))
        dic = json.load(open(newName))
        print(Color("Finish loading", 32))
    with open(original) as f:
        k = f.readlines()
    print(Color("Converting new itens...", 33))
    dic["!!Number_Of_Entries!!"] = 0
    for line in k:
        entry = json.loads(line)
        dic[entry["name"]] = entry["links"]
    dic["!!Number_Of_Entries!!"] = len(dic)-1
    print(Color("Finish converting", 32))
    with open(newName, "w+") as f:
        f.write(json.dumps(dic, sort_keys=True, indent=1))
        print(Color("Saved database", 32))

def Color(string, num):
    return (f"\033[1;{num}m{string}\033[0m")
