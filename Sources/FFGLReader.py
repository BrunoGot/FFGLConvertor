# -*- coding: utf-8 -*-
import re

class FFGLInformation:
    m_sClassName = "" #name of the cpp class file
    m_sID = "" #Id of the plugin
    m_sPluginName = "" #Name of the plugin
    m_sAPIMajVersion = "" #API major version
    m_sAPIMinVersion = "" #API minor version 
    m_sPluginMaj = "" #Plugin major version
    m_sPluginMin = "" #Plugin minor version
    m_sEffectType = "" #plugin effect type
    m_sDescription = "" #plugin description
    m_sAbout = "" #plugin About
    def __init__(self, _className, _id, _pluginName, _APIMaj, _APIMin, _pluginMaj, _pluginMin, _effectType, _description, _about):
        self.m_sClassName = _className
        self.m_sID = _id
        self.m_sPluginName = _pluginName
        self.m_sAPIMajVersion = _APIMaj
        self.m_sAPIMinVersion = _APIMin
        self.m_sPluginMaj = _pluginMaj
        self.m_sPluginMin = _pluginMin
        self.m_sEffectType = _effectType
        self.m_sDescription = _description
        self.m_sAbout = _about
        
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
    m_pluginInfo = FFGLInformation("","","","","","","","","","") #structure containing the plugin info section
    m_sSourceFile = "" #the file to read
   #obselete m_sPluginInfo = [] #var containing the plugin info section
    m_dicoParam = {} #var containing parameters in a dictionary struct
    m_bMultiComment = False #boolean helping to know if the current line is in a comment or not    
    # rajouter m_sVarParam contenant le nom de a variable relié a ce parametre
    def Convert(self, _sourceFile):
        self.m_sSourceFile = open(_sourceFile, "r")
        print("ready to parse %s" % self.m_sSourceFile)        
        self.Parse(self.m_sSourceFile)       
        return self.m_dicoParam
    
    def ParseShaderParameters(_inCode):
        print("Detect what parameters are used to control the shader")
        
    #diferent type of comments : 
    #  - code /*comments */ 
    #  - code /*comments */ code
    #  - code /*comments /*comments */ code
    #  - code /*comments */ code /*comments */ code
    #  - code /*comments */ code // */ code
    #  - code /* comments
    #  comments
    #  */ code
    # make a recursiv function of this shit (if tempLine >0 , call function(tempLine))
    #this function is obselete and shity
    def ClearCode(self,_inCode):
        print("Remove all inutile stuff from the code like comments")
        print(_inCode)
        newCode = ""
        bMultiCommented = False #boolean setted to True when a multiline comment is detected ("/*")
        for line in _inCode:
            #temp = line.replace("/*","") #remove temporary all "/*"symbole to get only the end of the comments : "*/"
            #splittedLine = temp.split("*/") #split the line with the end of the comment symbole "*/" to count exact comment number
            tempLine = line
            if bMultiCommented == False:
                #search for comment
                startComIndex = line.find("/*")
                if startComIndex != -1:
                    #Comment found
                    codePart = line[:startComIndex]
                    commentPart = line[(startComIndex +2):] #(startComIndex +2) is because we need the string part from "startComIndex" + the sperator length '/*' = 2 characters                        
                    tempLine = commentPart
                    bMultiCommented = True
            #search the end of the multicomment
            if bMultiCommented == True:
                for i in range(0,commentPart.count("*/")):
                    endComIndex = tempLine.find("*/") #search for end of comment in the rest of the line
                    if endComIndex != -1:
                        codePart+=tempLine[endComIndex+2:]
                        commentPart = tempLine[:endComIndex]
                        bMultiCommented = False
                    #search for new comment in the code part
                    startComIndex = codePart.find("/*")
                    if startComIndex != -1 :
                        codePart = codePart[:startComIndex] #clear the code part from the new comment
                        commentPart += line[(startComIndex +2):]
                        tempLine = commentPart
                        bMultiCommented = True
                        
    def ClearMultiComRec(self, _sLine, _bIsCommented):
        sLineToParse = "" #the line to give to the new function
        sLineToReturn = ""
        #if it's in a commented part
        if _bIsCommented == True: 
            #search for the end of the comment
            endIndex = _sLine.find("*/")
            if endIndex != -1:
                #end of the comment found
                commentPart = _sLine[:endIndex]
                codePart = _sLine[(endIndex+2):]
                _bIsCommented = False
                #give the rest of the line to parse in the recursiv call
                sLineToParse = codePart
            else:
                self.m_bMultiComment = _bIsCommented #Update the global comment flag
                #if the end of the comment is not found so all the line is commented and nothing is returned
                return ""
        else: #if it's a non commented part
            #search for a new comment in the line
            startIndex = _sLine.find("/*")
            if startIndex != -1:
                #new comment found
                commentPart = _sLine[(startIndex+2):]
                codePart = _sLine[:startIndex+1] #add the "/" character of "/*" to dected snicky comment like "//*..."
                if "//" in codePart:
                    #the multiline comment is not active bevause it's already commented by "//" so it will be cleaned in self.ClearSimpleComment()function
                    self.m_bMultiComment = _bIsCommented
                    return _sLine
                else :
                    codePart = _sLine[:startIndex] #if no snicky comment found reset the code part without the "/" character   
                    _bIsCommented = True
                    # give the comment part to be parsed in the recursiv call
                    sLineToParse = commentPart
                    #return the parsed code part
                sLineToReturn = codePart
            else:
                self.m_bMultiComment = _bIsCommented #Update the global comment flag                
                # no new comment has been found so return all the line 
                return _sLine
        self.m_bMultiComment = _bIsCommented #Update the global comment flag    
        #return the code part + call the recursiv function to clean the line to parse
        return sLineToReturn + self.ClearMultiComRec(sLineToParse,_bIsCommented)  
            
    def ClearSimpleComment(self, _inLine): #clear simple comment from line
        outLIne = _inLine #line to clear and return 
        if "//" in _inLine: #clear the comments with "//"
            newLine = _inLine.split("//")[0]
           # if newLine != "":
            outLIne = newLine #save the no commented part of the line
        return outLIne
    
    #Clear the code from all comments (//,/**/)
    def ClearComments(self, _inCode):
        newCode = []
        for line in _inCode:
            newLine = self.ClearMultiComRec(line, self.m_bMultiComment)
            newLine = self.ClearSimpleComment(newLine) #clear the simple '//' comments after the multiline comments
            newCode.append(newLine)
        return newCode
            

    #Enlever tout les commentaire
    # enlever tout les \n (obligé ?)
    # stocker le nouveau fichier dans une variable
    # dans differentes pass faire : 
    #  - parser infoParam 
    #  - parser les varParam
    #  - detecter les shader param            
    def Parse(self, _inFile): #new version of parse() function
        print("In Parse")
        #get the code        
        code = _inFile.readlines()
        #Clear the code from its comments
        newCode = self.ClearComments(code)
        # Get the Info about the FFGL itself
        self.RecordPluginInfo(newCode)
        print("ParseInfoParam : ")
        #Get the info about the FFGLs parameters
        self.ParseInfoParam(newCode)
        #Assign each FFGM Name to their variable name in the code
        self.ParseVariableName(newCode)
        #detect the FFGL parameters linked with shader parameters
        self.RecordGluniform(newCode)
                
    #get the informations about the plugin
    #todo : use an index to get the param number, use a switch case to parse each parameters differently
    def RecordPluginInfo(self, _code):
        bRecordPluginInfo = False #flag telling to record plugin info lines if is in true       
        paramIndex = 0 #index indcating the current parameter parsed
        tabInfo = [] # array containing the different info
        for line in _code:
            infoLine = "" #line containing the information
            if bRecordPluginInfo== True: #if we are in the info section
                line = self.ClearSymbols(line) #clear symbols "\t" and "\n"
                if ");" in line: #if the symbol ");" is detected so it's the end of the info section
                    bRecordPluginInfo = False
                    infoLine = line.split(");")[0] # get the left part of the last line to check if there is some code
                    #if lastLine != "":
                     #   self.m_sPluginInfo.append(lastLine)
                elif line != "":
                   # print("Add info : "+line)
                    #self.m_sPluginInfo.append(line )
                    infoLine = line 
            elif "CFFGLPluginInfo" in line :
                bRecordPluginInfo = True
                firstLine = line.split("(")[1] #get the right part of the "(" character to check if there is some code to add to the infoplugin.
                firstLine = self.ClearSymbols(firstLine)
                if self.ClearSpaces(firstLine) != "":
                    #self.m_sPluginInfo.append(firstLine)
                    infoLine = firstLine
            #appy different parsing according to the parameters index
            if infoLine != "":
                if paramIndex == 0:
                    print("parse first info : "+infoLine)
                    infoLine = infoLine.split("::")[0]
                else:
                    infoLine = infoLine.replace(",","")

                infoLine = self.ClearInutilChar(infoLine)                
                tabInfo.append(infoLine)
                paramIndex +=1
        self.m_pluginInfo = FFGLInformation(tabInfo[0],tabInfo[1], tabInfo[2], tabInfo[3],tabInfo[4],tabInfo[5],tabInfo[6],tabInfo[7],tabInfo[8],tabInfo[9])
        
    #Clear symbols and spaces
    def ClearInutilChar(self, _line):
        _line = self.ClearSymbols(_line)
        #clear spaces only inutil spaces, not spaces in strings
        if _line.find('"') != -1: #if the line contains sentences clear space only in the code part
            t = _line.split('"')
            i = 0
            sLine = ""
            for e in t:
                if i%2 == 0: #one element of two must be cleaned from spaces
                    sLine += self.ClearSpaces(e)
                else :
                    sLine += '"'+e+'"' #other elements are sentences and must keep their spaces
                i+=1
        else: #else clear all the spaces
            _line = self.ClearSpaces(_line)
        return _line

    def ClearSymbols(self, _line): #clear the line from special symbols like "\n", "\t" 
        print("clear line for : "+_line)
        outLine = _line.replace("\t","")
        outLine = outLine.replace("\n","")
        print("outLine = "+outLine)
        return outLine
    
    def ClearSpaces(self, _line):#clear the line from spaces like " " 
        outLine = _line.replace(" ","")
        return outLine
    
    def ParseInfoParam(self, _code):
        print("in ParseInfoParam")
        for line in _code:
            #print(line)
            if "SetParamInfo" in line:
                print("SetParamInfoDetected : "+line)
                self.RecordParam(line)              

    def ParseVariableName(self, _code):
        print("Get the varaible name linked with the parameters")       
        bInSetFloatParamFunction = False
        paramToAssign = "" #buffer containing the param 'FFPAram_*' to assign to a variable name 
        for line in _code:
            #print(line)
            if "SetFloatParameter" in line:
                bInSetFloatParamFunction = True
            elif bInSetFloatParamFunction == True:
                if "case" in line:
                    for param in self.m_dicoParam:
                        print("try to assign " + param+" in line : "+line)
                        if param in line:
                            paramToAssign = param
                            break #end the loop
                if "value" in line: #if the KeyWord "value" is detected we assume that this is the assignation line with the input value and the variableName
                    sVarName = line.split('=')[0] #get the left part of the assignation to get the vriableName
                    sVarName = sVarName.replace(' ','') #remove spaces
                    sVarName = sVarName.replace("\t","") #remove "\t" symbols
                    self.m_dicoParam[paramToAssign].m_sVarName = sVarName 
     
    #to continue here
    def RecordGluniform(self, _code):
        bRecordGlUniform = False        
        for line in _code:
            if "glUniform" in line:
                bRecordGlUniform = True
               # print("GLUniform detected in line : " + line)
            if bRecordGlUniform == True: 
                #if the line is in "glUniform(...)" section then search for all param if it's assigned to a LocalShaderVariable
                for i in self.m_dicoParam: 
                    param = self.m_dicoParam[i]
                    #print("search for "+param.m_sVarName+" in line : "+line)
                    if param.m_sVarName in line : #detect if the name of the parameter's variable is in the gluniform line.
                        print(param.m_sVarName+" found in line : "+line)                        
                        self.m_dicoParam[i].m_bIsShader = True # if true then it's a shader parameter   
                if ";" in line:
                    bRecordGlUniform = False #if a ";" symbol is dected, then it's the end of the section
                
    #code below is obselete 
    def Parse2(self, _file):
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
   #test : C:\Users\Natspir\Documents\Code\C++\VFXArtShopEffects_4\source\plugins\Geometric\NSGeometric.cpp
    def RecordParam(self, paramLine):
       # print("paramLine = "+paramLine)
        #remove "SetParamInfo" word from the line
        paramLine = paramLine.replace("\t", "") #remove \t symbols
        paramLine = paramLine.replace("SetParamInfo","")
        #remove '(' and ')' characters to get something like 'FFPARAM_MixVal, "Mixer Value", FF_TYPE_STANDARD, 0.5f'
        paramLine = paramLine.replace('(','') 
        paramLine = paramLine.replace(')','')
        paramLine = paramLine.replace(';',"")
        paramLine = self.ClearInutilChar(paramLine)
        print("paramLine after remove = "+paramLine)        
        paramLine = paramLine.split(',')
        paramStruct = FFGLParameter(paramLine[0],paramLine[2],False,paramLine[1],paramLine[3]) #continue here
        self.m_dicoParam[paramLine[0]] = paramStruct
