from OpenGL import GL
from array import array
import glfw
import glm
import ctypes 
import math
from PIL import Image

def compilaShaders(VERTEX_SHADER, FRAGMENT_SHADER):
    error = None
    progId = GL.glCreateProgram()
    for type, source in [ (GL.GL_VERTEX_SHADER, VERTEX_SHADER), (GL.GL_FRAGMENT_SHADER, FRAGMENT_SHADER) ]:
        shaderId = GL.glCreateShader(type)
        GL.glShaderSource(shaderId,[source])
        GL.glCompileShader(shaderId)
        status = GL.glGetShaderiv(shaderId,GL.GL_COMPILE_STATUS)
        if not status:
            error = GL.glGetShaderInfoLog(shaderId)
            GL.glDeleteShader(shaderId)
            break
        else:
            GL.glAttachShader(progId,shaderId)
    if error == None:
        GL.glLinkProgram(progId)
        status = GL.glGetProgramiv(progId,GL.GL_LINK_STATUS)
        if not status:
            error = GL.glGetProgramInfoLog(progId)
        else:
            return progId
    for shaderId in GL.glGetAttachedShaders(progId):
        GL.glDetachShader(progId, shaderId)
        GL.glDeleteShader(shaderId)
    GL.glDeleteProgram(progId)
    raise Exception(error)

class Shader:

    def __init__(self,vertexShader,fragmentShader):
        self.progId = compilaShaders(vertexShader,fragmentShader)

    def useProgram(self):
        GL.glUseProgram(self.progId)

    def setMat4(self,name,value):
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.progId,name),1,GL.GL_FALSE,glm.value_ptr(value))

    def setTextureSlot(self, slot):
        GL.glUniform1i(GL.glGetUniformLocation(self.progId, "textureSlot"),slot)


class App:

    def __init__(self, title="Open GL Application", width=800, height=600):
        if not glfw.init():
            return
        
        def windowSizeCallback(window, width, height):
            GL.glViewport(0,0,width,height)
            self.onResize(width,height)

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.SAMPLES, 4)
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            return
        glfw.make_context_current(self.window)
        self.setup()
        glfw.set_window_size_callback(self.window,windowSizeCallback)
        while not glfw.window_should_close(self.window):
            self.draw()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()

    def onResize(self, width, height):
        print(f"{width} x {height}")
    
    def setup(self):
        pass

    def draw(self):
        pass

    def loadTexture(self, filename):
        im = Image.open(filename)
        w, h = im.size
        if(im.mode == "RGBA"):
            modo = GL.GL_RGBA
            data = im.tobytes("raw", "RGBA", 0, -1)
        else:
            modo = GL.GL_RGB
            data = im.tobytes("raw", "RGB", 0, -1)
        textureId = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, textureId)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, modo, w, h, 0, modo,GL. GL_UNSIGNED_BYTE, data)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        return textureId


class GridMesh:

    def __init__(self, N=40, M=40):
        self.N = N
        self.M = M
        self.VAO = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.VAO)
        self.computePosition()
        self.computeIndex()

    def computePosition(self, attrIndex=0):
        N = self.N
        M = self.M
        position = array('f')
        for i in range(N):
            u = i/(N-1)
            for j in range(M):
                v = j/(M-1)
                x, y, z = self.f(u,v)
                position.append(x)
                position.append(y)
                position.append(z)
        self.attrBufferData(attrIndex, position)

    def computeIndex(self):
        N = self.N
        M = self.M
        index = array('H')
        for i in range(N-1):
            if i>0:
                index.append(i*M)
                index.append(i*M)
            for j in range(M):
                index.append(i*M+j)
                index.append((i+1)*M+j)
            index.append((i+1)*M+M-1)

        VBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, VBO)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, len(index)*index.itemsize, ctypes.c_void_p(index.buffer_info()[0]), GL.GL_STATIC_DRAW)
        self.indexLength = len(index)

    def attrBufferData(self, attrIndex, data, size=3, type=GL.GL_FLOAT):
        GL.glBindVertexArray(self.VAO)
        GL.glEnableVertexAttribArray(attrIndex)
        VBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(data)*data.itemsize, ctypes.c_void_p(data.buffer_info()[0]), GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(0,size,type,GL.GL_FALSE,0,ctypes.c_void_p(0))

    def f(self, u, v):
        return u*5, v*5, 0

    def draw(self):
        GL.glBindVertexArray(self.VAO)
        GL.glDrawElements(GL.GL_LINE_STRIP,self.indexLength,GL.GL_UNSIGNED_SHORT,ctypes.c_void_p(0))
        #GL.glDrawElements(GL.GL_TRIANGLE_STRIP,self.indexLength,GL.GL_UNSIGNED_SHORT,ctypes.c_void_p(0))

class Thorus(GridMesh):

    def __init__(self, R=0.5, a=1.5, N=30, M=30):
        self.R = R
        self.a = a
        super().__init__(N, M)

    def f(self,u,v):
        R = self.R
        a = self.a
        theta = u*2*math.pi
        phi = v*2*math.pi
        x = (a+R*math.cos(theta))*math.cos(phi)
        y = R*math.sin(theta)
        z = (a+R*math.cos(theta))*math.sin(phi)
        return x, y, z

class Sphere(GridMesh):

    def __init__(self, R=1.0, N=30, M=30):
        self.R = R
        super().__init__(N, M)

    def f(self,u,v):
        R = self.R
        theta = u*math.pi-math.pi/2
        phi = v*2*math.pi
        x = R*math.cos(theta)*math.cos(phi)
        y = R*math.sin(theta)
        z = R*math.cos(theta)*math.sin(phi)
        return x, y, z

class Cylinder(GridMesh):

    def __init__(self, R=1.0, H=2.0, N=30, M=30):
        self.R = R
        self.H = H
        super().__init__(N, M)

    def f(self,u,v):
        R = self.R
        H = self.H
        phi = v*2*math.pi
        x = R*math.cos(phi)
        y = u*H
        z = R*math.sin(phi)
        return x, y, z

class Cone(GridMesh):

    def __init__(self, R=1.0, H=2.0, N=30, M=30):
        self.R = R
        self.H = H
        super().__init__(N, M)

    def f(self,u,v):
        R = self.R
        H = self.H
        phi = v*2*math.pi
        x = (1-u)*R*math.cos(phi)
        y = u*H
        z = (1-u)*R*math.sin(phi)
        return x, y, z

class ConeFrustum(GridMesh):

    def __init__(self, R1=1.0, R2=0.5, H=2, N=30, M=30):
        self.R1 = R1
        self.R2 = R2
        self.H = H
        super().__init__(N, M)

    def f(self,u,v):
        R = (1-u)*(self.R1-self.R2)+self.R2 
        H = self.H
        phi = v*2*math.pi
        x = R*math.cos(phi)
        y = u*H
        z = R*math.sin(phi)
        return x, y, z

class Disk(GridMesh):

    def __init__(self, R1=1.0, R2=2.5, M=30):
        self.R1 = R1
        self.R2 = R2
        super().__init__(2, M)

    def f(self,u,v):
        R = (1-u)*(self.R1-self.R2)+self.R2 
        phi = v*2*math.pi
        x = R*math.cos(phi)
        y = 0
        z = R*math.sin(phi)
        return x, y, z

class Circle(GridMesh):

    def __init__(self, R=1.0, N=2, M=30):
        self.R = R
        super().__init__(N, M)

    def f(self,u,v):
        R = self.R 
        phi = v*2*math.pi
        x = R*math.cos(phi)
        y = 0
        z = R*math.sin(phi)
        return x, y, z


class Paraboloid(GridMesh):

    def __init__(self, R=1.0, N=30, M=30):
        self.R = R
        super().__init__(N, M)

    def f(self,u,v):
        R = self.R*u
        phi = v*2*math.pi
        x = R*math.cos(phi)
        y = R*R
        z = R*math.sin(phi)
        return x, y, z

class Paraboloid2(GridMesh):

    def __init__(self, x0=-2, y0=-2, xf=2, yf=2, N=30, M=30):
        self.x0 = x0
        self.y0 = y0
        self.rangeX = xf-x0
        self.rangeY = yf-y0
        super().__init__(N, M)

    def f(self,u,v):
        x = v*self.rangeX+self.x0
        y = u*self.rangeY+self.y0
        z = x**2+y**2
        return x, y, z