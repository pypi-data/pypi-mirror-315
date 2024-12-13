# Biblical Humans - Hebrews

########################################
## classes
########################################  
from . import Father

class Abraham(Father):
    def __init__(self):
        self.name = "Abraham"
        self.age_of_death = 175
        self.father = "Terah"
        self.wife = ["Sarah", "Keturah"]
        self.children = {
            "Sarah": ["Isaac"],
            "Hagar": ["Ishmael"],
            "Keturah": ["Zimran", "Jokshan", "Medan", "Midian", "Ishbak", "Shuah"]
        }
        self.n_children = self.get_n_children()
    
class Isaac(Father):
    def __init__(self):
        self.name = "Isaac"
        self.age_of_death = 180
        self.father = "Abraham"
        self.wife = ["Rebecca"]
        self.children = {
            "Rebecca": ["Esau", "Jacob"]
        }
        self.n_children = self.get_n_children()
        
class Jacob(Father):
    def __init__(self):
        self.name = "Jacob"
        self.age_of_death = 147
        self.father = "Isaac"
        self.wife = ["Leah", "Rachel"]
        self.children = {
            "Leah": ["Reuben", "Simeon", "Levi", "Judah", "Issachar", "Zebulun", "Dinah"],
            "Rachel": ["Joseph", "Benjamin"],
            "Bilhah": ["Dan", "Naphtali"],
            "Zilpah": ["Gad", "Asher"]
        }
        self.n_children = self.get_n_children()

class Joseph(Father):
    def __init__(self):
        self.name = "Joseph"
        self.age_of_death = 110
        self.father = "Jacob"
        self.wife = ["Asenath"]
        self.children = {
            "Asenath": ["Ephraim", "Manasseh"]
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
    
    abraham = Abraham()
    isaac = Isaac()
    jacob = Jacob()
    joseph = Joseph()
    
    fathers = [abraham, isaac, jacob, joseph]
    fathers_name = [i.name for i in fathers]

    mothers = sum([list(i.children.keys()) for i in fathers], [])
    children = sum([sum(i.children.values(), []) for i in fathers], [])
    
    if kind == "fathers":
        return sorted(fathers_name)
    if kind == "mothers":
        return sorted(mothers)
    if kind == "children":
        return sorted(children)
    if kind == "all":
        return sorted(list(set(fathers_name + mothers + children)))
    return None

########################################
## variables
########################################

fathers = read_humans("fathers")
mothers = read_humans("mothers")
children = read_humans("children")
everyone = read_humans("all")