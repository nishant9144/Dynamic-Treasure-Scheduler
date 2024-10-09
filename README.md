# Dynamic-Treasure-Scheduler
This repository contains the solution for the Dynamic Treasure Scheduler problem.
## Content
- [Background](#background)
- [State of the System](#state-of-the-system)
- [Scheduling Policy](#scheduling-policy)
- [Code](#code)
## Background
In large-scale systems, task scheduling and resource allocation are critical problems, and this project simulates a similar challenge faced by a team of pirates—specifically the Straw Hat crew from the popular series One Piece.

As the treasurer of the Straw Hat crew, your responsibility is to manage a growing collection of treasures efficiently. Each crew member can work on only one treasure at a time, and treasures arrive at different intervals and in varying sizes, representing a challenge in prioritization and resource distribution.

This project models the treasure management task as a scheduling problem, where the goal is to assign tasks (treasure processing) to resources (crewmates) in the most efficient manner possible. It involves concepts of load balancing, priority scheduling, and optimization using a custom-built heap structure.

The problem is further complicated by real-world constraints such as:

- Unequal processing times for different treasures.
- Variable arrival times, meaning treasures become available at different points in time.
- The necessity to prioritize older treasures while balancing overall workload across the crew.
## State of the system
At any given time t:
- Each crewmate maintains a list of treasure pieces assigned to them.
- The remaining size of a treasure piece j is given by:
<br>
<div style="text-align: center;">
Remaining Size = Original Size ( size<sub> j</sub> ) − Processed Time
</div><br>
where the processed time is the amount of time already spent managing that piece. Once the remaining Size of a treasure is zero, no more time can be spent on it for processing.

- The load on a crewmate is defined as the total remaining size of the
treasures in their queue.
- Note that at any given moment, a crewmate can only process one treasure i.e. a crewmate cannot process 2 or more treasures in parallel
## Scheduling Policy
When a new piece of treasure arrives, the following scheduling policies are applied:
- Treasure Assignment: The newly arrived treasure is assigned to the
crewmate with the least current load. This is calculated based on the
total remaining size of treasures assigned to each crewmate. In case more
than one crewmate has the least current load then the treasure can be
assigned to any one of them.
- Treasure Processing: At any time t, each crewmate will process the
treasure j for which:
<br>
<div style="text-align: center;">
Priority ( j ) = ( Wait Time ( j ) − Remaining Size ( j ) )
</div>
</br>
is maximized. Here, Wait Time(j) is the total time the treasure has been
waiting since its arrival time, i.e., at a time t after arrival of the treasure
j,
Wait Time(j) = t − arrival<sub> j </sub>

- In case more than one treasure has maximum priority, then the crewmate
will process the treasure with least id (having the maximum priority).
## Code
- **crewmate.py**: Implements the class for the crewmates responsible for processing the treasures.
- **heap.py**: Implements a custom heap structure used to manage the assignment of treasures.
- **straw_hat.py**: Implements the main class StrawHatTreasury which handles the overall treasure management system.
- **treasure.py**: Implements the class for individual treasures with attributes like size, arrival time, and ID.
## Time Complexity Analysis
- Adding the treasure to the respective crewmate takes O (log m) where m is the number of crewmates.
- Getting the completion time of all the treasure at any time takes O (n log n) where n is the total number of treasures at that time.