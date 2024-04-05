import threading


NUM_SCREWDRIVERS = 5


class Doctor(threading.Thread):
    def __init__(self, doctor_id, screwdriver_id, screwdrivers):
        threading.Thread.__init__(self)
        self.doctor_id = doctor_id
        self.left_hand = screwdrivers[screwdriver_id - 1]
        self.right_hand = screwdrivers[screwdriver_id]

    def run(self):
        self.left_hand.get()
        self.right_hand.get()
        print(f"Doctor {self.doctor_id}: BLAST!")
        self.left_hand.put()
        self.right_hand.put()


class Screwdriver:
    def __init__(self, id):
        self.id = id
        self.lock = threading.Lock()

    def get(self):
        self.lock.acquire()

    def put(self):
        self.lock.release()


if __name__ == '__main__':
    screwdrivers = [Screwdriver(id) for id in range(NUM_SCREWDRIVERS)]
    doctors = [Doctor(doctor_id, screwdriver_id, screwdrivers) for doctor_id, screwdriver_id in zip(range(9, 14), range(NUM_SCREWDRIVERS))]
    for doctor in doctors:
        doctor.start()
