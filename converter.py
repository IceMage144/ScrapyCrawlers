import json
import sys
from optparse import OptionParser

def jsonToList(inp, out, word):
    iDict = json.load(open(inp))
    del iDict["!!Number_Of_Entries!!"]
    res = []
    for key, val in iDict.items():
        if word in val:
            res.append(key + "\n")
    if out == None:
        return res
    with open(out, "w+") as f:
        for s in res:
            f.write(s)


def listToJson(inp, out, word):
    res = {}
    with open(inp) as f:
        for line in f.readlines():
            res[line.replace("\n", "")] = [word]
    if out == None:
        return res
    s = json.dumps(res, sort_keys=True, separators=(",\n", ":"))
    with open(out, "w+") as f:
        f.write(s)

def mergeLists(inp1, inp2, out):
    if type(inp1) == list:
        v1 = set(inp1)
    else:
        with open(inp1) as f:
            v1 = set(f.readlines())
    with open(inp2) as f:
        v2 = set(f.readlines())
    with open(out, "w+") as f:
        un = v1|v2
        for s in un:
            f.write(s)

def mergeJsons(inp1, inp2, out):
    if type(inp1) == dict:
        d1 = inp1
    else:
        d1 = json.load(open(inp1))
        del d1["!!Number_Of_Entries!!"]
    d2 = json.load(open(inp2))
    del d2["!!Number_Of_Entries!!"]
    for key, val in d1.items():
        tmp = d2.get(key)
        if tmp == None:
            d2[key] = val
        else:
            d2[key] = list(set(val)|set(tmp))
    with open(out, "w+") as f:
        f.write(json.dumps(d2, sort_keys=True, separators=(",\n", ":")))


def main():
    try:
        action = sys.argv[1]
        out = sys.argv[2]
        inp1 = sys.argv[3]
        if "to" not in action:
            inp2 = sys.argv[4]
    except IndexError:
        print("Usage: converter <action> <output file> <input file 1> (<input file 2>)")
    if action == "ml": # merges two lists
        mergeLists(inp1, inp2, out)
    elif action == "mj": # merges two jsons
        mergeJsons(inp1, inp2, out)
    elif action == "mlj": # merge a list to a json
        word = input("Word to put as json value:\n")
        j = listToJson(inp1, None, word)
        mergeJsons(j, inp2, out)
    elif action == "mjl": # merge a json to a list
        word = input("Word to search at json's values:\n")
        v = jsonToList(inp1, None, word)
        mergeLists(v, inp2, out)
    elif action == "ltoj": # converts list to json
        word = input("Word to put as json value:\n")
        listToJson(inp1, out, word)
    elif action == "jtol": # converts json to list
        word = input("Word to search at json's values:\n")
        jsonToList(inp1, out, word)
    else:
        print("I don't know this action")

if __name__=="__main__":
    main()
