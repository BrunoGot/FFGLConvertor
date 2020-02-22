from FFGLReader import FFGLInformation #test this import
#TODO : write the code ini a new file

class FFGLWriter():
    m_DicoParam= {} #dictionary containing parameters class as dico<int, FFGLParameter> (string) paramName, (string) param type : FF_TYPE_STANDARD/speed , (string) param default value, (bool) is connected to shader, (string) shader var name
    m_PluginInfo = FFGLInformation("","","","","","","","","","")
    m_bImplementTime = False
    m_dicoVar = {} #dictionary<string, string> (paramName,variable type) dictionary containing the new variables created and have to written in the header file
    m_dicoSpeedShader = {} #dictionary to implement speed into the shader. It contain all variables l
    m_tabFunction = [] #array[string] containing special functions to write in the header part
    def __init__(self, _dicoParam, _pluginInfo):
        self.m_DicoParam = _dicoParam
        index = 0
        for k in self.m_DicoParam:
            index+=1
            print("param %s" %index+" = " +self.m_DicoParam[k].m_sParamName+" - "+self.m_DicoParam[k].m_sTypeParam + " - "+self.m_DicoParam[k].m_sParamValue + " - is shader param = "+str(self.m_DicoParam[k].m_bIsShader) + " - VariableName = "+self.m_DicoParam[k].m_sVarName)        
        
        self.m_PluginInfo = _pluginInfo
        print("Plugin info className = "+self.m_PluginInfo.m_sClassName)
 #       print("plugin info = "+str(self.m_PluginInfoTab))
    
class FFGL20Writer(FFGLWriter):
    m_sIncludePart = '#include <FFGL.h>' +'\n#include <FFGLLib.h>' +'\n#include "AddSubtract.h"'+'\n#include "../../lib/ffgl/utilities/utilities.h"' # va disparaitre
    m_sTemplateFileName = "FFGLTemplateDefault2.cpp"
    m_sTemplateHeaderFile = "FFGLTemplateDefault2.h"
    test = ""
    def __init__(self, _dicoParam, _pluginInfo): #_dicoParam : dico<int, FFGLParameter>
        print("__Init__ FFGL20Writer")
        FFGLWriter.__init__(self,_dicoParam,_pluginInfo)
        self.ConvertParamInfo()
       # print("_dicoParam = " +self.m_DicoParam  )
        
        #super.m_DicoParam = _dicoParam
      #  print("include part = "+self.m_sIncludePart)
        
    #convert the paramInfo plugin sectin to the new format for FFGL2.0
    def ConvertParamInfo(self): 
       # self.m_PluginInfo = "PluginFactory< TemplateName >,// Create method"
        self.m_PluginInfo.m_sAPIMajVersion = "2" #,// API major version number"
        self.m_PluginInfo.m_sAPIMinVersion = "1" #,// API minor version number"
        self.m_PluginInfo.m_sPluginMaj = "1" #,// Plugin major version number"
        self.m_PluginInfo.m_sPluginMin = "0" #,// Plugin minor version number"
        #i = 0
        #just puts some tabulation symbols in the lines
        #for info in self.m_PluginInfoTab:
         #   parts = info.split(",")
          #  if len(parts)>1:
           #     self.m_PluginInfoTab[i] = parts[0]+", \t\t "+parts[1]
            #i+=1
                    
        
    #Todo divide Write FFGL in two Part:
    # - WriteCppFile()
    # - WriteHFile()
    # Todo : to improve the tool, the program should read the header part first, get variables, and function from here, then implement the cpp part
    def WriteFFGL(self):
        fileName = self.m_PluginInfo.m_sClassName 
        #write the input data into a FFGL2.0 code and save it in a buffer variable 
        cppCode = self.WriteCPPFile() #fill self.m_dicoVar with the variables to creates
        headerCode = self.WriteHeader(self.m_dicoVar) 
        #record the new code
        self.SaveFile(cppCode, fileName+".cpp") #save the implementation part into a .cpp file
        self.SaveFile(headerCode,fileName +".h") #save the header into a .h file
    
    def SaveFile(self, _tabCode, _fileName):
        fo = open(_fileName, "w")
        for line in _tabCode:
            if line.endswith("\n") == False:
                line+="\n"
            fo.write(line)
        fo.close()
        
    def WriteHeader(self, _dicoVar):
        f= open(self.m_sTemplateHeaderFile,"r")
        newCode = []
        code = f.readlines()
        bTimeVarDefined = False #boolean helping don't implement time var twice
        for line in code:
            line = line.replace("FXTemplate",self.m_PluginInfo.m_sClassName)
            newCode.append(line)
            if "/*###CustomParameters###*/" in line: #write custom parameters under this line
                newCode.append("\n") #jump a line bro !                
                for var in self.m_dicoVar:  
                    newCode.append("\t"+self.m_dicoVar[var] +" "+var+";\n")
                newCode.append("\n") #jump a line again
                if self.m_bImplementTime == True and bTimeVarDefined == False:
                    newCode.append("/*###define time variables###*/")
                    newCode.append("\tdouble elapsedTime;\n")
                    newCode.append("\tdouble lastTime;\n")                    
                    newCode.append("#if (defined(WIN32) || defined(_WIN32) || defined(__WIN32__))\n")
                    newCode.append("\t// windows\n")
                    newCode.append("\tdouble PCFreq;\n")
                    newCode.append("\t__int64 CounterStart;\n")
                    newCode.append("#else\n")
                    newCode.append("\t// posix c++11\n")
                    newCode.append("\tstd::chrono::steady_clock::time_point start;\n")
                    newCode.append("\tstd::chrono::steady_clock::time_point end;\n")
                    newCode.append("#endif\n")
                    newCode.append("\n")    #jump a line
                    bTimeVarDefined = True
                
            if "/*###CustomFunctions###*/" in line : #write custom function under this line
                newCode.append("\n") #jump a line !
                for f in self.m_tabFunction:
                    newCode.append("\t"+f+";\n")      
       # f.close()
        return newCode
        
    #this function define how many glUniform have to be created and what kind of glUniform (glUniform2f, glUniform4f...) it return the optiimal numer of glUniform to create 
    def CreateGlParam(self, _paramNumber):
        dicoGlParam = {} #create a dictionary containing the type of glUniform to create (key) and the number to create (value)
        rest = _paramNumber
        index = 4 #4 is the max number supported by gl function to send to a shader : glUniform4f 
        while rest >0:
            q = int(rest/index)
            if q>0 :
                rest = rest%index
                dicoGlParam [index] = q #if q = 2 and index = 4, then we will have to create 2 GLuniform4
            index-=1
        return dicoGlParam 
    
    #write the .cpp file and return all the variables to creates
    def WriteCPPFile(self):
        print("test WriteFFGL")
        templateFFGL = open(self.m_sTemplateFileName,"r")
        code = templateFFGL.readlines()
        dicoGluniform = {} #dico containing number of gluniform to create and gluniform type (uniform4,3,2...)
        listParamLocation = [] #list of paramterLocation
        listParamSpeedLocation = [] #list of paramterLocation linked to the time value
        dicoParamSpeedName = {} #list of parameter name linked to the time {paramVarName, time variable}
        newCode = ""
        print("###NewCode###")
        for line in code:
            #print(line)
            line = line.replace("FXTemplate",self.m_PluginInfo.m_sClassName)   #replace the template class name by the new class name         
            newCode += line

            if "/*###DefineSection###*/" in line:
                index = 0
                for i in self.m_DicoParam:
                    newCode+="#define "+i+" ("+str(index)+")\n"
                    index +=1
            #todo : make a structure for PluginInfo with it's name, id, version etc.... it will be easier and cleaner to conver it.
            
            if "/*###FFGLInfoSection###*/" in line :
                newCode += "PluginFactory< "+self.m_PluginInfo.m_sClassName+" >, \t// Create method\n"
                newCode +=  "\t"+self.m_PluginInfo.m_sID+",\t\t\t// Plugin unique ID of maximum length 4.\n"
                newCode +=  "\t"+self.m_PluginInfo.m_sPluginName+",\t\t// Plugin name\n"
                newCode +=  "\t"+self.m_PluginInfo.m_sAPIMajVersion+",\t\t\t// API major version number\n"
                newCode +=  "\t"+self.m_PluginInfo.m_sAPIMinVersion+",\t\t\t// API minor version number\n"
                newCode +=  "\t"+self.m_PluginInfo.m_sPluginMaj+",\t\t\t// Plugin major version number\n"
                newCode +=  "\t"+self.m_PluginInfo.m_sPluginMin+",\t\t\t// Plugin minor version number\n"
                newCode +=  "\t"+self.m_PluginInfo.m_sEffectType+",\t\t// Plugin type\n"
                newCode +=  "\t"+self.m_PluginInfo.m_sDescription+",\t// Plugin description\n"
                newCode +=  "\t"+self.m_PluginInfo.m_sAbout+"\t// About\n"           

            if "/*###InitParams###*/" in line:
#                print(self.m_DicoParam)
                newCode+="\t//init the params here \n"
                index = 0
                indexSpeed = 0
                for i in self.m_DicoParam:
                    newParam = ""
                    if self.m_DicoParam[i].m_sTypeParam == "Speed":
                        indexSpeed +=1
                        timeVarName = "m_time"+str(indexSpeed)
                        self.m_dicoVar[timeVarName] = "float" #save in this buffer to declare it in the header when needed                        
                        dicoParamSpeedName[self.m_DicoParam[i].m_sVarName] = timeVarName #save all the param who will be linked to the time in this array
                    if self.m_DicoParam[i].m_bIsShader == False:
                        newParam = self.m_DicoParam[i].m_sVarName #.replace('"','')
                    else:
                        index+=1
                        newParam = "m_param"+str(index) #rename only the parameters to link to the shader                    
                    #param ="write :" +self.m_DicoParam[i].m_sParamName+" - "+self.m_DicoParam[i].m_sTypeParam
                    #print(param)
                    newCode += "\t"+newParam+"("+self.m_DicoParam[i].m_sParamValue+" ),\n" #write parameters initialisation like m_param1(0.5)
                    self.m_dicoVar[newParam] = "float"
            if "/*###AddParameterSection###*/" in line:
                newCode+="\t//Add the params here \n"
                for i in self.m_DicoParam:
                    param = self.m_DicoParam[i]
                    paramType = param.m_sTypeParam
                    if paramType == "Speed": #some parameter type has been marked as "speed" because they need a different implementation of classic FF_Type_Standard
                        paramType = "FF_TYPE_STANDARD" #However, in the SetParamInfo section we need to write the param as a FF_Type_Standard
                        self.m_bImplementTime =True
                    newCode += "\tSetParamInfof("+i+", "+param.m_sParamName+", "+paramType+");\n"
                if self.m_bImplementTime == True:
                    newCode+="\n\t/*###Implement time###*/\n"
                    #init the time1....2...3 variable also here
                    for i in dicoParamSpeedName:
                        newCode+="\t"+dicoParamSpeedName[i]+" = 0.0;\n" #init the time counter at 0
                    newCode+="\telapsedTime = 0.0;\n"
                    newCode+="\tlastTime = 0.0;\n"
                    newCode+="\t#if (defined(WIN32) || defined(_WIN32) || defined(__WIN32__))\n"
                    newCode+="\tPCFreq = 0.0;\n"
                    newCode+="\tCounterStart = 0;\n"
                    newCode+="\t#else\n"
                    newCode+="\tstart = std::chrono::steady_clock::now();\n"
                    newCode+="\t#endif\n"
                    #add these variable to the dico var to implement them in the header
                   # self.m_dicoVar["elapsedTime"] = "double"
                   # self.m_dicoVar["lastTime"] = "double"
                   # self.m_dicoVar["PCFreq"] = "double"
                   # self.m_dicoVar["CounterStart"] = "__int64"
                   # self.m_dicoVar["start"] = "std::chrono::steady_clock::time_point"
                   # self.m_dicoVar["end"] = "std::chrono::steady_clock::time_point"
            if "/*###InitUniforms###*/" in line:
                paramNumber = 0 #count number of parameters linked with shaders
                paramSpeedNumber = len(dicoParamSpeedName) #count the number of parameter linked to the time
                #count the number of parameter who should be linked to the shader and give this number to the CreateGLParamFunction
                for i in self.m_DicoParam:
                    if self.m_DicoParam[i].m_bIsShader == True:
                        paramNumber+=1
                dicoGluniform = self.CreateGlParam(paramNumber)
                dicoGlSpeedUniform = self.CreateGlParam(paramSpeedNumber)
                
                newCode+="\t//assign the uniforms here \n"
                nbParam = 0
                for i in dicoGluniform: #for each element of the dico
                    for j in range(0,dicoGluniform[i]): #dicoGluniform[i] gives the number of GLUniform to create so (GLUniform number) X (Number of dico element) = Number of ParamLocation
                        nbParam+=1
                        paramName = "ParamLocation"+str(nbParam)
                        listParamLocation.append(paramName)
                        newCode+="\t"+paramName+" = m_shader.FindUniform(\"m_param"+str(nbParam)+"\");\n"
                
                #create paramLocation for speed
                nbParam = 0 #reinit the param counter
                for i in dicoGlSpeedUniform:
                    for j in range(0,dicoGlSpeedUniform[i]):
                        nbParam+=1
                        paramName = "ParamSpeedLocation"+str(nbParam)
                        listParamSpeedLocation.append(paramName)
                        newCode+="\t"+paramName+" = m_shader.FindUniform(\"m_time"+str(nbParam)+"\");\n"
                
                #if the time have to be implemented
                if self.m_bImplementTime==True:
                    newCode+="\n\t/*###init Time###*/\n"
                    newCode+="\tStartCounter();\n"
                    
            if "/*###LinkShaderParams###*/" in line:
                if self.m_bImplementTime==True:
                    #implement time
                    newCode+=self.UpdateTime(dicoParamSpeedName) #add the code to create time vraiable
                    #implement here connection with shader by ddefault. Add option to let the user choose if the speed must by linked to the shader or not  
                newCode+="\t//link the uniforms with the parameters here \n"
                index = 0
                paramCount = 0 #used to create the param names : m_param1,m_param2,m_param3
                for i in dicoGluniform: #get the key of the dico param in the i variable
                    for j in range(0,dicoGluniform[i]):
                        
                        unfiformName = listParamLocation[index] #name of the variable
                        self.m_dicoVar[unfiformName] = "GLint"
                        newCode+="\tglUniform"+str(i)+"f("+unfiformName+", "
                        index+=1
                        for k in range(0,i):
                            paramCount+=1
                            newCode += "m_param"+str(paramCount) #start at "m_param1"
                            if k==i-1: #if it's the last iteration, end the line
                                newCode+=");\n"
                            else:
                                newCode+=", "
                newCode+= "\n" #end of the section
                
                index=0 #reinit the index
                paramCount =0 #reinit the index
                for i in dicoGlSpeedUniform: #get the key of the dico param in the i variable
                    for j in range(0,dicoGlSpeedUniform[i]):
                        
                        unfiformName = listParamSpeedLocation[index] #name of the variable
                        self.m_dicoVar[unfiformName] = "GLint" #used for the header part
                        newCode+="\tglUniform"+str(i)+"f("+unfiformName+", "
                        index+=1
                        for k in range(0,i):
                            paramCount+=1
                            newCode += "m_time"+str(paramCount) #start at "m_param1"
                            if k==i-1: #if it's the last iteration, end the line
                                newCode+=");\n"
                            else:
                                newCode+=", "
                newCode+= "\n" #end of the section
                
            if "/*###DeInitParams###*/\n" in line:
                newCode+="\t//Deinitialize the parameters here \n"
                for ParamLoc in listParamLocation:
                    newCode += "\t"+ParamLoc + " = -1;\n"
                for ParamSpeedLoc in listParamSpeedLocation:
                    newCode += "\t"+ParamSpeedLoc + " = -1;\n"
            #TODO : renomer les varName des shader de l'objet self.m_DicoParam
            if "/*###SetParamValue###*/\n" in line:
                newCode+="\t//Set the parameters value here \n"
                nbParam=1
                for i in self.m_DicoParam:
                    newCode+="\tcase "+i+":\n"
                    if self.m_DicoParam[i].m_bIsShader==True:
                        newCode+="\t\tm_param"+str(nbParam)+" = value;\n"
                        nbParam+=1
                    else:
                        newCode+="\t\t "+self.m_DicoParam[i].m_sVarName+" = value;\n"                        
                    newCode+="\t\tbreak;\n"
            if "/*###GetParamValue###*/\n" in line:
                #write the parameters here
                newCode+="\t//Get the parameters value here \n"
                nbParam=1
                for i in self.m_DicoParam:
                    newCode+="\tcase "+i+":\n"
                    if self.m_DicoParam[i].m_bIsShader==True:                
                        newCode+="\t\t return m_param"+str(nbParam)+";\n"
                        nbParam+=1     
                    else:
                        newCode+="\t\treturn "+self.m_DicoParam[i].m_sVarName+";\n"           
        if self.m_bImplementTime == True:
            newCode+=self.ImplementTimeFunction()
        print(newCode)
        print("### End new code ###")
        return newCode.split('\n') #convert the string into a tab[] before return the value. 
        # create new cpp file
        # get FFGL2.0 template
        # insert parameter
        # print ffgltemplate into the cpp file
        # let see what's happen
        
    def UpdateTime(self, _dicoTime):
        code = "\n\t/*##Update Time##*/\n"
        code += "\t/*the time is just imlemented to gives you possibility to use it. recode manually the way your are using the time var*/\n"
        code+= "\t// Calculate elapsed time\n"
        code+= "\tlastTime = elapsedTime;\n"
        code+= "\telapsedTime = GetCounter() / 1000.0; // In seconds - higher resolution than timeGetTime()\n"
        index = 0
        #dicoParamSpeedShader = 
        for paramName in _dicoTime:
                paramTime = _dicoTime[paramName]
                code+= "\t"+paramTime +"= "+paramTime+" + (float)(elapsedTime - lastTime)*("+paramName+"*2.0-1.0); // time goes from -1 to 1 by default \n"
        return code+"\n"
    
    def ImplementTimeFunction(self):
        self.m_tabFunction.append("void StartCounter()")
        code = "\n/*###Implement the times functions###*/\n"
        code += "/*From Lynn Jarvis code : https://github.com/leadedge/ShaderMaker/blob/master/ShaderMaker.cpp*/\n"
        code += "void "+self.m_PluginInfo.m_sClassName+"::StartCounter()\n"
        code += "{\n"
        code += "#if (defined(WIN32) || defined(_WIN32) || defined(__WIN32__))\n"
        code += "\tLARGE_INTEGER li;\n"
        code += "\t// Find frequency\n"
        code += "\tQueryPerformanceFrequency(&li);\n"
        code += "\tPCFreq = double(li.QuadPart) / 1000.0;\n"
        code += "\t// Second call needed\n"
        code += "\tQueryPerformanceCounter(&li);\n"
        code += "\tCounterStart = li.QuadPart;\n"
        code += "#else\n"
        code += "\t// posix c++11\n"
        code += "\tstart = std::chrono::steady_clock::now();\n"
        code += "#endif\n"
        code += "}\n"

        self.m_tabFunction.append("double GetCounter()")
        code += "\n/*From Lynn Jarvis code : https://github.com/leadedge/ShaderMaker/blob/master/ShaderMaker.cpp/ */" 
        code += "\ndouble "+self.m_PluginInfo.m_sClassName+"::GetCounter()\n"
        code += "{\n"
        code += "#if (defined(WIN32) || defined(_WIN32) || defined(__WIN32__))\n"
        code += "LARGE_INTEGER li;\n"
        code += "\tQueryPerformanceCounter(&li);\n"
        code += "\treturn double(li.QuadPart - CounterStart) / PCFreq;\n"
        code += "#else\n"
        code += "\t// posix c++11\n"
        code += "\tend = std::chrono::steady_clock::now();\n"
        code += "\treturn std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() / 1000.;\n"
        code += "\t#endif\n"
        code += "\treturn 0;\n"
        code += "}\n"
        return code