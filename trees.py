from sys import stdout
from parseprereqs import courses, parse_prereq, tree_sub
from termcolor import colored
from errors import ParseException, AndOrException
from coursemaster import CourseMaster

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
    def printtree(self, level=0):
        try: year = int(self.name[4])
        except IndexError:
            year = None
        if (self.name == "" and self.children == []):# or year < 2:
            pass
        else:
            for i in range(level-1): stdout.write("    ")
            if level > 0:
                #if len(self.children) == 1: stdout.write("`+--")
                if self.andor == "or":    stdout.write("`+--")
                elif self.andor == "and":   stdout.write("`+==")
                else: assert False
            if self.name in courses:
                stdout.write(colored(self.name, 'green'))
            else:
                stdout.write(colored(self.name, 'red'))
            if int(self.score) > 50:
                stdout.write("[" + str(self.score) + "]")
            stdout.write("\n")
            if len(self.children) == 1:
                self.children[0].andor = "or"
                self.children[0].printtree(level+1)
            else:
                for node in self.children:
                    #if node.name != "" and len(node.children) != 0:
                        node.printtree(level+1)

'''def getprereqnode(name):
    try:
        parsed = parse_prereq(CourseMaster().getprereqs(name))
        evaled = eval(tree_sub(parsed.strip(",")))
        return evaled.setname(name)
    except ParseException:
        return Node(name)'''

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

#while "running":
#    getprereqnode(raw_input("course? \n>> ")).printtree()
'''andnode( ornode( andnode( "MATH121"), andnode( ornode( "MATH101", "MATH103", "MATH105", "SCIE001", grade=68)), grade=50)).setname("MATH223").printtree()

MATH120 = Node("MATH120")
MATH121 = Node("MATH121").addchild(MATH120, "or", 68)
MATH223 = Node("MATH223").addchild(MATH121, "or", 68)
MATH226 = Node("MATH226").addchild(MATH121,"or", 68)

MATH320 = Node("MATH320").addchild(MATH226, "or", 68)
MATH322 = Node("MATH322").addchild(MATH223, "or", 68)

MATH412 = Node("MATH412").addchild(MATH320, "and", 68).addchild(MATH322, "and", 68)

MATH412.printtree()
'''
