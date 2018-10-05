from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Turno(Base):
    __tablename__ = 'turnos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DATE, nullable=False)
    hora = Column(TIME, nullable=False)

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

    def buscarTurnosFecha(self, fecha):
        fech = self.session.query(Turnos).filter(Turnos.fecha == fecha).all()
        return fech

datos = Datos()
