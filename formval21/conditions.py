class Condition(object):
    def should_process(self, values):
        return True


class KeyCondition(Condition):
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def should_process(self, values):
        for k, v in values.iteritems():
            if k == self.key and v == self.val:
                return True
        return False
