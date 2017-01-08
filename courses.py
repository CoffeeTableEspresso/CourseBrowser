from termcolor import colored
from parseprereqs import parse_prereq, sub_prereq, allof, oneof
from sys import stdout
from errors import ParseException
from coursemaster import CourseMaster
from trees import getprereqnode


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

class Course(object):
    def __init__(self, name, lazy=True):
        self.name = name
        self.prereqs     = None
        self.coreqs      = None
        self.postreqs    = None
        self.description = None
        self.title       = None
        self.loaded = False
        if not lazy:
            self.loadinfo()
    def loadinfo(self):
        self.loadprereqs()
        self.loadcoreqs()
        self.loadtitle()
        self.loaddescription()
        self.loadpostreqs()
    def meetsprereqs(self):
        meets = True
        try:
            #print parse_prereq(self.prereqs)
            meets = eval(sub_prereq(parse_prereq(self.prereqs).strip(",").replace(",", ", "))) >= 50
        except ParseException:
            meets = True
            print colored("UNABLE TO PARSE", 'red')
        return meets
    def loadprereqs(self):
        self.prereqs = CourseMaster().getprereqs(self.name)
    def loadcoreqs(self):
        self.coreqs = CourseMaster().getcoreqs(self.name)
    def loadpostreqs(self):
        self.postreqs = CourseMaster().getpostreqs(self.name)
    def loadtitle(self):
        self.title = CourseMaster().gettitle(self.name)
    def loaddescription(self):
        self.description = CourseMaster().getdescription(self.name)
    def loadtree(self):
        self.tree = getprereqnode(self.name)
    def printtree(self):
        try:
            self.tree.printtree()
        except TypeError:
            print "Tree unavailable."
    def print_info(self):
        print self.title + ":"
        print self.description
        self.print_prereqs()
        print "Co-reqs:  " + self.coreqs
        print "Post-reqs: " + ", ".join(self.postreqs)
    def print_prereqs(self):
        print "Pre-reqs: " + self.prereqs
        if self.meetsprereqs():
            print colored("You have the required pre-reqs", 'green')
        else: print colored("You do not have the required pre-reqs", 'red')
