import random
import sys
from copy import deepcopy
from straw_hat import StrawHatTreasury
from treasure import Treasure
import time

class ProgressBar:
    def __init__(self, total, width=50, prefix='Progress:', suffix='Complete'):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.suffix = suffix
        self.count = 0
        
    def update(self, count=None):
        if count is not None:
            self.count = count
        else:
            self.count += 1
            
        filled = int(self.width * self.count / self.total)
        bar = '█' * filled + '-' * (self.width - filled)
        percent = f"{100 * self.count / self.total:.1f}%"
        print(f'\r{self.prefix} |{bar}| {percent} {self.suffix}', end='')
        
        if self.count == self.total:
            print()
            
    def print_state(self, state_msg):
        print(f"\r{' ' * (len(self.prefix) + self.width + 20)}", end='')
        print(f"\r{state_msg}", end='')
        self.update(self.count)

class ProcessVisualizer:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.state_line = ""
        self.crewmate_lines = ["" for _ in range(m)]
        
    def initialize_display(self):
        print("\nProcessing Simulation:")
        print("-" * 60)
        for i in range(self.m):
            self.update_crewmate_status(i)
        print("\n" * (self.m + 1))
        
    def update_crewmate_status(self, crewmate_id, current_treasure=None, progress=0):
        status = f"Crewmate {crewmate_id:2d}: "
        if current_treasure is None:
            status += "Idle    "
            bar = "-" * 20
        else:
            status += f"T{current_treasure.id:2d} "
            filled = int(20 * progress)
            bar = "█" * filled + "-" * (20 - filled)
        
        self.crewmate_lines[crewmate_id] = f"{status}|{bar}|"
        self.refresh_display()
        
    def print_state(self, message):
        self.state_line = message
        self.refresh_display()
        
    def refresh_display(self):
        # Move cursor up to the start of the visualization area
        for _ in range(len(self.crewmate_lines) + 2):  # +2 for state line and empty line
            print('\033[F', end='')
            
        # Print state
        print(f"\r{self.state_line}" + " " * 40)
        print()
        
        # Print each crewmate status
        for line in self.crewmate_lines:
            print(f"\r{line}")

class NaiveTreasure:
    def __init__(self, id, size, arrival_time):
        self.id = id
        self.size = size
        self.arrival_time = arrival_time
        self.completion_time = None
        self.remaining_size = size
        self.assigned_crewmate = None

class NaiveCrewmate:
    def __init__(self, id):
        self.id = id
        self.treasures = []
        self.current_load = 0
        self.current_treasure = None
        
    def calculate_load(self):
        return sum(t.remaining_size for t in self.treasures)

class NaiveTreasury:
    def __init__(self, m):
        self.crewmates = [NaiveCrewmate(i) for i in range(m)]
        self.unassigned_treasures = []
        self.visualizer = None
        
    def add_treasure(self, treasure):
        self.unassigned_treasures.append(treasure)
    
    def assign_available_treasures(self, current_time):
        available_treasures = [t for t in self.unassigned_treasures if t.arrival_time <= current_time]
        available_treasures.sort(key=lambda x: (x.arrival_time, x.id))
        
        for treasure in available_treasures:
            min_load = float('inf')
            selected_crewmate = None
            
            for crewmate in self.crewmates:
                current_load = crewmate.calculate_load()
                if current_load < min_load:
                    min_load = current_load
                    selected_crewmate = crewmate
                elif current_load == min_load and crewmate.id < selected_crewmate.id:
                    selected_crewmate = crewmate
            
            selected_crewmate.treasures.append(treasure)
            treasure.assigned_crewmate = selected_crewmate
            self.unassigned_treasures.remove(treasure)
            
            if self.visualizer:
                self.visualizer.print_state(f"Assigned T{treasure.id} to Crewmate {selected_crewmate.id}")
                time.sleep(0.05)  # Small delay to make assignment visible
    
    def process_treasures(self, current_time):
        if self.visualizer:
            self.visualizer.print_state(f"Processing time unit {current_time}")
        
        for crewmate in self.crewmates:
            available_treasures = [t for t in crewmate.treasures 
                                if t.arrival_time <= current_time and 
                                t.remaining_size > 0]
            
            if available_treasures:
                max_priority = float('-inf')
                selected_treasure = None
                
                for treasure in available_treasures:
                    wait_time = current_time - treasure.arrival_time
                    priority = wait_time - treasure.remaining_size
                    
                    if priority > max_priority or \
                        (priority == max_priority and treasure.id < selected_treasure.id):
                        max_priority = priority
                        selected_treasure = treasure
                
                selected_treasure.remaining_size -= 1
                progress = 1 - (selected_treasure.remaining_size / selected_treasure.size)
                
                if self.visualizer:
                    self.visualizer.update_crewmate_status(crewmate.id, selected_treasure, progress)
                
                if selected_treasure.remaining_size == 0:
                    selected_treasure.completion_time = current_time + 1
            elif self.visualizer:
                self.visualizer.update_crewmate_status(crewmate.id)
    
    def get_completion_time(self):
        all_treasures = self.unassigned_treasures.copy()
        for crewmate in self.crewmates:
            all_treasures.extend(crewmate.treasures)
        
        if not all_treasures:
            return []
            
        # Reset
        for treasure in all_treasures:
            treasure.remaining_size = treasure.size
            treasure.completion_time = None
            treasure.assigned_crewmate = None
        
        self.unassigned_treasures = all_treasures.copy()
        for crewmate in self.crewmates:
            crewmate.treasures = []
        
        # Initialize visualization
        self.visualizer = ProcessVisualizer(len(self.crewmates), len(all_treasures))
        self.visualizer.initialize_display()
        
        current_time = min(t.arrival_time for t in all_treasures)
        time_progress = ProgressBar(max(t.size for t in all_treasures) * len(all_treasures), 
                                  prefix='Time Progress:', suffix='')
        
        while any(t.completion_time is None for t in all_treasures):
            self.assign_available_treasures(current_time)
            self.process_treasures(current_time)
            current_time += 1
            time_progress.update()
            time.sleep(0.05)  # Small delay to make visualization visible
        
        print("\nProcessing complete!")
        return sorted(all_treasures, key=lambda x: x.id)

def compare_results(result1, result2):
    """Compare results from both implementations"""
    if len(result1) != len(result2):
        return False, f"Different number of treasures: {len(result1)} vs {len(result2)}"
    
    for t1, t2 in zip(result1, result2):
        if t1.id != t2.id:
            return False, f"Mismatched treasure IDs: {t1.id} vs {t2.id}"
        if t1.completion_time != t2.completion_time:
            return False, f"Different completion times for treasure {t1.id}: {t1.completion_time} vs {t2.completion_time}"
    
    return True, "Results match"

def run_single_test(test_num, m, n, max_size=20, max_arrival_gap=5):
    progress = ProgressBar(3, prefix=f'Test {test_num}:', suffix='')
    
    try:
        progress.print_state("Initializing test...")
        your_treasury = StrawHatTreasury(m)
        naive_treasury = NaiveTreasury(m)
        progress.update()
        
        progress.print_state("Generating and adding treasures...")
        current_time = 0
        treasures_added = []
        
        for i in range(n):
            id = i + 1
            size = random.randint(1, max_size)
            current_time += random.randint(1, max_arrival_gap)
            
            your_treasure = Treasure(id, size, current_time)
            naive_treasure = NaiveTreasure(id, size, current_time)
            
            your_treasury.add_treasure(your_treasure)
            naive_treasury.add_treasure(naive_treasure)
            treasures_added.append((id, size, current_time))
        progress.update()
        
        progress.print_state("Processing treasures...")
        print("\n")  # Add space for visualization
        your_result = your_treasury.get_completion_time()
        print("\n")  # Add space between implementations
        naive_result = naive_treasury.get_completion_time()
        progress.update()
        
        success, message = compare_results(your_result, naive_result)
        
        if success:
            print(f"\nTest {test_num} passed!")
            return True
        else:
            print(f"\nTest {test_num} failed!")
            print(f"Error: {message}")
            print("\nTest case details:")
            print(f"Number of crewmates: {m}")
            print("Treasures added (id, size, arrival_time):")
            for t in treasures_added:
                print(f"  {t}")
            print("\nYour implementation completion times:")
            for t in your_result:
                print(f"  Treasure {t.id}: {t.completion_time}")
            print("\nExpected completion times:")
            for t in naive_result:
                print(f"  Treasure {t.id}: {t.completion_time}")
            return False
            
    except Exception as e:
        print(f"\nTest {test_num} failed with exception!")
        print(f"Error: {str(e)}")
        return False

def run_tests(num_tests=10):
    overall_progress = ProgressBar(num_tests, prefix='Overall Progress:', suffix='')
    failed_tests = 0
    
    print("Starting test suite...")
    print("-" * 60)
    
    for test_num in range(num_tests):
        m = random.randint(1, 10)
        n = random.randint(1, 20)
        
        if not run_single_test(test_num, m, n):
            failed_tests += 1
            if failed_tests >= 3:
                print("\nStopping tests after 3 failures")
                break
        
        overall_progress.update()
        print("-" * 60)
    
    print(f"\nTests completed. {num_tests - failed_tests}/{num_tests} tests passed.")

if __name__ == "__main__":
    run_tests()