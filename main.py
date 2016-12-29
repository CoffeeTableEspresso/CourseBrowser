from courses import Course
from termcolor import colored
from parseprereqs import courses

location, course = "", None
while True:
    do = raw_input(location + ":\n>> ")
    do = do.split()
    print do
    while len(do) > 0:
        if do[0].lower() == "help":
            print ("goto [ARG]:  change current course to [ARG].\n" +
                  "prereqs:     print the prereqs for current course.\n" +
                  "coreqs:      print the coreqs for current course.\n" +
                  "description: print the description of current course.\n" +
                  "title:       print the title of current course.\n" +
                  "info:        print title, description, prereqs, coreqs for current course.\n" +
                  "mc:          print all courses user has taken, plus grades.\n")
            do = do[1:]
        elif do[0].lower() == "goto":
            try:
                course = Course(do[1].upper())
                #course.print_info()
                location = course.name
                print ""
            except IndexError:
                print "Not a valid course: %s. \nPlease try again.\n" % do[1].upper()
            except KeyError:
                print colored("Error parsing, we're sorry.\n", 'red')
            do = do[2:]
        elif do[0].lower() == "prereqs":
            course.print_prereqs()
            print ""
            do = do[1:]
        elif do[0].lower() == "title":
            print course.title + "\n"
            do = do[1:]
        elif do[0].lower() == "description":
            print course.description + "\n"
            do = do[1:]
        elif do[0].lower() == "coreqs":
            print "Co-reqs:  " + course.coreqs + "\n"
            do = do[1:]
        elif do[0].lower() == "info":
            course.print_info()
            print ""
            do = do[1:]
        elif do[0].lower() == "mc":
            print "My Courses:"
            for c in courses:
                print colored(str(c), 'green') + ": " + str(courses[c])
            print ""
            do = do[1:]
        else:
            print "Unknown Command\n"
            break
