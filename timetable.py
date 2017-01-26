from borg import Borg
from courses import courses, Course


class TimeTableMaster(Borg):
    courses = courses
    courselist = []
    def __init__(self):
        Borg.__init__(self)
    def addcourse(self, course):
        self.courselist.append(course)
    def drawtimetable(self, courselist=courselist, taken=courses.copy(), term=1, skip=[]):
        print "Term %d:" % term
        if term in skip:
            skip.remove(term)
            print "SKIP\n"
            drawtimetable(courselist, taken, term=term+1)
        else:
            takencopy = {}
            i = 0
            while i < len(courselist):
                #print taken
                course = courselist[i]
                courseinstance = Course(course)
                courseinstance.loadterm()
                currentterm = 1 if term % 2 else 2
                if courseinstance.meetsprereqs(taken) and currentterm in courseinstance.term and courseinstance.delay < term:
                    print course
                    takencopy[course] = '100'
                    courselist[i] = ""
                i+=1
            print ""
            courselist = filter(lambda x: x != "", courselist)
            taken.update(takencopy)
            #print courselist, taken
            #print taken
            if len(courselist):
                self.drawtimetable(courselist, taken, term=term+1, skip=skip)
