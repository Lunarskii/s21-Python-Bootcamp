import grpc
import test_pb2_grpc
import test_pb2
from concurrent.futures import ThreadPoolExecutor
from random import randint, choice, uniform


SHIP_NAMES = ['Amphibious', 'Aviso', 'Barque', 'Barquentine', 'Battlecruiser', 'Battleship', 'Bilander', 'Bireme',
              'Birlinn', 'Blockade runner', 'Boita', 'Brig', 'Brigantine', 'Caravel', 'Carrack', 'Cartel', 'Catboat',
              'Clipper', 'Coastal defense ship', 'Cog', 'Collier', 'Cruise ship', 'Destroyer escort', 'Dhow',
              'Drekar', 'Dromons', 'East Indiaman', 'Felucca', 'Fire ship', 'Floating fuel station', 'Fluyt', 'Galleass',
              'Galleon', 'Galley', 'Galliot', 'Gunboat', 'Hydrofoil', 'Ironclad', 'Junk', 'Karve', 'Ketch', 'Knarr']
RANKS = ['Captain', 'Chief officer', 'Second officer', 'Third officer', 'Cargo officer']
NAMES = ['Alice', 'Bob', 'Charlie', 'David', 'Emma', 'Frank', 'Liam', 'Noah', 'Oliver', 'James', 'Elijah', 'William',
         'Henry', 'Lucas', 'Benjamin', 'Theodore', 'Mateo', 'Levi', 'Sebastian', 'Daniel', 'Jack', 'Michael', 'Owen',
         'Alexander', 'Asher', 'Samuel', 'Ethan', 'Leo', 'Jackson', 'Mason', 'Ezra', 'John', 'Hudson', 'Luca', 'Aiden',
         'Joseph', 'Jacob', 'Logan', 'Luke', 'Julian', 'Gabriel', 'Grayson', 'Wyatt', 'Matthew', 'Maverick', 'Dylan',
         'Isaac', 'Elias', 'Anthony', 'Thomas', 'Jayden', 'Carter', 'Santiago', 'Ezekiel', 'Charles', 'Josiah', 'Caleb']
LAST_NAMES = ['Adams', 'Allen', 'Anderson', 'Armstrong', 'Austin', 'Alvarez', 'Ayala', 'Aguilar', 'Atkinson', 'Arnold',
              'Baker', 'Brown', 'Bailey', 'Barnes', 'Brooks', 'Bell', 'Bennett', 'Bryant', 'Blair', 'Burke', 'Carter',
              'Clark', 'Collins', 'Cooper', 'Campbell', 'Cruz', 'Carr', 'Carlson', 'Cameron', 'Casey', 'Davis', 'Diaz',
              'Dixon', 'Daniels', 'Douglas', 'Dunn', 'Dean', 'Duke', 'Day', 'Doyle', 'Edwards', 'Evans', 'Ellis', 'Eaton',
              'Estrada', 'English', 'Erickson', 'Emerson', 'Ellison', 'Flores', 'Fisher', 'Ferguson', 'Freeman', 'Ford']


class Service(test_pb2_grpc.ServiceServicer):
    def SendData(self, request, context):
        ships = [
            test_pb2.Ship(
                alignment=choice(test_pb2.Ship.Alignment.values()),
                name=choice(SHIP_NAMES),
                ship_class=choice(test_pb2.Ship.Class.values()),
                length=uniform(80, 20000),
                crew_size=randint(4, 500),
                armed=bool(randint(0, 1)),
                officers=[
                    test_pb2.Ship.Officer(
                        first_name=choice(NAMES),
                        last_name=choice(LAST_NAMES),
                        rank=choice(RANKS)
                    ) for _ in range(randint(0, 10))
                ]
            ) for _ in range(randint(1, 10))
        ]

        return test_pb2.Reply(ships=ships)


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_ServiceServicer_to_server(Service(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
