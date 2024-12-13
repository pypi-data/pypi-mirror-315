## Welcome to the Humans Library
########################################
## by: Mariya Sha

class Father:
    def __init__(self):
        self.name = ""
        self.age_of_death = 0
        self.father = ""
        self.wife = []
        self.children = {}
        self.n_children = self.get_n_children()
    
    def get_n_children(self):
        n_children = sum([
            len(i) for i in self.children.values()
        ])
        return n_children
 