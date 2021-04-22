import board
import adafruit_dotstar
 
DOTSTAR_DATA = board.D5
DOTSTAR_CLOCK = board.D6
dots = adafruit_dotstar.DotStar(DOTSTAR_CLOCK, DOTSTAR_DATA, 3, brightness=0.2)

def main():
    Response= 'Think about how the item would contribute to your physical or mental health'
    dots.fill((255,0,0))
    aiy.voice.tts.say(Response, lang='en-US', volume=8.5, pitch=120, speed=85, device='default')
    dots.fill((0,0,0))
    print(Response)

if __name__ == "__main__":
    main()
