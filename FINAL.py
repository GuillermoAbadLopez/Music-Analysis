import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

filename= "guitarra.wav"
file=wave.open(filename)

S_rate = file.getframerate()
n_frames = file.getnframes()
n_channels = file.getnchannels()
print("numero de frames:",n_frames)
print("numero de canales:",n_channels)
print("frequencia de grabación",S_rate)

data = file.readframes(n_frames)
w_data = np.frombuffer(data, np.int16)
w_data.shape = -1 , n_channels 
w_data = w_data.T
print(w_data)

abs_data = abs(w_data)
print(abs_data)

final_data=[]
final_data.append(abs_data[0][0])

#ENVOLVENT
c=0
n=100.0      #Mas precisa la envolvente "100" o menos precisa "0.1" [SOLO usar potencias de 10!]
data_stored=0
for i in range(n_frames-1):
    if c < S_rate/n:    
        c=c+1
        if abs_data[0][i] > data_stored:
            data_stored = abs_data[0][i]
    else:
        c=0
        final_data.append(data_stored)
        data_stored=0
        
        
        
media = np.mean (final_data)
media_o = np.mean (abs_data)
devest = np.std (final_data) 
devest_o= np.std (abs_data) 
fluctuaciones=devest/media
fluctuaciones_o=devest_o/media_o
print("ORIGINAL")
print("Media:",media_o)
print("Variación:",devest_o)
print("Fluctuaciones:",fluctuaciones_o)

print("LIMPIA")
print("Media:",media)
print("Variación:",devest)
print("Fluctuaciones:",fluctuaciones)



duration = 1/float(S_rate)
t_seq = np.arange (0, n_frames / float(S_rate), duration)
plt.plot(t_seq,w_data[0])   #abs_data[0/1] valor absoluto solo /// w_data[0/1] oscilación completa

t_seq = np.arange (0,len(final_data)/n, 1/n)
plt.plot(t_seq,final_data)      #Solo teninedo en cuenta los màximos relativos!!!

plt.show()



#FOURIER TRANSFORMATION
y = fft(w_data)
x = np.linspace(0.0, 2*S_rate/10, n_frames//20)
plt.plot(x, 2.0/n_frames * np.abs(y[0][0:n_frames//20]))
plt.grid()
plt.show()

mitja=0
denominador=0 #Denominador per normalitzar la mitja!
Sensibilitat=1/8 #Per fer la mitjana agafem nomes les frequencies amb amplitud superior a Sensibilitat * la maxima amplitud
maximum=max(np.abs(y[0]))
for i in range(n_frames//20):
    if y[0][i] > maximum*Sensibilitat:
        mitja=mitja + x[i]*np.abs(y[0][i])
        denominador = denominador+np.abs(y[0][i])
mitja=mitja/denominador  #Normalitzem
position=np.where(np.abs(y[0])==max(np.abs(y[0])))
print("frequencia mitja:", mitja)
print("frequencia moda:", x[position[0][0]])
    

