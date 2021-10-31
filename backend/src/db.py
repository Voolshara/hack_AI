import os
from contextlib import contextmanager
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import and_
from collections import Counter
from dotenv import load_dotenv


load_dotenv()

engine = sa.create_engine(
    'postgresql://{}:{}@{}:{}/{}'.format(
        os.getenv('PG_NAME'),
        os.getenv('PG_PASSWORD'),
        os.getenv('PG_HOST'),
        os.getenv('PG_PORT'),
        os.getenv('PG_DB_NAME'),
    )
)
Session = sessionmaker(bind=engine)
Base = declarative_base()


@contextmanager
def create_session(**kwargs):
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


class Marks(Base):
    __tablename__ = "Marks"
    id = sa.Column(sa.Integer, primary_key=True)
    street = sa.Column(sa.String())
    house = sa.Column(sa.String())
    coords_lat = sa.Column(sa.Float)
    coords_lon = sa.Column(sa.Float)
    level = sa.Column(sa.Integer)
    type = sa.Column(sa.String())


class Tasks(Base):
    __tablename__ = "Tasks"
    id = sa.Column(sa.Integer, primary_key=True)
    date = sa.Column(sa.String())
    text = sa.Column(sa.String())
    mark_id = sa.Column(sa.Integer, sa.ForeignKey(Marks.id))


class DB_new:
    def create_all_tables(self):
        Base.metadata.create_all(engine)

    def add_rows(self):
        with open(r"backend\src\output_full_full.csv", "r", encoding="utf-8") as file:
            data = file.readlines()
            ready_ids = []
            kol = 0
            for row in data[1:]:
                try:
                    street, house, date, text, coords, id, lvl, all_tasks, type, status = row.split(";")
                except:
                    # street = row[:row.find(";")]
                    # row = row[row.find(";") + 1:]
                    # house = row[:row.find(";")]
                    # row = row[row.find(";") + 1:]
                    # date = row[:row.find(";")]
                    # row = row[row.find(";") + 1:]
                    # all_tasks = row[row.rfind(";") + 1:]
                    # row = row[:row.rfind(";")]
                    # lvl = row[row.rfind(";") + 1:]
                    # row = row[:row.rfind(";")]
                    # id = row[row.rfind(";") + 1:]
                    # row = row[:row.rfind(";")]
                    # coords = row[row.rfind(";") + 1:]
                    # row = row[:row.rfind(";")]
                    # text =  row

                    # try:
                    #     float(coords.split()[0])
                    #     float(coords.split()[1])
                    # except:
                    #     kol += 1
                    continue
                if id in ready_ids:
                    pass
                else:
                    with create_session() as session:
                        for el in all_tasks[all_tasks.find("[") + 1:all_tasks.find("]")].split(", "):
                            ready_ids.append(el)
                        if coords != "NONE":
                            response = session.query(Marks).filter(and_(Marks.street == street, Marks.house == house)).first()
                            if response is None:
                                session.add(Marks(
                                    street=street,
                                    house=house,
                                    coords_lat = float(coords.split()[0]),
                                    coords_lon = float(coords.split()[1]),
                                    level = self.level_calculate(lvl, type, status, float(coords.split()[0]), float(coords.split()[1])),
                                    type = type,
                                ))
                with create_session() as session:
                    response = session.query(Marks).filter(and_(Marks.street == street, Marks.house == house)).first()
                    if response is not None:
                        session.add(Tasks(
                            date = date,
                            text = text,
                            mark_id = response.id 
                        ))

    def level_calculate(self, lvl, type=None, places=None, lat=None, lon=None):
        if places != 0:
            lvl = int(lvl) // 2
        if type == "Жилищно-коммунальные услуги":
            lvl = int(1.4 * int(lvl))
        elif type == "Дороги":
            lvl = int(1.2 * int(lvl))
        if 56.098432 <= lat <= 56.140517 and 47.180747 <= lon <= 47.214284:
            int(1.2 * int(lvl))
        if 56.091172 <= lat <= 56.130227 and 47.247459 <= lon <= 47.292564:
            int(1.2 * int(lvl))
        return lvl

    def set_right_number(self, n):
        return n if len(n) > 1 else "0" + n 

    def set_color(self, level, max_level):
        return '#ff' + self.set_right_number(str(hex(256 - int(level / max_level[0] * 256)))[2:]) + '00'

    def get_all_placemarks(self):
        with create_session() as session:
            response = session.query(Marks).filter(Marks.level > 0).all()
            max_lvl = session.query(func.max(Marks.level).label("max_score")).one()
            coords = []
            colors = []
            data = []
            for x in response:
                response_tasks = session.query(Tasks).filter(Tasks.mark_id == x.id).all()
                all_tasks = [r.text for r in response_tasks]
                coords.append([x.coords_lat, x.coords_lon])
                colors.append(self.set_color(x.level, max_lvl))
                data.append([", ".join([x.street, x.house]), x.type, min(all_tasks)])
            return coords, colors, data
    
    def find_place(self):
        A = {
            "SZ" : [],
            "UZ" : [],
            "C": [],
            "NU" : [],
            "U": [],
            "V" : [],
            "NOV": [],
        }

        С = {
           "SZ" : "Северо-Западный район",
            "UZ" : "Юго-Западный район",
            "C": "Центральный район",
            "NU" : "Новоюжный район",
            "U": "Южный район",
            "V" : "Восточный район",
            "NOV": "Новочебоксарск", 
        }
        with create_session() as session:
            response = session.query(Marks).filter(Marks.level > 0).all()
            for x in response:
                lat = x.coords_lat
                lon = x.coords_lon
                if 56.137157 <= lat <= 56.154374 and 47.164666 <= lon <= 47.227282: # Северо-Западный район
                    A["SZ"].append(x.type) 
                elif 56.108882 <= lat <= 56.127215 and 47.167332 <= lon <= 47.203927: # Юго-Западный район
                    A["UZ"].append(x.type)
                elif 56.110564 <= lat <= 56.152623 and 47.249090 <= lon <= 47.276263: # Центральный район
                    A["C"].append(x.type)
                elif 56.103899 <= lat <= 56.109167 and 47.231313 <= lon <= 47.338355: # Новоюжный район
                    A["NU"].append(x.type)
                elif 56.074650 <= lat <= 56.095252 and 47.256942 <= lon <= 47.330435: # Южный район
                    A["U"].append(x.type)
                elif 56.113920 <= lat <= 56.149875 and 47.281100 <= lon <= 47.367324: # Восточный район
                    A["V"].append(x.type)
                elif 56.090337 <= lat <= 56.132434 and 47.460847 <= lon <= 47.527168: # Новочебоксарск
                    A["NOV"].append(x.type)
        B = []
        for key in A:
            B.append({
                "region" : С[key],
                "problem" : [k for k,v in Counter(A[key]).items() if v>1][0],
                "num" : A[key].count([k for k,v in Counter(A[key]).items() if v>1][0])
                })
        return B

# DBN = DB_new()
# DBN.find_place()
# DBN.create_all_tables()
# DBN.add_rows()
# print(DBN.get_all_placemarks())