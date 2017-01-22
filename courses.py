from termcolor import colored
from parseprereqs import parse_prereq, sub_prereq, allof, oneof
from sys import stdout
from errors import ParseException
from coursemaster import CourseMaster
from trees import getprereqnode, getpostreqnode


with open("courses.txt") as f:
    courseslist = f.readlines()
courses = {}
i = 0
while i < len(courseslist):
    courses[courseslist[i].split()[0]] = courseslist[i].split()[1].strip()
    i += 1

class Course(object):
    def __init__(self, name, lazy=True):
        self.name = name
        self.prereqs     = None
        self.coreqs      = None
        self.postreqs    = None
        self.description = None
        self.title       = None
        self.tree = None
        self.potree = None
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
        if self.prereqs == None: self.loadprereqs()
        try:
            meets = eval(sub_prereq(parse_prereq(self.prereqs).strip(",").replace(",", ", "))) >= 50
        except ParseException:
            meets = True
        return meets
    def completed(self):
        return self.name in courses
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
    def loadpotree(self):
        #if self.postreqs == None: self.loadpostreqs()
        self.potree = getpostreqnode(self.name)
    def printtree(self,year):
        try:
            self.tree.printtree(year=year)
        except TypeError:
            print "Tree unavailable."
    def printpotree(self):
        try:
            self.potree.printtree()
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
        if self.completed():
            print colored("You have completed this course", 'green')
        elif self.meetsprereqs():
            print colored("You have the required pre-reqs", 'blue')
        else: print colored("You do not have the required pre-reqs", 'red')
