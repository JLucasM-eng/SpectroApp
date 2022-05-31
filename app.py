#import libs

import wave
import streamlit as st
import librosa
import matplotlib.pyplot as plt #Que tenta replicar os plots do matlab
import numpy as np #para o topico de senoides no python
import librosa.display
from PIL import Image
import time
# importar bibliotecas necessárias
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
#import pyaudio

import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic

import sounddevice
from scipy.io.wavfile import write



#"st.session_state object", st.session_state

#st.session_state.notFoundImageBool = True
#st.session_state['audio_gravado']=False
#st.session_state['upload_file']=False

##LAYOUT==================================================================

st.title("Espectrograma")
#st.beta_set_page_config(page_title='EspectroApp', page_icon = 'utils/pngTeste.ico', layout = 'wide', initial_sidebar_state = 'auto')
st.sidebar.title("Upload de arquivo")

uploaded_file = st.sidebar.file_uploader("Upload your input Audio file", type=["wav","ogg"])

st.sidebar.title("Gravar arquivo de áudio")

gravar = st.sidebar.button("Gravar áudio")
#apagargravacao = True
if gravar|('audio_gravado' in st.session_state):
    apagargravacao = st.sidebar.button("Apagar áudio gravado")
    if apagargravacao:
        if "audio_gravado" in st.session_state:
            del st.session_state["audio_gravado"]
            del st.session_state["notFoundImageBool"]
            gravar = False



showPlay = st.sidebar.checkbox('Visualizar player de áudio')
showWave = st.sidebar.checkbox('Visualizar Waveform')

st.sidebar.title("Configurações e parâmetros")
#width_figure_value = st.sidebar.number_input('Largura da imagem',min_value=18)
#height_figure_value = st.sidebar.number_input('Largura da imagem',min_value=2)

cmap_option = st.sidebar.selectbox('Tema do espectrograma',('magma','jet','gray_r'))

axisScale = st.sidebar.selectbox('Escala do eixo y',('log','linear'))
notFoundImage = Image.open(r"C:\Users\jose-\OneDrive\Documentos\Faculdade\IC\new ic\python-projects\streamlitApp\utils\notFound.png")

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
    fps = 44100
    duration = 10
    print("Recording...")
    recording = sounddevice.rec(int(duration*fps),samplerate=fps,channels=2)
    with st.spinner('Gravando...'):
        sounddevice.wait()

    print("Done!")
    write("output.wav",fps,recording)

    signal = basic.SignalObj("output.wav")
    pitch = pYAAPT.yaapt(signal)
    #
    y, sr = librosa.load("output.wav",mono=True,sr=44100)
    st.session_state['audio_gravado_file'] = y
        #print("Caiu no if",uploaded_file.name)
        #audio_file = open(y, 'rb')
        #audio_bytes = audio_file.read()
        #st.audio(audio_file, format='audio/ogg')
    fs = 44100 # Frequencia de amostragem
        #y, sr = librosa.load(fname,mono=True,sr=44100)
    S = librosa.stft(st.session_state['audio_gravado_file'],n_fft=2048, win_length=2048)#hop_length=200

    S = np.abs(S)
    plt.figure(figsize=(18,7))
    
    #plt.plot(pitch.samp_values, label='samp_values', color='blue')
    #plt.plot(pitch.samp_interp, label='samp_interp', color='green')
    T = librosa.amplitude_to_db(S,ref=np.max)

    if not showWave:
        
        librosa.display.specshow(T,y_axis=axisScale,x_axis='time',sr=fs,cmap=cmap_option)
        plt.xlabel('Time[s]')
        plt.ylabel('Frequency [ Hz ]')
        plt.colorbar(format='%2.0f db')
        st.pyplot(plt)
    
    if showWave:
        fig, (ax, ax2) = plt.subplots(nrows=2, sharex=True)
        librosa.display.specshow(T,y_axis=axisScale,x_axis='time',sr=fs,cmap=cmap_option,ax=ax )
        librosa.display.waveshow(y, sr=sr, alpha=0.5, ax=ax2)
        #ax.set_xlabel('Time[s]')
        #plt.set_ylabel('Frequency [ Hz ]')
        st.pyplot(fig)

    if showPlay:
        st.audio(uploaded_file, format="audio/wav", start_time=0)
elif 'audio_gravado' in st.session_state:

    signal = basic.SignalObj("output.wav")
    pitch = pYAAPT.yaapt(signal)
    #
    y, sr = librosa.load("output.wav",mono=True,sr=44100)
   
        #print("Caiu no if",uploaded_file.name)
        #audio_file = open(y, 'rb')
        #audio_bytes = audio_file.read()
        #st.audio(audio_file, format='audio/ogg')
    fs = 44100 # Frequencia de amostragem
        #y, sr = librosa.load(fname,mono=True,sr=44100)
    S = librosa.stft(y,n_fft=2048, win_length=2048)#hop_length=200

    S = np.abs(S)
    plt.figure(figsize=(18,7))
    
    #plt.plot(pitch.samp_values, label='samp_values', color='blue')
    #plt.plot(pitch.samp_interp, label='samp_interp', color='green')
    T = librosa.amplitude_to_db(S,ref=np.max)

    if not showWave:
        
        librosa.display.specshow(T,y_axis=axisScale,x_axis='time',sr=fs,cmap=cmap_option)
        plt.xlabel('Time[s]')
        plt.ylabel('Frequency [ Hz ]')
        plt.colorbar(format='%2.0f db')
        st.pyplot(plt)
    
    if showWave:
        fig, (ax, ax2) = plt.subplots(nrows=2, sharex=True)
        librosa.display.specshow(T,y_axis=axisScale,x_axis='time',sr=fs,cmap=cmap_option,ax=ax )
        librosa.display.waveshow(y, sr=sr, alpha=0.5, ax=ax2)
        #ax.set_xlabel('Time[s]')
        #plt.set_ylabel('Frequency [ Hz ]')
        st.pyplot(fig)

    if showPlay:
        st.audio('output.wav', format="audio/wav", start_time=0)

if uploaded_file is not None:
    
    if "notFoundImageBool" in st.session_state:
            del st.session_state["notFoundImageBool"]
    st.session_state['upload_file'] = True
    if "audio_gravado" in st.session_state:
        st.session_state['audio_gravado']=False
        del st.session_state["audio_gravado"]
        gravar = False
    st.session_state.notFoundImageBool = False
    #==========================================================================
    signal = basic.SignalObj(uploaded_file)
    pitch = pYAAPT.yaapt(signal)
    #
    y, sr = librosa.load(uploaded_file,mono=True,sr=44100)
        #print("Caiu no if",uploaded_file.name)
        #audio_file = open(y, 'rb')
        #audio_bytes = audio_file.read()
        #st.audio(audio_file, format='audio/ogg')
    fs = 44100 # Frequencia de amostragem
        #y, sr = librosa.load(fname,mono=True,sr=44100)
    S = librosa.stft(y,n_fft=2048, win_length=2048)#hop_length=200

    S = np.abs(S)
    plt.figure(figsize=(18,7))
    
    #plt.plot(pitch.samp_values, label='samp_values', color='blue')
    #plt.plot(pitch.samp_interp, label='samp_interp', color='green')
    T = librosa.amplitude_to_db(S,ref=np.max)

    if not showWave:
        
        librosa.display.specshow(T,y_axis=axisScale,x_axis='time',sr=fs,cmap=cmap_option)
        plt.xlabel('Time[s]')
        plt.ylabel('Frequency [ Hz ]')
        plt.colorbar(format='%2.0f db')
        st.pyplot(plt)
    
    if showWave:
        fig, (ax, ax2) = plt.subplots(nrows=2, sharex=True)
        librosa.display.specshow(T,y_axis=axisScale,x_axis='time',sr=fs,cmap=cmap_option,ax=ax )
        librosa.display.waveshow(y, sr=sr, alpha=0.5, ax=ax2)
        #ax.set_xlabel('Time[s]')
        #plt.set_ylabel('Frequency [ Hz ]')
        st.pyplot(fig)

    if showPlay:
        st.audio(uploaded_file, format="audio/wav", start_time=0)
    
elif uploaded_file is None and 'notFoundImageBool' not in st.session_state:
    
    st.image(notFoundImage, caption='File not found')
