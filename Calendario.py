import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
import calendar
import time
from Datos import Turno, Datos
import datetime
import time

class Turnos(Popup):
    turnoRoot = BoxLayout(orientation="vertical")
    # turnoRoot = GridLayout(cols=2,rows=4)

    def __init__(self,fec, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.add_widget(self.turnoRoot)
        self.datos=Datos()
        self.fecha=fec
        self.create_turno()

    def create_turno(self):
        titulo = GridLayout(cols=1, row_force_default=True, row_default_height=40, padding=10)
        if self.turnoRoot:
            self.turnoRoot.clear_widgets()
        tit = Label(text="Deslize para seleccionar el horario en que desea el turno")
        titulo.add_widget(tit)
        self.turnoRoot.add_widget(titulo)

        # Creacion del dropbox
        dropdown = DropDown(width=475, auto_dismiss=False, dismiss_on_select=False, height=240)
        for index in range(10, 19):
            btn = Button(text='%d:00' % index, size_hint_y=None, height=44)
            # btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            btn.bind(on_release=self.mostrar)
            dropdown.add_widget(btn)
        # mainbutton = Button(text='Hello', size_hint=(None, None))
        # mainbutton.bind(on_release=dropdown.open)
        # dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        self.turnoRoot.add_widget(dropdown)

        botones = GridLayout(cols=2, row_force_default=True, row_default_height=40, padding=10)
        acept = Button(text="Aceptar")
        canc = Button(text="Cancelar")
        botones.add_widget(acept)
        botones.add_widget(canc)
        self.turnoRoot.add_widget(botones)

    def mostrar(self, event):
        self.hora = time.strptime(event.text, '%H:%M')
        self.datos.alta(Turno(fecha=self.fecha, hora=self.hora))
        print(time.strftime('%H:%M', self.hora))
        print(datetime.datetime.strftime(self.fecha,'%Y-%m-%d'))




class Calendar(Popup):
    day = NumericProperty(0)
    month = NumericProperty(6)
    year = NumericProperty(2010)
    root = BoxLayout(orientation="vertical")

    def __init__(self, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.add_widget(self.root)
        self.create_calendar()

    def create_calendar(self):
        self.day_str = ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']
        self.month_str = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre',
                          'Octubre', 'Noviembre', 'Diciembre']

        self.dy = calendar.monthcalendar(self.year, self.month)
        self.title = (self.month_str[self.month - 1] + ", " + str(self.year))

        layout = GridLayout(cols=7)

        for d in self.day_str:
            b = Label(text='[b]' + d + '[/b]', markup=True)
            layout.add_widget(b)

        for wk in range(len(self.dy)):
            for d in range(0, 7):
                if not (d == 6 or d == 5):
                    dateOfWeek = self.dy[wk][d]
                    if not dateOfWeek == 0:
                        b = Button(text=str(dateOfWeek))
                        b.bind(on_release=self.date_selected)
                    else:
                        b = Label(text='')
                    layout.add_widget(b)
                else:
                    dateOfWeek = self.dy[wk][d]
                    if not dateOfWeek == 0:
                        b = Button(text=str(dateOfWeek), background_color=(1.0, 0.0, 0.0, 1.0))
                    else:
                        b = Label(text='')
                    layout.add_widget(b)
        if self.root:
            self.root.clear_widgets()
        self.root.add_widget(layout)
        bottombox = BoxLayout(orientation="horizontal", size_hint=(1, None), height=40)
        bottombox.add_widget(Button(text='<', on_release=self.change_month))
        bottombox.add_widget(Button(text='>', on_release=self.change_month))
        self.root.add_widget(bottombox)

    def change_month(self, event):
        if event.text == '>':
            if self.month == 12:
                self.month = 1
                self.year = self.year + 1
            else:
                self.month = self.month + 1
        elif event.text == '<':
            if self.month == 1:
                self.month = 12
                self.year = self.year - 1
            else:
                self.month = self.month - 1

    def date_selected(self, event):
        self.day = int(event.text)
        print(self.day)
        self.dismiss()

    def on_month(self, widget, event):
        self.create_calendar()

    def on_year(self, widget, event):
        self.create_calendar()


class MyCalendar(App):
    def build(self):
        """Inicializa en el mes actual y año actual"""
        mes = time.strftime('%m')
        año = time.strftime('%Y')
        self.popup = Calendar(month=int(mes), year=int(año),
                              size_hint=(None, None), size=(500, 400))
        self.popup.bind(on_dismiss=self.on_dismiss)
        return Button(text="Show calendar", on_release=self.show_calendar)

    def show_calendar(self, event):
        self.popup.open()

    def on_dismiss(self, arg):
        # Do something on close of popup
        self.mostrarTurno()
        print("Date selected: ", str(self.popup.day) + '/' + str(self.popup.month) + '/' + str(self.popup.year))

    def mostrarTurno(self):
        titulo = 'Turno para el ' + str(self.popup.day) + '/' + str(self.popup.month) + '/' + str(self.popup.year)
        fec = datetime.datetime.strptime((str(self.popup.year) + '-' + str(self.popup.month) + '-' + str(self.popup.day)), '%Y-%m-%d')
        self.turnosPop = Turnos(fec ,title=str(titulo), size_hint=(None, None), size=(500, 400))
        print("Date selected: ", str(self.popup.day) + '/' + str(self.popup.month) + '/' + str(self.popup.year))
        self.turnosPop.open()


if __name__ == "__main__":
    MyCalendar().run()
