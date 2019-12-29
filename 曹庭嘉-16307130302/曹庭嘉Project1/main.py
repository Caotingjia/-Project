import warnings
warnings.simplefilter("ignore", DeprecationWarning)#防止报警告
import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import sys

fig = plt.figure(figsize=(8, 3))

ax = p3.Axes3D(fig)
ax.invert_xaxis()
ax.invert_yaxis()

N = 5

_x = np.arange(20)
_y = np.arange(20)
_xx, _yy = np.meshgrid(_x, _y)
x, y = _xx.ravel(), _yy.ravel()
top = x+y
bottom = np.zeros_like(top)
width = depth = 1

CHUNK = 1024

wf = wave.open("Adrian Belew-Piper.wav", 'rb')


p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)


data = wf.readframes(CHUNK)


i=0
collection_l = []


top = x+y

line=[ax.plot(x, y, top, color='coral',  linestyle=':', marker='_')[0]]

# plt.show()
def animate(fi, line):

    global stream
    global data
    if data=='':
        stream.stop_stream()
        stream.close()
        p.terminate()
        line.set_data(x, y)
        line.set_3d_properties([0]*400)
        sys.exit(1)
    else:

        stream.write(data)  
        data = wf.readframes(CHUNK)  
        numpydata = np.fromstring(data, dtype=np.int16)  
        if numpydata.shape[0] == 0:
            stream.stop_stream()
            stream.close()
            p.terminate()
            line.set_data(x, y)
            line.set_3d_properties([0] * 400)
            sys.exit(1)



        else:
            transforamed = np.real(np.fft.fft(numpydata))  
            count = 5  
            collection = []
            for n in range(0, transforamed.size, count):  
                hight = abs(int(transforamed[n] / 10000))  
                collection.append(hight)

            collection = collection[1:-1]

            if len(collection) == 0:
                stream.stop_stream()
                stream.close()
                p.terminate()
                line.set_data(x, y)
                line.set_3d_properties([0] * 400)
                sys.exit(1)


            if len(collection) < 400:
                diff = 400 - len(collection)
                a = diff // 2
                b = diff - a
                collection = [0]*a + collection + [0]*b
            else:
                diff = len(collection) - 400
                a = diff // 2
                b = diff - a
                collection = collection[a:-b]


            ax.set_zlim(0, max(collection) + 3)
            for i in range(20):
                collection[i*20] = 0
                collection[i*20 - 1] = 0
            line.set_data(x, y)
            line.set_3d_properties(collection)

            return line



anim = animation.FuncAnimation(fig, animate, frames=1000000000, interval=1, fargs = (line),repeat=False)

plt.axis('off')
plt.legend(loc='upper left')

plt.show()

