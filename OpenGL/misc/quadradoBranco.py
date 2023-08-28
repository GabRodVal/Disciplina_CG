from OpenGL import GL
import glm
import math
from glApp import *

VERTEX_SHADER = """
#version 400

layout (location=0) in vec3 attr_position;
layout (location=1) in vec2 attr_textureCoord;

out vec2 textureCoord;
uniform mat4 mvp;

void main(void) 
{
    gl_Position = mvp*vec4(attr_position,1.0);
    textureCoord = attr_textureCoord;
}
"""

FRAGMENT_SHADER = """
#version 400

in vec2 textureCoord;
out vec4 color;
uniform sampler2D textureSlot;

void main(void) 
{
    color = texture(textureSlot,textureCoord);
}
"""

class Quadrado:

    def __init__(self):
        position = array('f',[
            -1.0, -1.0, 0.0,
            1.0, -1.0, 0.0,
            1.0,  1.0, 0.0,
            -1.0, 1.0, 0.0
        ])

        textcoord = array('f',[
            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0
        ])

        index = array('H',[
            0, 1, 2,
            0, 2, 3
        ])

        self.VAO = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.VAO)

        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)

        VBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize, ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

        VBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(textcoord)*textcoord.itemsize, ctypes.c_void_p(textcoord.buffer_info()[0]), GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(1,2,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

        VBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, VBO)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, len(index)*index.itemsize, ctypes.c_void_p(index.buffer_info()[0]), GL.GL_STATIC_DRAW)
        self.indexLength = len(index)

    def draw(self):
        GL.glBindVertexArray(self.VAO)
        GL.glDrawElements(GL.GL_TRIANGLES,self.indexLength,GL.GL_UNSIGNED_SHORT,ctypes.c_void_p(0))

class QuadradoBranco(App):

    def setup(self):
        self.projection = glm.perspective(math.pi/4,800/600,0.1,100)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)
        self.shader = Shader(VERTEX_SHADER,FRAGMENT_SHADER)
        self.mesh = Quadrado()

        GL.glActiveTexture(GL.GL_TEXTURE0)
        self.loadTexture("uv_grid_opengl.png")

    def onResize(self, width, height):
        self.projection = glm.perspective(math.pi/4,width/height,0.1,100)

    def draw(self):
        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        camera = glm.lookAt(glm.vec3(0,0,3),glm.vec3(0,0,0),glm.vec3(0,1,0))
        mvp = self.projection * camera
        self.shader.useProgram()
        self.shader.setTextureSlot(0)
        self.shader.setMat4("mvp",mvp)
        self.mesh.draw()

if __name__ == "__main__":
    QuadradoBranco()
