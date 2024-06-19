import glfw
from OpenGL.GL import *
from PIL import Image
import numpy as np

# Compile and link shaders
def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        info_log = glGetShaderInfoLog(shader)
        raise Exception(f"Shader compilation failed: {info_log}")

    return shader

# Load the texture image using PIL and set up the texture in OpenGL
def load_texture(image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    img_data = np.array(image)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    return texture_id

if __name__ == "__main__":
    # Initialize GLFW
    if not glfw.init():
        raise Exception("GLFW can't be initialized")

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(800, 600, "Texture Example", None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")

    glfw.make_context_current(window)

    # Vertex Shader Source
    vertex_shader_source = """
    #version 410 core
    layout(location = 0) in vec3 aPos;    
    layout(location = 1) in vec2 aTexCoord;
    
    out vec2 TexCoord;
    
    void main()
    {
        gl_Position = vec4(aPos, 1.0);
        TexCoord = aTexCoord;
    }
    """

    # Fragment Shader Source
    fragment_shader_source = """
    #version 410 core
    in vec2 TexCoord;
    out vec4 FragColor;
    
    uniform sampler2D texture1;
    
    void main()
    {
        FragColor = texture(texture1, TexCoord);
    }
    """

    vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        info_log = glGetProgramInfoLog(shader_program)
        raise Exception(f"Program linking failed: {info_log}")

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    # Define vertices and texture coordinates
    vertices = np.array([
        # positions        # texture coords
        1.0,  1.0, 0.0,    1.0, 2.0,  # top right
        1.0, -1.0, 0.0,    1.0, 0.0,  # bottom right
       -1.0, -1.0, 0.0,    0.0, 0.0,  # bottom left
       -0.5,  0.5, 0.0,    0.0, 1.0   # top left
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 3,  # First triangle
        1, 2, 3   # Second triangle
    ], dtype=np.uint32)

    # Setup buffers
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Texture coordinate attribute
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    path = r"C:\Users\Natspir\Pictures\Resources\TalesOfTheUnderground\ClownMakeup\6a21e6a92d0d22453f9f73986e0cc12b.jpg"

    # Load and set up the texture
    texture_id = load_texture(path)

    glUseProgram(shader_program)
    texture_location = glGetUniformLocation(shader_program, "texture1")
    glUniform1i(texture_location, 0)

    # Render loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glUseProgram(shader_program)
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()