class Trak(object):
    # DISCLAIMER: Could be that the class name starts with _ and this prints it without

    # Class control
    trackOnlyClss = ()  # If empty track all, else track classes here named
    trakOnlyMeths = ()  # If empty track all, else track methods here named. All methods in inheritance tree be tracked
    printStack = True
    printPath, printLine, printMeth, printCode, printLocals = True, True, True, True, True

    # Imports
    import inspect as ins

    # Strings to exclude
    localsExcl = (  # Add here any f_locals that keep cluttering your printouts
        'frame',
        'stack_info',
        '__builtins__',
        '__file__',
        'Trak',
        '__package__',
    )

    methNames = (  # Intended for meths of this class but can exclude any meth you don't want in the call stack prints
        '__getattribute__',
        '__demangleMethName',
        '__classNameThatDefinedMethod',
        '__callStackStr',
    )

    # Formatting
    divLine = '-------------------------------------------------------------------------------------'
    bigSpace = '\n\n\n'
    stackFormat = (', localVars: ', '', ', ln ', ', ', ', code:',)
    stackOrder = (1, 2, 3, 4, 0)
    trakFlag = '[TRAK]'

    def __getattribute__(self, methName):
        attr = object.__getattribute__(self, methName)
        if callable(attr):
            clsName, methName = Trak.__demangleMethName(methName)
            mroClassName = Trak.__classNameThatDefinedMethod(attr)
            clsName = mroClassName if mroClassName else clsName

            if not Trak.trackOnlyClss or clsName in Trak.trackOnlyClss or Trak.trakOnlyMeths and methName not in Trak.trakOnlyMeths:
                print self.trakFlag + ' ' + str(clsName) + '.' + methName
                if Trak.printStack:
                    print Trak.__callStackStr() + Trak.bigSpace + Trak.divLine
        return attr

    @staticmethod
    def __demangleMethName(mangledMethName):
        import re
        match = re.match(r'_(.*?)__(.*)', mangledMethName)
        if match:
            className, methName = match.group(1), match.group(2)
            methName = '__' + methName
            return className, methName
        return None, mangledMethName

    @classmethod
    def __classNameThatDefinedMethod(cls, meth):
        if hasattr(meth, 'im_class'):
            for obj in cls.ins.getmro(meth.im_class):
                if meth.__name__ in obj.__dict__:
                    return obj.__name__

    @classmethod
    def __callStackStr(cls):
        stackList = []
        for frame in cls.ins.stack():
            frameObj, filePath, lineNum, methName, codeList = frame[0], frame[1], frame[2], frame[3], frame[4]
            if methName not in cls.methNames:
                locals = str({k: str(v).split(' at 0x')[0] for k, v in frameObj.f_locals.items() if k not in Trak.localsExcl and v})
                codeStr = ' '.join(line.lstrip().rstrip('\n') for line in codeList) if codeList else ''
                stackList.append(
                    '{}{}{}{}{}\n'.format(
                        filePath if cls.printPath else '',
                        ', ln ' + str(lineNum) if cls.printLine else '',
                        ', ' + methName if cls.printMeth else '',
                        ', ' + codeStr if cls.printCode and codeStr else '',
                        ', ' + locals if cls.printLocals else ''
                    ).lstrip(', ')
                )
        return ''.join(stackList)

class MyParent(object):
    j = 640

    def __init__(self):
        self.x = 69
        self.y = 32

    def parentInstanceMethod(self):
        i = self.x + self.y
        return i

    @classmethod
    def parentClassMethod(cls):
        k = cls.j**2
        return k + 210 * 2

    @staticmethod
    def parentStaticMethod():
        l = MyParent.j//10
        return l + 420


class MySon(MyParent, Trak):
    f = 32
    g = 64

    def __init__(self):
        super(MySon, self).__init__()

        self.m = 254
        self.n = 465456

    def testMeth(self, a, b):
        c = 3
        d = b + 1 + a * self.m
        e = self.compute_sum(c, d)
        parentInstanceMethodRes = self.parentInstanceMethod()
        h = self.classMethExample()
        k = self.__mangledMeth()
        return e + h + k

    def __mangledMeth(self):
        return 68+1

    @staticmethod
    def compute_sum(x, y):
        return x + y

    @classmethod
    def classMethExample(cls):
        return cls.f + cls.g


mySonInstance = MySon()
result = mySonInstance.testMeth(453, 79)
