class Trak(object):
    # DISCLAIMER: Could be that the class name starts with _ and this prints it without
    trackOnlyClss = ()  # If empty track all, else track classes here named
    trakOnlyMeths = ()  # If empty track all, else track methods here named
    trakFlag = '[TRAK]'

    def __getattribute__(self, methName):
        attr = object.__getattribute__(self, methName)
        if callable(attr):
            clsName, methName = Trak.__demangleMethName(methName)
            mroClassName, objId = Trak.__classNameThatDefinedMethodAndId(attr)
            clsName = mroClassName if mroClassName else clsName

            if not Trak.trackOnlyClss or clsName in Trak.trackOnlyClss or Trak.trakOnlyMeths and methName not in Trak.trakOnlyMeths:
                print Trak.trakFlag + ' ' + str(clsName) + '.' + methName + '.id(' + str(objId) + ')'
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

    @staticmethod
    def __classNameThatDefinedMethodAndId(meth):
        import inspect
        if hasattr(meth, 'im_class'):
            for obj in inspect.getmro(meth.im_class):
                if meth.__name__ in obj.__dict__:
                    return obj.__name__, id(obj)
