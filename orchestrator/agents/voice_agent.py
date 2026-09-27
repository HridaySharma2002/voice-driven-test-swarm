import time
from test_runner import run_tests_and_parse

def listen_and_execute():
    print("\n[MIC BYPASSED] Simulating voice command capture...")
    time.sleep(1)

    command = "run api regression tests"
    print(f"Recognized: '{command}'")

    if "run" in command and ("test" in command or "regression" in command):
        print("Intent recognized: Triggering CI/CD Pipeline...")
        run_tests_and_parse()
    else:
        print("No actionable intent detected. Ignoring.")

if __name__ == "__main__":
    listen_and_execute()
