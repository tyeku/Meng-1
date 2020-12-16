#Figuring out which device number is the microphone
#import pyaudio
#p = pyaudio.PyAudio()
#for ii in range(p.get_device_count()):
#    print(p.get_device_info_by_index(ii).get('name'))
    
import pyaudio
import wave

import aiy.voice.audio
import aiy.cloudspeech
import argparse
import locale
import logging
import aiy.voice.tts
from time import sleep
from gpiozero import Button, LED
from signal import pause

def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('testing',
                'turn off the light',
                'blink the light',
                'goodbye')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language


def main():
    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 16000 # 44.1kHz sampling rate
    chunk = 12288 # 2^12 samples for buffer
    record_secs = 10 # seconds to record
    dev_index = 1 # device index found by p.get_device_info_by_index(ii)
    wav_output_filename = 'test1.wav' # name of .wav file
    
    speakvol= 8.5
    speakpitch= 120
    speakspeed= 85
    
    Response1= "Hi, I'm PurPal, your personal purchasing pal! Let me know what you're thinking of purchasing!"
    aiy.voice.tts.say(Response1, lang='en-US', volume=8.5, pitch=120, speed=85, device='default')
    
    sleep(5)
    
    #Record answer to 1st question -------------------------------------------------------
    audio = pyaudio.PyAudio() # create pyaudio instantiation

    # create pyaudio stream
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
    
    print("recording")
    frames = []
    led.on()
    
    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("finished recording")
    led.off()
    
    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # save the audio frames as .wav file
    #wavefile = wave.open(wav_output_filename,'wb')
    #wavefile.setnchannels(chans)
    #wavefile.setsampwidth(audio.get_sample_size(form_1))
    #wavefile.setframerate(samp_rate)
    #wavefile.writeframes(b''.join(frames))
    #wavefile.close()

    #playback for debugging purposes
    #aiy.voice.audio.play_wav('test1.wav')

    #Send to cloud for transcription
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)

    newdata=b''.join(frames)

    client=aiy.cloudspeech.CloudSpeechClient()
    text1=client.recognize_bytes(newdata, language_code='en-US', hint_phrases=hints)
    if text1==None:
        main()
    logging.info('You said: "%s"' % text1)
    
    #Tts --------------------------------------------------------------------------
    Response2= 'Is it for you, or someone else?'
    aiy.voice.tts.say(Response2, lang='en-US', volume=speakvol, pitch=speakpitch, speed=speakspeed, device='default')
    
    sleep(5)

    #Record answer to 2nd question -------------------------------------------------
    audio2 = pyaudio.PyAudio() # create pyaudio instantiation

    # create pyaudio stream
    stream2 = audio2.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)

    
    print("recording")
    frames2 = []
    led.on()
    
    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data2 = stream2.read(chunk)
        frames2.append(data2)

    print("finished recording")
    led.off()
    
    # stop the stream, close it, and terminate the pyaudio instantiation
    stream2.stop_stream()
    stream2.close()
    audio2.terminate()

    newdata2=b''.join(frames2)

    text2=client.recognize_bytes(newdata2, language_code='en-US', hint_phrases=hints)
    if text2==None:
        Restart="Sorry, I didn't get that. Let's start over!"
        aiy.voice.tts.say(Restart, lang='en-US', volume=speakvol, pitch=speakpitch, speed=speakspeed, device='default')
        main()
    logging.info('You said: "%s"' % text2)

    #Look for response topic
    if 'sports equipment' in text1 and 'some' in text2: #some is in someone and somebody
        exec(open("sportsequipment_else.py").read())
    elif 'sports equipment' in text1 and 'me' in text2:
        exec(open("sportsequipment_me.py").read())
    elif 'sports equipment' in text1: #default to someone else answer
        exec(open("sportsequipment_else.py").read())
        
    #Generic responses
    elif 'some' in text2:
        Response3= 'Think about what you want to say when you offer it'
        aiy.voice.tts.say(Response3, lang='en-US', volume=speakvol, pitch=speakpitch, speed=speakspeed, device='default')
        print(Response3)
    elif 'me' in text2:
        Response4= 'Think about how this will positively contribute to your life'
        aiy.voice.tts.say(Response4, lang='en-US', volume=speakvol, pitch=speakpitch, speed=speakspeed, device='default')
        print (Response4)        
    else: #Default to someone else answer
        Response5= 'Think about what you want to say when you offer it'
        aiy.voice.tts.say(Response5, lang='en-US', volume=speakvol, pitch=speakpitch, speed=speakspeed, device='default')


#Initialize LED
led=LED(17)
#Press button to run main script
button = Button(2)
button.when_pressed = main
pause()

#testing without needing to press a button
#if __name__ == "__main__":
#    main()
