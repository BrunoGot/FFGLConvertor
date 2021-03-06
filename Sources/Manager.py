# Use Python 3.x.x
#Todo : continue the RecordParam function in the FFGL Reader

from Form1 import *
from FFGLReader import *
from FFGLWriter import *
from FFGLWriters import FFGL20Writer2
import FFGLParameter     
import FFGLInformation

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
    
    def IDGenerator(self): #ake a class for the FFGL creator
        print("coder l'ID Generator !!")
        return 'test'    

    def CreateFFGL(self,  _sFFGLVersion):
        '''CreateFFGL works in two steps : input user parameters, then put all these parameters in the FFGL Writer function '''
        if(_sFFGLVersion == "1"):
            print("You have to code the module to create FFGL 1.5")
        elif(_sFFGLVersion == "2"):
            listParams = {} #actualy it's a dictionary but it should be an array
            ffglType = input("what kind of plugin do you want to create ? : \n 1 = 'Source' \n 2 = 'Effect' \n choice = ")
            if(ffglType=='1'):
                pluginType="FF_Source"
            elif(ffglType=='2'):
                pluginType="FF_Effect"
            else:
                print("wrong answere, I have to handle this case, I have to handle the 'Mixer' type also")

            paramNumber = input("how many parameters do you want to create ?") #be careful it must be an integer
            for i in range(0,int(paramNumber)):
                print("parameter one : ")
                paramName = input("name of this parameter : ")
                paramType = input("Type of parameter ? \n 1 = standard \n 2 = boolean \n 3 = speed control \n choice = ")
                paramVal = input("Default value of the parameter (between 0 to 1) ? : ")
                var = input("Is the parameter linked to the fragment shader? : \n 1 = yes \n 2 = no ")
                if(var == '1'):
                    isShaderLinked = True
                elif(var == '2'):
                    isShaderLinked = False
                else:
                    print('wrong answere, have to handle this case')
                paramVarName = "m_param"+str(i)
                param = FFGLParameter.FFGLParameter(paramName, paramType, isShaderLinked, paramVarName, paramVal)
                listParams[i] = param
            pluginDescription = input("Quick Description of the plugin")
            pluginNote = input("Additional comments for the plugin")
            pluginName = input("Name of the plugin ?")
            pluginId = self.IDGenerator()
            apiMaj = "2"
            apiMin = "1"
            pluginMaj = "1"
            pluginMin = "0"
            ffglInfo = FFGLInformation.FFGLInformation(pluginName, '"'+pluginId+'"', '"'+pluginName+'"', apiMaj, apiMin, pluginMaj, pluginMin, pluginType, '"'+pluginDescription+'"', '"'+pluginNote+'"')
            ffglWriter = FFGL20Writer2.FFGL20Writer2(listParams, ffglInfo) #todo : factorise this line with the ffgl convertion 15-20 module
            ffglWriter.WriteFFGL()

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
