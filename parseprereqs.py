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

#print allof(59, 50, 10, 19, grade=6)


#tree_sub(parse_prereq("Either (a) MATH 121 or (b) a score of 68% or higher in one of MATH 101, MATH 103, MATH 105, SCIE 001."))
#first example, for MATH424, doesn't work
#print_prereq("Either (a) a score of 68% or higher in MATH 223 or (b) a score of 80% or higher in one of MATH 152, MATH 221; and either (a) a score of 68% or higher in MATH 227 or (b) a score of 80% or higher in one of MATH 217, MATH 263, MATH 317. ")
#print eval(sub_prereq(parse_prereq("One of MATH 300, MATH 305 and one of MATH 215, MATH 255, MATH 256, MATH 265. ").strip(",").replace(",", ", ")))
#print_prereq("Either (a) MATH 121 or (b) a score of 68% or higher in one of MATH 101, MATH 103, MATH 105, SCIE 001.")
#print_prereq("Either (a) a score of 68% or higher in MATH 226 or (b) one of MATH 200, MATH 217, MATH 226, MATH 253, MATH 263 and a score of 80% or higher in MATH 220. ")
#print parse_prereq("A score of 68% or higher in all of MATH 320, MATH 322.")
#print parse_prereq("A score of 68% or higher in MATH 226.")
#print parse_prereq("One of MATH 200, MATH 217, MATH 226, MATH 253, MATH 263.")
#print parse_prereq("Either (a) MATH 121 or (b) a score of 68% or higher in one of MATH 101, MATH 103, MATH 105, SCIE 001.")
#print parse_prereq("Either (a) MATH 121 or (b) a score of 68% or higher in one of MATH 101, MATH 103, MATH 105, SCIE 001. ")
