from lxml import html, etree
import requests
from errors import MissingException

class Borg(object):
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class MetaCourse(type):
    def __new__(cls, name, parents, dct):
        if 'class_id' not in dct: dct['class_id'] = name.lower()
        if 'code' in dct: pass
        return super(MetaCourse, cls).__new__(cls, name, parents, dct)


class CourseMaster(Borg):
    __metaclass__ = MetaCourse
    prereqs  = {}
    coreqs   = {}
    postreqs = {}
    descriptions = {}
    titles = {}
    trees = {}
    def __init__(self):
        Borg.__init__(self)
    def loadinfo(self, name):
        page = requests.get("https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=3&dept=" + name[0:4] \
                +"&course=" + name[4:])
        tree = html.fromstring(page.content)
        self.prereqs[name], self.coreqs[name] = "", ""
        pp = tree.xpath('//p')
        for p in pp:
            if p.text_content().startswith("Pre-reqs:"):
                self.prereqs[name] = p.text_content().strip("Pre-reqs:").strip()
            if p.text_content().startswith("Co-reqs:"):
                self.coreqs[name] = p.text_content().strip("Co-reqs:").strip()
        try:
            self.descriptions[name] = pp[0].text_content().split("Please")[0].strip().split("Consult ")[0]
            self.titles[name] = tree.xpath('//h4/text()')[0]
        except IndexError:
            self.descriptions[name] = ""
            self.titles[name] = ""
    def loadpostreqs(self, name):
        page = requests.get("https://courses.students.ubc.ca/cs/main?pname=subjarea&req=1&dept=" + name[:4])
        tree = html.fromstring(page.content)
        tdd = tree.xpath("//td")
        postreqs = []
        for td in tdd:
            if td.text_content().startswith(name[:4]) and \
            int(td.text_content()[5]) >= int(name[4]) and \
            4 >= int(td.text_content()[5]):
                self.loadinfo(td.text_content().replace(" ", ""))
                if name in self.getprereqlist(td.text_content().replace(" ", "")):
                    postreqs.append(td.text_content().replace(" ", ""))
        self.postreqs[name] = postreqs
    def settree(self, name, tree):
        self.trees[name] = tree
    def getprereqlist(self, name):
            #print self.getprereqs(name)
            prereqbadlist = iter(self.getprereqs(name).split())
            prereqs = []
            for c in prereqbadlist:
                if c.isupper():
                    try: prereqs.append((c + next(prereqbadlist)).strip(".").strip(","))
                    except StopIteration: pass
            #print prereqs
            return prereqs
    def gettree(self, name):
        if name not in self.trees:
            raise MissingException
        return self.trees[name]
    def getprereqs(self, name):
        if name not in self.prereqs:
            self.loadinfo(name)
        return self.prereqs[name]
    def getcoreqs(self, name):
        if name not in self.coreqs:
            self.loadinfo(name)
        return self.coreqs[name]
    def getpostreqs(self, name):
        if name not in self.postreqs:
            self.loadpostreqs(name)
        return self.postreqs[name]
    def gettitle(self, name):
        if name not in self.titles:
            self.loadinfo(name)
        return self.titles[name]
    def getdescription(self, name):
        if name not in self.descriptions:
            self.loadinfo(name)
        return self.descriptions[name]

'''class Course(object):
    def __init__(self, name):
        self.name = name
        self.prereqs     = CourseMaster().getprereqs(name)
        self.coreqs      = CourseMaster().getcoreqs(name)
        self.postreqs    = CourseMaster().getpostreqs(name)
        self.description = CourseMaster().getdescription(name)
        self.title       = CourseMaster().gettitle(name)'''



'''print "loading"
print CourseMaster().getpostreqs("MATH223")
print "loading"
print CourseMaster().getpostreqs("MATH223")'''
'''math215 = Course("MATH215")
print math223, math223.code
print math221, math221.code
print math215, math215.code
math221.code = 'MATH221'
print math223, math223.code
print math221, math221.code
print math215, math215.code'''

#MATH412 = InterfaceMeta('MATH412', (), dict(pagename='MATH412'))

'''
a = Example('Lara')
b = Example()
print a, b
c = Example('Boris')
print a, b, c
b.name = 'Marcel'
print a, b, c '''
