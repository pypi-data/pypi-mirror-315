import subprocess
import sys
import re
import time
import random
import string

def check_command(command):
    return subprocess.call(['which', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def argon2_hash(password, salt, time_cost, memory_cost):
    result = subprocess.run(
        ['argon2', password, '-t', time_cost, '-k', memory_cost, '-p', '1', '-id', '-v', '13', '-r', salt],
        capture_output=True,
        text=True
    )
    return result.stdout.splitlines()[0]

def main():
    required_utils = ['argon2', 'xxd', 'bc']
    for util in required_utils:
        if not check_command(util):
            print(f"{util} is not installed. Please install it and try again.")
            return

    challenge = sys.argv[1] if len(sys.argv) > 1 else input("Enter Challenge Code: ").strip()

    if not re.match(r'^([0-9]+):([0-9]+):([A-Za-z0-9]+):([0-9]+)$', challenge):
        print("Invalid challenge format. Expected format: memory_cost:time_cost:salt:difficulty")
        return

    memory_cost, time_cost, salt, difficulty = map(str.strip, challenge.split(':'))

    print(f"Memory Cost: {memory_cost}")
    print(f"Time Cost: {time_cost}")
    print(f"Salt: {salt}")
    print(f"Difficulty: {difficulty}")

    pw_prefix = f"UNBLOCK-{generate_random_string(8)}-"
    difficulty_raw = round(256 ** (4 - len(difficulty) / 256))

    print(f"Estimated iterations: {difficulty}")
    print(f"Time Cost: {time_cost}\n")

    n = 1
    start_time = time.time()

    while True:
        pw = f"{pw_prefix}{n}"
        hash_result = argon2_hash(pw, salt, time_cost, memory_cost)
        hash_bytes = hash_result[:8]

        if int(hash_bytes, 16) < difficulty_raw:
            print("\nSOLUTION FOUND")
            print(f"Your unblock code is: {pw}")
            print("This is the code you enter into the site to pass the challenge.\n")
            return

        elapsed_time = time.time() - start_time
        print(f"\rElapsed Time: {elapsed_time:.0f} seconds.", end='')

        n += 1

if __name__ == "__main__":
    main()
