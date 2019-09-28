#pragma once
#include <string>
#include <ffgl/FFGLPluginSDK.h>
#include <ffglex/FFGLShader.h>
#include <ffglex/FFGLScreenQuad.h>

class FXTemplate : public CFreeFrameGLPlugin
{
public:
FXTemplate();
        ~FXTemplate();

        //CFreeFrameGLPlugin
        FFResult InitGL( const FFGLViewportStruct* vp ) override;
        FFResult ProcessOpenGL( ProcessOpenGLStruct* pGL ) override;
        FFResult DeInitGL() override;

        FFResult SetFloatParameter( unsigned int dwIndex, float value ) override;

        float GetFloatParameter( unsigned int index ) override;

private:
/*###CustomParameters###*/

//	float param1;

        ffglex::FFGLShader m_shader;   //!< Utility to help us compile and link some shaders into a program.
        ffglex::FFGLScreenQuad quad; //!< Utility to help us render a full screen quad.
        GLint m_maxUVLocation;
        /*###CustomFunctions###*/
};
