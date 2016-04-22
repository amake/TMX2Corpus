

class Filter(object):
    def filter(self, bitext):
        '''Override this to return a bool indicating whether to keep the segment.'''
        return True
