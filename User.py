
class User:
    
    def __init__(self, login, password):
        self.login = login 
        self.password = password
        self.description = ""
        self.name = ""
        self.friends = []
        
        with open(r"internet-communicator\users.txt", "r") as f:
            for line in f:
                tmp = line.split()
                login, password, name = tmp[0], tmp[1], " ".join(tmp[2:])
                if(self.login == login):
                    self.name = name

        with open(r"internet-communicator\friends.txt", 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith(self.login):
                    friendsLogins = lines[i].split()[1:]
                    self.friends = friendsLogins
                    # self.friends = [self.getUser(name) for name in friendsLogins]

        with open(r"internet-communicator\descriptions.txt", 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith(self.login):
                    tmp = lines[i].split()[1:]
                    self.description = " ".join(tmp)
        
    def toString(self):
        return f"{self.name} ({self.login}): {self.description}"

    def updateDescription(self, description):
        self.description = description

        # TODO zle sie zmienia, dopisuje bez sensu na koncu pliku, nwm o co chodzi

        notInFile = True
        
        with open(r"internet-communicator\descriptions.txt", 'r+') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith(self.login):
                    notInFile = False
                    lines[i] = f"{self.login} {description} \n"

            f.seek(0)
            for line in lines:
                f.write(line)
            
            if notInFile:
                f.write(f"{self.login} {description} \n")
        

def getUser(wantedLogin):
    print(f"zaczynam szukac uzytkownika o loginie {wantedLogin}")

    with open(r"internet-communicator\users.txt", "r") as f:
        for line in f:
            tmp = line.split()
            login, password, name = tmp[0], tmp[1], " ".join(tmp[2:])
            if(wantedLogin == login):
                print(f"znaleziony {wantedLogin}")
                return User(login, password)

    print(f"nie ma uzytkownika o loginie {wantedLogin}")
    
    return None

def addFriend(user1, user2):
    login1, login2 = user1.login, user2.login

    user1.friends.append(login2)
    user2.friends.append(login1)

    print(f"znajomi: {login1} i {login2}")

    with open(r"internet-communicator\friends.txt", 'r+') as f: 
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith(login1):
                lines[i] = lines[i].strip() + " " + login2 + "\n"
        f.seek(0)
        for line in lines:
            f.write(line)    

    with open(r"internet-communicator\friends.txt", 'r+') as f: 
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith(login2):
                lines[i] = lines[i].strip() + " " + login1 + "\n"
        f.seek(0)
        for line in lines:
            f.write(line)
