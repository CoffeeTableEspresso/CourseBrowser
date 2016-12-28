from courses import Course
from termcolor import colored

print ""
while True:
    try:
        coursecode = raw_input("Enter a course-code.\n>> ").upper()
        course = Course(coursecode)
        course.print_info()
        print ""
    except IndexError:
        print "Not a valid course, please try again.\n"
    except KeyError:
        print colored("Error parsing, we're sorry.\n", 'red')
