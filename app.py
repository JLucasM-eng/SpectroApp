#import libs


import streamlit as st
import librosa
import matplotlib.pyplot as plt
import numpy as np 
import librosa.display
from PIL import Image
from scipy.io.wavfile import write
import sounddevice


import parselmouth
import seaborn as sns


if "dynamic_range" not in st.session_state:
    st.session_state['dynamic_range'] = 70

if "pitch.ceiling" not in st.session_state:
    st.session_state['pitch.ceiling'] = 0


def draw_spectrogram(spectrogram,dynamic_range=st.session_state['dynamic_range']):
    fig = plt.figure(figsize=(16,7))
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap=cmap_option)
    plt.ylim([spectrogram.ymin, spectrogram.ymax])
    plt.xlabel("time [s]")
    plt.ylabel("frequency [Hz]")
    plt.colorbar(format='%2.0f db')
    
def draw_pitch(pitch):
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
    plt.grid(False)
    plt.ylim(0, pitch.ceiling + st.session_state['pitch.ceiling'])
    plt.ylabel("fundamental frequency [Hz]")



##LAYOUT==================================================================


st.sidebar.title("Upload de arquivo")

uploaded_file = st.sidebar.file_uploader("Upload your input Audio file", type=["wav"])


st.sidebar.title("Gravar arquivo de áudio")

#Configurações para gravação do áudio=================

time_duration = st.sidebar.number_input('Informe o tempo de gravação (sec) que deseja realizar:',step=1,min_value=0,value=5)
tooltip_text_fs = 'Número de amostras de sinal por segundo'
st.session_state['freq_amostragem'] = st.sidebar.number_input('Informe a frequencia de amostragem desejada', value=44100,min_value = 0,help=tooltip_text_fs)

gravar = st.sidebar.button("Gravar áudio")

#===============================


if gravar|('audio_gravado' in st.session_state):
    apagargravacao = st.sidebar.button("Apagar áudio gravado")
    
    if apagargravacao:
        if "audio_gravado" in st.session_state :
            del st.session_state["audio_gravado"]
            if "notFoundImageBool" in st.session_state :
                del st.session_state["notFoundImageBool"]
            gravar = False
        


st.sidebar.title("Configurações e parâmetros")



showPlay = st.sidebar.checkbox('Visualizar player de áudio')
showWave = st.sidebar.checkbox('Visualizar Waveform')


cmap_option = st.sidebar.selectbox('Mapa de cores do espectrograma',('magma','jet','gray_r','afmhot'))

notFoundImage = Image.open(r"C:\Users\jose-\OneDrive\Documentos\Faculdade\IC\new ic\python-projects\streamlitApp\utils\notFound.png")

config_avancada = st.sidebar.checkbox('Mostrar configurações avançadas')

if "freq_amostragem" not in st.session_state:
    st.session_state['freq_amostragem'] = 44100


if "comp_janela" not in st.session_state:
    st.session_state['comp_janela'] = 0.01

if "max_freq" not in st.session_state:
    st.session_state['max_freq'] = 8000




if config_avancada:

    st.session_state['comp_janela'] = st.sidebar.number_input('Informe o comprimento de janela desejado', value=0.01,min_value = 0.00000, step=0.001,format='%e')

    tooltip_text_dr = 'Intervalo em que os sinais de força mínima a máxima podem ser detectados e medidos antes que artefatos indesejados apareçam acima do nível de ruído.'
    st.session_state['dynamic_range'] = st.sidebar.slider('Faixa dinâmica', value=70,min_value = 50,help=tooltip_text_dr)

    st.session_state['max_freq'] = st.sidebar.number_input('Frequência máxima do Espectrograma', value=8000,min_value = 0, step=1000)

    tooltip_text_pc = 'Informe em quanto você deseja aumentar ou diminuir a escala do pitch.'
    st.session_state['pitch.ceiling'] = st.sidebar.number_input('Aterar frequência máxima (Pitch) em:', value=0,min_value = -600, step=100,help=tooltip_text_pc)



#==========================================================================
sr = 0
y = []

if uploaded_file is None and gravar == False:
    if "notFoundImageBool" in st.session_state:
        del st.session_state["notFoundImageBool"]

#Carregando o audio 
#=========================================================================
if gravar:
    
    st.session_state.notFoundImageBool = False
    st.session_state['audio_gravado']=True
    notFoundImageBool = False

    uploaded_file = None
    
    print("Recording...")
    recording = sounddevice.rec(int(time_duration*st.session_state['freq_amostragem']),samplerate=st.session_state['freq_amostragem'],channels=2)
    with st.spinner('Gravando...'):
        sounddevice.wait()

    print("Done!")
    write("output.wav",st.session_state['freq_amostragem'],recording)



    sns.set() 

    snd = parselmouth.Sound("output.wav")


    plt.figure(figsize=(18,7))
    

        
    st.title("Resultado | Espectrograma")
    st.header("Informações:")
    st.write("Taxa de amostragem utilizada: ",st.session_state['freq_amostragem'])
    st.write("Comprimento da janela: ",st.session_state['comp_janela'])
    


    pitch = snd.to_pitch()
    pre_emphasized_snd = snd.copy()
    pre_emphasized_snd.pre_emphasize()
    spectrogram = pre_emphasized_snd.to_spectrogram(window_length=st.session_state['comp_janela'], maximum_frequency=st.session_state['max_freq'])
    plt.figure()
    draw_spectrogram(spectrogram)
    plt.twinx()
    draw_pitch(pitch)
    plt.xlim([snd.xmin, snd.xmax])
    
    #----------------------------------------------
    
    
    
    st.pyplot(plt)
        
        
    
    if showWave:
        st.warning('Esta visualização ainda se está em fase de desenvolvimento')
        plt.figure()
        plt.plot(snd.xs(), snd.values.T,linewidth=0.5)
        plt.xlim([snd.xmin, snd.xmax])

        plt.xlabel("time [s]")
        plt.ylabel("amplitude",fontsize=8)

        
        st.pyplot(plt)


    if showPlay:
        st.title("Resultado | Espectrograma")
        st.header("Informações:")
        st.write("Taxa de amostragem utilizada: ",st.session_state['freq_amostragem'])
        st.write("Comprimento da janela: ",st.session_state['comp_janela'])

        st.audio('output.wav', format="audio/wav", start_time=0)
elif 'audio_gravado' in st.session_state:


    plt.figure(figsize=(18,7))
    


    sns.set() 

    snd = parselmouth.Sound("output.wav")
    #========================================================

    st.title("Resultado | Espectrograma")
    st.header("Informações:")
    st.write("Taxa de amostragem utilizada: ",st.session_state['freq_amostragem'])
    st.write("Comprimento da janela: ",st.session_state['comp_janela'])



    pitch = snd.to_pitch()
    pre_emphasized_snd = snd.copy()
    pre_emphasized_snd.pre_emphasize()
    spectrogram = pre_emphasized_snd.to_spectrogram(window_length=st.session_state['comp_janela'], maximum_frequency=st.session_state['max_freq'])
    plt.figure()
    draw_spectrogram(spectrogram)
    plt.twinx()
    draw_pitch(pitch)
    plt.xlim([snd.xmin, snd.xmax])

    #----------------------------------------------

    
    st.pyplot(plt)
    
    if showWave:
        st.warning('Esta visualização ainda se está em fase de desenvolvimento')
        plt.figure()
        plt.plot(snd.xs(), snd.values.T,linewidth=0.5)
        plt.xlim([snd.xmin, snd.xmax])

        plt.xlabel("time [s]")
        plt.ylabel("amplitude",fontsize=8)
        
        st.pyplot(plt)


    if showPlay:
        st.audio('output.wav', format="audio/wav", start_time=0)

if uploaded_file is not None:



    with open(uploaded_file.name,'wb') as f:
        f.write(uploaded_file.getbuffer())
    string = '"'+uploaded_file.name+'"'
    
    #========================================
    
    if "notFoundImageBool" in st.session_state:
            del st.session_state["notFoundImageBool"]
    st.session_state['upload_file'] = True
    if "audio_gravado" in st.session_state:
        st.session_state['audio_gravado']=False
        del st.session_state["audio_gravado"]
        gravar = False
    st.session_state.notFoundImageBool = False
    #==========================================================================

    st.title("Resultado | Espectrograma")
    st.header("Informações:")
    st.write("Taxa de amostragem utilizada: ",st.session_state['freq_amostragem'])
    st.write("Comprimento da janela: ",st.session_state['comp_janela'])


    sns.set() 
    
    snd = parselmouth.Sound(uploaded_file.name)
    #========================================================



    pitch = snd.to_pitch()
    pre_emphasized_snd = snd.copy()
    pre_emphasized_snd.pre_emphasize()
    spectrogram = pre_emphasized_snd.to_spectrogram(window_length=st.session_state['comp_janela'],  maximum_frequency=st.session_state['max_freq'])
    plt.figure()
    draw_spectrogram(spectrogram)
    plt.twinx()
    draw_pitch(pitch)
    plt.xlim([snd.xmin, snd.xmax])

#----------------------------------------------

    st.pyplot(plt)
    
    if showWave:
      
        st.warning('Esta visualização ainda se está em fase de desenvolvimento')

        plt.figure()
        plt.plot(snd.xs(), snd.values.T,linewidth=0.5)
        plt.xlim([snd.xmin, snd.xmax])
       
        plt.xlabel("time [s]")
        plt.ylabel("amplitude",fontsize=8)

        
        st.pyplot(plt)

            

    if showPlay:
        st.audio(uploaded_file, format="audio/wav", start_time=0)
    
elif uploaded_file is None and 'notFoundImageBool' not in st.session_state and 'audio_gravado' not in st.session_state:
    st.title("EspectroApp")
    st.write("Faça upload do seu arquivo de áudio .wav ou grave agora mesmo o áudio à ser analisado. Realize análises de maneira simples e precisa.")
    st.image(notFoundImage, caption='File not found')
