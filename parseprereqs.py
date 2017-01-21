from termcolor import colored
from errors import ParseException, ArgumentException
with open("courses.txt") as f:
    courseslist = f.readlines()
courses = {}
i = 0
while i < len(courseslist):
    #print 'blah;'
    courses[courseslist[i].split()[0]] = courseslist[i].split()[1].strip()
    #courses[i] = courses[i][:-1] ### .strip("")
    i += 1
#print courses

def parse_prereq(prereq):
    #print prereq
    prereqs  = prereq.lower().strip().split(".")[0].replace(".", '')
    #print prereq
    if ";" in prereqs:
        prereqs = prereqs.split('and')
    elif not prereqs.startswith("either"):
        prereqs = prereqs.split("and ")
    else: prereqs = [prereqs]
    running = "allof( "
    score = "50"
    for p in prereqs:
        #print prereqs
        p = p.replace(";",'').strip()
        if p.strip().startswith("one of"):
            running += "oneof( " + p.strip("one of").strip(".").upper().replace(" ", '')
            running += ', grade=' + score + "), "
        elif p.startswith("all of"):
            running += "allof( " + p.strip("all of").strip(".").upper().replace(" ", '')
            running += ', grade=' + score + "), "
        elif p.startswith("a score of"):
            p = p.strip("a score of ")
            score = p[0:2]
            p = p[17:] #.strip("%% or higher in")
            if p.startswith("all of"):
                running += "allof( " + p.strip("all of").strip(".").upper().replace(" ", '')
                running += ', grade=' + score + "), "
            elif p.startswith("one of"):
                running += "oneof( " + p.strip("one of").strip(".").upper().replace(" ", '')
                running += ', grade=' + score + "), "
            else:
                running += p.upper().strip().replace(" ", '') + ', grade=' + score
        elif p.startswith("either"):
            p = p.strip("either (").split("or (")
            running += "oneof( "
            for course in p:
                running += parse_prereq(course[3:])
            running += ' grade=' + score + "), "
        elif len(p.replace(" ", '')) < 9  and p.replace(" ", '').isalnum():
            running += p.replace(" ", '').upper().strip() + ", "
        else:
            raise ParseException
    return running + '),'


def sub_prereq(prereq):
    #print prereq
    thing = prereq.split(" ")
    #print thing
    i = 0
    while i < len(thing):
        if thing[i].isupper():
            #print thing
            try: thing[i] = courses[thing[i].strip(",")] + ", "
            except KeyError:
                thing[i] = "0, "
        i+=1
    return " ".join(thing)

def tree_sub(prereq):
    prereq = prereq.replace(" ", "").replace(",", " , ").replace("(", "( ").replace("allof", "andnode").replace("oneof", "ornode")
    prereq = prereq.split()
    i = 0
    while i < len(prereq):
        if prereq[i].isalnum():
            prereq[i] = "\"" + prereq[i] + "\""
        i += 1
    prereq = " ".join(prereq)
    #print prereq
    return prereq

def allof(*args, **kwargs):
    #make sure we have the right kwargs
    for k in kwargs:
        if k != "grade": raise ArgumentException
    #if len(kwargs) > 1: raise ArgumentException
    try:
        grade = kwargs["grade"]
    except KeyError:
        grade = 50
    return (min(args) >= grade)*min(args)

def oneof(*args, **kwargs):
    #make sure we have the right kwargs
    for k in kwargs:
        if k != "grade": raise ArgumentException
    #if len(kwargs) > 1: raise ArgumentException
    try:
        grade = kwargs["grade"]
    except KeyError:
        grade = 50
    return (max(args) >= grade)*max(args)
