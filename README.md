# CourseBrowser

Description: includes all relevant course info (title, description, pre-reqs,
etc), as well as more features, such as informing the user whether or not they
have the required pre-reqs, printing out trees of a courses pre-reqs, and
telling the user what courses have any given course as a pre-req. Courses are
in blue if the user meets the pre-reqs, green if the course has been completed,
and red otherwise.

Set-up: create a file named "courses.txt", containing on each line, a coursecode
followed by a space, followed by a grade.  These are all the courses the user
has taken.  (Note: this will likely be updated eventually to have a login to
the UBC SSC, which would let CourseBrowser automatically get this info, but for
now it is merely stored in a text file.)  An example of a line of a
course.txt file is as follows, for MATH223 with an overall grade of 92%:

MATH223 92

Usage: run "main.py".  Type "help" or "h" (no quotes) for list of available
commands.

dependencies:
  termcolor,
  lxml,
  requests
