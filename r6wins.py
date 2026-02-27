import json

stats = {}

class Operator:
    def __init__(self, name, valid_list):
        if name not in valid_list:
            raise ValueError(f"'{name}' is not a valid operator.")
        self.name = name

class Attacker(Operator):
    all_names = [
        "Sledge", "Thatcher", "Ash", "Thermite", "Twitch", "Montagne", "Glaz", "Fuze", "Blitz", "IQ",
        "Buck", "Blackbeard", "Capitão", "Hibana", "Jackal", "Ying", "Zofia", "Dokkaebi", "Lion", "Finka",
        "Maverick", "Nomad", "Gridlock", "Nøkk", "Amaru", "Kali", "Iana", "Ace", "Zero", "Flores",
        "Osa", "Sens", "Grim", "Brava", "Ram", "Deimos"
    ]
    def __init__(self, name):
        super().__init__(name, Attacker.all_names)

class Defender(Operator):
    all_names = [
        "Smoke", "Mute", "Castle", "Pulse", "Doc", "Rook", "Kapkan", "Tachanka", "Jäger", "Bandit",
        "Frost", "Valkyrie", "Caveira", "Echo", "Mira", "Lesion", "Ela", "Vigil", "Maestro", "Alibi",
        "Clash", "Kaid", "Mozzie", "Wamai", "Goyo", "Warden", "Oryx", "Melusi", "Aruni", "Thunderbird",
        "Thorn", "Azami"
    ]
    def __init__(self, name):
        super().__init__(name, Defender.all_names)


def get_operator_of_this_round():
    operator_input = input("Operator you used this round was: ").strip()
    
    # Check Attackers
    for name in Attacker.all_names:
        if name.lower() == operator_input.lower():
            return Attacker(name)
            
    # Check Defenders 
    for name in Defender.all_names:
        if name.lower() == operator_input.lower():
            return Defender(name)

    raise ValueError(f"'{operator_input}' is not a valid operator.")
    

def win_or_lose() -> bool:
    while True:
        try:
            result = input("WIN / LOSE: ").strip().lower()
            if result == "win":
                return True
            elif result == "lose":
                return False
            else:
                raise ValueError("Invalid input. Please enter 'WIN' or 'LOSE'.")
        except ValueError as e:
            print(e)
            continue

def display_statistics():  #when keyboard interrupt is detected, this function will be called to display the statistics of all operators that was mentioned by the exact user in the stats dictionary
    if not stats:
        print("No statistics available.")
        return
    print("Operator Statistics:")
    for operator in sorted(stats.keys()):
        record = stats[operator]
        wins = record.get("wins", 0)
        losses = record.get("losses", 0)
        kills = record.get("kills", 0)
        deaths = record.get("deaths", 0)

        total = wins + losses
        win_rate = (wins / total) * 100 if total > 0 else 0
        # If deaths are 0, K/D is simply the number of kills
        kd_ratio = kills / deaths if deaths > 0 else float(kills)

        print(f"{operator}: {wins}W-{losses}L ({win_rate:.2f}%) | K/D: {kd_ratio:.2f} ({kills}K/{deaths}D)")


def calculate_statistics(): # calculates the statistics for the current round and updates the stats dictionary and the .json file
    now_opp = get_operator_of_this_round()
    now_result = win_or_lose()
    kills, deaths = input_kills_and_deaths()

    if kills is None: # Handle cancellation of K/D input
        print("K/D input cancelled. Recording round with 0 kills and 0 deaths.")
        kills, deaths = 0, 0

    name = now_opp.name 

    if name not in stats:
        stats[name] = {"wins": 0, "losses": 0, "kills": 0, "deaths": 0}

    stats[name].setdefault("kills", 0)
    stats[name].setdefault("deaths", 0)

    if now_result:
        stats[name]["wins"] += 1
        print(f"Nice! {name} win added.")
    else:
        stats[name]["losses"] += 1
        print(f"GG. {name} loss added.")
        
    stats[name]["kills"] += kills
    stats[name]["deaths"] += deaths
    print(f"Added {kills} kills and {deaths} deaths for {name}.")

    KD = stats[name]["kills"] / stats[name]["deaths"] if stats[name]["deaths"] > 0 else float(stats[name]["kills"])
    print(f"Current K/D for {name}: {KD:.2f}")

    winrate = (stats[name]["wins"] / (stats[name]["losses"]) * 100) if (stats[name]["wins"] + stats[name]["losses"]) > 0 else 0
    print(f"Current winrate for {name}: {winrate:.2f}%")


    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=4)


def input_kills_and_deaths():
    while True:
        try:
            kills = int(input("Number of kills: ").strip())
            deaths = int(input("Number of deaths: ").strip())
            if kills < 0 or deaths < 0:
                raise ValueError("Kills and deaths cannot be negative.")
            return kills, deaths
        except ValueError as e:
            print(e)
            continue
        except KeyboardInterrupt:
            print("\nExiting kill/death input. Returning to main menu.")
            return None, None


if __name__ == "__main__": #main loop of the program that does everything
    try:
        with open("stats.json", "r") as f:
            stats = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        stats = {}
    while True:
        try:
            calculate_statistics()
        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            display_statistics()
            print("Exiting program. Goodbye!")
            exit()
