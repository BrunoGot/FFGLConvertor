#include "NSCirclize.h"
#include <ffgl/FFGLLib.h>
#include <ffglex/FFGLScopedShaderBinding.h>
#include <ffglex/FFGLScopedSamplerActivation.h>
#include <ffglex/FFGLScopedTextureBinding.h>
using namespace ffglex;

//#define FFPARAM_Param1 ( 0 )
/*###DefineSection###*/
#define FFPARAM_Speed (0)
#define FFPARAM_Control1 (1)
#define FFPARAM_Control2 (2)
#define FFPARAM_But1 (3)
/*###EndDefineSection###*/

static CFFGLPluginInfo PluginInfo(
/*###FFGLInfoSection###*/
PluginFactory< NSCirclize >, 	// Create method
	"NCI1",			// Plugin unique ID of maximum length 4.
	"NSCirclize1",		// Plugin name
	2,			// API major version number
	1,			// API minor version number
	1,			// Plugin major version number
	0,			// Plugin minor version number
	FF_EFFECT,		// Plugin type
	"Demo Version : Distort the image and bend it into a circle this is the version 1.2" ,	// Plugin description
	"Premium version from www.VFXArtShop.com"	// About
/*###EndFFGLInfoSection###*/
);

static const char vertexShaderCode[] = R"(#version 410 core
uniform vec2 maxUV;

layout( location = 0 ) in vec4 vPosition;
layout( location = 1 ) in vec2 vUV;

out vec2 uv;

void main()
{
        gl_Position = vPosition;
        uv = vUV * maxUV;
}
)";

static const char fragmentShaderCode[] = R"(
#version 410 core
uniform sampler2D inputTexture;

in vec2 uv;

out vec4 fragColor;

void main()
{
        
        vec2 p = uv;


        vec4 _out =vec4(1.0,0.0,0.0,1.0);
        
        
        fragColor = vec4(_out);//mask;

}
)";

NSCirclize::NSCirclize() :

        /*###InitParams###*/
	//init the params here 
	m_paramSpeed( 0.5f ),
	m_param1( 0.0f ),
	m_param2( 0.5f ),
	m_param3( 0.0f ),
        /*###EndInitParams###*/
        
        m_maxUVLocation(-1)
{
        // Input properties
        SetMinInputs( 1 );
        SetMaxInputs( 1 );


        // Parameters
        /*###AddParameterSection###*/
	//Add the params here 
	SetParamInfof(FFPARAM_Speed,  "Speed", FF_TYPE_STANDARD);
	SetParamInfof(FFPARAM_Control1,  "Form", FF_TYPE_STANDARD);
	SetParamInfof(FFPARAM_Control2,  "Frequency", FF_TYPE_STANDARD);
	SetParamInfof(FFPARAM_But1,  "Link Freq&Speed", FF_TYPE_BOOLEAN);

	/*###Implement time###*/
	elapsedTime = 0.0;
	lastTime = 0.0;
	#if (defined(WIN32) || defined(_WIN32) || defined(__WIN32__))
	PCFreq = 0.0;
	CounterStart = 0;
	#else
	start = std::chrono::steady_clock::now();
	#endif
        /*###EndAddParameterSection###*/
}
NSCirclize::~NSCirclize()
{
}

FFResult NSCirclize::InitGL( const FFGLViewportStruct* vp )
{
        if( !m_shader.Compile( vertexShaderCode, fragmentShaderCode ) )
        {
                DeInitGL();
                return FF_FAIL;
        }
        if( !quad.Initialise() )
        {
                DeInitGL();
                return FF_FAIL;
        }

        //FFGL requires us to leave the context in a default state on return, so use this scoped binding to help us do that.
        ScopedShaderBinding shaderBinding( m_shader.GetGLID() );

        //We're never changing the sampler to use, instead during rendering we'll make sure that we're always
        //binding the texture to sampler 0.
        glUniform1i( m_shader.FindUniform( "inputTexture" ), 0 );
        //We need to know these uniform locations because we need to set their value each frame.
        m_maxUVLocation = m_shader.FindUniform("maxUV");
        //m_resolutionLocation = m_shader.FindUniform("resolution");
        
        //init parameters
        /*###InitUniforms###*/
	//assign the uniforms here 
	ParamLocation1 = m_shader.FindUniform("m_param1");

	/*###init Time###*/
	StartCounter();
        /*###EndInitUniforms###*/

        //ParamLocation1= m_shader.FindUniform( "Param1" );
        
        //Use base-class init as success result so that it retains the viewport.
        return CFreeFrameGLPlugin::InitGL( vp );
}
FFResult NSCirclize::ProcessOpenGL( ProcessOpenGLStruct* pGL )
{
        if( pGL->numInputTextures < 1 )
                return FF_FAIL;

        if( pGL->inputTextures[ 0 ] == NULL )
                return FF_FAIL;

        //FFGL requires us to leave the context in a default state on return, so use this scoped binding to help us do that.
        ScopedShaderBinding shaderBinding( m_shader.GetGLID() );

        FFGLTextureStruct& Texture = *( pGL->inputTextures[ 0 ] );

        //The input texture's dimension might change each frame and so might the content area.
        //We're adopting the texture's maxUV using a uniform because that way we dont have to update our vertex buffer each frame.
        FFGLTexCoords maxCoords = GetMaxGLTexCoords( Texture );
        
        glUniform2f( m_maxUVLocation, maxCoords.s, maxCoords.t );
        //glUniform2f(m_resolutionLocation, Texture.Height, Texture.Width);
        
        /*###LinkShaderParams###*/

	/*##Update Time##*/
	/*the time is just imlemented to gives you possibility to use it. recode manually the way your are using the time var*/
	// Calculate elapsed time
	lastTime = elapsedTime;
	elapsedTime = GetCounter() / 1000.0; // In seconds - higher resolution than timeGetTime()
	m_Time1= m_Time1 + (float)(elapsedTime - lastTime)*(m_paramSpeed*2.0-1.0); // time goes from -1 to 1 by default 

	//link the uniforms with the parameters here 
	glUniform3f(ParamLocation1, m_param1, m_param2, m_param3);
        /*###EndLinkShaderParams###*/

        /*	glUniform3f( ParamLocation1,
                                 param1 ,
                                 param2 ,
                                 param3 );*/

        //The m_shader's sampler is always bound to sampler index 0 so that's where we need to bind the texture.
        //Again, we're using the scoped bindings to help us keep the context in a default state.
        ScopedSamplerActivation activateSampler( 0 );
        Scoped2DTextureBinding textureBinding( Texture.Handle );

        quad.Draw();

        return FF_SUCCESS;
}
FFResult NSCirclize::DeInitGL()
{
        m_shader.FreeGLResources();
        quad.Release();
        m_maxUVLocation = -1;
        //m_resolutionLocation = -1;

        /*###DeInitParams###*/
	//Deinitialize the parameters here 
ParamLocation1 = -1;
        //ParamLocation1 = -1;
        //ParamLocation2 = -1;
        /*###EndDeInitParams###*/

        return FF_SUCCESS;
}

FFResult NSCirclize::SetFloatParameter( unsigned int dwIndex, float value )
{
        switch( dwIndex )
        {
        /*case FFPARAM_Param1:
                param1 = value;
                break;
        case FFPARAM_Param2:
                param2 = value;
                break;
        case FFPARAM_Param3:
                param3 = value;
                break;
        case FFPARAM_Param4:
                param4 = value;
                break;
        case FFPARAM_Param5:
                param5 = value;
                break;*/

        /*###SetParamValue###*/
	//Set the parameters value here 
	case FFPARAM_Speed:
		 m_paramSpeed = value;
		break;
	case FFPARAM_Control1:
		m_param1 = value;
		break;
	case FFPARAM_Control2:
		m_param2 = value;
		break;
	case FFPARAM_But1:
		m_param3 = value;
		break;
        /*###EndSetParamValue###*/

        default:
                return FF_FAIL;
        }

        return FF_SUCCESS;
}

float NSCirclize::GetFloatParameter( unsigned int dwIndex )
{
        switch( dwIndex )
        {
        /*case FFPARAM_Param1:
                return param1;
        case FFPARAM_Param2:
                return param2;
        case FFPARAM_Param3:
                return param3;
        case FFPARAM_Param4:
                return param4;
        case FFPARAM_Param5:
                return param5;*/
        /*###GetParamValue###*/
	//Get the parameters value here 
	case FFPARAM_Speed:
		return m_paramSpeed;
	case FFPARAM_Control1:
		 return m_param1;
	case FFPARAM_Control2:
		 return m_param2;
	case FFPARAM_But1:
		 return m_param3;
        /*###EndGetParamValue###*/
        default:
                return 0.0f;
        }
}

/*###Implement the times functions###*/
/*Inspired from shaderloader code*/
void NSCirclize::StartCounter()
{
#if (defined(WIN32) || defined(_WIN32) || defined(__WIN32__))
	LARGE_INTEGER li;
	// Find frequency
	QueryPerformanceFrequency(&li);
	PCFreq = double(li.QuadPart) / 1000.0;
	// Second call needed
	QueryPerformanceCounter(&li);
	CounterStart = li.QuadPart;
#else
	// posix c++11
	start = std::chrono::steady_clock::now();
#endif
}

double NSCirclize::GetCounter()
{
#if (defined(WIN32) || defined(_WIN32) || defined(__WIN32__))
LARGE_INTEGER li;
	QueryPerformanceCounter(&li);
	return double(li.QuadPart - CounterStart) / PCFreq;
#else
	// posix c++11
	end = std::chrono::steady_clock::now();
	return std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() / 1000.;
	#endif
	return 0;
}

