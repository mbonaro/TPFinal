from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Dia(Base):
    __tablename__ = 'diaturnos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DATE, nullable=False, unique=True)
    horaInicio = Column(TIME)
    horaFin = Column(Time)

class Hora(Base):
    __tablename__ = 'horasdia'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DATE, primary_key=True, nullable=False)
    hora = Column(TIME, unique=True)

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

    def buscarHoras(self, fecha):
        fech = self.session.query(Hora).filter(Hora.fecha == fecha).all()
        return fech

datos = Datos()
fechas = datos.buscarHoras('2018-10-07')
for i in fechas:
    print(i.hora)