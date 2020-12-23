def load_data(filename):
    with open(filename) as f:
        player_data = {"p1":[],"p2":[]}
        active_player = "p1"
        for line in f:
            line = line.strip()
            if line.startswith("Player"):
                continue
            if line == "":
                active_player = "p2"
                continue
            
            player_data[active_player].append(int(line))
                
        return player_data


def simulate_round(data):

    winner = "p2"
    loser = "p1"
    if data["p1"][0] > data["p2"][0]:
        winner = "p1"
        loser = "p2"
        
    data[winner] += [data[winner][0], data[loser][0]]
    del data[winner][0]
    del data[loser][0]
    return data


def play_game(data):

    num_rounds = 0
    while data["p1"] and data["p2"]:
        num_rounds += 1
        data = simulate_round(data)
        if num_rounds % 100 == 0:
            print("Num rounds: {}".format(num_rounds))

    print("Game finished after {} rounds".format(num_rounds))
    return data

def find_winner_score(final_data):
    for p,v in final_data.items():
        if not v:
            continue
        score = 0
        count = 1
        for n in reversed(v):
            score += n*count
            count += 1
        print("{} wins with score of {}".format(p,score))


def simulate_round_recursive(data):
    # Check if there are enough cards to recurse
    if data["p1"][0] <= (len(data["p1"])-1) and data["p2"][0] <= (len(data["p2"])-1):
        deck_copy = {}
        deck_copy["p1"] = data["p1"][1:data["p1"][0]+1]
        deck_copy["p2"] = data["p2"][1:data["p2"][0]+1]
        winner, loser, _ = play_game_recursive(deck_copy)
        data[winner] += [data[winner][0], data[loser][0]]
        del data[winner][0]
        del data[loser][0]
    else:
        data = simulate_round(data)
    return data

def play_game_recursive(data):

    num_rounds = 0
    prev_states = set()
    while data["p1"] and data["p2"]:
        num_rounds += 1
        
        # Check if the previous state rule applis
        cur_state = (tuple(data["p1"]), tuple(data["p2"]))
        if cur_state in prev_states:
            print("Prev state matched, game finished fter {} rounds for p1".format(num_rounds))
            return "p1", "p2", data
        else:
            prev_states.add(cur_state)

        # Otherwise simulate a round of the game
        data = simulate_round_recursive(data)
        if num_rounds % 100 == 0:
            print("Num rounds: {}".format(num_rounds))

    print("Game finished after {} rounds".format(num_rounds))
    winner = "p2"
    loser = "p1"
    if len(data["p1"]) > len(data["p2"]):
        winner = "p1"
        loser = "p2"
    return winner, loser, data


if __name__ == '__main__':

    sample_data = load_data("day22/sample_input.txt")
    data = load_data("day22/input.txt") 

    # Part 1
    # final_data = play_game(data)
    # find_winner_score(final_data)

    # Part 2
    winner, loser, final_data = play_game_recursive(data)
    find_winner_score(final_data)