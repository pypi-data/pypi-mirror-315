class NumberIterator:
    def __init__(self, limit):
        self.current = 10
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.limit:
            raise StopIteration
        else:
            result = self.current
            self.current += 1
            return result


limit = 15
iterator = NumberIterator(limit)

for number in iterator:
    print(number)