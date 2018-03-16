class classInfo:
    '''
    * class of lesson
    * including many attribute
    '''
    def __init__(self):
        self.teacher="NULL"
        self.limit=""
        self.selected=""
        self.optional=""
        self.schedule=""
        self.campus=""
        self.id=""
        self.name=""
    def addSchedule(self,sche):
        self.schedule+=","+sche
        return 0

    def printInfo(self):
        print "name: ",self.name," teacher: ",self.teacher," campus: ",self.campus,\
            " schedule: ",self.schedule," id: ",self.id,\
            "  limit: ",self.limit," selected: ",self.selected, " optional: ",self.optional

    def setAttr(self,**kw):
        self.teacher=kw['teacher'] if 'teacher' in kw else "NULL"
        self.limit=kw['limit'] if 'limit' in kw else ""
        self.selected=kw['optional'] if 'optional' in kw else ""
        self.optional=kw['selected'] if 'selected' in kw else ""
        self.schedule=kw['schedule'] if 'schedule' in kw else ""
        self.campus=kw['campus'] if 'campus' in kw else ""
        self.id=kw['id'] if 'id' in kw else ""
        self.name=kw['name'] if 'name' in kw else ""
        return 0
