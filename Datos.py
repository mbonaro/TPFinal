from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import datetime
Base = declarative_base()

class Turno(Base):
    __tablename__ = 'turnos'
    fecha = Column(DATE, primary_key=True, nullable=False)
    hora = Column(TIME, primary_key=True, nullable=False)

class Datos(object):

    def __init__(self):
        engine = create_engine('mysql+pymysql://root:root@localhost/soportetpfinal')
        Base.metadata.bind = engine
        db_session = sessionmaker()
        db_session.bind = engine
        self.session = db_session()

    def alta(self, entrada):
        self.session.add(entrada)
        self.session.commit()
        return entrada

    def baja(self,fecha, hora):
        self.session.query(Turno).filter(Turno.fecha == fecha and Turno.hora == hora).delete()
        self.session.commit()
        return True

    def buscarTurnosFecha(self, fecha):
        fech = self.session.query(Turno.hora).filter(Turno.fecha == fecha).all()
        h=[]
        for i in fech:
            h.append(datetime.time.strftime(i.hora, '%H'))
        return h

datos = Datos()
datos.buscarTurnosFecha('2018-10-18')

