from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import datetime
Base = declarative_base()

class Turno(Base):
    __tablename__ = 'turnos'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    fecha = Column(DATE, nullable=False)
    hora = Column(TIME, nullable=False)
    usuario = Column(String, nullable=False)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String, nullable=False)
    usuario = Column(String, nullable=False, unique=True)
    contrasena =Column(String, primary_key=True, nullable=False)

class Datos(object):

    def __init__(self):
        engine = create_engine('mysql+mysqlconnector://sql10261861:Ti7VgbdEtT@sql10.freemysqlhosting.net/sql10261861')
        Base.metadata.bind = engine
        db_session = sessionmaker()
        db_session.bind = engine
        self.session = db_session()

    def alta(self, entrada):
        self.session.add(entrada)
        self.session.commit()
        return entrada

    def bajaTurno(self, entrada):
        self.session.query(Turno).filter(Turno.id == entrada.id).delete()
        self.session.commit()
        return True

    def bajaUsuario(self, entrada):
        self.session.query(Usuario).filter(Usuario.id == entrada.id).delete()
        self.session.commit()
        return True

    def buscarTurnosFecha(self, fecha):
        fech = self.session.query(Turno.hora).filter(Turno.fecha == fecha).all()
        h=[]
        for i in fech:
            h.append(datetime.time.strftime(i.hora, '%H'))
        return h

    def verificarUsuario(self, usuario,password):
        us = self.session.query(Usuario).filter(Usuario.usuario == usuario).all()
        if (len(us)==0):
            return 0
        elif(us[0].contrasena == password):
            return us
        else:
            return 0



def pruebas():
    datos = Datos()

    # Alta de usuario
    usuario = datos.alta(Usuario(nombre='jose prueba', usuario='prueba123', contrasena='123456'))

    # Alta de turno
    turno = datos.alta(Turno(fecha='2018-12-12', hora='12:00', usuario=usuario.usuario ))
    assert turno.id>0

    # Verificacion Usuario
    assert (datos.verificarUsuario(usuario.usuario, usuario.contrasena)!=0)

    # Busqueda
    horas = datos.buscarTurnosFecha(turno.fecha)
    assert (horas[0]==datetime.time.strftime(turno.hora, '%H'))
    #assert (turno.hora == datetime.datetime.strptime(horas[0], '%H'))

    # Bajas
    datos.bajaTurno(turno)
    datos.bajaUsuario(usuario)
    assert (datos.verificarUsuario(usuario.usuario, usuario.contrasena) == 0)


pruebas()
