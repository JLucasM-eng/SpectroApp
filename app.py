#import libs


import streamlit as st
import librosa
import matplotlib.pyplot as plt
import numpy as np 
import librosa.display
from PIL import Image
from scipy.io.wavfile import write
import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic
import sounddevice





##LAYOUT==================================================================




st.sidebar.title("Upload de arquivo")

uploaded_file = st.sidebar.file_uploader("Upload your input Audio file", type=["wav"])

st.sidebar.title("Gravar arquivo de áudio")

time_duration = st.sidebar.number_input('Informe o tempo de gravação (sec) que deseja realizar:',step=1,min_value=0,value=5)

gravar = st.sidebar.button("Gravar áudio")



if gravar|('audio_gravado' in st.session_state):
    apagargravacao = st.sidebar.button("Apagar áudio gravado")
    #finalizar = st.sidebar.button("Finalizar Gravação")
    if apagargravacao:
        if "audio_gravado" in st.session_state :
            del st.session_state["audio_gravado"]
            if "notFoundImageBool" in st.session_state :
                del st.session_state["notFoundImageBool"]
            gravar = False
        
    #if finalizar:
    #       st.session_state["finalizar_rec"] = True



showPlay = st.sidebar.checkbox('Visualizar player de áudio')
showWave = st.sidebar.checkbox('Visualizar Waveform')
showpitch = st.sidebar.checkbox('Visualizar Pitch')


st.sidebar.title("Configurações e parâmetros")
#width_figure_value = st.sidebar.number_input('Largura da imagem',min_value=18)
#height_figure_value = st.sidebar.number_input('Largura da imagem',min_value=2)

cmap_option = st.sidebar.selectbox('Tema do espectrograma',('magma','jet','gray_r'))

axisScale = st.sidebar.selectbox('Escala do eixo y',('log','linear'))
notFoundImage = Image.open(r"C:\Users\jose-\OneDrive\Documentos\Faculdade\IC\new ic\python-projects\streamlitApp\utils\notFound.png")

config_avancada = st.sidebar.checkbox('Mostrar configurações avançadas')

if "freq_amostragem" not in st.session_state:
    st.session_state['freq_amostragem'] = 44100

if "comp_janela" not in st.session_state:
    st.session_state['comp_janela'] = 2048

if "hop_length" not in st.session_state:
    st.session_state['hop_length'] = 512
if config_avancada:
    tooltip_text_fs = 'Número de amostras de sinal por segundo'
    st.session_state['freq_amostragem'] = st.sidebar.number_input('Informe a frequencia de amostragem desejada', value=44100,min_value = 0,help=tooltip_text_fs)
    
    tooltip_text_ft = 'Número de amostras entre quadros.'
    st.session_state['hop_length'] = st.sidebar.number_input('Informe o número de amostras de áudio entre quadros', value=512,min_value = 0,help=tooltip_text_ft)

    tooltip_text_cj = 'Comprimento com que cada quadro de áudio será janelado, '
    st.session_state['comp_janela'] = st.sidebar.number_input('Informe o comprimento de janela desejada', value=2048,min_value = 0,help=tooltip_text_cj)



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

    signal = basic.SignalObj("output.wav")
    pitch = pYAAPT.yaapt(signal)
    #time_stamp_in_seconds = pitch.frame_pos/signal.fs
    #print("time_stamp_in_seconds",pitch.samp_interp)
    #Carregando o áudio
    y, sr = librosa.load("output.wav",mono=True,sr=st.session_state['freq_amostragem'])
    st.session_state['audio_gravado_file'] = y
    #Cálculo da stft   
    S = librosa.stft(st.session_state['audio_gravado_file'],hop_length=st.session_state['hop_length'],n_fft=st.session_state['comp_janela'], win_length=st.session_state['comp_janela'])#
    #Conversão da amplitude para dB
    S = np.abs(S)
    T = librosa.amplitude_to_db(S,ref=np.max)

    plt.figure(figsize=(18,7))
    
    #plt.plot(pitch.samp_values, label='samp_values', color='blue')
    #plt.plot(pitch.samp_interp, label='samp_interp', color='green')
    

    if not showWave:
        
        st.title("Resultado | Espectrograma")
        st.header("Informações:")
        st.write("Taxa de amostragem utilizada: ",st.session_state['freq_amostragem'])
        st.write("Comprimento da janela: ",st.session_state['comp_janela'])
        
        librosa.display.specshow(T,y_axis=axisScale,x_axis='time',sr=st.session_state['freq_amostragem'],cmap=cmap_option)
        plt.xlabel('Time[s]')
        plt.ylabel('Frequency [ Hz ]')
        plt.colorbar(format='%2.0f db')
        st.pyplot(plt)
        
        
    
    if showWave:
        st.title("Resultado | Espectrograma")
        st.header("Informações:")
        st.write("Taxa de amostragem utilizada: ",st.session_state['freq_amostragem'])
        st.write("Comprimento da janela: ",st.session_state['comp_janela'])

        fig, (ax, ax2) = plt.subplots(nrows=2, sharex=True)
        librosa.display.specshow(T,y_axis=axisScale,x_axis='time',sr=st.session_state['freq_amostragem'],cmap=cmap_option,ax=ax )
        librosa.display.waveshow(y, sr=st.session_state['freq_amostragem'], alpha=0.5, ax=ax2)
        st.pyplot(fig)

    if showpitch:
        
        st.title("Resultado | Pitch Tracking")

        fig, ax = plt.subplots() 
        plt.plot(pitch.values_interp,pitch.frame_pos/signal.fs, label='samp_interp', color='green')
        plt.xlabel('frames', fontsize=10)
        plt.ylabel('pitch (Hz)', fontsize=10)
        plt.legend(loc='upper right')
        axes = plt.gca()
        #axes.set_xlim(0)
        plt.show()

        st.pyplot(fig)

    if showPlay:
        st.title("Resultado | Espectrograma")
        st.header("Informações:")
        st.write("Taxa de amostragem utilizada: ",st.session_state['freq_amostragem'])
        st.write("Comprimento da janela: ",st.session_state['comp_janela'])

        st.audio(uploaded_file, format="audio/wav", start_time=0)
elif 'audio_gravado' in st.session_state:

    signal = basic.SignalObj("output.wav")
    pitch = pYAAPT.yaapt(signal)

    y, sr = librosa.load("output.wav",mono=True,sr=st.session_state['freq_amostragem'])

    S = librosa.stft(y,n_fft=st.session_state['comp_janela'],hop_length=st.session_state['hop_length'], win_length=st.session_state['comp_janela'])#hop_length=200

    S = np.abs(S)
    plt.figure(figsize=(18,7))
    
    #plt.plot(pitch.samp_values, label='samp_values', color='blue')
    #plt.plot(pitch.samp_interp, label='samp_interp', color='green')
    T = librosa.amplitude_to_db(S,ref=np.max)

    if not showWave:
        st.title("Resultado | Espectrograma")
        st.header("Informações:")
        st.write("Taxa de amostragem utilizada: ",st.session_state['freq_amostragem'])
        st.write("Comprimento da janela: ",st.session_state['comp_janela'])

        librosa.display.specshow(T,y_axis=axisScale,x_axis='time',sr=st.session_state['freq_amostragem'],cmap=cmap_option)
        plt.xlabel('Time[s]')
        plt.ylabel('Frequency [ Hz ]')
        plt.colorbar(format='%2.0f db')
        st.pyplot(plt)
    
    if showWave:
        st.title("Resultado | Espectrograma")
        st.header("Informações:")
        st.write("Taxa de amostragem utilizada: ",st.session_state['freq_amostragem'])
        st.write("Comprimento da janela: ",st.session_state['comp_janela'])


        fig, (ax, ax2) = plt.subplots(nrows=2, sharex=True)
        librosa.display.specshow(T,y_axis=axisScale,x_axis='time',sr=st.session_state['freq_amostragem'],cmap=cmap_option,ax=ax )
        librosa.display.waveshow(y, sr=st.session_state['freq_amostragem'], alpha=0.5, ax=ax2)
        #ax.set_xlabel('Time[s]')
        #plt.set_ylabel('Frequency [ Hz ]')
        st.pyplot(fig)
    if showpitch:
        
        st.title("Resultado | Pitch Tracking")

        fig, ax = plt.subplots() 
        plt.plot(pitch.values_interp,pitch.frame_pos/signal.fs, label='samp_interp', color='green')
        plt.xlabel('frames', fontsize=10)
        plt.ylabel('pitch (Hz)', fontsize=10)
        plt.legend(loc='upper right')
        axes = plt.gca()
        #axes.set_xlim(0)
        plt.show()

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
    y, sr = librosa.load(uploaded_file,mono=True,sr=st.session_state['freq_amostragem'])
        #print("Caiu no if",uploaded_file.name)
        #audio_file = open(y, 'rb')
        #audio_bytes = audio_file.read()
        #st.audio(audio_file, format='audio/ogg')
    fs = 44100 # Frequencia de amostragem
        #y, sr = librosa.load(fname,mono=True,sr=44100)
    S = librosa.stft(y,n_fft=st.session_state['comp_janela'],hop_length=st.session_state['hop_length'], win_length=st.session_state['comp_janela'])#hop_length=200

    S = np.abs(S)
    plt.figure(figsize=(18,7))
    
    #plt.plot(pitch.samp_interp, label='samp_interp', color='green')
    T = librosa.amplitude_to_db(S,ref=np.max)

    if not showWave:
        st.title("Resultado | Espectrograma")
        st.header("Informações:")
        st.write("Taxa de amostragem utilizada: ",st.session_state['freq_amostragem'])
        st.write("Comprimento da janela: ",st.session_state['comp_janela'])

        librosa.display.specshow(T,y_axis=axisScale,x_axis='time',sr=st.session_state['freq_amostragem'],cmap=cmap_option)
        plt.xlabel('Time[s]')
        plt.ylabel('Frequency [ Hz ]')
        plt.colorbar(format='%2.0f db')
        st.pyplot(plt)
    
    if showWave:
        st.title("Resultado | Espectrograma")
        st.header("Informações:")
        st.write("Taxa de amostragem utilizada: ",st.session_state['freq_amostragem'])
        st.write("Comprimento da janela: ",st.session_state['comp_janela'])

        fig, (ax, ax2) = plt.subplots(nrows=2, sharex=True)
        librosa.display.specshow(T,y_axis=axisScale,x_axis='time',sr=st.session_state['freq_amostragem'],cmap=cmap_option,ax=ax )
        librosa.display.waveshow(y, sr=sr, alpha=0.5, ax=ax2)
        st.pyplot(fig)

    if showpitch:
        
        st.title("Resultado | Pitch Tracking")

        fig, ax = plt.subplots() 
        plt.plot(pitch.values_interp, label='samp_interp', color='green')
        plt.xlabel('frames', fontsize=10)
        plt.ylabel('pitch (Hz)', fontsize=10)
        plt.legend(loc='upper right')
        axes = plt.gca()
        #axes.set_xlim(0)
        plt.show()

        st.pyplot(fig)

    if showPlay:
        st.audio(uploaded_file, format="audio/wav", start_time=0)
    
elif uploaded_file is None and 'notFoundImageBool' not in st.session_state and 'audio_gravado' not in st.session_state:
    st.title("EspectroApp")
    st.write("Faça upload do seu arquivo de áudio .wav ou grave agora mesmo o áudio à ser analisado. Realize análises de maneira simples e precisa.")
    st.image(notFoundImage, caption='File not found')
