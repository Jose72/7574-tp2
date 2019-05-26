class Counter:

    def __init__(self, limit):
        self.counter = 0
        self.limit = int(limit)

    def increment(self):
        self.counter += 1
        #print("counter: " + str(self.counter) " - limit:" )
        return self.counter == self.limit
