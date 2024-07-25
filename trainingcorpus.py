import os
 
class TrainingCorpus:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_names = os.listdir(self.file_path)
        with open(self.file_path + '/' + '!truth.txt', 'r', encoding="utf-8") as file:
            self.truth_body = file.read().split('\n')
 
    def get_class(self, file_name):
        for name in self.truth_body:
            name = name.split()
            if file_name == name[0]:
                if name[1] == 'OK':
                    return 'OK'
                else:
                    return 'SPAM'
     
    def is_ham(self, file_name):
        for name in self.truth_body:
            name = name.split()
            if file_name == name[0]:
                if name[1] == 'OK':
                    return True
                else:
                    return False
     
    def is_spam(self, file_name):
        for name in self.truth_body:
            name = name.split()
            if file_name == name[0]:
                if name[1] == 'SPAM':
                    return True
                else:
                    return False
     
    def spams(self):
        for name in self.truth_body:
            name = name.split()
 
            if len(name) == 0 or name[0] == '!' or name[1] != 'SPAM':
                continue
            name = name[0]
            with open(self.file_path + '/' + name, 'r', encoding="utf-8") as file:
                body = file.read()
                yield name, body
     
    def hams(self):
        for name in self.truth_body:
            name = name.split()
             
            if len(name) == 0 or name[0] == '!' or name[1] != 'OK':
                continue
            name = name[0]
            with open(self.file_path + '/' + name, 'r', encoding="utf-8") as file:
                body = file.read()
                yield name, body
