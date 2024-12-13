# Biblical Humans - Mesopotamians 

########################################
## classes
########################################   
from . import Father

class Noah(Father):
    def __init__(self):
        self.name = "Noah"
        self.age_of_death = 950
        self.father = "Lamech"
        self.wife = ["Unknown"]
        self.children = {
            "Unknown": ["Shem", "Ham", "Japheth"]
        }
        self.n_children = self.get_n_children()
        
class Shem(Father):
    def __init__(self):
        self.name = "Shem"
        self.age_of_death = 600
        self.father = "Noah"
        self.wife = ["Unknown"]
        self.children = {
            "Unknown": ["Cush", "Mizraim", "Phut", "Canaan"]
        }
        self.n_children = self.get_n_children()
        
class Ham(Father):
    def __init__(self):
        self.name = "Ham"
        self.age_of_death = None
        self.father = "Noah"
        self.wife = ["Unknown"]
        self.children = {
            "Unknown": ["Elam", "Ashur", "Arphaxad", "Lud", "Aram"]
        }
        self.n_children = self.get_n_children()
        
class Japheth(Father):
    def __init__(self):
        self.name = "Japheth"
        self.age_of_death = None
        self.father = "Noah"
        self.wife = ["Unknown"]
        self.children = {
            "Unknown": ["Gomer", "Magog", "Tiras", "Javan", "Meshech", "Tubal", "Madai"]
        }
        self.n_children = self.get_n_children()
    
########################################
## functions
########################################

def read_humans(kind):
    """
    - input: string of either [fathers, mothers, children, all]
    - output: list of matching humans
    """
    
    noah = Noah()
    shem = Shem()
    ham = Ham()
    japheth = Japheth()
    
    fathers = [noah, shem, ham, japheth]
    fathers_name = [i.name for i in fathers]

    children = sum([sum(i.children.values(), []) for i in fathers], [])
    
    if kind == "fathers":
        return sorted(fathers_name)
    if kind == "children":
        return sorted(children)
    if kind == "all":
        return sorted(list(set(fathers_name + children)))
    return None

########################################
## variables
########################################

fathers = read_humans("fathers")
children = read_humans("children")
everyone = read_humans("all")
        
 