from os import fdopen
import sys, getopt, re


def parseLine(raw, units, line):
    """Parses variables of one entry, populates the raw values and the units if it doesn't exist

    Args:
        raw (dict): Dict of arrays for every variable's value
        units (dict): Dict of string for every variable's unit
        line (string): Current line
    """
    obj = line.split(" ")
    for o in obj:
        o = o.split(":")
        k = o[0]
        v = o[1]
        u = v

        if (not (k in raw)):
            raw[k] = []
            try:
                u = re.sub('\d', '', u).replace("\n", '')
            except Exception:
                u = ""
            units[k] = u
        try:
            v = float(re.findall(r'[-+]?(\d+([.,]\d*)?|[.,]\d+)([eE][-+]?\d+)?', v)[0][0])
            v = round(v, 2)
        except Exception:
            v = 0

        raw[k].append(v)


def variableNotNull(data, k):
    """Returns whenever a variable has any data except zeroes

    Args:
        data (dict): Dataset
        k (string): key, name of the variable

    Returns:
        bool: 1 if variable not null, 0 otherwise
    """
    return (not(data["min"][k] == 0 and data["max"][k] == 0))


def getStats(data):
    """Extracts min, max and average from dataset

    Args:
        data (dict): Dataset
    """
    for k in data["raw"]:
        sum = 0
        data["min"][k] = data["raw"][k][0]
        data["max"][k] = data["raw"][k][0]

        for e in data["raw"][k]:
            sum += e
            if (e < data["min"][k]) :
                data["min"][k] = e
            if (e > data["max"][k]) :
                data["max"][k] = e
        data["avg"][k] = round(sum / data["total"], 2)


def prettyPrint(data):
    """Pretty prints the analysis' summary

    Args:
        data (dict): Dataset
    """
    print("Analyzed ", data["total"], " items, with ", len(data["units"]), " variables")
    print("Showing non-NULL only\n")
    print("---")
    for k in data["raw"]:
        if (variableNotNull(data, k)):            
            print(k)
            print("avg : ", data["avg"][k], "\t", data["units"][k])
            print("min : ", data["min"][k], "\t", data["units"][k])
            print("max : ", data["max"][k], "\t", data["units"][k])
            print("---\n")


def parseSRTs(path):
    """Parses .SRT DJI file and extracts data

    Args:
        path (string): File path

    Returns:
        dict: Dataset
    """
    data = {
        "raw": {},
        "units": {},
        "min": {},
        "max": {},
        "avg": {},
        "total": 0
    }

    try:
        file = open(path, "r")
        line = file.readline()
        ltype = 1
        i = 1
        while (line):
            if (ltype == 3):
                parseLine(data["raw"], data["units"], line)
                data["total"] += 1
            elif (ltype == 1):

                if ((i-1) != (int(line)-1)*4):
                    print("ERROR : File doesn't respect the default DJI SRT format. Do you have a different version ?")
                    exit(-3)
            line = file.readline()
            i += 1
            ltype += 1
            if (ltype > 4): ltype = 1

    except Exception:
        print("ERROR : Cannot open / read specified file." + Exception)
        exit(-2)

    return data


def printhelp():
    """Prints help
    """
    print("Usage : parse.py -i <file.srt>")
    sys.exit(-1)


def main(argv):
    """Basic argument handling and the rest

    Args:
        argv (array of strings): Passed arguments
    """
    try:
        opts, args = getopt.getopt(argv,"i:",["ifile="])
    except getopt.GetoptError:
        printhelp()
    
    if (len(opts) > 0):
        data = parseSRTs(opts[0][1])
        getStats(data)
        prettyPrint(data)
    else:
        printhelp()


if __name__ == "__main__":
   main(sys.argv[1:])