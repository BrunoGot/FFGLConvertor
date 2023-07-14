class FFGLParameter:
    m_sFFParamName = "" #name of the parameter
    m_sTypeParam = "" #standrad, speed, boolean
    m_bIsShader = True #link this parameter to a shader
    m_sParamName = "" #name of the parameter
    m_sParamValue = []#default value of the parameter
    m_sVarName = "" #the variable name assigned to the parameter


    def __init__(self, _sTypeParam, _bIsShader, _sParamName, _sParamValue, _index):
        """

        :param _sTypeParam:
        :param _bIsShader:
        :param _sParamName:
        :param _sParamValue:
        :param _index integer: the parameter number (must be unique)
        """
        self.m_sTypeParam = _sTypeParam.replace(" ","")
        print("self.m_sTypeParam = "+str(self.m_sTypeParam))
        self.m_bIsShader = _bIsShader
        self.m_sParamName = _sParamName
        self.m_sParamValue = _sParamValue
        self.m_sVarName = f"m_param{_sParamName}"
        self._index = _index
        #parse name to set paramType as "Speed" type if the param is linked with time
        paramName = _sParamName.lower()
        if "speed" in paramName:
            print("speed = -"+self.m_sTypeParam +"-")
            if self.m_sTypeParam == "FF_TYPE_STANDARD": 
                print("speed2 = "+self.m_sTypeParam )                
                self.m_sTypeParam  = "Speed"

    @property
    def index(self):
        """return integer"""
        return self._index

    @property
    def ffgl_param_index(self):
        """:rtype string: """
        return f"FFPARAM_{self._index+1}"