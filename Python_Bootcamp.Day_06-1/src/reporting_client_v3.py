import sys
import reporting_client_v2
import json

from sqlalchemy import create_engine, func, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
DB_URL = 'postgresql://postgres:postgres@localhost/postgres'


class Officer(Base):
    __tablename__ = 'officers'
    id = Column(Integer, primary_key=True)
    ship_id = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    rank = Column(String)


class Ship(Base):
    __tablename__ = 'ships'
    id = Column(Integer, primary_key=True)
    alignment = Column(String)
    name = Column(String)
    ship_class = Column(String)
    length = Column(Float)
    crew_size = Column(Integer)
    armed = Column(Boolean)


class DB:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()

    def run_query(self, query):
        return self.session.query(query)

    def __del__(self):
        self.session.close()


def create_ship(db: DB, data):
    db.add(
        Ship(
            alignment=data.alignment,
            name=data.name,
            ship_class=data.ship_class,
            length=data.length,
            crew_size=data.crew_size,
            armed=data.armed
        )
    )
    max_ship_id = db.run_query(func.max(Ship.id)).scalar()
    if max_ship_id:
        [
            db.add(
                Officer(
                    ship_id=max_ship_id,
                    first_name=officer.first_name,
                    last_name=officer.last_name,
                    rank=officer.rank
                )
            )
            for officer in data.officers
        ]
    print(data.model_dump_json(by_alias=True, indent=4))


def list_traitors(db):
    ships = db.run_query(Ship).all()
    ally = []
    enemy = []
    for ship in ships:
        officers = db.run_query(Officer).filter_by(ship_id=ship.id)
        if ship.alignment == 'Ally':
            [ally.append(officer) for officer in officers]
        else:
            [enemy.append(officer) for officer in officers]
    for ally_officer in ally:
        for enemy_officer in enemy:
            if ally_officer.first_name == enemy_officer.first_name and ally_officer.last_name == enemy_officer.last_name:
                print(
                    json.dumps
                    (
                        {
                            'first_name': ally_officer.first_name,
                            'last_name': ally_officer.last_name,
                            'rank': ally_officer.rank
                        }
                    )
                )


if __name__ == '__main__':
    db = DB(DB_URL)
    args = sys.argv
    if 'scan' in args:
        elem_index = args.index('scan')
        if elem_index + 6 < len(args):
            ships = reporting_client_v2.main(list(map(float, args[elem_index + 1:])))
            [create_ship(db, ship) for ship in ships]
    elif 'list_traitors' in args:
        list_traitors(db)
