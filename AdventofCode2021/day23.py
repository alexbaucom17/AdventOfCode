import sys
sys.path.append('.')
import aoc
import math
from dataclasses import dataclass, field
from enum import Enum
import queue
from typing import Any
import cProfile
from collections import defaultdict

class State(Enum):
    E = 0,
    A = 1,
    B = 2,
    C = 3,
    D = 4
    def __str__(self):
        if self.name == 'E':
            return '.'
        else:
            return self.name

class Room(Enum):
    H = 0,
    A = 1,
    B = 2, 
    C = 3,
    D = 4

state_to_room = {State.A: Room.A, State.B: Room.B, State.C: Room.C, State.D: Room.D}
room_to_state = {Room.A: State.A, Room.B: State.B, Room.C: State.C, Room.D: State.D}
move_costs = {State.A:1, State.B:10, State.C:100, State.D:1000}
n_slots = 4
# Compensate for extra steps calculated during estimated cost
estimated_cost_offset = -1*sum([i for i in range(n_slots-1)])

@dataclass(eq=True, frozen=True)
class RoomId:
    room: Room
    index: int

    def is_hall(self):
        return self.room == Room.H
    def is_A(self):
        return self.room == Room.A
    def is_B(self):
        return self.room == Room.B
    def is_C(self):
        return self.room == Room.C
    def is_D(self):
        return self.room == Room.D
    def is_doorway(self):
        return self.is_hall() and self.index in room_to_doorway_index.values()
    def __str__(self):
        return f"{self.room.name}{self.index}"
    def __repr__(self):
        return str(self)
    def __eq__(self, other):
        return self.index == other.index and self.room == other.room
    @classmethod
    def from_str(cls, s):
        room = Room[s[0]]
        index = int(s[1:])
        return cls(room, index)

room_to_doorway_index = {Room.A: 2, Room.B: 4, Room.C: 6, Room.D: 8}

def build_all_room_ids():
    ids = []
    for room in [Room.H, Room.A, Room.B, Room.C, Room.D]:
        num = n_slots if not room == Room.H else 11
        for i in range(num):
            ids.append(RoomId(room, i))
    return ids
all_room_ids = build_all_room_ids()

def room_state_match(room: Room, state: State) -> bool:
    # print(room)
    # print(state)
    # print(state_to_room[state])
    return room == state_to_room[state]

def room_doorway(room: RoomId):
    return RoomId(Room.H, room_to_doorway_index[room.room])

def next_hall_step(start: RoomId, goal: RoomId):
    assert start.is_hall()
    assert goal.is_hall()
    dir = goal.index - start.index
    new_index = start.index + int(math.copysign(1, dir))
    return RoomId(Room.H, new_index)

def next_alley_step(start: RoomId, out: bool):
    step = -1 if out else 1
    return RoomId(start.room, start.index + step)

def next_room(start: RoomId, goal: RoomId) -> RoomId:
    if start.is_hall() and goal.is_hall():
        return next_hall_step(start, goal)
    elif not start.is_hall() and goal.is_hall():
        if start.index == 0:
            return room_doorway(start)
        else:
            return next_alley_step(start, out=True)
    elif start.is_hall() and not goal.is_hall():
        if start == room_doorway(goal):
            return RoomId(goal.room, 0)
        else:
            return next_hall_step(start, room_doorway(goal))
    else: # start and end are not hall
        if start.room == goal.room:
            return next_alley_step(start, out=start.index>goal.index)
        else:
            if start.index == 0:
                return room_doorway(start)
            else:
                return next_alley_step(start, out=True)

def build_one_path(start: RoomId, goal: RoomId, paths):
    current = start
    out_path = []
    count = 0
    # print(f"Building path from {start} to {goal}")
    while current != goal:
        current = next_room(current, goal)
        out_path.append(current)

        if (current, goal) in paths:
            out_path += paths[(current, goal)]
            # print(f"Found memoized path from {current} to {goal}")
            break

        count += 1
        if count > 50:
            raise ValueError(f"Got stuck in loop when building path from {start} to {goal}. Path: {out_path}")

    return out_path

def build_all_paths():
    paths = {}
    for start in all_room_ids:
        for goal in all_room_ids:
            path = []
            if start != goal:
                path = build_one_path(start, goal, paths)
            paths[(start, goal)] = path
    return paths
all_paths = build_all_paths()

halls_non_door = [id for id in all_room_ids if id.is_hall() and not id.is_doorway()]
def possible_move_locations(agent: State):
    if agent == State.E: 
        return []
    alley_locations = [RoomId(state_to_room[agent], i) for i in range(n_slots)]
    return halls_non_door + alley_locations

class AllRoomState:
    def __init__(self, A, B, C, D):
        # ids = set()
        # for k in [A,B,C,D]:
        #     assert len(k) == n_slots
        #     for i in range(n_slots):
        #         assert type(k[i]) == RoomId
        #         assert k[i] not in ids, f"Duplicate room {k[i]}"
        #         ids.add(k[i])
            
        self.data = {
            State.A: list(A),
            State.B: list(B),
            State.C: list(C),
            State.D: list(D)
        }
        # self.state_mem = defaultdict(lambda: State.E)
        # self.mem_set = False

    def __eq__(self, other):
        for state, locs in self.data.items():
            for id in locs:
                if id not in other.data[state]:
                    return False
        return True

    def as_tuple(self):
        return tuple(self.data[State.A] + self.data[State.B] + self.data[State.C] + self.data[State.D])

    @classmethod
    def from_tuple(cls, T):
        assert len(T) == 4*n_slots
        return cls(T[0:n_slots], T[n_slots:2*n_slots], T[2*n_slots:3*n_slots], T[3*n_slots:4*n_slots])

    # def _mem_room_state(self):
    #     self.mem_set = True
    #     for agent, locs in self.data.items():
    #         for id in locs:
    #             self.state_mem[id] = agent

    # def get_room_state_mem(self, room: RoomId):
    #     if not self.mem_set:
    #         self._mem_room_state()
    #     return self.state_mem[room]

    def get_room_state(self, room: RoomId):
        for agent, locs in self.data.items():
            for id in locs:
                if room == id:
                    return agent
        return State.E

    def _move_agent(self, start: RoomId, goal: RoomId):
        agent = self.get_room_state(start)
        assert agent != State.E
        agent_locations = self.data[agent]
        i = agent_locations.index(start)
        self.data[agent][i] = goal
        # self.mem_set = False
        return agent

    def _room_has_invalid_occupants(self, room: Room):
        for agent, locs in self.data.items():
            for id in locs:
                if id.room == room and not room_state_match(room, agent):
                    return True
        return False

    def _room_fully_valid(self, room: Room):
        if room == Room.H:
            return False
        state_locs = self.data[room_to_state[room]]
        for loc in state_locs:
            if loc.room != room:
                return False
        return True

    def _room_behind_fully_valid(self, id: RoomId):
        if id.room == Room.H:
            return False
        if id.index == (n_slots - 1):
            return True
        state_locs = self.data[room_to_state[id.room]]
        valid_ix = [False for i in range(n_slots)]
        for loc in state_locs:
            if loc.room == id.room:
                valid_ix[loc.index] = True
        return all(valid_ix[id.index:])

    def _is_path_blocked(self, start_loc, end_loc):
        path = all_paths[(start_loc, end_loc)]
        for space in path:
            if self.get_room_state(space) != State.E:
                return True
        return False

    def _is_blocking_back_of_room(self, loc: RoomId):
        for i in range(loc.index+1, n_slots):
            if self.get_room_state(RoomId(loc.room, i)) == State.E:
                return True
        return False

    def _is_valid_move(self, start_loc: RoomId, end_loc: RoomId):
        start_state = self.get_room_state(start_loc)
        end_state = self.get_room_state(end_loc)

        if start_state == State.E:
            # print('empty start')
            return False
        if end_state != State.E:
            # print('empty end')
            return False
        if end_loc.is_doorway():
            # print('end doorwar')
            return False
        if start_loc.is_hall() and end_loc.is_hall():
            # print('only hall')
            return False
        if self._is_path_blocked(start_loc, end_loc):
            # print('blocked')
            return False
        if not start_loc.is_hall():
            if self._room_fully_valid(start_loc.room):
                return False
            if room_state_match(start_loc.room, start_state) and self._room_behind_fully_valid(start_loc):
                # print('Valid at back of room, shouldn't move)
                return False
        if not end_loc.is_hall():
            if not room_state_match(end_loc.room, start_state):
                # print('not hall and not match')
                return False
            if self._room_has_invalid_occupants(end_loc.room):
                # print('not hall and invalid others')
                return False
            if self._is_blocking_back_of_room(end_loc):
                # print('Blocking back of room')
                return False
        return True

    def maybe_do_move(self, start_loc: RoomId, end_loc: RoomId):
        if not self._is_valid_move(start_loc, end_loc):
            return False, None
        agent = self._move_agent(start_loc, end_loc)
        return True, agent
        
    def possible_moves(self):
        moves = []
        for state, locs in self.data.items():
            for id in locs:
                for goal in possible_move_locations(state):
                    moves.append((id, goal))
        return moves

    def cost_from_finished(self):
        total_cost = 0
        for state, locs in self.data.items():
            goal = RoomId(state_to_room[state], n_slots-1)
            total_steps = estimated_cost_offset
            for loc in locs:
                total_steps += len(all_paths[(loc, goal)])
            total_cost += total_steps * move_costs[state]
        return total_cost


    def _to_locs(self):
        area = {
            Room.H: [State.E] * 11,
            Room.A: [State.E] * n_slots,
            Room.B: [State.E] * n_slots,
            Room.C: [State.E] * n_slots,
            Room.D: [State.E] * n_slots,
        }
        for state, locs in self.data.items():
            for id in locs:
                area[id.room][id.index] = state
        return area

    def __str__(self):
        locs = self._to_locs()
        s = "#############\n#"
        for c in locs[Room.H]:
            s += str(c)
        s += "#\n"
        for i in range(n_slots):
            lpad = "  #"
            rpad = "#  "
            if i == 0:
                lpad = "###"
                rpad = "###"
            s += f"{lpad}{locs[Room.A][i]}#{locs[Room.B][i]}#{locs[Room.C][i]}#{locs[Room.D][i]}{rpad}\n"
        s += "  #########  "
        return s

sample_initial_room = AllRoomState(
    A = [RoomId.from_str('A3'), RoomId.from_str('C2'), RoomId.from_str('D1'), RoomId.from_str('D3')],
    B = [RoomId.from_str('A0'), RoomId.from_str('B2'), RoomId.from_str('C0'), RoomId.from_str('C1')],
    C = [RoomId.from_str('B0'), RoomId.from_str('B1'), RoomId.from_str('C3'), RoomId.from_str('D2')],
    D = [RoomId.from_str('A1'), RoomId.from_str('A2'), RoomId.from_str('B3'), RoomId.from_str('D0')],
)
real_initial_room = AllRoomState(
    A = [RoomId.from_str('A0'), RoomId.from_str('C0'), RoomId.from_str('C2'), RoomId.from_str('D1')],
    B = [RoomId.from_str('A3'), RoomId.from_str('B2'), RoomId.from_str('C1'), RoomId.from_str('D0')],
    C = [RoomId.from_str('B1'), RoomId.from_str('B3'), RoomId.from_str('D2'), RoomId.from_str('D3')],
    D = [RoomId.from_str('A1'), RoomId.from_str('A2'), RoomId.from_str('B0'), RoomId.from_str('C3')],
)
final_room = AllRoomState(
    A = [RoomId.from_str('A0'), RoomId.from_str('A1'), RoomId.from_str('A2'), RoomId.from_str('A3')],
    B = [RoomId.from_str('B0'), RoomId.from_str('B1'), RoomId.from_str('B2'), RoomId.from_str('B3')],
    C = [RoomId.from_str('C0'), RoomId.from_str('C1'), RoomId.from_str('C2'), RoomId.from_str('C3')],
    D = [RoomId.from_str('D0'), RoomId.from_str('D1'), RoomId.from_str('D2'), RoomId.from_str('D3')],
)
# test_room = AllRoomState(
#     A = [RoomId.from_str('A1'), RoomId.from_str('H1'), RoomId.from_str('D1'), RoomId.from_str('D1')],
#     B = [RoomId.from_str('B1'), RoomId.from_str('H3'), RoomId.from_str('D1'), RoomId.from_str('D1')],
#     C = [RoomId.from_str('C1'), RoomId.from_str('H4'), RoomId.from_str('D1'), RoomId.from_str('D1')],
#     D = [RoomId.from_str('D1'), RoomId.from_str('H0'), RoomId.from_str('D1'), RoomId.from_str('D1')],
# )

@dataclass(order=True)
class PrioritizedItem:
    sort_cost: int
    state_tuple: Any=field(compare=False)
    steps: Any=field(compare=False)
    actual_cost: int=field(compare=False)

# print(test_room == final_room)
# print(test_room.maybe_do_move(RoomId.from_str('H10'), RoomId.from_str('C0')))
# print(test_room)
# print(sample_initial_room.maybe_do_move(RoomId.from_str('B0'), RoomId.from_str('C0')))
# print(sample_initial_room)

def draw_moves(room, moves):
    print(room)
    for move in moves:
        print(f"Move {room.get_room_state(move[0])} from {move[0]} to {move[1]}")
        ok = room.maybe_do_move(move[0], move[1])
        assert ok
        print(room)

# draw_moves(sample_initial_room, [(RoomId.from_str('C0'), RoomId.from_str('H3')), (RoomId.from_str('B0'), RoomId.from_str('C0'))])

def part1():
    q = queue.PriorityQueue()
    explored = set()
    start_room = real_initial_room
    print(start_room)
    q.put(PrioritizedItem(0, start_room.as_tuple(), [], 0))
    iter_count = 0

    while not q.empty():
    # for i in range(10):
        item = q.get()
        iter_count += 1
        if iter_count % 10000 == 0:
            print(iter_count)
            # print(item.state_tuple)
            print(f"Cost: {item.actual_cost}, Sort cost: {item.sort_cost}, steps: {item.steps}")
            state = AllRoomState.from_tuple(item.state_tuple)
            print(state)

        if item.state_tuple in explored:
            continue

        state = AllRoomState.from_tuple(item.state_tuple)
        # print(state)

        if state == final_room:
            print("-----------------Found!-------------")
            print(item.actual_cost)
            print(item.steps)
            draw_moves(start_room, item.steps)
            break

        explored.add(item.state_tuple)
        for move in state.possible_moves():
            tmp_state = AllRoomState.from_tuple(item.state_tuple)
            ok, moving_agent = tmp_state.maybe_do_move(move[0], move[1])
            if not ok: 
                continue
            move_len = len(all_paths[move])
            move_cost = move_costs[moving_agent] * move_len
            new_actual_cost = item.actual_cost + move_cost
            new_sort_cost = new_actual_cost + tmp_state.cost_from_finished()
            new_item = PrioritizedItem(new_sort_cost, tmp_state.as_tuple(), item.steps + [move], new_actual_cost)
            # print(new_item)
            q.put(new_item)
        # print(explored)
        # print("-------------------")

    print("Finished")

# pr = cProfile.Profile()
# pr.enable()
# pr.run('part1()')
# pr.disable()
# import pstats
# p = pstats.Stats(pr)
# p.sort_stats(pstats.SortKey.TIME)
# p.print_stats()
# p.print_callers('get_room_state')

part1()

