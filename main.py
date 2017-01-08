from courses import Course
from termcolor import colored
from parseprereqs import courses

location, course = "", None
while True:
    do = raw_input(location + ":\n>> ")
    do = do.split()
    #print do
    while len(do) > 0:
        #print do
        if do[0] == "": do = do[1:]
        elif do[0].lower() == "help" or do[0].lower() == "h":
            print ("goto [ARG]:         change current course to [ARG].\n" +
                  "prereqs or prr:      print the prereqs for current course.\n" +
                  "coreqs or cor:       print the coreqs for current course.\n" +
                  "postreqs or por:     print the postreqs for current course.\n" +
                  "description or dsc:  print the description of current course.\n" +
                  "title or ttl:        print the title of current course.\n" +
                  "info or i:           print title, description, prereqs, coreqs, postreqs for current course.\n" +
                  "tree or tr:          print tree of prereqs.\n" +
                  "grade or gr:         print grade received in course if available.\n" +
                  "reload or rl:        reload all info for current course.\n" +
                  "mc:                  print all courses user has taken, plus grades.\n"
                  "quit or q:           exit program.\n")
            do = do[1:]
        elif do[0].lower() == "goto":
            try:
                course = Course(do[1].upper())
                #course.print_info()
                location = course.name
                print (location + ":")
            except IndexError:
                print "Not a valid course: %s. \nPlease try again.\n" % do[1].upper()
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
        elif do[0].lower() == "tree" or do[0].lower() == "tr":
            course.loadtree()
            course.printtree()
            do = do[1:]
        elif do[0].lower() == "postreqs" or do[0].lower() == "por":
            course.loadpostreqs()
            print "Post-reqs: " + ", ".join(course.postreqs)
            do = do[1:]
        elif do[0].lower() == "title" or do[0].lower() == "t":
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
        elif do[0].lower() == "mc":
            print "My Courses:"
            for c in courses:
                print colored(str(c), 'green') + ": " + str(courses[c])
            print ""
            do = do[1:]
        elif do[0].lower() == "quit" or do[0].lower() == "q":
            raise SystemExit
        else:
            print "Unknown Command\n"
            break
