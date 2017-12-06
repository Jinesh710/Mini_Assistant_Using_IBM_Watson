import requests
import pyaudio
import tkinter as gui
import wave


def createGUI():
    print()
    frame=gui.Tk()
    frame.title("Mini Assistant")
    frame.geometry("200x100")
    but=gui.Button(frame, text="Record Audio", command=recordAudio)
    but.pack()
    exi = gui.Button(frame, text="Exit", command=frame.destroy)
    exi.pack(side='bottom')
    mesVar=""
    mes=gui.Message(frame,textvariable=mesVar)
    mes.pack
    frame.mainloop()

def recordAudio():
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 3

    audio = pyaudio.PyAudio()
    WAVE_OUTPUT_FILENAME = "file.wav"

    # start Recorbding
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    getWordFromAudio()

def getWordFromAudio():
    url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'
    username = "1f9603b6-478a-44e6-8497-a9e94406a3e5"
    password = "qzlSfwmfeKmE"
    headers = {'Content-Type': 'audio/wav'}
    audio=open('recordings\mumbai.wav','rb') #Pre recorded audio.
    # audio = open("file.wav", 'rb')#Real Time Recording
    r = requests.post(url, data=audio, headers=headers, auth=(username, password))
    if len(r.json()['results'])!=0:
        inpWord = r.json()['results'][0]['alternatives'][0]['transcript'].strip().lower()
        searchCorpusAndDisplayResults(inpWord)
    else:print("No Input")

def searchCorpusAndDisplayResults(inpWord):
    print("You said",inpWord)
    countryFile = open("countryCodes.csv", )
    countryDict = {}
    for line in countryFile:
        countryDict[line.split(",")[1].strip().lower()] = line.split(",")[0].strip()
    file = open("worldcitiespop.txt", encoding="latin-1")
    flag = False
    for line in file:
        line = line.split(",")
        # print(line[1])
        if line[1].strip() == inpWord and line[0] in countryDict:
            flag=True
            mesVar="The city " + line[2].strip()+ " is situated in the country "+ countryDict[line[0].strip()]+". "
            #if line[3]:
            #    mesVar+= "It lies in the region", line[3].strip()+". "
            if line[4]:
                mesVar= mesVar+ "It has a population of "+ line[4].strip()+". "
            if line[5].strip() and line[6].strip():
                mesVar= mesVar+ "It is situated at latitude "+ line[5].strip()+" and longitude "+ line[6].strip()+"."
            print(mesVar)
    if flag:
        print("Done Answering")
    else: print("No Information found")


createGUI()