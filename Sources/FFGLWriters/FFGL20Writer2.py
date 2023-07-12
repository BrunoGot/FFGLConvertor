from FFGLWriter import FFGL20Writer

'''FFGL Writer for new C++ library style with optimized algo & template'''
class FFGL20Writer2(FFGL20Writer):
    def __init__(self, parameters, _pluginInfo):
        """

        :param parameters: list [FFGLParameter]
        :param _pluginInfo:
        """
        print("__Init__ FFGL20Writer_2")
        FFGL20Writer.__init__(self, parameters, _pluginInfo)
        '''#Todo take a new template
        analyze it : 
            How to add Parameter
            How to connect it with the shader
            How to realease it
             - plugin info : no changes
             - add parameters = addParam( hue1 = Param::create( "Hue 1", 0.5f ) );
             - 
        '''