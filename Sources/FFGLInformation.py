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