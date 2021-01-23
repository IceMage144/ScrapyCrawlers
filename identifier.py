import json
import sys

ignoredChars = [",", ":", ";", "-", "!", "?", "\'", "’", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "`", "/", ".", "\"", "(", ")", "”", "\n", "“"]

def takeOutForbs(string):
    ret = string
    for c in ignoredChars:
        ret = ret.replace(c, " ")
    return ret

def analizeFile(d):
    source = input("Input the name of a file to analize:\n")
    with open(source, "r") as f:
        k = f.readlines()
    k = list(filter(None, takeOutForbs("".join(k).lower()).split(" ")))
    out = "out" + source
    with open(out, "w+") as f:
        for w in k:
            y = w.lower()
            g = d.get(y)
            if g == None:
                f.write(y + "\n")

def analizeWord(d):
    word = "o"
    print("Input '-1' to stop")
    while word != "-1":
        word = input("Input an word to search:\n")
        if (d.get(word) == None):
            print("I don't know this word")
        else:
            print("Found it!")

def searchWord(d):
    word = "o"
    print("Input '-1' to stop")
    while word != "-1":
        word = input("Input an word to search:\n")
        g = d.get(word)
        if (g == None):
            print("I don't know this word")
        else:
            print(g)

def main():
    try:
        name = sys.argv[1]
    except IndexError:
        print("Usage: identifier <dict file>")
    print("Exporting dictionary...")
    d = json.load(open(name))
    print("Dictionary exported successfuly!")
    action = input("analize file (f) or have words (h) or search definitions (d)?")
    if action == "f":
        analizeFile(d)
    elif action == "h":
        analizeWord(d)
    elif action == "d":
        searchWord(d)
    else:
        print("Wrong letter")


main()
