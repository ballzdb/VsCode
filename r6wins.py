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
    operator = input("Operator you used this round was: ")
    if operator in Attacker.all_names:
        return Attacker(operator)
    elif operator in Defender.all_names:
        return Defender(operator)
    else:
        raise ValueError(f"'{operator}' is not a valid operator.")
    

def win_or_lose() -> bool:
    while True:
        try:
            result = input("WIN / LOSE: ")
            if result.lower() == "win":
                return True
            elif result.lower() == "lose":
                return False
            else:
                raise ValueError("Invalid input. Please enter 'WIN' or 'LOSE'.")
        except ValueError as e:
            print(e)
            continue
        break 


def calculate_statistics(): 
    now_opp = get_operator_of_this_round()
    now_result = win_or_lose()

    name = now_opp.name 

    if name not in stats:
        stats[name] = {"wins": 0, "losses": 0}

    if now_result:
        stats[name]["wins"] += 1
        print(f"Nice! {name} win added.")
    else:
        stats[name]["losses"] += 1
        print(f"GG. {name} loss added.")
        
    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=4)


if __name__ == "__main__":
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