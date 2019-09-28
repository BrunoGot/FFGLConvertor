import os
#from Manager import *

class Form1():
    m_bNext = False #flag to stay in the input loop
    m_sMode = "" #flag to convert or create FFGL
    m_sConvertMode = ""
    m_sSrcPath = ""
    m_Manager = ""
    m_sParams = [] #parameters as tuple defined to the user to give to the manager
    
    def __init__(self):
        m_bNext = False
        #m_Manager = _manager
        
    def SelectPath(self):
        repeat = True
        while repeat == True:
            path = input("Path to .cpp file to convert = ")
            if(os.path.exists(path)):
                repeat = False #quit the loop
                print("file selected = "+path)
            else:
                print("file "+path+" not found try again")
        return path
    
    def ConvertFFGLForm(self):
        result = "15"
        repeat = True
        while repeat == True:
            option1 = input("1 = convert from FFGL 1.5 to FFGL 2.0 \n2 = convert from FFGL 2.0 to FFGL 1.5 \n choice = ")
            if(option1 == "1"):
                print("Convert FFGL from 1.5 to 2.0")
                repeat = False #quit the loop
                result = "15"
            elif(option1 == "2"):
                print("Convert FFGL from 2.0 to 1.5")
                repeat = False #quit the loop
                result = "20"
            else:
                print("wrong answere")        
        return result
     
    
    def ShowForm(self):
        while self.m_bNext == False:
            option1 = input("what do you want to do ? \n 1 = convertFFGL \n 2 = create FFGL \n choice = ")
            if(option1 == "1"):
                print("FFGL convert mode")
                self.m_bNext = True #quit the loop
                self.m_sMode = "1"
            elif(option1 == "2"):
                print("FFGL create mode")
                self.m_bNext = True #quit the loop
                self.m_sMode = "2"
            else:
                print("wrong answere")
        self.m_sParams.append(self.m_sMode)                
        if(self.m_sMode == "1"):
            self.m_sConvertMode = self.ConvertFFGLForm()
            self.m_sSrcPath = self.SelectPath()
            self.m_sParams.append(self.m_sConvertMode)
            self.m_sParams.append(self.m_sSrcPath)            
           # m_Manager.SetCommand(self.m_sMode, self.m_sConvertMode, m_sSrcPath)
        else:
            print("code the create plugin module here")
    
    def GetParams(self):
        return self.m_sParams
            