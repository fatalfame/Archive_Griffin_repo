import pythoncom, win32com.server.register

class Python_For_VBS:
    _public_methods_ = [ 'MachineInfo' ]
    _reg_progid_ = "PythonForVBS.Utilities"
    _reg_clsid_ = pythoncom.CreateGuid()

    def MachineInfo(selfself, item=None):
        import platform
        msg = "Your operating system: " + platform.platform()
        return msg

if __name__=='__main__':
    print "Registering COM server?quo"
    win32com.server.register.UseCommandLine(Python_For_VBS)