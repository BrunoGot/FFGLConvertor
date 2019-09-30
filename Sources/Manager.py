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
        self.SetCommand(param[0],param[1],param[2])
        
    def SetCommand(self, _sMode,  _sConvertMode, _sSrcPath):
        if(_sMode == "1"):
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
     
           
m = Manager()
