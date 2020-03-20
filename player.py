class Player:
    def __init__(self, starting_room):
        self.current_room = starting_room

    def travel(self, direction, travel_path=None, show_rooms = False):
        next_room = self.current_room.get_room_in_direction(direction)
#        print('Traveling to', next_room.id)

        if travel_path is not None:
            travel_path.append(direction)

        if next_room is not None:
            self.current_room = next_room
            if (show_rooms):
                next_room.print_room_description(self)
        else:
            print("You cannot move in that direction.")
