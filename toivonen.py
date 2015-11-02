
"""
Problem 1: Toivonen Algorithm


Executing code: 
1) $ python toivonen.py input.txt 4
2) $ python toivonen.py input1.txt 20


"""


# note: error existing inside apriori

import sys
import re
import random

def toivonen(inputfile, support):
    iterations = 0
    result = []
    ck = True
    while ck:
        ans_one = pass_one(inputfile, support)
        ans_two = pass_two(inputfile, ans_one[1], ans_one[2], support)
        ck = ans_two[0]
        iterations += 1
    result.append(iterations)
    result.append(ans_one[0])
    result.append(ans_two[1])
    display_result(result)
    return result

def display_result(result):
    print result[0]# , "\n" # number of iterations performed
    print result[1]# , "\n" # fraction of transactions used
    frequent_items = result[2]
    for item in frequent_items:
        print item, "\n"

def pass_one(inputfile, support):
    result = []
    p = 0.4 # 0.6
    baskets = generate_baskets(inputfile)
    sample_baskets = sampling(baskets, p)
    result.append(len(sample_baskets)*1./len(baskets))
    adjusted_support = 0.9 * p * support # use lower threshold
    frequent_items = apriori(sample_baskets, p, adjusted_support)
    result.append(frequent_items)
    negative_border_items = generate_negative_border(frequent_items, sample_baskets)
    result.append(negative_border_items)
    return result

def pass_two(inputfile, frequent_items, negative_border_items, support):
    baskets = generate_baskets(inputfile)  
    ans = check_negative_border_items(negative_border_items, baskets, support)
    if ans:
        return [True]
    ffi = filter_frequent_items(frequent_items, baskets, support)
    return [False, ffi]

def filter_frequent_items(frequent_items, baskets, support):
    result = []
    for fi in frequent_items:
        ans = []
        for i in fi:
            count = 0
            for basket in baskets:
                inside = True
                for item in i:
                    if item not in basket:
                        inside = False
                        break
                if inside == True:
                    count += 1
            if count >= support: 
                ans.append(i)
        if ans:
            result.append(ans)
    return result

def check_negative_border_items(negative_border_items, baskets, support):
    for items in negative_border_items:
        count = 0
        for basket in baskets:
            inside = True
            for item in items:
                if item not in basket:
                    inside = False
                    break
            if inside == True:
                count += 1
        if count >= support: # this nb item is frequent
            return True
    return False
        
def sampling(baskets, probability):
    # result = []
    # for basket in baskets:
    #     if random.random() <= probability:
    #         result.append(basket)
    # return result
    size = len(baskets)
    return random.sample(baskets, int(probability*size))    

def generate_baskets(inputfile):
    inputdata = open(inputfile, 'rU')
    baskets = []
    for line in inputdata:
        basket = []
        for item in line: # or basket[:-1] to delete '\n'
            if item == ' ' or item == ',' or item == '\n':
                continue
            basket.append(item)
        baskets.append(basket)
    return baskets

"""""""""""""""""""""""""""
    Negative Border

"""""""""""""""""""""""""""
def generate_negative_border(frequent_items, baskets):
    result = []
    candidates = []    
    while 1:
        if not candidates:
            candidates = generate_singletons_pair(baskets)
        if len(frequent_items) < len(candidates[0]):
                break
        for candidate in candidates:
            pos = len(candidate) - 1
            if candidate not in frequent_items[pos]:
                result.append(candidate)
        frequent_candidates =  frequent_items[len(candidates[0]) - 1]
        candidates = generate_pairs(frequent_candidates, baskets, len(frequent_candidates[0]) + 1)
        if not candidates:
            break
    return result

"""""""""""""""""""""""""""
    Apriori Algorithm

"""""""""""""""""""""""""""
def apriori(baskets, probability, support):
    k = 1
    result = []
    candidates = []
    while 1:
        frequent_items = apriori_first_pass(k, baskets, candidates, support)
        if frequent_items:
            result.append(frequent_items)
        else:
            break
        candidates = apriori_second_pass(frequent_items, baskets, support)
        if not candidates:
            break
    return result

def apriori_first_pass(k, baskets, candidates, support):
    item_counts = count_items(candidates, baskets)
    frequent_items = generate_frequent_items(item_counts, support)
    return frequent_items

def apriori_second_pass(frequent_items, baskets, support):
    itemset_size = len(frequent_items[0])
    pairs = generate_pairs(frequent_items, baskets, itemset_size + 1)
    if pairs:
        count_pairs(pairs, baskets)
    return pairs

def count_items(candidates, baskets):
    itemset_size = 1
    result = []
    if candidates:
        itemset_size = len(candidates[0])
    if not candidates:
        ht_item = {}  
        for basket in baskets:
            for item in basket:
                ht_item.setdefault(item, 0)
                ht_item[item] += 1

        for (item, count) in ht_item.items():
            result.append([item, count])
    else:
        result = candidates
    return result

def count_pairs(pairs, baskets):
    itemset_size = len(pairs[0])
    for pair in pairs:
        count = 0
        for basket in baskets:
            if len(basket) < itemset_size:
                continue
            inside = True
            for i in range(len(pair)):
                if pair[i] not in basket:
                    inside = False
                    break
            if inside == True:
                count += 1
        pair.append(count)

def generate_frequent_items(item_counts, support):
    itemset_size = len(item_counts[0]) - 1
    frequent_items = []
    for item in item_counts:
        if item[itemset_size] >= support:
            frequent_items.append(item[:-1])
    frequent_items.sort()
    return frequent_items

def generate_pairs(frequent_items, baskets, itemset_size):
    result = []
    frequent_item_processed = []    # avoid case like ab ba
    frequent_singletons = generate_singletons(frequent_items)
    for frequent_item in frequent_items:
        ht = {}
        for basket in baskets:
            if len(basket) < itemset_size + 1:
                continue
            inside = True
            for item in frequent_item:
                if item not in basket:
                    inside = False
                    break
            if inside == True:

                for item in basket:
                    if (item not in frequent_singletons) or (item in frequent_item):
                        continue
                    ht.setdefault(item, 0)
        keys = ht.keys()
        keys.sort()
        for key in keys:
            tmp = list(frequent_item)
            tmp.extend(key)
            tmp.sort()
            if tmp not in result:
                result.append(tmp)
        frequent_item_processed.append(frequent_item)
    true_result = []
    for items in result:
        inside = True
        for i in range(len(items)):
            tmp = list(items)
            tmp.pop(i)
            if tmp not in frequent_items:
                inside = False
                break
        if inside == True:
            true_result.append(items)
    return true_result

def generate_singletons(itemsets):
    ht = {}
    for items in itemsets:
        for item in items:
            ht.setdefault(item, 0)
    keys = ht.keys()
    keys.sort()
    return keys

def generate_singletons_pair(itemsets):
    result = []
    singletons = generate_singletons(itemsets)
    for singleton in singletons:
        result.append([singleton])
    return result

if __name__ == '__main__':
    toivonen(sys.argv[1], int(sys.argv[2]))



