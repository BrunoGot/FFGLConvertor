# Use Python 3.x.x
#Todo : continue the RecordParam function in the FFGL Reader

from Form1 import *
from FFGLReader import *
from FFGLWriter import*

class Manager():
    def __init__(self): 
        form = Form1()
        form.ShowForm()
        param = form.GetParams()
        print("init : param = %s" % param)
        if(param[0] == "1"): #if the mode =="1" convert ffgl        
            self.ConvertFFGL(param[1],param[2])
        elif(param[0] == "2"): #else if the mode =="2" create ffgl        
            self.CreateFFGL(param[1])
        
    def ConvertFFGL(self,  _sConvertMode, _sSrcPath):
            if(_sConvertMode == "15"):
                ffglReader = FFGLReader() 
                listParam = ffglReader.Convert(_sSrcPath) #get the list of the parameters as a dico<int, FFGLParameter>
                print("try FFGL20Writer")
                ffglWriter = FFGL20Writer(listParam, ffglReader.m_pluginInfo)
                ffglWriter.WriteFFGL()
                #create FFGL reader(set source)
                #//FFGLReader.SetSource(file.cpp)
                #instruction = FFGL20Reader.Convert(file.cpp)
                #FFGL20Writer(instruction)
                
    def CreateFFGL(self,  _sFFGLVersion):
            if(_sFFGLVersion == "1"):
                print("You have to code the module to create FFGL 1.5")
            elif(_sFFGLVersion == "2"):
                #listParams = 
                paramNumber = input("how many parameters do you want to create ?")
                for i in range(0,int(paramNumber)):
                    print("parameter one : ")
                    paramType = input("Type of parameter ? \n 1 = standard \n 2 = boolean \n 3 = speed control \n choice =  ")
                    paramDefaultVal = input("Default value of the parameter (between 0 to 1) ? : ")
                    isShaderLinked = input("Is the parameter linked to the fragment shader? : ")
                    
                pluginDescription = input("Quick Description of the plugin")
                pluginNote = input("Additional comments for the plugin")
                
                """todo : 
                ask for the number of param
                for each param in this number ask for
                    ParamName, Type (standard, boolean, speed), default value, is linked with shader ?
                then ask for the name of the plugin and the description
                generate the id
                give all this stuff to the FFGL Writer
            
                """ 
                print("You have to code the module to create FFGL 2.0")
           
m = Manager()
