class GenericStore:
    def __init__(self, filename, deserialize, open_func=open):
        self.filename = filename
        self.deserialize = deserialize
        self.open_func = open

    def add(self, model):
        self.persist(entry.serialize())

    def persist(self, serialized):
        with self.open_func(self.filename, "a") as output_file:
            output_file.write(serialized)
            output_file.write("\n")

    def read(self):
        with self.open_func(self.filename, deserialize) as input_file:
            return [self.deserialize(line) for line in input_file]
