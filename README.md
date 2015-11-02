# Apriori-and-its-improvements

Implemented applied Apriori algorithm and its improvements (PCY, multihash) in Python

## Problems

### Problem 1: PCY Algorithm

Implement PCY algorithm using a single hash and print all frequent itemsets. You can use a hashing function of your choice.

Input Parameters:

1. Input.txt: This is the input file containing all transactions. Each line corresponds to a transaction. Each transaction has items that are comma separated. Use input.txt to test this algorithm.
2. Support: Integer that defines the minimum count to qualify as a frequent itemset.
3. Bucket size: This is the size of the hash table.

Output:

The output needs to contain the frequent itemsets of all sizes sorted lexicographically. It should also contain the hash buckets with their count of candidates. If the result just contains itemsets of size1 just print them and return. If it contains itemsets of size >= 2 print the bucket counts of the hash as well. For example consider the output below.

[‘a’, ‘b’, ‘d’]
{0:0, 1:2, 3:5} [[‘a’, ‘b’]]

Here [‘a’, ‘b’, ‘d’] represents itemsets of size 1 and {0:0, 1:2, 3:5} represents the hash counts before calculating frequent itemsets of size 2. [[‘a’, ‘b’]] represents itemsets of size 2. Print all bucket counts only for ith frequent itemset where i >= 2. The counts in the buckets can vary depending on the hashing function used. So do not try to match this with the output files provided.
File Name​: Please name your python script as pcy.py. Executing code: python pooja_anand_pcy.py input.txt 4 8.
Where support = 4 and buckets = 8

### Problem 2: Multi­Hash Algorithm

Implement the multi­hash algorithm to generate frequent itemsets. You need to use 2 independent hashing functions for this. Make sure that all candidates are hashed to both the hashing functions to generate 2 different bit vectors. Both the hashes will have the same number of buckets.
Input parameters are same as above. For output follow the same format, but since we have two different hashing functions, print both the hash bucket counts. The counts in the buckets can vary depending on the hashing function used. So do not try to match this with the output files provided

For example:
[‘a’, ‘b’, ‘c’]
{0:0, 1:2, 3:5} {0:1, 1:4, 3:2} [[‘a’, ‘b’]]

File Name​: Please name your python script as multihash.py. Executing code: python pooja_anand_multihash.py input.txt 4 8
Where support = 4 and bucket size = 8

### Problem 3: Toivonen Algorithm
Implement the Toivonen algorithm to generate frequent itemsets. For this algorithm you need to use a sample size of less than 60% of your entire dataset. Use an appropriate sampling method to get the random sample set. Also perform a simple Apriori algorithm with the random sample set. Check for negative borders and run the algorithm again with a different sample set if required till there are no negative borders that have frequency > support.

Input Parameters:
1. Input.txt: This is the input file containing all transactions. Each line corresponds to a transaction. Each transaction has items that are comma separated. Use input1.txt to test this algorithm.
2. Support: Integer that defines the minimum count to qualify as a frequent itemset.

Output:
Line 1 <number of iterations performed>
Line 2 <fraction of transactions used>
Line 3 onwards <frequent itemsets lexicographically sorted>
File Name​: Please name your python script as toivonen.py. Executing code​: ​python pooja_anand_toivonen.py input1.txt 4
Where support = 4

