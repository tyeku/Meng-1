def main():
    Response= 'Think about how the item would contribute to your physical or mental health'
    aiy.voice.tts.say(Response, lang='en-US', volume=8.5, pitch=120, speed=85, device='default')
    print(Response)

if __name__ == "__main__":
    main()