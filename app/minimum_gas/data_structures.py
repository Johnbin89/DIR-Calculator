class StopPair():
    def __init__(self, depth, time):
        self.depth = depth
        self.time = time

    def get_depth(self):
        return self.depth

    def get_time(self):
        return self.time
    
    def to_dict(self):
        return {'depth': self.get_depth(), 'time': self.get_time()}