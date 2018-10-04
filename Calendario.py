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
import calendar
import time

class Turnos(Popup):
    turnoRoot = BoxLayout(orientation = "vertical")

    def __init__(self, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.add_widget(self.turnoRoot)
        self.create_turno()

    def create_turno(self):
        layout = GridLayout(cols=7)
        if self.turnoRoot:
            self.turnoRoot.clear_widgets()
        b = Button(text = "turno")
        self.turnoRoot.add_widget(b)


class Calendar(Popup):
    day = NumericProperty(0)
    month = NumericProperty(6)
    year = NumericProperty(2010)
    root = BoxLayout(orientation = "vertical")
    
    def __init__(self, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.add_widget(self.root)
        self.create_calendar()

    def create_calendar(self):
        self.day_str = [ 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom' ]
        self.month_str = [ 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre' ]
    
        self.dy = calendar.monthcalendar(self.year, self.month)
        self.title = (self.month_str[self.month-1] + ", " + str(self.year) )        
        
        layout = GridLayout(cols=7)  

        for d in self.day_str:
            b = Label(text = '[b]'+d+'[/b]' , markup=True )
            layout.add_widget(b)
         
        for wk in range(len(self.dy)):
            for d in range(0,7):    
                dateOfWeek = self.dy[wk][d]
                if not dateOfWeek == 0:
                    b = Button(text = str(dateOfWeek))
                    b.bind(on_release = self.date_selected)
                else:
                    b = Label(text = '' )
                layout.add_widget(b)
        if self.root:
            self.root.clear_widgets()
        self.root.add_widget(layout)
        bottombox = BoxLayout(orientation = "horizontal", size_hint = (1,None), height = 40)
        bottombox.add_widget(Button(text = '<', on_release = self.change_month))
        bottombox.add_widget(Button(text = '>', on_release = self.change_month))
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
        self.popup = Calendar(month = int(mes), year = int(año),
            size_hint=(None, None), size=(500, 400))
        self.popup.bind(on_dismiss = self.on_dismiss)
        return Button(text = "Show calendar", on_release = self.show_calendar)
    
    def show_calendar(self, event):
        self.popup.open()

    def on_dismiss(self, arg):
        # Do something on close of popup
        self.mostrarTurno()
        print("Date selected: ", str(self.popup.day) + '/' + str(self.popup.month) + '/' + str(self.popup.year))

    def mostrarTurno(self):
        titulo = 'Turno para el '+ str(self.popup.day) + '/' + str(self.popup.month) + '/' + str(self.popup.year)
        self.turnosPop = Turnos(title=str(titulo) , size_hint=(None, None), size=(500, 400))
        print("Date selected: ", str(self.popup.day) + '/' + str(self.popup.month) + '/' + str(self.popup.year))
        self.turnosPop.open()



if __name__ == "__main__":
    MyCalendar().run()
