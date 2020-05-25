class FFGLParameter:
    m_sFFParamName = "" #name of the parameter
    m_sTypeParam = "" #standrad, speed, boolean
    m_bIsShader = True #link this parameter to a shader
    m_sParamName = "" #name of the parameter
    m_sParamValue = []#default value of the parameter
    m_sVarName = "" #the variable name assigned to the parameter
    def __init__(self, m_sFFParamName, _sTypeParam, _bIsShader, _sParamName, _sParamValue):
        self.m_sTypeParam = _sTypeParam.replace(" ","")
        print("self.m_sTypeParam = "+str(self.m_sTypeParam))
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
