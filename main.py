from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.scrollview import MDScrollView

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.image import Image
from kivy.clock import Clock


# -------- SPLASH -------- #
class SplashScreen(MDScreen):
    def on_enter(self):
        self.clear_widgets()

        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        layout.add_widget(MDLabel(text="", size_hint=(1, 0.3)))
        layout.add_widget(Image(source="logo.png", size_hint=(1, 0.5)))
        layout.add_widget(MDLabel(text="KLE College", halign="center", font_style="H4"))
        layout.add_widget(MDLabel(text="Loading...", halign="center"))

        self.add_widget(layout)

        Clock.schedule_once(self.go_login, 3)

    def go_login(self, dt):
        self.manager.current = "login"


# -------- LOGIN -------- #
class LoginScreen(MDScreen):
    def on_enter(self):
        self.clear_widgets()

        layout = MDBoxLayout(orientation='vertical', padding=30, spacing=20)

        layout.add_widget(MDLabel(text="Login", halign="center", font_style="H4"))

        self.username = MDTextField(hint_text="Username")
        self.password = MDTextField(hint_text="Password", password=True)
        self.msg = MDLabel(text="", halign="center")

        btn = MDRaisedButton(text="Login", pos_hint={"center_x": 0.5})
        btn.bind(on_release=self.login)

        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(btn)
        layout.add_widget(self.msg)

        self.add_widget(layout)

    def login(self, instance):
        if self.username.text == "admin" and self.password.text == "1234":
            self.manager.current = "home"
        else:
            self.msg.text = "Invalid login"


# -------- HOME -------- #
class HomeScreen(MDScreen):
    def on_enter(self):
        self.clear_widgets()

        nav = MDBottomNavigation()

        dash = MDBottomNavigationItem(name="home", text="Home", icon="home")

        box = MDBoxLayout(orientation='vertical', padding=15, spacing=10)
        box.add_widget(MDLabel(text="Dashboard", font_style="H5"))

        box.add_widget(self.card("About", "about", "information"))
        box.add_widget(self.card("Courses", "courses", "book"))
        box.add_widget(self.card("Notifications", "notifications", "bell"))
        box.add_widget(self.card("Contact", "contact", "phone"))

        dash.add_widget(box)

        profile = MDBottomNavigationItem(name="profile", text="Profile", icon="account")
        profile.add_widget(MDLabel(text="Welcome Student", halign="center"))

        nav.add_widget(dash)
        nav.add_widget(profile)

        self.add_widget(nav)

    def card(self, text, screen, icon):
        card = MDCard(padding=15, size_hint=(1, None), height=80, elevation=6, radius=[15])

        layout = MDBoxLayout()
        layout.add_widget(MDIconButton(icon=icon))
        layout.add_widget(MDLabel(text=text))

        btn = MDRaisedButton(text="Open", size_hint=(0.3, 1))
        btn.bind(on_release=lambda x: self.go(screen))

        layout.add_widget(btn)
        card.add_widget(layout)

        return card

    def go(self, screen):
        self.manager.current = screen


# -------- NOTIFICATIONS -------- #
class NotificationScreen(MDScreen):
    def on_enter(self):
        self.clear_widgets()

        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(MDLabel(text="Notifications", font_style="H4"))

        scroll = MDScrollView()
        container = MDBoxLayout(orientation='vertical', size_hint_y=None)
        container.bind(minimum_height=container.setter('height'))

        for note in self.app.notifications:
            container.add_widget(self.card(note["title"], note["msg"]))

        scroll.add_widget(container)
        layout.add_widget(scroll)

        btn = MDRaisedButton(text="Add Notification", pos_hint={"center_x": 0.5})
        btn.bind(on_release=self.add_notification)

        layout.add_widget(btn)

        back = MDRaisedButton(text="Back", pos_hint={"center_x": 0.5})
        back.bind(on_release=lambda x: self.go_home())

        layout.add_widget(back)

        self.add_widget(layout)

    def card(self, title, msg):
        card = MDCard(padding=15, size_hint=(1, None), height=100, elevation=5, radius=[15])

        box = MDBoxLayout(orientation='vertical')
        box.add_widget(MDLabel(text=title, bold=True))
        box.add_widget(MDLabel(text=msg))

        card.add_widget(box)
        return card

    def add_notification(self, instance):
        self.app.notifications.append({
            "title": "New Notice",
            "msg": "This is a new notification"
        })
        self.on_enter()

    def go_home(self):
        self.manager.current = "home"

    @property
    def app(self):
        return MDApp.get_running_app()


# -------- SIMPLE SCREENS -------- #
class SimpleScreen(MDScreen):
    def __init__(self, title, content, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.content = content

    def on_enter(self):
        self.clear_widgets()

        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(MDLabel(text=self.title, font_style="H4"))
        layout.add_widget(MDLabel(text=self.content))

        btn = MDRaisedButton(text="Back", pos_hint={"center_x": 0.5})
        btn.bind(on_release=lambda x: self.go_home())

        layout.add_widget(btn)

        self.add_widget(layout)

    def go_home(self):
        self.manager.current = "home"


# -------- APP -------- #
class KLEApp(MDApp):

    notifications = [
        {"title": "Exam Update", "msg": "Mid exams start next week"},
        {"title": "Holiday", "msg": "College closed on Friday"},
    ]

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        sm = ScreenManager()

        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))

        sm.add_widget(SimpleScreen(name="about", title="About", content="Welcome To KLE Established in the year 1963, KLES’ S. Nijalingappa College is one of the 250 institutions under KLE Society whose founding date goes back to 1916. Our campus is located in the heart of Bangalore, and sprawls across 5 acres with easy connectivity. Over the years, there has been dynamic progress in all academic and research activities and a commensurate up-gradation of facilities and infrastructure, to keep on par with the best institutions in the country."))
        sm.add_widget(SimpleScreen(name="courses", title="Courses", content="Undergraduate (UG): BA, B.Sc (Physics, Chemistry, Maths, Botany, Zoology, Biotech), B.Com, BBA, BCA, and BSc in Fashion and Apparel Design.Postgraduate (PG): M.Sc (Computer Science, IT, Data Analytics), MCA, and MBA.Special Programs: 4-year Integrated B.Sc-B.Ed (recognized by NCTE) and various short-term courses like vermiculture and landscaping.New Syllabus: The college has implemented the new NEP/CBCS syllabus for 2024-25."))
        sm.add_widget(NotificationScreen(name="notifications"))
        sm.add_widget(SimpleScreen(name="contact", title="Contact", content="admissions@klesnc.org"))

        sm.current = "splash"
        return sm


if __name__ == "__main__":
    KLEApp().run()