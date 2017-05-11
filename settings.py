import  random

ERROR_THRESHOLD = 0.3
SEED_SIZE = 3
MAX_ERROR_THRESHOLD = 0.1

half_window = 5
window_size = 11
n_pixel_window = 121

input_path=".//textures//"
output_path=".//output//"


def set_window(window):
    global half_window, window_size, n_pixel_window
    window_size = window
    n_pixel_window = window ** 2
    half_window = (window - 1) / 2


def quote():
    quotes = ["Hitler was okay, I guess", "LOL --> Lucifer Our Lord", "I can speak snakes",
              "Let's put a smile on this face", "Harambe was just a Gorilla", "Let's make America great again",
              "Let's make Germany great again", "Justin Bieber is okay, I guess", "Some animals are more equal",
              "ROFL --> Rise Our Father Lucifer", "Evolution is just a theory", "Global warming is not a problem",
              "Talk to the hand"]
    print random.choice(quotes)