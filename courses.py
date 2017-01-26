from termcolor import colored
from parseprereqs import parse_prereq, sub_prereq, allof, oneof
from sys import stdout
from errors import ParseException, MissingException
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
        self.term = None
        self.delay = 0
        if not lazy:
            self.loadinfo()
    def loadinfo(self):
        self.loadprereqs()
        self.loadcoreqs()
        self.loadtitle()
        self.loaddescription()
        self.loadpostreqs()
        self.loadterm()
    def meetsprereqs(self, courses=courses):
        meets = True
        if self.prereqs == None: self.loadprereqs()
        try:
            meets = eval(sub_prereq(parse_prereq(self.prereqs).strip(",").replace(",", ", "), courses)) >= 50
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
    def loadterm(self):
        self.term = CourseMaster().getterm(self.name)
    def loadtree(self):
        try:
            self.tree = CourseMaster().gettree(self.name)
        except MissingException:
            self.tree = getprereqnode(self.name)
            CourseMaster().settree(self.name, self.tree)
    def loadpotree(self):
        try:
            self.potree = CourseMaster().getpotree(self.name)
        except MissingException:
            self.potree = getpostreqnode(self.name)
            CourseMaster().setpotree(self.name, self.potree)
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
    def print_term(self):
	if len(self.term) > 1:
            print "The following sections are available in the %s session:" % self.term[0]
            for t in self.term[1:]:
                print "Section available in term %s." % t
	else:
	    print "No sections are available this session."

'''drawtimetable(["MATH227", "MATH316", "MATH320", "MATH321", "MATH420", "MATH421", \
               "MATH322", "MATH323", "MATH412", "MATH340", "MATH442", "MATH422", \
               "MATH423", "MATH424", "MATH425", "MATH426", "MATH427", "CPSC221", \
               "CPSC213", "CPSC312", "CPSC320", "CPSC313", "CPSC322", "CPSC310", \
               "CPSC420", "CPSC421", "CPSC422", "CPSC302", "GERM110", "GERM200", \
               "GERM210", "GERM300", "GERM310", "GERM400", "GERM410"], courses.copy(), term=4, skip=6)'''
