
# Curve Fitting based Array search

This project presents an algorithm which aims to reduce the number of search comparisons in a sorted array search by reducing the search to only a small part of array. The main steps during this search is

- based on value to be searched, find the approximate index
- based of index deviation values (discussed later), find the sub-array that can possibly contain the value
- **instead of searching the entire array, search only the sub-array**

Note: This is not a greedy-approach based algorithm. The sub-array we find is the only place in the array that could possibly contain the value.

This algorithm is useful iff:

- The array is significantly large
- The array needs to be searched multiple times
- The array itself doesn't need to be modified
- It is possible to find a good fitting curve that maps values to array-index

Now let us see how this algorithm works in a little more details.

## Pre-processing (Simplified Informal Version)

- Step 0: Sort the array (if required).
- Step 1: Find a curve fitting function that is a good fit for value to array-index mapping
- Step 2: For each element of array, find the difference between actual index and the index predicted by the function of curve. These differences are stored in positive and negative deviation array.

## Search (Simplified Informal Version)

- Step 1: Based on the given value to be searched, find the approximate index based on the curve function.
- Step 2a: If found at predicted index, return index
- Step 2b: Else
  - if the value is greater than the array value at predicted index, we find the sub-array above (in index) the predicted index based on positive deviation array.
  - if the value is less than the array value at predicted index, we find the sub-array below (in index) the predicted index based on negative deviation array.
- Step 3: We only search this sub-array using our preferred search algorithm (binary search or something else)

## Time-Complexity

Assuming we are using binary search for searching within sub-array.

N is the size of array.

O(f) is the time complexity of computation for curve fitting function(f). Usually, O(f) = O(1).

**Time-Complexity: O(log2(max(max(positive_deviation_array), max(negative_deviation_array)))) + O(f)**

For a good curve fitting, max(max(positive_deviation_array), max(negative_deviation_array)) <<< N

Even for a bad curve fitting, max(max(positive_deviation_array), max(negative_deviation_array)) <= N
