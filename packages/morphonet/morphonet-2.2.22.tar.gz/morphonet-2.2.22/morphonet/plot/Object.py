from morphonet.tools import get_name, printv


class Object():
    """ Object
    """

    def __init__(self, t, id,channel=0):
        self.t = t
        self.id = id
        self.channel=channel
        self.daughters = []
        self.mothers=[]
        self.s=None

    def __str__(self):
        return "({},{},{})".format(self.t,self.id,self.channel)

    def __repr__(self):
        return self.__str__()

    def get_name(self):
        return get_name(self.t, self.id,self.channel)

    def clear_temporal_links(self):
        self.daughters.clear()
        self.mothers.clear()

    # PAST LINKS
    def add_mother(self, m):
        if m is not None:
            return m.add_daughter(self)
        return False

    def del_mother(self, m):
        if m is not None:
            return m.del_daughter(self)
        return False

    # FUTUR LINKS
    def add_daughter(self, d):
        if d is not None and d not in self.daughters:
            printv("Add temporal link for " + str(self.id) + " at " + str(self.t) + " with " + str(d.id) + " at " + str(d.t), 3)
            self.daughters.append(d)
            if self not in d.mothers:
                d.mothers.append(self)
            return True
        return False

    def del_daughter(self, d):
        if d in self.daughters:
            printv("Remove temporal link for "+str(self.id)+ " at "+str(self.t)+" with "+str(d.id)+ " at "+str(d.t),2)
            self.daughters.remove(d)
            d.mothers.remove(self)
            return True
        return False

    def del_daughters(self):
        if len(self.daughters)>0:
            printv("Clear all daughters for  " + str(self.id) + " at " + str(self.t) , 2)
            self.daughters.clear()
            return True
        return False


    def nb_daughters(self):
        return len(self.daughters)

    def nb_mothers(self):
        return len(self.mothers)


    #NODES FOR CELl LINEAGE DISTANCE
    def get_node(self, shift=1):
        node = [self.get_name()] #Ids of the dons
        life=[1] #Life lenght
        adj=[] #Lineage relation
        if self.nb_daughters() == 0:  # [a],[]
            adj= [[]]
        elif self.nb_daughters() == 1:  # [a,b],[[1],[]]
            node, adj ,life= self.daughters[0].get_node(shift=shift )
            life[0]+=1
            node[0]=self.get_name()
        else:   # Multiples Daughters (Division)
            final_adj = []
            for d in self.daughters:
                adj.append(shift)
                d_node, d_adj,d_life = d.get_node(shift=shift + 1)
                node += d_node
                life+=d_life
                for dd in d_adj: final_adj.append(dd)
                shift += len(node) - 1
            adj=[adj] + final_adj

        return node, adj, life  # Correspond to x_node,x_adj, x_life



