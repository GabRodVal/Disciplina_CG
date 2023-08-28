

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

class Cubo:

    def __init__(self):

        # position = array('f',[
        #     -1.0, -1.0, 0.0,
        #     1.0, -1.0, 0.0,
        #     1.0,  1.0, 0.0,
        #     -1.0, 1.0, 0.0
        # ])

        position = array('f',[
            -1.0, -1.0,  1.0, # 0
            1.0, -1.0,  1.0, # 1
            1.0,  1.0,  1.0, # 2
            -1.0,  1.0,  1.0, # 3
            1.0, -1.0, -1.0, # 4
            -1.0, -1.0, -1.0, # 5
            -1.0,  1.0, -1.0, # 6
            1.0,  1.0, -1.0,  # 7

            -1.0, -1.0,  1.0, # 8
            1.0, -1.0,  1.0, # 9
            1.0,  1.0,  1.0, # 10
            -1.0,  1.0,  1.0, # 11
            1.0, -1.0, -1.0, # 12
            -1.0, -1.0, -1.0, # 13
            -1.0,  1.0, -1.0, # 14
            1.0,  1.0, -1.0,  # 15

            -1.0, -1.0,  1.0, # 16
            1.0, -1.0,  1.0, # 17
            1.0,  1.0,  1.0, # 18
            -1.0,  1.0,  1.0, # 19
            1.0, -1.0, -1.0, # 20
            -1.0, -1.0, -1.0, # 21
            -1.0,  1.0, -1.0, # 22
            1.0,  1.0, -1.0,  # 23
        ])

        # textcoord = array('f',[
        #      0.0, 0.0,
        #      1.0, 0.0,
        #      1.0, 1.0,
        #      0.0, 1.0
        #  ])

        textcoord = array('f',[
              0.0, 0.5, #1
              1/3 , 0.5,
              1/3, 1.0,
              0.0, 1.0,

              2/3, 0.0, #6
              1.0, 0.0,
              1.0, 0.5,
              2/3, 0.5,

              #2/5
              2/3, 0.5,
              1/3, 0.0,
              1/3, 0.5,
              2/3, 1.0,
              2/3, 0.0,
              1/3, 0.5,
              1/3, 1.0,
              2/3, 0.5,

              #3/4

              1/3, 0.0,
              0.0, 0.0,
              1.0, 0.5,
              2/3, 0.5,
              0.0, 0.5,
              1/3, 0.5,
              2/3, 1.0,
              1.0, 1.0





            #   1/3, 0.5, #2
            #   2/3, 0.5,
            #   2/3, 1.0,
            #   1/3, 1.0,

            #   1/3, 0.0, #5
            #   2/3, 0.0,
            #   2/3, 0.5,
            #   1/3, 0.5

          ])


        index = array('H',[
            0, 1, 2, 0, 2, 3, #1
            4, 5, 6, 4, 6, 7,#6

            9, 12, 15, 9, 15, 10, #2
            8, 13, 14, 8, 14, 11,  #5



            19, 18, 23, 19, 23, 22, #3
            16, 21, 20, 16, 20, 17  #4
        ])

        # index = array('H',[
        #     0, 1, 2,
        #     0, 2, 3
        # ])

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

class Dado(App):

    def setup(self):
        self.projection = glm.perspective(math.pi/4,800/600,0.1,100)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)
        self.shader = Shader(VERTEX_SHADER,FRAGMENT_SHADER)
        self.mesh = Cubo()
        self.a = 0

        GL.glActiveTexture(GL.GL_TEXTURE0)
        self.loadTexture("dado.png")

    def onResize(self, width, height):
        self.projection = glm.perspective(math.pi/4,width/height,0.1,100)

    def draw(self):
        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        camera = glm.lookAt(glm.vec3(0,2,6),glm.vec3(0,0,0),glm.vec3(0,1,0))
        model = glm.rotate(self.a,glm.vec3(0.5,1,0.5))
        mvp = self.projection * camera * model
        self.shader.useProgram()
        self.shader.setMat4("mvp",mvp)
        self.mesh.draw()
        self.a += 0.02

if __name__ == "__main__":
    Dado()
