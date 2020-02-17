#include "FXTemplate.h"
#include <ffgl/FFGLLib.h>
#include <ffglex/FFGLScopedShaderBinding.h>
#include <ffglex/FFGLScopedSamplerActivation.h>
#include <ffglex/FFGLScopedTextureBinding.h>
using namespace ffglex;

//#define FFPARAM_Param1 ( 0 )
/*###DefineSection###*/
/*###EndDefineSection###*/

static CFFGLPluginInfo PluginInfo(
/*###FFGLInfoSection###*/
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

FXTemplate::FXTemplate() :

        /*###InitParams###*/
        /*###EndInitParams###*/
        
        m_maxUVLocation(-1)
{
        // Input properties
        SetMinInputs( 1 );
        SetMaxInputs( 1 );


        // Parameters
        /*###AddParameterSection###*/
        /*###EndAddParameterSection###*/
}
FXTemplate::~FXTemplate()
{
}

FFResult FXTemplate::InitGL( const FFGLViewportStruct* vp )
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
        /*###EndInitUniforms###*/

        //ParamLocation1= m_shader.FindUniform( "Param1" );
        
        //Use base-class init as success result so that it retains the viewport.
        return CFreeFrameGLPlugin::InitGL( vp );
}
FFResult FXTemplate::ProcessOpenGL( ProcessOpenGLStruct* pGL )
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
FFResult FXTemplate::DeInitGL()
{
        m_shader.FreeGLResources();
        quad.Release();
        m_maxUVLocation = -1;
        //m_resolutionLocation = -1;

        /*###DeInitParams###*/
        //ParamLocation1 = -1;
        //ParamLocation2 = -1;
        /*###EndDeInitParams###*/

        return FF_SUCCESS;
}

FFResult FXTemplate::SetFloatParameter( unsigned int dwIndex, float value )
{
        switch( dwIndex )
        {
        /*###SetParamValue###*/
        /*###EndSetParamValue###*/

        default:
                return FF_FAIL;
        }

        return FF_SUCCESS;
}

float FXTemplate::GetFloatParameter( unsigned int dwIndex )
{
        switch( dwIndex )
        {
        /*###GetParamValue###*/
        /*###EndGetParamValue###*/
        default:
                return 0.0f;
        }
}
