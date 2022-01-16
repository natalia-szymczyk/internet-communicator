
class User:
    
    def __init__(self, login, password):
        self.login = login 
        self.password = password
        self.description = ""
        self.name = ""
        self.friends = []

#   TODO : list of friends
        
        with open(r"internet-communicator\users.txt", "r") as f:
            for line in f:
                tmp = line.split()
                login, password, name = tmp[0], tmp[1], " ".join(tmp[2:])
                if(self.login == login):
                    self.name = name

        