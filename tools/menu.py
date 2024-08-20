class Option:

    def __init__(self, name, funk, args=None):
        self.name = name
        self.funk = funk
        self.args = args

    def execute(self):
        self.funk()
        
    def exe_with_args(self, args):
        self.funk(args)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()
    
    def get_name(self):
        return self.name
    
    def get_args(self):
        return self.args if self.args is not None else ""
    
class Menu:

    def __init__(self, *options, indent=""):
        self.indent = indent
        self.options = {}
        for id, option in enumerate(options):
            self.options[id+1] = option
        self.user = None
        self.app_name = None
        
    def __str__(self):
        s = f"{self.app_name}\n" if self.app_name else ""
        for key, value in self.options.items():
            s += f"{self.indent} {key} - {value}\n"
        s += f"{self.indent} q - Wyjscie\n"
        return s

    def start(self):
        while True:
            action = input(f"{self}")
            if action.isnumeric():
                action = int(action)
                if action in self.options.keys():
                    if self.user:
                        self[action].exe_with_args(self.user)
                    else:
                        self[action].execute()
                else:
                    print("Nie znaleziono polecenia.")
            elif action == 'q':
                break
                
        
    def __getitem__(self, key):
        return self.options[key]
    

class MenuArgs:
    
    def __init__(self, options, indent=""):
        self.indent = indent
        self.options = options
        self.commands = list(options.keys())
        self.commands.append("-q")
        self.app_name = None
        
    def __str__(self):
        s = f"{self.app_name}\n" if self.app_name else ""
        for key, value in self.options.items():
            name = value.get_name()+':'
            s += f"{self.indent} {name.ljust(24)} {key} {value.get_args()}\n"
        s += f"{self.indent} {"Wyjscie:".ljust(24)} -q\n"
        return s

    def start(self):
        while True:
            user_input = input(f"{self}")
            action_list = user_input.split(" ")
            action = action_list[0]
            args = action_list[1:]
            if action in self.commands:
                if action == '-q':
                    break
                if args:
                    self[action].exe_with_args(args)
                else:
                    self[action].execute()
            else:
                print("Nie znaleziono polecenia.")

    def __getitem__(self, key):
        return self.options[key]
    