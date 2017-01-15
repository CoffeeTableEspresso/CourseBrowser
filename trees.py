from sys import stdout
from parseprereqs import courses, parse_prereq, tree_sub
from termcolor import colored
from errors import ParseException, AndOrException
from coursemaster import CourseMaster
import courses


class Node(object):
    def __init__(self, name):
        self.name = name
        self.children = []
        self.score = 50
    def addchild(self, node, andor, score=50):
        if andor != "and" and andor != "or":
            raise AndOrException
        node.andor = andor
        node.score = score
        self.children.append(node)
        return self
    def setname(self, name):
        self.name = name
        return self
    def printtree(self, level=0, year=1):
        try: courseyear = int(self.name[4])
        except IndexError:
            courseyear = None
        if (self.name == "" and self.children == []):#or year < 2:
            pass
        if courseyear < year and self.name != "": pass
        else:
            for i in range(level-1): stdout.write("    ")
            if level > 0:
                #if len(self.children) == 1: stdout.write("`+--")
                if self.andor == "or":    stdout.write("`+--")
                elif self.andor == "and":   stdout.write("`+==")
                else: assert False
            if courses.Course(self.name).completed():
                stdout.write(colored(self.name, 'green'))
            elif courses.Course(self.name).meetsprereqs():
                stdout.write(colored(self.name, 'blue'))
            else:
                stdout.write(colored(self.name, 'red'))
            if int(self.score) > 50:
                stdout.write("[" + str(self.score) + "]")
            stdout.write("\n")
            if len(self.children) == 1:
                self.children[0].andor = "or"
                self.children[0].printtree(level+1,year)
            else:
                for node in self.children:
                    #if node.name != "" and len(node.children) != 0:
                        node.printtree(level+1,year)

def andornodefactory(andor):
    if andor != "or" and andor != "and":
        raise AndOrException
    def andornode(*args, **kwargs):
        for k in kwargs:
            if k != "grade": raise ArgumentException
        try:
            grade = kwargs["grade"]
        except KeyError:
            grade = 50

        node = Node("")
        if len(args) == 1 and isinstance(args[0], Node):
            return args[0]
        try:
            for arg in args:
                #print arg
                if type(arg) is str:
                    child = getprereqnode(arg).setname(arg)
                else:
                    child = arg
                node.addchild(child, andor, score=grade)#"or", score=grade)
            return node
        except SyntaxError:
            return Node("")
    return andornode

ornode = andornodefactory("or")
andnode = andornodefactory("and")

def getprereqnode(name):
    name = name.upper()
    if name in CourseMaster().trees:
        return CourseMaster().gettree(name)
    try:
        parsed = parse_prereq(CourseMaster().getprereqs(name))
        evaled = eval(tree_sub(parsed.strip(",")))
        evaled.setname(name)
        CourseMaster().settree(evaled, name)
        return evaled.setname(name)
    except ParseException:
        CourseMaster().settree(Node(name), name)
        return Node(name)
