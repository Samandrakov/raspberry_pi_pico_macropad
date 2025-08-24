import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Инициализация клавиатуры
keyboard = Keyboard(usb_hid.devices)

# Настройка кнопок (GP0-GP8)
buttons = []
pins = [board.GP2, board.GP3, board.GP4, board.GP5,
        board.GP6, board.GP7, board.GP8, board.GP9, board.GP10]

# Клавиши для каждой кнопки (можно изменить)
key_actions = [
    Keycode.ONE,
    Keycode.TWO,
    Keycode.THREE,
    Keycode.FOUR,
    Keycode.FIVE,
    Keycode.SIX,
    Keycode.SEVEN,
    Keycode.EIGHT,
    Keycode.NINE
]

# Инициализация всех кнопок
for pin in pins:
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons.append(btn)

# Для защиты от дребезга
last_press_time = [0] * 9
debounce_delay = 0.3

while True:
    for i in range(9):
        if not buttons[i].value and (time.monotonic() - last_press_time[i] > debounce_delay):
            action = key_actions[i]

            # Обработка разных типов действий
            if isinstance(action, list):  # Если это комбинация клавиш
                keyboard.press(*action)
            else:  # Если одиночная клавиша
                keyboard.press(action)

            keyboard.release_all()
            last_press_time[i] = time.monotonic()

            # Вывод отладочной информации
            print(f"Button {i + 1} pressed")
