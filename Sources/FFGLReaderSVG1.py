import re

class FFGLParameter:
    m_sFFParamName = ""
    m_sTypeParam = "" #standrad, speed, boolean
    m_bIsShader = True #link this parameter to a shader
    m_sParamName = "" #name of the parameter
    m_sParamValue = []#default value of the parameter
    m_sVarName = "" #the variable name assigned to the parameter
    def __init__(self, m_sFFParamName, _sTypeParam, _bIsShader, _sParamName, _sParamValue):
        self.m_sTypeParam = _sTypeParam.replace(" ","")
        self.m_bIsShader = _bIsShader
        self.m_sParamName = _sParamName
        self.m_sParamValue = _sParamValue
        #parse name to set paramType as "Speed" type if the param is linked with time
        paramName = _sParamName.lower()
        if "speed" in paramName:
            print("speed = -"+self.m_sTypeParam +"-")
            if self.m_sTypeParam == "FF_TYPE_STANDARD": 
                print("speed2 = "+self.m_sTypeParam )                
                self.m_sTypeParam  = "Speed"        
        
        
class FFGLReader:
    m_sSourceFile = "" #the file to read
    m_sPluginInfo = [] #var containing the plugin info section
    m_dicoParam = {} #var containing parameters in a dictionary struct
    # rajouter m_sVarParam contenant le nom de a variable relié a ce parametre
    def Convert(self, _sourceFile):
        self.m_sSourceFile = open(_sourceFile, "r")
        print("ready to parse %s" % self.m_sSourceFile)        
        self.Parse(self.m_sSourceFile)       
        return self.m_dicoParam
    
    
    #Refaire le parse :
    #Enlever tout les commentaire
    # enlever tout les \n (obligé ?)
    # stocker le nouveau fichier dans une variable
    # dans differentes pass faire : 
    #  - parser infoParam 
    #  - parser les varParam
    #  - detecter les shader param
    def ParseInfoParam(_inCode):
        print("get the informations about the parameters")
    def ParseVariableName(_inCode):
        print("Get the varaible name linked with the parameters")
    def ParseShaderParameters(_inCode):
        print("Detect what parameters are used to control the shader")
    
    def Parse(self, _file):
        print("Parse function need to be coded")
        code = _file.readlines() 
        #print(code)
        bRecordPluginInfo = False #flag telling to record plugin info lines if is in true
        bRecordParams = False #flag to record parameters line if true
        bCommantedLine = False
        bRecordGlUniform = False #Flag set to true when a line like glUniform3f( ParamLocation1,param1 ,param2 ,param3 ); is detected.  
        for raw_line in code :
            #get the plugins info
            line=raw_line.replace("\t", "")
            #print(line)            
            if "//" not in line[:2]: #si la ligne n'est pas commantée (looks for '//' char at the begining of the string 
                #ignore commanted line with "/*" 
                if "/*" in line : 
                    bCommantedLine = True
                elif "*/" in line :
                    bCommantedLine = False
                #if there is no commented line : 
                if bCommantedLine == False :
                    #print(line)
                    if bRecordPluginInfo== True:
                        if ");" in line:
                            bRecordPluginInfo = False
                        else:
                            self.m_sPluginInfo.append(line )  
                    elif "CFFGLPluginInfo" in line :
                        bRecordPluginInfo = True
                    
                    if "SetParamInfo" in line:
                        self.RecordParam(line)  
                    if "glUniform" in line:
                        bRecordGlUniform = True
                    if bRecordGlUniform == True:
                        self.RecordGluniform(line)
        print("plugin info = %s" % self.m_sPluginInfo)
        print("#######")
        print("Plugins params")
        index = 0
        for k in self.m_dicoParam:
            index+=1
            print("param %s" %index+" = " +self.m_dicoParam[k].m_sParamName+" - "+self.m_dicoParam[k].m_sTypeParam)
        #go to the first occurence of 'SetParamInfo'
        
   # def RecordParamInfo(self):
   #test : C:\Users\Natspir\Documents\Code\C++\VFXArtShopEffects_4\source\plugins\Circlize\NSCirclize.cpp
    def RecordParam(self, paramLine):
        print("paramLine = "+paramLine)
        paramLine = paramLine[13:-3] #remove first 13 characters and last 3 characters to get something like 'FFPARAM_MixVal, "Mixer Value", FF_TYPE_STANDARD, 0.5f'
        print("paramLine after remove = "+paramLine)        
        paramLine = paramLine.split(',')
        paramStruct = FFGLParameter(paramLine[0],paramLine[2],False,paramLine[1],paramLine[3]) #continue here
        self.m_dicoParam[paramLine[0]] = paramStruct
        
       #to continue here
    def RecordGluniform(self, _glUniformline):
        for i in self.m_dicoParam:
            param = self.m_dicoParam[i]
            if param.m_sVarName in line : #detect if the name of the parameter's variable is in the gluniform line.
                param.m_sIsShader = True # if true then it's a shader parameter