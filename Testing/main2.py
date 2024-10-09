from straw_hat import *
from heap import *
from treasure import *
import random
import time

random.seed(42)


def progress_bar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    total = len(iterable)
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    printProgressBar(0)
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    print()


class Chest:
    def __init__(self, chest_id, arrival_time, original_size):
        self.chest_id = chest_id
        self.arrival_time = arrival_time
        self.original_size = original_size
        self.remaining_size = original_size
        self.waiting_time = 0
        self.processed = 0

    def __str__(self):
        return f"[{self.chest_id}] - ({self.original_size}, {self.arrival_time})"


class Worker:
    def __init__(self, worker_id):
        self.worker_id = worker_id
        self.chests = []
        self.current_chest = None


class Manual:
    def __init__(self, chests, n):
        self.chests = [Chest(*chest) for chest in chests]
        self.workers = [Worker(i) for i in range(n)]
        self.time = 0
        self.completion_times = {}
        for chest in self.chests:
            self.completion_times[chest.chest_id] = 0
            if chest.arrival_time == 0:
                self.workers[0].chests.append(chest)

    def tick(self):
        self.time += 1
        for worker in self.workers:
            for chest in worker.chests:
                chest.waiting_time += 1
        for chest in self.chests:
            if chest.arrival_time == self.time:
                min_load = sum([sum([chest.remaining_size for chest in worker.chests]) for worker in self.workers])
                best_worker = None
                for worker in self.workers:
                    load = sum([chest.remaining_size for chest in worker.chests])
                    if load <= min_load:
                        min_load = load
                        best_worker = worker
                best_worker.chests.append(chest)
        for worker in self.workers:
            if worker.current_chest:
                worker.current_chest.remaining_size -= 1
                worker.current_chest.processed += 1
                if worker.current_chest.remaining_size == 0:
                    worker.chests.remove(worker.current_chest)
                    self.completion_times[worker.current_chest.chest_id] = self.time
                    worker.current_chest = None
            if worker.chests:
                max_cri = self.time - worker.chests[0].arrival_time - worker.chests[0].remaining_size
                best_chest = None
                for chest in worker.chests:
                    cri = chest.waiting_time - chest.remaining_size
                    if cri > max_cri:
                        max_cri = cri
                        best_chest = chest
                    elif cri == max_cri:
                        if best_chest is None:
                            best_chest = chest
                        elif chest.chest_id < best_chest.chest_id:
                            best_chest = chest
                worker.current_chest = best_chest

    def print_current_status(self):
        print(f"Time: {self.time}")
        for worker in self.workers:
            print(f"Worker {worker.worker_id}: ", end="")
            if worker.current_chest:
                print(f"Processing Chest {worker.current_chest.chest_id} with {worker.current_chest.remaining_size} units left")
            else:
                print("Idle")
        print()

    def get_completion_time(self):
        return sorted([(chest_id, time) for chest_id, time in self.completion_times.items()], key=lambda x: x[0])


class StupidHeap:
    def __init__(self, comparison_function, init_array):
        self.comparison_function = comparison_function
        self.heap = sorted(init_array, key=comparison_function)

    def insert(self, item):
        self.heap.append(item)
        self.heap = sorted(self.heap, key=self.comparison_function)

    def extract(self):
        return self.heap.pop(0)

    def top(self):
        return self.heap[0]

    def empty(self):
        return len(self.heap) == 0

# manual = Manual([(1, 1, 8), (2, 2, 7), (3, 4, 4), (4, 5, 1)], 3)
# for i in range(9):
#     manual.tick()
# print(manual.get_completion_time())

# treasury = StrawHatTreasury(3)
# treasury.add_treasure(Treasure(1, 8, 1))
# treasury.add_treasure(Treasure(2, 7, 2))
# treasury.add_treasure(Treasure(3, 4, 4))
# treasury.add_treasure(Treasure(4, 1, 5))
# treasury.print_completion_times(treasury.get_completion_time())


def main(n=10**3, m=12):
    format_len = 25
    workers = m
    print("[+] Welcome to Ani's Testcase (V3.1) [still in development, this tc is complete], this will be a comprehensive testcase and will automatically check for correctness.\n[*] Do not rely on the correctness checker for time complexity, rely purely on the time complexity tables given ahead\n[!] Unlike last time, this testcase will strictly adhere to possible operations, any errors indicate an issue in your code.\n[!] If you think that there is an error in the testcase or if I'm missing something, dm me whatsapp pr")
    stupid_heap = StupidHeap(lambda x: x, [1, 2, 3, 4, 5])
    test_heap = Heap(lambda x, y: x < y, [1, 2, 3, 4, 5])
    for i in progress_bar(range(n), "Random Heap Operations".ljust(format_len)):
        op = random.randint(0, 100)
        if op <= 75:
            val = random.randint(0, 10000)
            if val not in stupid_heap.heap:
                stupid_heap.insert(val)
                test_heap.insert(val)
            stupid_top = stupid_heap.top()
            test_top = test_heap.top()
            if stupid_top != test_top:
                print(f"\n[!] Error while checking min value in heap after adding {val}, expected {stupid_top}, received {test_top}")
                exit(1)
        else:
            if not stupid_heap.empty():
                stupid_top = stupid_heap.top()
                test_top = test_heap.top()
                if stupid_top != test_top:
                    print(f"\n[!] Error while checking min value in heap, expected {stupid_top}, received {test_top}")
                    exit(1)
                stupid_pop = stupid_heap.extract()
                test_pop = test_heap.extract()
                if stupid_pop != test_pop:
                    print(f"\n[!] Pretty Major Error in your heap, running the top() function gave the correct value ({test_top}) but running the pop() function gave the value ({stupid_pop})")
                    exit(1)
                stupid_top = stupid_heap.top()
                test_top = test_heap.top()
                if stupid_top != test_top:
                    print(f"\n[!] Error while checking min value in heap after removing {test_pop}, expected {stupid_top}, received {test_top}")
                    exit(1)
    to_delete = stupid_heap.heap.copy()
    random.shuffle(to_delete)
    for i in progress_bar(to_delete, "Clearing Heap".ljust(format_len)):
        if not stupid_heap.empty():
            stupid_top = stupid_heap.top()
            test_top = test_heap.top()
            if stupid_top != test_top:
                print(f"\n[!] Error while checking min value in heap, expected {stupid_top}, received {test_top}")
                exit(1)
            stupid_pop = stupid_heap.extract()
            test_pop = test_heap.extract()
            if stupid_pop != test_pop:
                print(f"\n[!] Pretty Major Error in your heap, running the top() function gave the correct value ({test_top}) but running the pop() function gave the value ({stupid_pop})")
                exit(1)
        else:
            if stupid_heap.empty() ^ test_heap.empty():
                print(f"\n[!] Error while checking if heap is empty, expected {stupid_heap.empty()}, received {test_heap.empty()}")
                exit(1)
    to_add = [(1, 1, 8), (2, 2, 7), (3, 4, 4), (4, 5, 1)]
    test_treasury = StrawHatTreasury(3)
    for i in progress_bar(range(4), "Piazza TC1".ljust(format_len)):
        stupid_treasury = Manual(to_add[:i+1], 3)
        test_treasury.add_treasure(Treasure(to_add[i][0], to_add[i][2], to_add[i][1]))
        completion_times = test_treasury.get_completion_time()
        for j in range(10):
            stupid_treasury.tick()
        stupid_completion_times = stupid_treasury.get_completion_time()
        for j in range(i+1):
            if completion_times[j].completion_time != stupid_completion_times[j][1]:
                print(f"\n[!] Error in completion times, expected {stupid_completion_times[j]}, received {(completion_times[j].id, completion_times[j].completion_time)}")
                exit(1)
    to_add = [(1000, 1, 1000000000), (1001, 300000000, 2000000000), (1002, 400000000, 100000000), (1003, 600000000, 5000000000), (1004, 700000000, 1200000000)]
    test_treasury = StrawHatTreasury(2)
    expected_output = [
        [(1000, 1000000001)],
        [(1000, 1000000001), (1001, 2300000000)],
        [(1000, 1100000001), (1001, 2300000000), (1002, 500000000)],
        [(1000, 1100000001), (1001, 2300000000), (1002, 500000000), (1003, 6100000001)],
        [(1000, 1100000001), (1001, 2300000000), (1002, 500000000), (1003, 6100000001), (1004, 3500000000)]
    ]
    for i in progress_bar(range(5), "Piazza TC2".ljust(format_len)):
        test_treasury.add_treasure(Treasure(to_add[i][0], to_add[i][2], to_add[i][1]))
        completion_times = test_treasury.get_completion_time()
        for j in range(i+1):
            if completion_times[j].id != expected_output[i][j][0] or completion_times[j].completion_time != expected_output[i][j][1]:
                print(f"\n[!] Error in completion times, expected {expected_output[i][j]}, received {(completion_times[j].id, completion_times[j].completion_time)}")
                exit(1)
    to_add = [
        (1, 1, 8),
        (2, 2, 7),
        (3, 4, 4),
        (4, 5, 1),
        (5, 6, 4),
        (6, 7, 4),
        (7, 30, 5),
        (8, 31, 4),
        (9, 32, 6)
    ]
    test_treasury = StrawHatTreasury(3)
    for i in progress_bar(range(len(to_add)), "Bansal TC".ljust(format_len)):
        stupid_treasury = Manual(to_add[:i+1], 3)
        test_treasury.add_treasure(Treasure(to_add[i][0], to_add[i][2], to_add[i][1]))
        completion_times = test_treasury.get_completion_time()
        for j in range(50):
            stupid_treasury.tick()
        stupid_completion_times = stupid_treasury.get_completion_time()
        for j in range(i+1):
            if completion_times[j].completion_time != stupid_completion_times[j][1]:
                print(f"\n[!] Error in completion times, expected {stupid_completion_times[j]}, received {(completion_times[j].id, completion_times[j].completion_time)}")
                exit(1)
    # test_treasury = StrawHatTreasury(4)
    # sz = 3030
    # t = 1
    # to_add = []
    # for i in range(1, 31):
    #     test_treasury.add_treasure(Treasure(id=i, size=sz, arrival_time=i+t))
    #     to_add.append((i, i+t, sz))
    #     sz -= 1
    #     if i % 3 == 0:
    #         t += 1
    # sz -= 10
    # stupid_treasury = Manual(to_add, 4)
    # for i in range(28000):
    #     stupid_treasury.tick()
    # completion_1 = test_treasury.get_completion_time()
    # stupid_completion_times = stupid_treasury.get_completion_time()
    # print(stupid_completion_times)
    # for i in range(len(to_add)):
    #     print(completion_1[i].id, completion_1[i].completion_time)
    # for i in range(len(to_add)):
    #     if completion_1[i].id != stupid_completion_times[i][0] or completion_1[i].completion_time != stupid_completion_times[i][1]:
    #         print(f"\n[!] Error in completion times, expected {stupid_completion_times[i]}, received {(completion_1[i].id, completion_1[i].completion_time)}")
    #         exit(1)
    # print("[+] TC1 Passed")
    # for i in range(31, 34):
    #     test_treasury.add_treasure(Treasure(id=i, size=sz, arrival_time=i+t))
    #     to_add.append((i, i+t, sz))
    #     sz -= 1
    # stupid_treasury = Manual(to_add, 4)
    # for i in range(28000):
    #     stupid_treasury.tick()
    # completion_2 = test_treasury.get_completion_time()
    # stupid_completion_times = stupid_treasury.get_completion_time()
    # for i in range(len(to_add)):
    #     if completion_2[i].id != stupid_completion_times[i][0] or completion_2[i].completion_time != stupid_completion_times[i][1]:
    #         print(f"\n[!] Error in completion times, expected {stupid_completion_times[i]}, received {(completion_2[i].id, completion_2[i].completion_time)}")
    #         exit(1)
    # print("[+] TC2 Passed")
    # for i in range(34, 37):
    #     test_treasury.add_treasure(Treasure(id=i, size=sz, arrival_time=i+27147-50))
    #     to_add.append((i, i+27147-50, sz))
    #     sz -= 1
    # stupid_treasury = Manual(to_add, 4)
    # for i in range(32000):
    #     stupid_treasury.tick()
    # completion_3 = test_treasury.get_completion_time()
    # stupid_completion_times = stupid_treasury.get_completion_time()
    # for i in range(len(to_add)):
    #     if completion_3[i].id != stupid_completion_times[i][0] or completion_3[i].completion_time != stupid_completion_times[i][1]:
    #         print(f"\n[!] Error in completion times, expected {stupid_completion_times[i]}, received {(completion_3[i].id, completion_3[i].completion_time)}")
    #         exit(1)
    # print("[+] TC3 Passed")
    test_treasury = StrawHatTreasury(workers)
    last_added = 0
    added = []
    for i in progress_bar(range(n), "Adding Treasure".ljust(format_len)):
        arrival_time = last_added + random.randint(1, 20)
        size = random.randint(1, 40)
        test_treasury.add_treasure(Treasure(i, size, arrival_time))
        added.append((i, arrival_time, size))
        last_added = arrival_time
    stupid_treasury = Manual(added, workers)
    completion_times = test_treasury.get_completion_time().copy()
    completion_times_2 = test_treasury.get_completion_time().copy()
    max_time = max([completion_times[i].completion_time for i in range(n)])
    for i in progress_bar(range(max_time), "Manually Running Time".ljust(format_len)):
        stupid_treasury.tick()
    stupid_completion_times = stupid_treasury.get_completion_time()
    for i in progress_bar(range(n+1), "Checking Completion Times"):
        if i == 0:
            for j in range(len(completion_times)):
                if not(completion_times[j].id == completion_times_2[j].id and completion_times[j].completion_time == completion_times_2[j].completion_time):
                    print(f"\n[!] Running get_completion_time() twice gave different results at index ({j}), this should not happen.")
                    exit(1)
        else:
            if completion_times[i - 1].completion_time != stupid_completion_times[i - 1][1]:
                print(f"\n[!] Error in completion times, expected {stupid_completion_times[i - 1]}, received {(completion_times[i - 1].id, completion_times[i - 1].completion_time)}")
                exit(1)
    for i in progress_bar(range(n), "Adding Treasure".ljust(format_len)):
        arrival_time = last_added + random.randint(1, 20)
        size = random.randint(1, 40)
        test_treasury.add_treasure(Treasure(n+i, size, arrival_time))
        added.append((n+i, arrival_time, size))
        last_added = arrival_time
    stupid_treasury = Manual(added, workers)
    completion_times = test_treasury.get_completion_time().copy()
    completion_times_2 = test_treasury.get_completion_time().copy()
    max_time = max([completion_times[i].completion_time for i in range(2*n)])
    for i in progress_bar(range(max_time), "Manually Running Time".ljust(format_len)):
        stupid_treasury.tick()
    stupid_completion_times = stupid_treasury.get_completion_time()
    for i in progress_bar(range(2*n + 1), "Checking Completion Times"):
        if i == 0:
            for j in range(len(completion_times)):
                if not (completion_times[j].id == completion_times_2[j].id and completion_times[j].completion_time == completion_times_2[j].completion_time):
                    print(f"\n[!] Running get_completion_time() twice gave different results at index ({j}), this should not happen.")
                    exit(1)
        else:
            if completion_times[i - 1].completion_time != stupid_completion_times[i - 1][1]:
                print(f"\n[!] Error in completion times, expected {stupid_completion_times[i - 1]}, received {(completion_times[i - 1].id, completion_times[i - 1].completion_time)}")
                exit(1)
    last_added = 0
    added = []
    for i in progress_bar(range(n//3), "Deep Check".ljust(format_len)):
        workers = random.randint(max(m//2, 1), 2*m)
        test_treasury = StrawHatTreasury(workers)
        arrival_time = last_added + random.randint(1, 20)
        size = random.randint(1, 40)
        added.append((n+i, arrival_time, size))
        last_added = arrival_time
        stupid_treasury = Manual(added, workers)
        for j in added:
            test_treasury.add_treasure(Treasure(j[0], j[2], j[1]))
        completion_times = test_treasury.get_completion_time().copy()
        completion_times_2 = test_treasury.get_completion_time().copy()
        max_time = max([completion_times[_].completion_time for _ in range(len(added))])
        for j in range(max_time):
            stupid_treasury.tick()
        stupid_completion_times = stupid_treasury.get_completion_time()
        for j in range(i + 1):
            if j == 0:
                for k in range(len(completion_times)):
                    if not (completion_times[k].id == completion_times_2[k].id and completion_times[k].completion_time == completion_times_2[k].completion_time):
                        print(f"\n[!] Running get_completion_time() twice gave different results at index ({k}), this should not happen.")
                        exit(1)
            else:
                if completion_times[j - 1].completion_time != stupid_completion_times[j - 1][1]:
                    print(f"\n[!] Error in completion times, expected {stupid_completion_times[j - 1]}, received {(completion_times[j - 1].id, completion_times[j - 1].completion_time)}")
                    exit(1)
    print("[+] Correctness checked successfully, no errors found.")
    print("[*] Checking Time Complexity")
    n_values = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
    m_values = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
    print("-" * 54)
    for n in n_values:
        print(f"| add_treasure() | n = {str(n).ljust(7)} | m = 10 | ", end="")
        test_treasury = StrawHatTreasury(10)
        last_added = 0
        for i in range(n):
            r = random.randint(1, 5)
            test_treasury.add_treasure(Treasure(i, 10 ** 9, last_added + 10 ** 9 * r))
            last_added += 10 ** 9 * r
        start_time = time.perf_counter_ns()
        test_treasury.add_treasure(Treasure(n, 10 ** 9, last_added + random.randint(1,5) * 10 ** 9))
        end_time = time.perf_counter_ns()
        print_str = f'{(end_time-start_time)/1000000:.4f}ms'.ljust(10)
        print(f'{print_str} |')
    print("-" * 62)
    for n in n_values:
        test_treasury = StrawHatTreasury(10)
        last_added = 0
        print(f"| get_completion_time() | n = {str(n).ljust(7)} | m = 10 | ", end="")
        for i in range(n):
            r = random.randint(1, 5)
            test_treasury.add_treasure(Treasure(i, 10 ** 9, last_added + 10 ** 9 * r))
            last_added += 10 ** 9 * r
        start_time = time.perf_counter_ns()
        test_treasury.get_completion_time()
        end_time = time.perf_counter_ns()
        print_str = f'{(end_time-start_time)/1000000:.4f}ms'.ljust(11)
        print(f'{print_str} |')
    print("-" * 62)
    for m in m_values:
        print(f"| add_treasure() | n = 20 | m = {str(m).ljust(8)} | ", end="")
        test_treasury = StrawHatTreasury(m)
        last_added = 0
        for i in range(20):
            r = random.randint(1, 5)
            test_treasury.add_treasure(Treasure(i, 10 ** 9, last_added + 10 ** 9 * r))
            last_added += 10 ** 9 * r
        start_time = time.perf_counter_ns()
        test_treasury.add_treasure(Treasure(20, 10 ** 9, last_added + random.randint(1,5) * 10 ** 9))
        end_time = time.perf_counter_ns()
        print_str = f'{(end_time-start_time)/1000000:.4f}ms'.ljust(10)
        print(f'{print_str} |')
    print("-" * 62)
    for m in m_values:
        print(f"| get_completion_time() | n = 20 | m = {str(m).ljust(8)} | ", end="")
        test_treasury = StrawHatTreasury(m)
        last_added = 0
        for i in range(20):
            r = random.randint(1, 5)
            test_treasury.add_treasure(Treasure(i, 10 ** 9, last_added + 10 ** 9 * r))
            last_added += 10 ** 9 * r
        start_time = time.perf_counter_ns()
        test_treasury.get_completion_time()
        end_time = time.perf_counter_ns()
        print_str = f'{(end_time-start_time)/1000000:.4f}ms'.ljust(10)
        print(f'{print_str} |')
    print("-" * 62)
    for m in m_values:
        print(f"| StrawHatTreasury() | m = {str(m).ljust(8)} | ", end="")
        start_time = time.perf_counter_ns()
        StrawHatTreasury(m)
        end_time = time.perf_counter_ns()
        print_str = f'{(end_time-start_time)/1000000:.4f}ms'.ljust(11)
        print(f'{print_str} |')
    print("-" * 51)
    print("[*] ^^ Check your time complexities manually, ensure that they scale how you expect them to ^^")
    print("[+] All checks done!!")


if __name__ == "__main__":
    main(m=20)
    print("PASSED FOR 20 CREWMATES, NOW TESTING FOR 1 CREWMATE")
    main(m=1)
    print("PASSED FOR 1 CREWMATE, ALL GOOD!!")

