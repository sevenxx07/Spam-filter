import os
 
class Corpus:
    def __init__(self, filepath):
        self.filepath = filepath
         
    def emails(self):
        filenames = os.listdir(self.filepath)
         
        for name in filenames:
            if name[0] == '!':
                continue
 
            with open(self.filepath + '/' + name, 'r', encoding="utf-8") as file:
                body = file.read()
                yield name, body
