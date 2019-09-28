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

	float m_param1;
	float m_param2;
	float m_param3;
	float m_param4;
	double elapsedTime;
	double lastTime;
	double PCFreq;
	__int64 CounterStart;
	std::chrono::steady_clock::time_point start;
	std::chrono::steady_clock::time_point end;
	float m_Time1;
	GLint ParamLocation1;


//	float param1;

        ffglex::FFGLShader m_shader;   //!< Utility to help us compile and link some shaders into a program.
        ffglex::FFGLScreenQuad quad; //!< Utility to help us render a full screen quad.
        GLint m_maxUVLocation;
        /*###CustomFunctions###*/

	void StartCounter();
	double GetCounter();
};
