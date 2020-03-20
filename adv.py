from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
#world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

opposite_dirs = {'n':'s', 'e':'w', 'w':'e', 's':'n'}

# fill out traversal path
def do_traversal():
    player.current_room = world.starting_room
    graph = {}
    q = [ [player.current_room.id] ]
    travel_path = []


    def add_knowledge(room):
        nonlocal graph
        node_knowledge = graph.get(room.id)
        exits = room.get_exits()
        if node_knowledge is None:
            graph[room.id] = dict(zip(exits, '?'*len(exits)))
            node_knowledge = graph[room.id]
#        print('Graph: ', graph)

    def is_dead_end(room):
        for exit in room.get_exits():
            if graph[room.id].get(exit) == '?':
                return False
        return True

    add_knowledge(player.current_room)

    while len(q):
        room = player.current_room
        exits = room.get_exits()

        # dead end case
        if is_dead_end(room):
#            print(f'Dead end {room.id} {len(q)}')

            last_path = q.pop()  # stack
            last_room = last_path[-1]
            travel_back = '?'

            if len(q) == 0:
                continue

#            print(type(graph[room.id]))
#            print(type(last_room))

            for _dir in graph[room.id]:
                if graph[room.id][_dir] == last_room:
                    travel_back = _dir
                    break

            # go back to previous room since reached dead end
#            print('Travel back', travel_back)

            player.travel(travel_back, travel_path)
            continue

        # room with unexplored rooms case
        else:
            node_knowledge = graph[room.id]
            for exit in exits:
#                print('Exit: ', exit)
                current_path = q[-1]
                result = node_knowledge.get(exit)
 #               print('Result: ', result)
                # unexplored room
                if result == '?':
                    player.travel(exit, travel_path)  # travel towards it
                    new_room = player.current_room
                    graph[room.id][exit] = new_room.id
                    add_knowledge(new_room)
                    graph[new_room.id][ opposite_dirs[exit] ] = room.id

#                    print('Graph: ', graph)

                    path = current_path.copy()
                    path.append(room.id)
                    q.append(path)
                    break
                # explored room
                else:
                    pass
    return travel_path

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

traversal_path = do_traversal()

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

def print_results():
    if len(visited_rooms) == len(room_graph):
        print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
    else:
        print("TESTS FAILED: INCOMPLETE TRAVERSAL")
        print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")




#print(world.rooms)
print_results()



#######
# UNCOMMENT TO WALK AROUND
#######
#player.current_room.print_room_description(player)
while False:
    print(traversal_path)

    cmds = input("-> ").lower().split(" ")

    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], show_rooms=True)
        visited_rooms.add(player.current_room)


    elif cmds[0] == "q":
        break
    elif cmds[0] == "p":
        world.print_rooms()
    else:
        print("I did not understand that command.")
