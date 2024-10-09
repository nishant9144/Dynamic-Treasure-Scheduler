import crewmate
import heap
import treasure

def comparator(a, b):
    return a.key < b.key
    
def comparator2(x, y):
    if x[0] + x[1].arrival_time == y[0] + y[1].arrival_time:
        return x[1].id < y[1].id
    else:
        return x[0] + x[1].arrival_time < y[0] + y[1].arrival_time
    
class StrawHatTreasury:    
    def __init__(self, m):
        '''
        Arguments:
            m : int : Number of Crew Mates (positive integer)
        Returns:
            None
        Description:
            Initializes the StrawHat
        Time Complexity:
            O(m)
        '''

        self.number_crew = m

        # Create m crewmates
        crewmates = [crewmate.CrewMate() for _ in range(m)]

        self.crew_heap = heap.Heap(comparator, crewmates) 
        self.taken_crew = [] 
    
    def add_treasure(self, treasure):
        '''
        Arguments:
            treasure : Treasure : The treasure to be added to the treasury
        Returns:
            None
        Description:
            Adds the treasure to the treasury
        Time Complexity:
            O(log(m) + log(n)) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''

        # Extract the crewmate with the least key (free time)
        crewmate_in_which_treasure_is_added = self.crew_heap.extract()
        
        # Add the treasure to the crewmate's list
        crewmate_in_which_treasure_is_added.treasure.append(treasure)
        
        # Update the crewmate's key (free time) based on treasure's arrival time and size
        if crewmate_in_which_treasure_is_added.key < treasure.arrival_time:
            crewmate_in_which_treasure_is_added.key = treasure.arrival_time + treasure.size
        else:
            crewmate_in_which_treasure_is_added.key += treasure.size
        
        # Re-insert the updated crewmate back into the heap
        if crewmate_in_which_treasure_is_added.is_taken == False:
            crewmate_in_which_treasure_is_added.is_taken = True
            self.taken_crew.append(crewmate_in_which_treasure_is_added)

        self.crew_heap.insert(crewmate_in_which_treasure_is_added)

    def get_completion_time(self):
        '''
        Arguments:
            None
        Returns:
            List[Treasure] : List of treasures in the order of their completion after updating Treasure.completion_time
        Description:
            Returns all the treasure after processing them
        Time Complexity:
            O(n(log(m) + log(n))) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''

        treasure_array = []
        for crew in range(len(self.taken_crew)): #self.number_crew
            treasure_list = self.taken_crew[crew].treasure
            # if not treasure_list:  # Skip if no treasures
            #     continue

            priority_list = heap.Heap(comparator2, [])

            priority_list.insert((treasure_list[0].size,treasure_list[0])) # rem_size, treasure

            processed_time = treasure_list[0].arrival_time

            for i in range(1, len(treasure_list)):
                time_diff = treasure_list[i].arrival_time - processed_time# - priority_list.top()[0] # how much time more needed for the treasure to complete

                while priority_list.size > 0 and (time_diff - priority_list.top()[0]) >= 0:
                    top_treasure = priority_list.extract()
                    rem_size, my_treasure = top_treasure[0], top_treasure[1]

                    my_treasure.completion_time = processed_time + rem_size
                    processed_time += rem_size
                    treasure_array.append(my_treasure)
                    time_diff -= rem_size

                if priority_list.size > 0:
                    top_treasure = priority_list.extract()
                    rem_size, my_treasure = top_treasure[0], top_treasure[1]   

                    new_rem_size = rem_size - (treasure_list[i].arrival_time - processed_time)
                    processed_time = treasure_list[i].arrival_time

                    priority_list.insert((new_rem_size, my_treasure))
                
                elif priority_list.size == 0:
                    processed_time = treasure_list[i].arrival_time

                priority_list.insert((treasure_list[i].size,treasure_list[i]))

            while priority_list.size > 0:
                top_treasure = priority_list.extract()
                rem_size, my_treasure = top_treasure[0], top_treasure[1]

                my_treasure.completion_time = processed_time + rem_size
                treasure_array.append(my_treasure)
                processed_time += rem_size

        # Sort the treasure_array based on treasure ID
        treasure_array.sort(key=lambda treasure: treasure.id)
        return treasure_array        