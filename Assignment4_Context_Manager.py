import time
import tracemalloc
import os
import shutil
from contextlib import contextmanager
from functools import wraps

class DatabaseConnection:
    def __init__(self, host="localhost", port=5432, database="mydb"):
        self.host = host
        self.port = port
        self.database = database

    def __enter__(self):
        print("[db] Connecting...")
        print("[db] Connection established!")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("[db] Committing transaction...")
        else:
            print(f"[db] Exception detected: {exc_type.__name__} - Rolling back...")
        print("[db] Connection closed!")

    def execute(self, query):
        print(f"[db] Executing: {query}")



class TimerContext:
    def __init__(self, label="Operation"):
        self.label = label

    def __enter__(self):
        print(f"[Time] Starting: {self.label}")
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        print(f"[Timer] {self.label} completed in {end - self.start:.6f} sec")


@contextmanager
def measure_memory(label="Operation"):
    tracemalloc.start()
    yield
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"[Memory] {label}:")
    print(f"Current: {current / 1024:.2f} KB")
    print(f"Peak: {peak / 1024:.2f} KB")



@contextmanager
def file_transaction(filepath):
    temp_file = filepath + ".tmp"

    if os.path.exists(filepath):
        shutil.copy(filepath, temp_file)
    else:
        open(temp_file, "w").close()

    try:
        yield temp_file
        shutil.move(temp_file, filepath)
        print(f"[File] Successfully wrote: {filepath}")
    except Exception as e:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        print(f"[File] Error occurred: {e} (Original preserved)")



def with_transaction(db_connection_class):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with db_connection_class() as db:
                kwargs["db"] = db
                return func(*args, **kwargs)
        return wrapper
    return decorator


def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[Log] Starting: {func.__name__}")
        start = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"[Log] Error: {e}")
            raise
        finally:
            end = time.time()
            print(f"[Log] Finished in {end - start:.6f} seconds")
    return wrapper




with DatabaseConnection() as db:
    db.execute("SELECT * FROM users")


with TimerContext("Computing"):
    time.sleep(0.5)


with measure_memory("List"):
    data = [i for i in range(100000)]


def write_file(path):
    with open(path, "w") as f:
        f.write("Hello World")

with file_transaction("data.txt") as tmp:
    write_file(tmp)


@with_transaction(DatabaseConnection)

@log_execution

def insert_data(x, db=None):
    db.execute(f"INSERT INTO table VALUES ({x})")

insert_data(10)