from OpenGL import GL
import glm
import math
from glApp import *

VERTEX_SHADER = """
#version 400

layout (location=0) in vec3 attr_position;
layout (location=1) in vec3 attr_normal;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

out vec3 normal;
out vec3 fragCoord;

void main(void) 
{
    gl_Position = projection * view * model * vec4(attr_position,1.0);
    normal = mat3(transpose(inverse(model))) * attr_normal;
    fragCoord = vec3(model*vec4(attr_position,1.0));
}
"""

FRAGMENT_SHADER = """
#version 400

in vec3 normal;
in vec3 fragCoord;
out vec4 color;

uniform vec3 cameraPos;

void main(void) 
{
    float ambientCoef = 0.1;
    vec3 lightPosition = vec3(0,5,5);
    vec4 lightColor = vec4(1.0,1.0,1.0,1.0);
    vec4 objectColor = vec4(1.0,0.0,0.0,1.0);

    vec3 norm = normalize(normal);
    vec3 lightDir = normalize(lightPosition - fragCoord);
    float difuseCoef = max(dot(lightDir,norm),0.0);

    vec3 cameraDir = normalize(cameraPos-fragCoord);
    vec3 reflectionDir = reflect(-lightDir,norm);
    float specularCoef = 0.5*pow(max(dot(cameraDir,reflectionDir),0.0),256);

    color = (ambientCoef+(difuseCoef*lightColor)+(specularCoef*lightColor))*objectColor;
}
"""

class EsferaApp(App):

    def setup(self):
        self.projection = glm.perspective(math.pi/4,800/600,0.1,100)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)
        self.shader = Shader(VERTEX_SHADER,FRAGMENT_SHADER)
        self.mesh = Thorus()
        self.a = 0

    def onResize(self, width, height):
        self.projection = glm.perspective(math.pi/4,width/height,0.1,100)

    def draw(self):
        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        self.shader.useProgram()
        cameraPos = glm.vec3(0,0,5)
        view = glm.lookAt(cameraPos,glm.vec3(0,0,0),glm.vec3(0,1,0))
        model = glm.rotate(self.a,glm.vec3(1,0,1))

        self.shader.setMat4("model",model)
        self.shader.setMat4("view",view)
        self.shader.setMat4("projection",self.projection)
        self.shader.setVec3("cameraPos",cameraPos)
        self.mesh.draw()

        self.a += 0.005

if __name__ == "__main__":
    EsferaApp()
