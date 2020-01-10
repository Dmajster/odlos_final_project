import pandas

class MovieData:
    def __init__(self, path: str):
        self.path = path    
        self.data = pandas.read_csv(path, sep='\t', encoding = 'ISO-8859-1')

    def get_title(self, id: int):
        matches = self.data.loc[self.data['id'] == id, 'title']
        return next(iter(matches), 'no match')