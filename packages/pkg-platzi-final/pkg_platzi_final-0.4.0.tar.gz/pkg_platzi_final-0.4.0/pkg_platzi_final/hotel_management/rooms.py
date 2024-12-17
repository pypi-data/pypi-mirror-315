class Room:
    def __init__(self, room_number, room_type, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.available = True

class RoomManagement:
    def __init__(self):
        self.rooms = {}

    def add_room(self, room):
        """Agrega una nueva habitación al sistema."""
        self.rooms[room.room_number] = room
        print(f'La habitación número {room.room_number} ha sido agregada!')

    def check_availability(self, room_number):
        """Verifica si una habitación está disponible."""
        room = self.rooms.get(room_number)
        if room and room.available:
            print(f'La habitación {room_number} está disponible!')
            return True
        else:
            print(f'La habitación {room_number} NO está disponible!')
            return False

    def update_availability(self, room_number):
        """Verifica si una habitación está disponible."""
        room = self.rooms.get(room_number)
        if room and room.available:
            room.available = False
            print(f'La habitación {room_number} ahora NO está disponible!')
            return False
        else:
            room.available = True
            print(f'La habitación {room_number} ahora está disponible!')
            return True
