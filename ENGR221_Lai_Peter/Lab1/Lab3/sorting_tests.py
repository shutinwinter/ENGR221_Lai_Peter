"""
Name: Peter Lai
sortingFunctions.py
Descrption: Implementation of sorting algorithms.
"""

import time, random

# Implementation of insertionSort algorithm
def insertionSort(list_to_sort:list) -> list:
    for i in range (1, len(list_to_sort)):
        key = list_to_sort[i]
        j = i - 1
        while j >= 0 and list_to_sort[j] > key:
            list_to_sort[j + 1] = list_to_sort[j]
            j -= 1
            list_to_sort[j + 1] = key
    return list_to_sort

# implementation of bubbleSort algorithm
def bubbleSort(list_to_sort: list) -> list:
    n = len(list_to_sort)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if list_to_sort[j] > list_to_sort[j + 1]:
                list_to_sort[j], list_to_sort[j + 1] = list_to_sort[j + 1], list_to_sort[j]
    return list_to_sort

# Returns a random list of the given length
def createRandomList(length:int) -> list:
    return random.sample(range(max(100, length)), length)

# Returns the length of time (sec) that it took
# for the function_to_run to sort a list of length list_length
def getRuntime(function_to_run, list_length) -> float:
    # Create a new list to sort
    list_to_sort = createRandomList(list_length)
    # Get the time before running
    start_time = time.time()
    # Sort the given list
    function_to_run(list_to_sort)
    # Get the time after running
    end_time = time.time()
    # Return the difference
    return end_time - start_time

if __name__ == '__main__':
    print ("Insertion sort runtime")
    print ("100 items: ", getRuntime(insertionSort, 100))
    print ("1,000 items: ", getRuntime(insertionSort, 1000))
    print ("10,000 items: ", getRuntime(insertionSort, 10000))

    print ("\nBubblesort runtime")
    print ("100 items: ", getRuntime(bubbleSort, 100))
    print ("1,00 items: ", getRuntime(bubbleSort, 10000))
    print ("10,000 items: ", getRuntime(bubbleSort, 10000))