def djb2_hash(text):
    h = 5381
    for char in text:
        h = (h * 33) + ord(char)
    return h


class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''

    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity

    def __getitem__(self, key):
        return self.retrieve(key)

    def __setitem__(self, key, value):
        self.insert(key, value)

    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.
        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)

    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash
        OPTIONAL STRETCH: Research and implement DJB2
        '''
        return djb2_hash(key)

    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return djb2_hash(key) % self.capacity

    def insert(self, key, value):
        '''
        Store the value with the given key.
        Hash collisions should be handled with Linked List Chaining.
        '''
        index = self._hash_mod(key)
        linked_pair = LinkedPair(key, value)

        if not self.storage[index]:
            self.storage[index] = linked_pair
            return

        previous_head = self.storage[index]
        self.storage[index] = linked_pair

        self.storage[index].next = previous_head

    def remove(self, key):
        '''
        Remove the value stored with the given key.
        Print a warning if the key is not found.
        '''
        index = self._hash_mod(key)
        current_pair = self.storage[index]
        left_pair = None

        if not current_pair:
            print(f"LinkedPair with key: {key} does not exist!")
            return

        while current_pair:
            if current_pair.key == key:
                # print(
                #     "found", current_pair.value, [pair.value for pair in self.storage if pair is not None])
                if not left_pair:
                    self.storage[index] = current_pair.next
                    del current_pair
                    # print([pair.value for pair in self.storage if pair is not None])
                    return

                left_pair.next = current_pair.next
                del current_pair
                # print([pair.value for pair in self.storage if pair is not None])
                return
            left_pair = current_pair
            current_pair = current_pair.next

    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.
        Returns None if the key is not found.
        '''
        index = self._hash_mod(key)

        if not self.storage[index]:
            return None

        current_pair = self.storage[index]

        while current_pair:
            if current_pair.key == key:
                return current_pair.value
            current_pair = current_pair.next

        # Don't think we'll ever reach here actually
        return None

    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.
        '''
        old_storage = self.storage

        self.storage = [None] * len(old_storage) * 2

        for pair in old_storage:
            if not pair:
                continue

            current_pair = pair

            while current_pair:
                self.insert(current_pair.key, current_pair.value)
                current_pair = current_pair.next


if __name__ == "__main__":
    ht = HashTable(2)

    ht["line_1"] = "Tiny hash table"
    ht["line_2"] = "Filled beyond capacity"
    ht["line_3"] = "Linked list saves the day!"

    print("# Test storing beyond capacity")
    print(ht["line_1"])
    print(ht["line_2"])
    print(ht["line_3"])

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    print("# Test if data intact after resizing")
    print(ht["line_1"])
    print(ht["line_2"])
    print(ht["line_3"])

    print("")
