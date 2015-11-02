
"""
Problem 2: Multi-Hash Algorithm

Hashing Function 1: i * j * ... * z mod bucket_size
Hashing Function 2: i + j + ... + z mod bucket_size


Executing code: 
1) $ python multihash.py input.txt 4 5
2) $ python multihash.py input1.txt 20 5

"""
import sys
import re

def multihash(inputfile, support, bucket_size):
    result = {}
    candidates = []
    step = 1
    while 1:
        ans_one = pass_one(inputfile, candidates, support, bucket_size)
        ans_two = pass_two(inputfile, ans_one, bucket_size)
        frequent_items = ans_two[0]
        result.setdefault(step, [])
        result[step].append(ans_two[0])
        if len(ans_two) == 1:
            break
        buckets = ans_one[1]
        candidates = ans_two[2]
        if not candidates:
            break
        result.setdefault(step+1, [])
        result[step+1].append(buckets)
        step += 1
    # print result
    display_result(result)
    return result

def display_result(result):
    for (k, v) in result.items():
        if k == 1:
            itemsets = v[0]
            tmp = []
            for item in itemsets:
                tmp.append(item[0])
            print "\n", tmp, "\n"
        else:
            
            bucket_counts = v[0]
            itemsets = v[1]
            for bucket_count in bucket_counts:
                print bucket_count
            print itemsets, "\n"
    print "\n"

def pass_one(inputfile, candidates, support, bucket_size):
    result = []
    itemset_size = 1
    if candidates:
        itemset_size = len(candidates[0])
    baskets = generate_baskets(inputfile)
    item_counts = count_items(candidates, support, baskets)
    frequent_items = generate_frequent_items(item_counts, support)
    result.append(frequent_items)
    pairs = generate_pairs(frequent_items, baskets, itemset_size + 1)
    if not pairs:
        return result
    buckets = hash_pairs(pairs, baskets, bucket_size)
    result.append(buckets)

    bitmap_one = generate_bitmap(buckets[0], support)
    bitmap_two = generate_bitmap(buckets[1], support)

    result.append([bitmap_one, bitmap_two])
    return result

def pass_two(inputfile, ans_one, bucket_size):
    result = []
    frequent_items = ans_one[0]
    result.append(frequent_items)
    if len(ans_one) == 1:
        return result

    bitmaps = ans_one[2]
    itemset_size = len(frequent_items[0]) + 1
    baskets = generate_baskets(inputfile)
    pairs = generate_pairs(frequent_items, baskets, itemset_size + 1)
    buckets = maping_pairs_bucket(pairs, baskets, bucket_size)

    candidates_one = get_candidates(buckets[0], bitmaps[0])
    candidates_two = get_candidates(buckets[1], bitmaps[1])

    candidates = []
    for item in candidates_one:
        if item in candidates_two:
            candidates.append(item)
    result.append(buckets)
    result.append(candidates)
    return result

def get_candidates(bucket, bitmap):
    bitmap_list = bitmap_to_list(bitmap)
    candidates = []
    for i in range(len(bitmap_list)):
        digit = bitmap_list[i]
        if digit == 1:
            for item in bucket[i]:
                candidates.append(item)
    return candidates

def bitmap_to_list(bitmap):
    bitmap_str = str(bin(bitmap))
    slen = len(bitmap_str)
    result = []
    for i in range(0, slen - 2):
        digit = int(bitmap_str[slen - 1 - i])
        result.append(digit)
    return result

def generate_frequent_items(item_counts, support):
    itemset_size = len(item_counts[0]) - 1
    frequent_items = []
    for item in item_counts:
        if item[itemset_size] >= support:
            frequent_items.append(item[:-1])
    frequent_items.sort()
    return frequent_items

def count_items(candidates, support, baskets):
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

def generate_bitmap(bucket, support):
    bitmap = 0
    for (k, v) in bucket.items():
        if v >= support:
            bitmap += 1 << k
    return bitmap

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

def maping_pairs_bucket(pairs, baskets, bucket_size):
    pair_size = len(pairs[0])
    ht_item_to_num = numbering(pairs)
    count_pairs(pairs, baskets)
    bucket_one = hash_function_one(pairs, ht_item_to_num, bucket_size)
    bucket_two = hash_function_two(pairs, ht_item_to_num, bucket_size)
    return [bucket_one, bucket_two]

def hash_function_one(pairs, ht_item_to_num, bucket_size):
    pair_size = len(pairs[0]) - 1
    bucket = {} # key: bucket_no, value: pairs
    for pair in pairs:
        bucket_no = 1
        for i in range(pair_size):
            c = pair[i]
            bucket_no *= ht_item_to_num[c]
        bucket_no %= bucket_size

        bucket.setdefault(bucket_no, [])
        bucket[bucket_no].append(pair)
    return bucket

def hash_function_two(pairs, ht_item_to_num, bucket_size):
    pair_size = len(pairs[0]) - 1
    bucket = {} # key: bucket_no, value: pairs
    for pair in pairs:
        bucket_no = 1
        for i in range(pair_size):
            c = pair[i]
            bucket_no += ht_item_to_num[c]
        bucket_no %= bucket_size

        bucket.setdefault(bucket_no, [])
        bucket[bucket_no].append(pair)
    return bucket


def hash_pairs(pairs, baskets, bucket_size):
    pair_size = len(pairs[0])
    buckets = maping_pairs_bucket(pairs, baskets, bucket_size)
    for bucket in buckets:
        count_bucket(pair_size, bucket, bucket_size)
    return buckets

def count_bucket(pair_size, bucket, bucket_size):
    for (k, v) in bucket.items():
        count = 0
        for item in v:
            count += item[pair_size]
        bucket[k] = count
    for i in range(bucket_size):
        bucket.setdefault(i, 0)
    [(k,bucket[k]) for k in sorted(bucket.keys())]

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

def numbering(pairs):
    ht_item_to_num = {}
    number = 1
    for pair in pairs:      # O(n), since length of pair is constant
        for c in pair:
            if c not in ht_item_to_num.keys():
                ht_item_to_num.setdefault(c, number)
                number += 1
    return ht_item_to_num

def generate_singletons(itemsets):
    ht = {}
    for items in itemsets:
        for item in items:
            ht.setdefault(item, 0)
    keys = ht.keys()
    keys.sort()
    return keys

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

if __name__ == '__main__':
    multihash(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))








