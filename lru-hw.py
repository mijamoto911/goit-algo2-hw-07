import random
import time
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate(self, index):
        keys_to_remove = [k for k in list(self.cache.keys()) if k[0] <= index <= k[1]]
        for key in keys_to_remove:
            del self.cache[key]


def range_sum_no_cache(array, l, r):
    result = 0
    for i in range(l, r + 1):
        result += array[i]
        for _ in range(10):
            _ = i * 2
    return result


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, l, r, cache):
    key = (l, r)
    result = cache.get(key)
    if result is None:
        result = 0
        for i in range(l, r + 1):
            result += array[i]
            for _ in range(10):
                _ = i * 2
        cache.put(key, result)
    return result


def update_with_cache(array, index, value, cache):
    array[index] = value
    cache.invalidate(index)


def generate_realistic_queries(num_queries, array_size):
    """Generate queries with a realistic pattern that benefits from caching"""
    queries = []
    hot_spots = []
    for _ in range(5):
        l = random.randint(0, array_size - 1000)
        r = l + random.randint(100, 999)
        hot_spots.append((l, r))

    for _ in range(num_queries):
        query_type = random.choices(["Range", "Update"], weights=[0.8, 0.2])[0]
        if query_type == "Range":
            if random.random() < 0.8:
                l, r = random.choice(hot_spots)
                variation = random.randint(-5, 5)
                l = max(0, l + variation)
                r = min(array_size - 1, r + variation)
            else:
                l = random.randint(0, array_size - 101)
                r = l + random.randint(20, 100)
            queries.append(("Range", l, r))
        else:
            index = random.randint(0, array_size - 1)
            value = random.randint(1, 1000)
            queries.append(("Update", index, value))

    return queries


def main():

    ARRAY_SIZE = 10_000
    NUM_QUERIES = 5_000
    CACHE_SIZE = 500

    array_no_cache = [random.randint(1, 1000) for _ in range(ARRAY_SIZE)]
    array_with_cache = array_no_cache.copy()
    queries = generate_realistic_queries(NUM_QUERIES, ARRAY_SIZE)
    lru_cache = LRUCache(CACHE_SIZE)

    start_time = time.time()
    for i, query in enumerate(queries):
        if query[0] == "Range":
            range_sum_no_cache(array_no_cache, query[1], query[2])
        else:  # Update
            update_no_cache(array_no_cache, query[1], query[2])
    no_cache_time = time.time() - start_time

    start_time = time.time()
    for i, query in enumerate(queries):
        if query[0] == "Range":
            range_sum_with_cache(array_with_cache, query[1], query[2], lru_cache)
        else:
            update_with_cache(array_with_cache, query[1], query[2], lru_cache)
    with_cache_time = time.time() - start_time

    print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {with_cache_time:.2f} секунд")
    print(f"Прискорення: {no_cache_time / with_cache_time:.2f}x")

    print(f"\nСтатистика кешу:")
    print(f"Кількість попадань в кеш: {lru_cache.hits}")
    print(f"Кількість промахів кешу: {lru_cache.misses}")
    print(
        f"Відсоток попадань: {lru_cache.hits / (lru_cache.hits + lru_cache.misses) * 100:.2f}%"
    )
    print(f"Розмір кешу після всіх операцій: {len(lru_cache.cache)}")


if __name__ == "__main__":
    main()
