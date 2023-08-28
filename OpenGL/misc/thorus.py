from OpenGL import GL
import glm
import math
from glApp import *

VERTEX_SHADER = """
#version 400

in vec3 attr_posicao;
uniform mat4 mvp;

void main(void) 
{
    gl_Position = mvp * vec4(attr_posicao,1.0f);
}
"""

FRAGMENT_SHADER = """
#version 400

out vec4 color;

void main(void) 
{
    color = vec4(0.2f,0.2f,0.2f,1.0f);
}
"""

class ThorusApp(App):

    def setup(self):
        self.projection = glm.perspective(math.pi/4,800/600,0.1,100)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)
        self.shader = Shader(VERTEX_SHADER,FRAGMENT_SHADER)
        self.mesh = Paraboloid()
        self.a = 0
    
    def onResize(self, width, height):
        self.projection = glm.perspective(math.pi/4,width/height,0.1,100)

    def draw(self):
        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        camera = glm.lookAt(glm.vec3(0,5,10),glm.vec3(0,0,0),glm.vec3(0,1,0))
        model = glm.rotate(self.a,glm.vec3(0,1,1))
        mvp = self.projection * camera * model
        self.shader.useProgram()
        self.shader.setMat4("mvp",mvp)
        self.mesh.draw()
        self.a += 0.005

if __name__ == "__main__":
    ThorusApp()
