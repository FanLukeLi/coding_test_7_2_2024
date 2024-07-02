# Review 1

def add_to_list(value, my_list=[]):
    my_list.append(value)

    return my_list


# Review 2
# Answer: The string should be f-string so that "name" and "age" could be replaced by inputs
def format_greeting(name, age):
    return "Hello, my name is {name} and I am {age} years old."
    # Answer: return f"Hello, my name is {name} and I am {age} years old. "


# Review 3
# Answer: The count attribute belongs to the class not the instances
class Counter:
    count = 0

    def __init__(self):
        # Answer: self.count = 0
        self.count += 1

    def get_count(self):
        return self.count


# Review 4

import threading


class SafeCounter:

    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

# Answer: counter could be specified to SafeCounter class, to guarantee the input has increment method
# Answer: def worker(counter: SafeCounter):
def worker(counter):
    for _ in range(1000):
        counter.increment()


counter = SafeCounter()

threads = []

for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))

    t.start()

    threads.append(t)

for t in threads:
    t.join()


# Review 5
# Answer: replace '=+' with '+='
def count_occurrences(lst):
    counts = {}

    for item in lst:

        if item in counts:

            counts[item] = + 1
            # Answer: counts[item] += 1

        else:

            counts[item] = 1

    return counts
