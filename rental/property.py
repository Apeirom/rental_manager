# rental/property.py
import uuid

class Property:
    def __init__(self, property_name, owner_name, address, room_count=0):
        self.id = str(uuid.uuid4())
        self.property_name = property_name
        self.owner_name = owner_name
        self.address = address
        self.room_count = room_count

    def add_room(self):
        self.room_count += 1

    def remove_room(self):
        self.room_count -= 1
    