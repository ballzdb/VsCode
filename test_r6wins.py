import json
import r6wins

# --- Simple Test Framework ---

# We need to "mock" (fake) the input and print functions so we can 
# test the code automatically without a human typing.

# 2. Create buffers to hold our fake inputs and capture outputs
fake_inputs = []
captured_output = []

# 3. Define our fake functions
def mock_input(prompt=""):
    if len(fake_inputs) > 0:
        return fake_inputs.pop(0)
    raise Exception("Test ran out of inputs!")

def mock_print(*args, **kwargs):
    # Convert all arguments to strings and join them, just like real print
    msg = " ".join(map(str, args))
    captured_output.append(msg)

class MockFile:
    def __init__(self, filename, mode): pass
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass
    def write(self, data): pass # We just ignore file writes for these tests
    def read(self): return "{}"

def mock_open(filename, mode="r", *args, **kwargs):
    return MockFile(filename, mode)

# 4. Helper to run a test
def run_test(test_name, test_function):
    # Setup
    r6wins.input = mock_input
    r6wins.print = mock_print
    r6wins.open = mock_open
    fake_inputs.clear()
    captured_output.clear()
    r6wins.stats = {} # Reset stats

    try:
        test_function()
        print(f"PASS: {test_name}")
    except AssertionError as e:
        print(f"FAIL: {test_name} - {e}")
    except Exception as e:
        print(f"ERROR: {test_name} - {e}")
    finally:
        # Teardown (Remove mocks so r6wins uses builtins again)
        del r6wins.input
        del r6wins.print
        del r6wins.open

# --- The Actual Tests ---

def test_get_operator():
    fake_inputs.append("ash")
    op = r6wins.get_operator_of_this_round()
    assert op.name == "Ash"
    assert isinstance(op, r6wins.Attacker)

def test_win_or_lose():
    fake_inputs.append("win")
    assert r6wins.win_or_lose() == True
    
    fake_inputs.append("LOSE")
    assert r6wins.win_or_lose() == False

def test_input_kills_deaths():
    fake_inputs.append("5")
    fake_inputs.append("2")
    k, d = r6wins.input_kills_and_deaths()
    assert k == 5
    assert d == 2

def test_calculate_statistics():
    # Simulate: Ash, Win, 10 kills, 2 deaths
    fake_inputs.extend(["Ash", "win", "10", "2"])
    
    r6wins.calculate_statistics()
    
    # Check if stats were updated in the dictionary
    assert r6wins.stats["Ash"]["wins"] == 1
    assert r6wins.stats["Ash"]["kills"] == 10
    
    # Check if the program printed the correct confirmation
    output_text = "\n".join(captured_output)
    assert "Nice! Ash win added." in output_text
    assert "Current K/D for Ash: 5.00" in output_text

def test_display_statistics():
    # Manually set up some stats
    r6wins.stats = {
        "Jäger": {"wins": 10, "losses": 0, "kills": 20, "deaths": 5}
    }
    r6wins.display_statistics()
    
    output_text = "\n".join(captured_output)
    assert "Jäger: 10W-0L (100.00%) | K/D: 4.00 (20K/5D)" in output_text

if __name__ == "__main__":
    print("Running custom tests...\n")
    run_test("Get Operator", test_get_operator)
    run_test("Win/Lose Logic", test_win_or_lose)
    run_test("Kills/Deaths Input", test_input_kills_deaths)
    run_test("Calculate Statistics (Full Round)", test_calculate_statistics)
    run_test("Display Statistics", test_display_statistics)
    print("\nTests finished.")
