from courses import Course
from depts import Dept
from termcolor import colored
from parseprereqs import courses
from sys import stdout
from timetable import TimeTableMaster

helpmenu = """goto or g [ARG]:        change current course to [ARG].
showall or
sa [ARG1] [ARGS]:       show all courses in dept [ARG1] for each year in [ARGs]. e.g. 'sa cpsc 3 4'
                        shows all 3rd and 4th year cpsc courses.

title or ttl:           print the title of current course.
description or dsc:     print the description of current course.
prereqs or prr:         print the prereqs for current course.
coreqs or cor:          print the coreqs for current course.
postreqs or por:        print the postreqs for current course.
info or i:              print title, description, prereqs, coreqs, postreqs for current course.
info- or i-:            print title, description, prereqs, coreqs for current course.
reload or rl:           reload all info for current course.

prereqtree or tree or
prtree or tr or
prtr [OARG]:            print tree of prereqs. optional [OARG] specifies the lowest year level to
                        include in tree; defaults to 1.
postreqtree or potree
or potr:                print tree of all postreqs for current course.  WARNING: MAY TAKE A VERY
                        LONG TIME TO LOAD, ESPECIALLY FOR LOWER LEVEL COURSES.

grade or gr:            print grade received in course if available.
mc:                     print all courses user has taken, plus grades.

help or h:              print help menu.
quit or q:              exit program.\n"""

location, course = "", None
while True:
    do = raw_input(location + ":\n>> ")
    do = do.split()
    #print do
    while len(do) > 0:
        #print do
        if do[0] == "": do = do[1:]
        elif do[0].lower() == "help" or do[0].lower() == "h":
            print helpmenu
            do = do[1:]
        elif do[0].lower() == "goto" or do[0].lower() == "g":
	    if len(do) == 1:
		do = do[1:]
		print ""
		break
            course = Course(do[1].upper())
            location = course.name
            print "" #(location + ":")
            do = do[2:]
        elif do[0].lower() == "prereqs" or do[0].lower() == "prr":
            course.loadprereqs()
            try:
                course.print_prereqs()
                print ""
            except AttributeError:
                print "You have not selected a course.\n"
            except KeyError:
                print colored("Error parsing, we're sorry.\n", 'red')
            do = do[1:]
        elif do[0].lower() == "terms" or do[0].lower() == "trm":
            course.loadterm()
            course.print_term()
	    print ""
            do = do[1:]
        elif do[0].lower() == "setdelay" or do[0].lower() == "sd":
            try:
                course.delay = do[1]
                #print course.name
                print course.name + " delayed until term " + course.delay + ".\n"
                do = do[1:]
            except IndexError:
                print "sd requires an argument.\n"
            except AttributeError:
                print "You have not selected a course.\n"
                do = do[1:]
            do = do[1:]
        elif do[0].lower() == "add":
            try:
                TimeTableMaster().addcourse(course.name)
                print "%s added to timetable." % course.name
            except IndexError:
                print "You have not selected a course.\n"
            do = do[1:]
        elif do[0].lower() == "tree" or do[0].lower() == "prtree" or do[0].lower() == "tr" or \
        do[0].lower() == "prereqtree" or do[0].lower() == "prtr":
            try:
                year = int(do[1])
                do = do[1:]
            except (IndexError, ValueError):
                year = 1
            try:
                course.loadtree()
                course.printtree(year=year)
            except AttributeError:
                print "You have not selected a course.\n"
            do = do[1:]
        elif do[0].lower() == "potree" or do[0].lower() == "postreqtree" or do[0].lower() == "potr":
            try:
                course.loadpotree()
                print "\033[K", "\r", " " * 16, "\r",
                stdout.flush()
                course.printpotree()
            except (IndexError, AttributeError):
                print "You have not selected a course.\n"
            do = do[1:]
        elif do[0].lower() == "postreqs" or do[0].lower() == "por":
            course.loadpostreqs()
            print "Post-reqs: " + ", ".join(course.postreqs) + "\n"
            do = do[1:]
        elif do[0].lower() == "title" or do[0].lower() == "ttl":
            course.loadtitle()
            try:
                print course.title + "\n"
            except AttributeError:
                print "You have not selected a course.\n"
            do = do[1:]
        elif do[0].lower() == "description" or do[0].lower() == "dsc":
            course.loaddescription()
            try:
                print course.description + "\n"
            except AttributeError:
                print "You have not selected a course.\n"
            do = do[1:]
        elif do[0].lower() == "coreqs" or do[0].lower() == "cor":
            course.loadcoreqs()
            try:
                print "Co-reqs:  " + course.coreqs + "\n"
            except AttributeError:
                print "You have not selected a course.\n"
            do = do[1:]
        elif do[0].lower() == "info" or do[0].lower() == "i":
            course.loadinfo()
            try:
                course.print_info()
                print ""
            except AttributeError:
                print "You have not selected a course.\n"
            except KeyError:
                print colored("Error parsing, we're sorry.\n", 'red')
            do = do[1:]
        elif do[0].lower() == "info-" or do[0].lower() == "i-":
            course.loadtitle()
            course.loaddescription()
            course.loadprereqs()
            course.loadcoreqs()
            try:
                print course.title + ":"
                print course.description
                course.print_prereqs()
                print "Co-reqs:  " + course.coreqs
                print ""
            except AttributeError:
                print "You have not selected a course.\n"
            except KeyError:
                print colored("Error parsing, we're sorry.\n", 'red')
            do = do[1:]
        elif do[0].lower() == "grade" or do[0].lower() ==  "gr":
            try:
                if course.name in courses:
                    print "Grade: " , colored(str(courses[course.name]), 'green'), "\n"
                else:
                    print colored("You have not taken %s.\n" % course.name, 'red')
            except AttributeError:
                print "You have not selected a course.\n"
            do = do[1:]
        elif do[0].lower() == "reload" or do[0].lower() == "rl":
            course.loadinfo()
            do = do[1:]
        elif do[0].lower() == "showall" or do[0].lower() == "sa":
            try:
                for course in Dept(do[1]).getyear(int(do[2])):
                    course.loadtitle()
                    course.loadprereqs()
                    if course.name in courses:
                        print colored(course.title, 'green')
                    elif course.meetsprereqs():
                        print colored(course.title, 'blue')
                    else:
                        print colored(course.title, 'red')
            except (IndexError, ValueError):
                print "Please specify dept and year level."
            try:
                int(do[3])
                do = do[0:2] + do[3:]
            except (IndexError, ValueError):
                do = do[3:]
        elif do[0].lower() == "mc":
            print "My Courses:"
            for c in courses:
                print colored(str(c), 'green') + ": " + str(courses[c])
            print ""
            do = do[1:]
        elif do[0].lower() == "quit" or do[0].lower() == "q":
            raise SystemExit
        else:
            print "Unknown Command: %s\n" % do[0]
            break
