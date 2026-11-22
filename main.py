# -*- coding: utf-8 -*-
"""حال امروز - اپلیکیشن ساده فارسی با Kivy"""
from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    def fa(text):
        return get_display(arabic_reshaper.reshape(text))
except Exception:
    def fa(text):
        return text

Window.clearcolor = get_color_from_hex('#080B1B')

class NeonButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = get_color_from_hex('#F4F3FF')
        self.font_size = sp(18)
        self.bold = True
        self.halign = 'center'
        self.valign = 'middle'
        self.bind(size=lambda *_: setattr(self, 'text_size', self.size))
        with self.canvas.before:
            self._c = Color(*get_color_from_hex('#20264A'))
            self._r = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
        with self.canvas.after:
            Color(0.35, 0.42, 1, 0.45)
            self._line = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
        self.bind(pos=self._update, size=self._update)
    def _update(self, *_):
        self._r.pos = self.pos; self._r.size = self.size
        self._line.pos = self.pos; self._line.size = self.size

class MoodRoot(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_background()
        self.welcome = Label(text=fa('خوش اومدی!'), font_size=sp(30), bold=True,
            color=(0.78, 0.82, 1, 1), size_hint=(.9, .18), pos_hint={'center_x':.5,'center_y':.56})
        self.add_widget(self.welcome)
        self.question = Label(text='', font_size=sp(27), bold=True,
            color=(1,1,1,1), size_hint=(.92,.18), pos_hint={'center_x':.5,'center_y':.52},
            halign='center', valign='middle')
        self.question.bind(size=lambda *_: setattr(self.question, 'text_size', self.question.size))
        self.add_widget(self.question)
        self.option_buttons = []
        Clock.schedule_once(self.show_question, 1.7)

    def build_background(self):
        with self.canvas.before:
            Color(*get_color_from_hex('#080B1B'))
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])
            Color(0.20, 0.12, 0.55, 0.18)
            self.orb1 = Ellipse(size=(dp(270),dp(270)), pos=(-dp(95), dp(430)))
            Color(0.05, 0.55, 0.75, 0.13)
            self.orb2 = Ellipse(size=(dp(230),dp(230)), pos=(dp(190), -dp(45)))
        self.bind(size=self._bg_update, pos=self._bg_update)
    def _bg_update(self, *_):
        self.bg.pos=self.pos; self.bg.size=self.size
        self.orb1.pos=(-dp(95), self.height*.60); self.orb2.pos=(self.width*.55,-dp(45))

    def show_question(self, *_):
        self.welcome.opacity = 0
        self.question.text = fa('امروز روزت چطور بود؟')
        self.question.opacity = 0
        self.question.pos_hint = {'center_x':.5, 'center_y':.52}
        Animation(opacity=1, duration=.65).start(self.question)
        Clock.schedule_once(self.move_question_up, 1.25)

    def move_question_up(self, *_):
        Animation(pos_hint={'center_x':.5,'center_y':.86}, duration=.65, t='out_cubic').start(self.question)
        Clock.schedule_once(self.show_options, .55)

    def show_options(self, *_):
        options = [
            ('عالی', '#244C68'),
            ('بد بود', '#56334E'),
            ('می‌خوام برنامه رو پاک کنم', '#493C69'),
            ('علی بهترینه', '#244F55'),
        ]
        ys = [.65, .49, .33, .17]
        for i, (caption, _color) in enumerate(options):
            b = NeonButton(text=fa(caption), size_hint=(.84,.105),
                           pos_hint={'center_x':.5,'center_y':ys[i]})
            # رنگ هر گزینه
            b._c.rgba = get_color_from_hex(_color)
            b.bind(on_release=lambda instance, idx=i, txt=caption: self.choose(idx, txt))
            self.add_widget(b); self.option_buttons.append(b)
            b.opacity = 0
            Animation(opacity=1, duration=.35, t='out_cubic').start(b)

    def choose(self, index, caption):
        for b in self.option_buttons:
            self.remove_widget(b)
        self.option_buttons.clear()
        # گزینه انتخاب‌شده در بالای صفحه
        selected = Label(text=fa(caption), font_size=sp(19), bold=True,
            color=(0.75,0.82,1,1), size_hint=(.9,.12), pos_hint={'center_x':.5,'center_y':.82},
            halign='center', valign='middle')
        selected.bind(size=lambda *_: setattr(selected,'text_size',selected.size))
        self.add_widget(selected)
        messages = {
            0: 'باشه',
            1: 'ان‌شاءالله زنت باهات حرف بزنه، روزت خوب شه',
            2: 'برای حذف برنامه، تأیید نهایی رو در گوشی بزن',
            3: 'ده میلیارد پول به حسابت واریز شد',
        }
        message = Label(text=fa(messages[index]), font_size=sp(25 if index != 1 else 20),
            bold=True, color=(0.62,0.88,1,1), size_hint=(.88,.28),
            pos_hint={'center_x':.5,'center_y':.49}, halign='center', valign='middle', opacity=0)
        message.bind(size=lambda *_: setattr(message,'text_size',message.size))
        with message.canvas.before:
            Color(0.22,0.42,1,0.12)
            glow = RoundedRectangle(pos=message.pos, size=message.size, radius=[dp(28)])
        message.bind(pos=lambda w,_: setattr(glow,'pos',w.pos), size=lambda w,_: setattr(glow,'size',w.size))
        self.add_widget(message)
        Animation(opacity=1, duration=.8).start(message)
        if index == 0:
            Clock.schedule_once(lambda *_: App.get_running_app().stop(), 2.0)
        elif index == 2:
            Clock.schedule_once(self.ask_uninstall, 1.8)

    def ask_uninstall(self, *_):
        # اندروید اجازه حذف بی‌صدا نمی‌دهد؛ تأیید نهایی باید توسط خود کاربر انجام شود.
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            activity = PythonActivity.mActivity
            intent = Intent(Intent.ACTION_DELETE)
            intent.setData(Uri.parse('package:com.alihal.todaymood'))
            activity.startActivity(intent)
        except Exception:
            from kivy.uix.popup import Popup
            Popup(title=fa('حذف برنامه'), content=Label(text=fa('در نسخه اندروید، پنجره حذف برنامه باز می‌شود.')), size_hint=(.85,.3)).open()

class MoodApp(App):
    def build(self):
        self.title = 'حال امروز'
        return MoodRoot()

if __name__ == '__main__':
    MoodApp().run()
