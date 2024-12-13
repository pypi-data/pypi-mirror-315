import os 
import sys
import pandas as pd
#sys.path.append(r'./LDP')
#from LDP.functions import signal_upload
import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt

def signal_upload(signal_path, PP=True):

  '''
  Function created to upload a signal from a csv file to the enviroment of 
  work, saving it in a pandas DataFrame and then in a numpy array. In this 
  function, to all the channels is substracted Fcz channel that works as 
  a reference. Then the raw signal is plotted.

  Input: signal_path --> str (path where the csv file is located with the data)

         subject --> str (code of identification of the subject)

         electrodes --> list (contains the names of the electrodes used in the recording)
         

  Output: vision_signal --> Numpy array (array with the uploaded signal)

          signals_marks --> Numpy array (array where the marks are located)
  '''
  if PP:
     
    signal=pd.read_csv(signal_path, skiprows=4,sep=',')
    signal.drop(['Sample Index',
                        ' Accel Channel 0',
                        ' Accel Channel 1',
                        ' Accel Channel 2',
                        ' Other', ' Other.1',
                        ' Other.2',' Other.3',
                        ' Other', ' Other.1',
                        ' Other.2', ' Other.3',
                        ' Other.4', ' Other.5',
                        ' Other.6', ' Analog Channel 0',
                        ' Analog Channel 1', ' Analog Channel 2',
                        ' Timestamp', ' Other.7',
                        ' Timestamp (Formatted)'],
                        axis=1,
                        inplace=True)
    
    signal = signal.to_numpy()[5:-5] #Quitando primeras y últimas 5 muestras por el pico al encender el open y el final del registro
    num_channels = signal.shape[1]

  else:
    signal=pd.read_csv(signal_path, skiprows=1,sep=',')
    signal = signal.to_numpy()[5:-5] #Quitando primeras y últimas 5 muestras por el pico al encender el open y el final del registro
    num_channels = signal.shape[1]

  return signal.T
tasks=['CE','ST1','ST2','DTAN','DTF','DTV', 'DTS1','DTS7','DTCT']
#tasks=['CE']
path= r'C:\Users\Luisa\Documents\PROYECTO_PORTABELS\data_tutorial_APPLEE'

# Recorrer todas las carpetas de sujetos
for j in tasks:
    path_save= rf'C:\Users\Luisa\Documents\PROYECTO_PORTABELS\revision_tutorial\{j}'
    os.makedirs(path_save, exist_ok=True)
    count=0
    for subdir in os.listdir(path):
        if subdir.startswith('sub-CTR'):
            # Construir la ruta completa a la carpeta del sujeto
            ruta_sujeto = os.path.join(path, subdir)
            # Construir la ruta completa a la carpeta 'ses-V0' dentro del sujeto
            ruta_sesion = os.path.join(ruta_sujeto, 'ses-V0')
            # Construir la ruta completa a la carpeta 'eeg' dentro de la sesión
            ruta_eeg = os.path.join(ruta_sesion, 'eeg')
            
            
            # Recorrer todos los archivos en la carpeta 'eeg'
            for archivo in os.listdir(ruta_eeg):
                #count=0
                #try:
                if archivo.endswith('_eeg.txt'):
                    if f'_{j}_eeg' in archivo :
                        
                        ruta_archivo = os.path.join(ruta_eeg, archivo)
                        ruta_archivo = ruta_archivo.replace('\\', '/')  # Asegurarse de que la ruta tenga el formato correcto
                        print(ruta_archivo)
                        signal_uploaded = signal_upload(ruta_archivo, PP=False)
                        for i in range(8):
                            #plt.plot(signal_uploaded[i,:])  # Crea una nueva figura para cada plot
                            plt.plot(signal_uploaded[i,:])
                        
                        #plt.show()
                        #plt.title(f'{archivo}')
                        #pdf.savefig()  # Guarda la figura actual en el PDF
                        plt.savefig(f'{path_save}\{archivo}.png')
                        plt.close()
                        count=count+1
    print(f'numero de sujetos para {j}: {count}')
                            #pdf.close()
                    
                # except:
                #     print(f'No existe el archivo {archivo}')