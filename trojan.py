
import random
import os

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle


SKULL = r"""
          uu$$$$$$$$$$$$uu
        uu$$$$$$$$$$$$$$$$uu
       u$$$$$$$$$$$$$$$$$$$$u
      u$$$$$$$$$$$$$$$$$$$$$$u
     u$$$$$$$$$$$$$$$$$$$$$$$$u
     u$$$$$$$$$$$$$$$$$$$$$$$$u
     u$$$$$$*   *$$$*   *$$$$$$u
      *$$$$$*   u$u   *$$$$$*
       $$$u     u$u     u$$$
       $$$u    u$$$u    u$$$
        *$$$$uu$$$ $$$uu$$$$*
         *$$$$$$$* *$$$$$$$*
          u$$$$$$$u$$$$$$$u
           u$*$*$*$*$*$*$u
  uuu       $$u$ $ $ $u$$       uuu
 u$$$$$     $$$$$u$u$u$$$$$     u$$$$$
  $$$$$$uu   *$$$$$$$$$$$*   uu$$$$$$
u$$$$$$$$$$$uu   *****   uu$$$$$$$$$$$u
$$$***$$$$$$$$$$uuu   uuu$$$$$$$$$$***$$$
***    **$$$$$$$$$$$u $$$$$$$$$$$**    ***
       uuuu **$$$$$$$$$$$** uuuu
  u$$$uuu$$$$$$$$$u **$$$$$$$$$uuu$$$u
  $$$$$$$$$$****         ****$$$$$$$$$$
    *$$$$$*                   *$$$$$*
     $$$*     PRESS ANY KEY!     *$$$
"""


class HorrorApp(App):

    def build(self):
        Window.clearcolor = (0.005, 0.003, 0.008, 1)

        self.seconds = 300
        self.finished = False
        self.errors = 0

        # Стан друку логів
        self.log_lines = []
        self.typing_text = ""
        self.typing_position = 0
        self.typing_pause = 0

        # Стан мерехтіння
        self.blink_counter = 0
        self.blink_brightness = 1

        root = FloatLayout()

        mono = "/system/fonts/DroidSansMono.ttf"
        if not os.path.exists(mono):
            mono = "Roboto"

        # Системні повідомлення
        self.logs = Label(
            text="",
            font_name=mono,
            font_size=dp(10),
            color=(0, 1, 0.25, 1),
            halign="left",
            valign="top",
            size_hint=(0.96, 0.19),
            pos_hint={"x": 0.02, "top": 0.99}
        )
        self.logs.bind(size=self.logs.setter("text_size"))
        root.add_widget(self.logs)

        self.add_line(root, 0.795)

        # Череп
        skull = Label(
            text=SKULL,
            font_name=mono,
            font_size=dp(8.5),
            color=(1, 0.025, 0.025, 1),
            halign="center",
            valign="middle",
            size_hint=(1, 0.43),
            pos_hint={"center_x": 0.5, "center_y": 0.57}
        )
        root.add_widget(skull)

        # Попередження
        self.warning = Label(
            text=">>> ВАС ЗАМЕТИЛИ <<<",
            color=(1, 0, 0, 1),
            font_size=dp(24),
            bold=True,
            size_hint=(1, 0.06),
            pos_hint={"center_x": 0.5, "center_y": 0.335}
        )
        root.add_widget(self.warning)

        subtitle = Label(
            text="UNKNOWN PROCESS DETECTED",
            color=(0.7, 0.12, 0.12, 1),
            font_size=dp(10),
            size_hint=(1, 0.04),
            pos_hint={"center_x": 0.5, "center_y": 0.295}
        )
        root.add_widget(subtitle)

        self.add_line(root, 0.265)

        # Таймер
        self.timer_label = Label(
            text="05:00",
            color=(1, 0.02, 0.02, 1),
            font_size=dp(36),
            bold=True,
            size_hint=(1, 0.08),
            pos_hint={"center_x": 0.5, "center_y": 0.215}
        )
        root.add_widget(self.timer_label)

        # Помилки
        self.error_label = Label(
            text="FAILED ATTEMPTS: 0",
            color=(0.8, 0.15, 0.15, 1),
            font_size=dp(10),
            size_hint=(1, 0.035),
            pos_hint={"center_x": 0.5, "center_y": 0.16}
        )
        root.add_widget(self.error_label)

        # Поле коду
        self.code_input = TextInput(
            hint_text="ENTER ACCESS CODE",
            multiline=False,
            halign="center",
            size_hint=(0.78, 0.055),
            pos_hint={"center_x": 0.5, "center_y": 0.105},
            background_color=(0.08, 0.015, 0.02, 1),
            foreground_color=(1, 0.2, 0.2, 1),
            hint_text_color=(0.5, 0.2, 0.2, 1),
            cursor_color=(1, 0, 0, 1)
        )
        root.add_widget(self.code_input)

        # Кнопка
        verify = Button(
            text="VERIFY CODE",
            size_hint=(0.55, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.045},
            background_normal="",
            background_color=(0.5, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        verify.bind(on_press=self.check_code)
        root.add_widget(verify)

        footer = Label(
            text="YOU FILE INFECTED",
            color=(0.35, 0.35, 0.35, 1),
            font_size=dp(9),
            size_hint=(1, 0.025),
            pos_hint={"center_x": 0.5, "y": 0.0}
        )
        root.add_widget(footer)

        # Запускаємо цикли лише один раз
        self.create_new_log()

        Clock.schedule_interval(self.update_timer, 1)
        Clock.schedule_interval(self.type_tick, 0.07)
        Clock.schedule_interval(self.blink_tick, 0.12)

        return root

    def add_line(self, root, y):
        with root.canvas:
            Color(0.65, 0.015, 0.015, 0.8)
            Rectangle(
                pos=(dp(12), Window.height * y),
                size=(Window.width - dp(24), dp(1))
            )

    # Створення нового рядка
    def make_log(self):
        fake_ips = [
            "192.0.2.14",
            "198.51.100.27",
            "203.0.113.52",
            "192.0.2.88",
            "198.51.100.103"
        ]

        messages = [
            "[SYSTEM] ANDROID 13 / API 33",
            "[NETWORK] TEST CONNECTION",
            "[WARNING] UNKNOWN PROCESS",
            "[SCAN] DEMO ENVIRONMENT",
            "[SYSTEM] MEMORY STATUS: NORMAL",
            "[ALERT] SIGNAL LOST",
            "[TRACE] " + random.choice(fake_ips),
            "[PORT] " + str(random.randint(1000, 9999)),
            "[ERROR] ACCESS DENIED",
            "[SYSTEM] UNKNOWN DEVICE",
            "[WARNING] CONNECTION UNSTABLE",
            "[TRACE] SEARCHING...",
            "[DATA] " + "".join(
                random.choice("0123456789ABCDEF")
                for _ in range(12)
            ),
            "[CORE] " + str(random.randint(10, 99)) + "%"
        ]

        return random.choice(messages)

    def create_new_log(self):
        self.typing_text = self.make_log()
        self.typing_position = 0

    # Єдиний цикл друку
    def type_tick(self, dt):
        if self.finished:
            return

        if self.typing_pause > 0:
            self.typing_pause -= 1
            return

        if self.typing_position < len(self.typing_text):
            self.typing_position += 1

            current = self.typing_text[:self.typing_position]

            display = self.log_lines + [current]
            self.logs.text = "\n".join(display)

            # Невелика випадкова пауза
            if random.random() < 0.12:
                self.typing_pause = random.randint(1, 5)

        else:
            self.log_lines.append(self.typing_text)

            if len(self.log_lines) > 7:
                self.log_lines.pop(0)

            self.logs.text = "\n".join(self.log_lines)

            self.typing_pause = random.randint(3, 12)
            self.create_new_log()

    # Нерівномірне мерехтіння
    def blink_tick(self, dt):
        if self.finished:
            return

        if self.blink_counter <= 0:
            if random.random() < 0.22:
                self.blink_brightness = random.choice(
                    [0.08, 0.2, 0.4, 0.65]
                )
                self.blink_counter = random.randint(1, 3)
            else:
                self.blink_brightness = 1
                self.blink_counter = random.randint(2, 10)
        else:
            self.blink_counter -= 1

        b = self.blink_brightness
        self.warning.color = (b, 0, 0, 1)

    # Таймер
    def update_timer(self, dt):
        if self.finished:
            return

        self.seconds -= 1

        if self.seconds <= 0:
            self.seconds = 0
            self.finish_demo()
            return

        minutes = self.seconds // 60
        seconds = self.seconds % 60

        self.timer_label.text = f"{minutes:02d}:{seconds:02d}"

        if self.seconds <= 30:
            self.timer_label.color = (1, 0.15, 0.15, 1)

    # Перевірка коду
    def check_code(self, instance):
        if self.finished:
            return

        code = self.code_input.text.strip()

        if code == "2422":
            self.finished = True

            self.timer_label.text = "ACCESS GRANTED"
            self.timer_label.font_size = dp(22)
            self.timer_label.color = (0, 1, 0.2, 1)

            Clock.schedule_once(
                lambda dt: self.stop(), 2
            )

        else:
            self.errors += 1

            self.error_label.text = (
                f"FAILED ATTEMPTS: {self.errors}"
            )

            self.seconds = max(0, self.seconds - 60)
            self.code_input.text = ""

            if self.seconds <= 0:
                self.finish_demo()

    # Завершення демо
    def finish_demo(self):
        if self.finished:
            return

        self.finished = True

        self.timer_label.text = "ЧАС ВИЙШОВ"
        self.timer_label.font_size = dp(25)
        self.timer_label.color = (1, 0, 0, 1)

        self.warning.text = "SESSION TERMINATED"

        Clock.schedule_once(
            lambda dt: self.stop(), 2
        )


if __name__ == "__main__":
    HorrorApp().run()
