import os
import random
import time
from datetime import datetime

import pyautogui
from pyautogui import press
from pynput import mouse


def simulate_typing(min_num_words:int=1, max_num_words:int=10):
    """
    Simulate typing words with random slight paused in between each characters and spaces.
    
    :param int min_num_words: Minimum number of words to type.
    :param int max_num_words: Maximum number of words to type.
    """
    print(f"Running derp")
    file_path = os.path.join(os.path.dirname(__file__), 'word_file.txt')
    with open(file_path, 'r') as word_file:
        n_words = random.randrange(min_num_words, max_num_words)
        word_list = [f"{datetime.now().time()}"]

        word_list.extend(random.sample(word_file.read().splitlines(), n_words))
        print(f"Typing: {word_list}")
        for word in word_list:
            for letter in word:
                press(letter)
                time.sleep(random.randrange(50) / 100)
            press('space')
            time.sleep(random.randrange(100) / 100)
        time.sleep(random.randrange(50) / 100)
        press('enter')


class CursorUtils:
    def on_click(self, x, y, button, pressed):
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
        if pressed:
            print(f"This is x, y: {(x, y)}")
            return (x, y)
        if not pressed:
            return False

    def get_cursor_location(self):
        print(f"Place cursor at clicking position")
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
        controller = mouse.Controller()
        print(f"Controller position: {controller.position}")
        return controller.position

    def random_cursor_movement(self, x, y, min_time=1):
        pyautogui_mouse_movement_type = [key for key in list(pyautogui.__dict__.keys()) if key.startswith('ease')]
        n_random_movements = random.randrange(10, 50)
        total_time = min_time + random.randrange(100) / 100
        interval_time = total_time / n_random_movements
        if x and y:
            for i in range(10):
                interval = interval_time + random.randrange(-100, 101) / 100
                if interval < 0:
                    continue
                selected_movement_type = random.choice(pyautogui_mouse_movement_type)
                selected_movement = getattr(pyautogui, selected_movement_type)
                pyautogui.moveTo(random.randrange(50) + x, random.randrange(50) + y, interval, selected_movement)
            pyautogui.leftClick()
            time.sleep(random.randrange(100) / 100)
        return


def stay_online(
        stop_hhmm:str='1800', 
        min_delay_seconds:int=180, 
        max_delay_seconds:int=120, 
        min_num_words:int=1, 
        max_num_words:int=10):
    """
    Simulate fake movement and fake keyboard typing.

    :param str stop_hhmm: Time to stop running the simulation in HHMM format, example 1700.
    :param int min_delay_seconds: Minimum delay seconds.
    :param int max_delay_seconds: Maximum delay seconds.
    :param int min_num_words: Minimum number of words to type.
    :param int max_num_words: Maximum number of words to type.
    """
    cursor_location_object = CursorUtils()
    cursor_location = cursor_location_object.get_cursor_location()
    time.sleep(3)
    while True:
        current_time = datetime.now().time()
        print(f"Current time is: {datetime.now().time()}")
        if current_time > datetime.strptime(stop_hhmm, "%H%M").time():
            break
        try:
            cursor_location_object.random_cursor_movement(*cursor_location)
            simulate_typing(max_num_words=min_num_words, max_num_words=max_num_words)
            time.sleep(random.randrange(min_delay_seconds, max_delay_seconds))
        except:
            pass
