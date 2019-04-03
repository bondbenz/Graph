#!/usr/bin/python
import numpy as np
from collections import defaultdict
import operator
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import pylab

class Sommet:
    def __init__(self, sommet, num):
        self.nom = sommet
        self.adjs = []
        self.arcs = []
        self.num = int(num)
        self.couleur = ''

    def __str__(self):
        return str(self.nom)

    def __repr__(self):
        return str(self.nom)

    def ajouterAdj(self, adj):
        if isinstance(adj, Sommet):
            if adj not in self.adjs:
                self.adjs.append(adj)
                if gl==1:
                    adj.adjs.append(self)
            else:
                raise Exception('Deja un adjacent')
        else:
            raise Exception('Ne\'st pas un sommet!')

    def ajouterArc(self, arc):
        if isinstance(arc, Arc):
            if arc not in self.arcs:
                self.arcs.append(arc)
            else:
                raise Exception('Deja existe!')
        else:
            raise Exception('Ne\'st pas un arc!')

    def trierArc(self):
        self.arcs.sort(key=lambda arc: arc.poid)


class Arc:
    def __init__(self, arc, num, poid, src, des):
        self.nom = arc
        self.num = num
        self.poid = poid
        if (isinstance(src, Sommet) and isinstance(des, Sommet)):
            self.source = src
            self.destination = des
        else:
            print 'Error Sommet'

    def __str__(self):
        return str(self.nom)

    def __repr__(self):
        return str(self.nom)

class Graphe:
    def __init__(self,grapheType):
        self.sommets = []
        self.sommetsNoms = []
        self.arcs = []
        self.matricePonderation = []
        self.matriceAdjacence = []
        self.grapheType = grapheType
        self.matriceIncidence = []
        self.listeAdjacence = defaultdict(list)
        self.arbres = []
        self.kruskal = []
        self.u = []
        self.f = []
        self.co = []
        self.couleurs = ['red', 'green', 'blue', 'yellow', 'brown', 'purple', 'black', 'white']
        self.visit = []
        self.d = {}
        self.p = {}
        self.djikstra = {}
        self.pbellman = {}
        self.bellmanford = {}
        self.dbellsimple = {}
        self.bp = {}
        self.p = defaultdict(list)
        self.niveaux = defaultdict(list)
        self.t = []
        self.sos = {}
        self.dfloyd = []
        self.pfloyd = []

    def ajouterSommet(self, sommet):
        if isinstance (sommet, Sommet):
            self.sommets.append(sommet)
            self.sommetsNoms.append(sommet.nom)
        else:
            raise Exception('%s Ne\'st pas un sommet!') %(str(sommet.nom))

    def ajouterArc(self, arc):
        if isinstance (arc, Arc):
            self.arcs.append(arc)
        else:
            raise Exception('%s N\'est pas un arc!') % (str(arc.nom))


    #lire depuis fichier
    def grapheRemplire(self):
        #pour les sommets
        sommetsAajout = []
        graphef = open('graphe.txt','r').readlines()
        for arc in graphef:
            arc = arc.rstrip().split(' ')
            if arc[0] not in sommetsAajout:
                sommetsAajout.append(arc[0])
            if arc[1] not in sommetsAajout:
                sommetsAajout.append(arc[1])
        i = 0
        for s in sommetsAajout:
            sommet = Sommet(s,i)
            self.ajouterSommet(sommet)
            i+=1

        #pour les arcs
        i = 0
        for arc in graphef:
            arc = arc.rstrip().split(' ')
            arcSource = str(arc[0])
            arcDestination = str(arc[1])
            arcPoid = int(arc[2])
            if ((arcSource and arcDestination) in self.sommetsNoms):
                arc = Arc('u'+str(i), i, arcPoid, self.sommets[self.sommetsNoms.index(arcSource)], self.sommets[self.sommetsNoms.index(arcDestination)])
                self.ajouterArc(arc)
                if self.grapheType == 1:
                    self.sommets[self.sommetsNoms.index(arcSource)].ajouterAdj(self.sommets[self.sommetsNoms.index(arcDestination)])
            #graphe.sommets[graphe.sommetsNoms.index(arcDestination)].ajouterAdj(graphe.sommets[graphe.sommetsNoms.index(arcSource)])
                else:
                    self.sommets[self.sommetsNoms.index(arcSource)].ajouterAdj(self.sommets[self.sommetsNoms.index(arcDestination)])
                self.sommets[self.sommetsNoms.index(arcSource)].ajouterArc(arc)
                self.sommets[self.sommetsNoms.index(arcDestination)].ajouterArc(arc)
            else:
                print 'Source ou destination nest pas valid'
            i+=1
    def matriceGUI(self,matrice,title):
        w = 5
        h = 5
        plt.figure(1, figsize=(w, h))
        tb = plt.table(cellText=matrice, loc=(0,0), cellLoc='center')
        tb.set_fontsize(25)
        tc = tb.properties()['child_artists']
        for cell in tc:
            cell.set_height(1.0/matrice.shape[0])
            cell.set_width(1.0/matrice.shape[1])
        ax = plt.gca()
        ax.set_xticks([])
        ax.set_yticks([])
        plt.suptitle(str(title), fontsize=16)
        plt.show()

    #TP1
    def matriceAdjacenceGen(self):
        shape = int(len(self.sommets))
        self.matriceAdjacence = np.full((shape,shape), 0)
        if self.grapheType==1:
            for arc in self.arcs:
                    for sommet in self.sommets:
                        if (arc.destination in sommet.adjs):
                            self.matriceAdjacence[arc.source.num][arc.destination.num] = 1
                            self.matriceAdjacence[arc.destination.num][arc.source.num] = 1
                        else:
                            self.matriceAdjacence[sommet.num][arc.destination.num] = 0
                            self.matriceAdjacence[arc.destination.num][sommet.num] = 0
        else:
            for arc in self.arcs:
                    for sommet in self.sommets:
                        if (arc.destination in sommet.adjs):
                            self.matriceAdjacence[arc.source.num][arc.destination.num] = 1
                        else:
                            self.matriceAdjacence[sommet.num][arc.destination.num] = 0

        np.fill_diagonal(self.matriceAdjacence, 0)
        print self.matriceAdjacence
        self.matriceGUI(self.matriceAdjacence,'Matrice Adjacence')

    def matriceIncidenceGen(self):
        self.matriceIncidence = np.zeros(shape=(len(self.sommets), len(self.arcs)))
        for arc in self.arcs:
            if self.grapheType == 1:
                self.matriceIncidence[arc.source.num][arc.num] = 1
                self.matriceIncidence[arc.destination.num][arc.num] = 1
            else:
                self.matriceIncidence[arc.source.num][arc.num] = 1
                self.matriceIncidence[arc.destination.num][arc.num] = -1
        print self.matriceIncidence
        self.matriceGUI(self.matriceIncidence,'Matrice Incidence')

    def listeGen(self):
        for sommet in self.sommets:
            for adj in sommet.adjs:
                self.listeAdjacence[sommet.nom].append(adj.nom)
        print self.listeAdjacence
    #TP2
    def matricePonderationGen(self):
        shape = int(len(self.sommets))
        self.matricePonderation = np.full((shape,shape), 999)
        if self.grapheType==1:
            for arc in self.arcs:
                    for sommet in self.sommets:
                        if (arc.destination in sommet.adjs):
                            self.matricePonderation[arc.source.num][arc.destination.num] = arc.poid
                            self.matricePonderation[arc.destination.num][arc.source.num] = arc.poid
                        else:
                            self.matricePonderation[sommet.num][arc.destination.num] = 999
                            self.matricePonderation[arc.destination.num][sommet.num] = 999
        else:
            for arc in self.arcs:
                    for sommet in self.sommets:
                        if (arc.destination in sommet.adjs):
                            self.matricePonderation[arc.source.num][arc.destination.num] = arc.poid
                        else:
                            self.matricePonderation[sommet.num][arc.destination.num] = 999

        np.fill_diagonal(self.matricePonderation, 0)
        print self.matricePonderation
        self.matriceGUI(self.matricePonderation,'Matrice Ponderation')

    def kruskalAlgo(self):
        self.arcs.sort(key=lambda arc: arc.poid)
        for sommet in self.sommets:
            tmp = [sommet]
            self.arbres.append(tmp)
        lenghtArbre = len(self.arbres)
        for arc in self.arcs:
            i = 0
            a1 =  -1
            a2 =  -1
            while (i<lenghtArbre):
                if arc.source in self.arbres[i]:
                    a1 = i
                if arc.destination in self.arbres[i]:
                    a2 = i
                if a1!=-1 and a2!=-1 and len(self.arbres)>1:
                    for s in self.arbres[max(a1,a2)]:
                        k = 0
                        if s not in self.arbres[min(a1,a2)]:
                            k = 1
                            self.arbres[min(a1,a2)].append(s)
                    if k == 1:
                        del self.arbres[max(a1,a2)]
                        self.kruskal.append(arc)
                    lenghtArbre = len(self.arbres)
                    break
                i+=1

        for arc in self.kruskal:
            print '('+str(arc.poid)+',('+arc.source.nom+','+arc.destination.nom+'))'
        G = nx.Graph()
        for arc in self.kruskal:
            G.add_edges_from([(arc.source,arc.destination)],weight=arc.poid)

        edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])

        pos=nx.spring_layout(G)
        #les poids
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_size=14)
        nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
        nx.draw(G,pos,node_size=1000)
        pylab.show()

    def primAlgo(self):
        #remove cycles
        sanscycle = []
        for sommet in self.sommets:
            tmp = [sommet]
            self.arbres.append(tmp)
        lenghtArbre = len(self.arbres)
        for arc in self.arcs:
            i = 0
            a1 =  -1
            a2 =  -1
            while (i<lenghtArbre):
                if arc.source in self.arbres[i]:
                    a1 = i
                if arc.destination in self.arbres[i]:
                    a2 = i
                if a1!=-1 and a2!=-1 and len(self.arbres)>1:
                    for s in self.arbres[max(a1,a2)]:
                        k = 0
                        if s not in self.arbres[min(a1,a2)]:
                            k = 1
                            self.arbres[min(a1,a2)].append(s)
                    if k == 1:
                        del self.arbres[max(a1,a2)]
                        sanscycle.append(arc)
                    lenghtArbre = len(self.arbres)
                    break
                i+=1
        self.u.append(self.sommets[0])
        self.sommets[0].trierArc()
        for arc in self.sommets[0].arcs:
            if (arc.destination not in self.u and arc.source in self.u) and (arc not in self.co):
                    v = arc.destination
                    if arc in sanscycle:
                        self.co.append(arc)
            if (arc.destination in self.u and arc.source not in self.u) and (arc not in self.co):
                    v = arc.source
                    if arc in sanscycle:
                        self.co.append(arc)
        if (self.sommets[0].arcs[0].destination not in self.u and self.sommets[0].arcs[0].source in self.u):
                v = arc.destination
        if (self.sommets[0].arcs[0].destination in self.u and self.sommets[0].arcs[0].source not in self.u):
                v = arc.source

        while (len(self.u)!=len(self.sommets)):
            if v not in self.u:
                self.u.append(v)
                if self.co[0] not in self.f:
                    self.f.append(self.co[0])
                    save = self.co[0]
                    while (save.source  in self.u and save.destination in self.u) and (len(self.co))>1:
                        self.co.remove(save)
                        save = self.co[0]

                for arc in v.arcs:
                    if (arc.destination not in self.u and arc.source in self.u) and (arc not in self.co):
                        self.co.append(arc)
                    if (arc.destination in self.u and arc.source not in self.u) and (arc not in self.co):
                        self.co.append(arc)
                if (self.co[0].destination not in self.u and self.co[0].source in self.u):
                    v = self.co[0].destination
                if (self.co[0].destination in self.u and self.co[0].source not in self.u):
                    v = self.co[0].source
                self.co.remove(save)
                self.co.sort(key=lambda arc :arc.poid)
        print self.f
        #print sanscycle
        #for arc in self.f:
        #    if arc not in sanscycle:
        #        self.f.remove(arc)

        print 'F:'
        for arc in self.f:
            print '('+str(arc.poid)+',('+arc.source.nom+','+arc.destination.nom+'))'
        G = nx.Graph()
        for arc in self.f:
            G.add_edges_from([(arc.source,arc.destination)],weight=arc.poid)

        edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])

        pos=nx.spring_layout(G)
        #les poids
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_size=14)
        nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
        nx.draw(G,pos,node_size=1000)
        pylab.show()

    def welshNpowell(self):
        i = 0
        adjcouleurs = []
        self.sommets.sort(key=lambda degre: len(degre.adjs), reverse=True)
        print self.sommets
        for sommet in self.sommets:
            if sommet.couleur == '':
                while(sommet.couleur == ''):
                    for adj in sommet.adjs:
                        if adj.couleur not in adjcouleurs:
                            adjcouleurs.append(adj.couleur)
                    if self.couleurs[i] not in adjcouleurs:
                        sommet.couleur = self.couleurs[i]
                        i = 0
                    else:
                        i=+1
                    if len(adjcouleurs)==len(sommet.adjs):
                        for couleur in self.couleurs:
                            if couleur not in adjcouleurs:
                                sommet.couleur = couleur
                                i = 0
                                break
                adjcouleurs = []
        for sommet in self.sommets:
            print("Sommet "+str(sommet)+" Couleur -> "+str(sommet.couleur))
            print sommet.adjs

        G = nx.Graph()
        for arc in self.arcs:
            G.add_edges_from([(arc.source,arc.destination)])


        #colorisation
        couleurs_map = []
        for node in G.nodes():
            for sommet in self.sommets:
                if node == sommet:
                    couleurs_map.append(sommet.couleur)
        pos=nx.spring_layout(G)
        nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
        nx.draw(G,pos,node_size=1000,node_color = couleurs_map)
        pylab.show()

    #TP3

    def djikstraAlgo(self):
        #verification des arcs negative
        for arc in self.arcs:
            if (arc.poid<0):
                print 'Arc avec un poid negatif a ete detecte'
                exit()
        #ajoute a dicionnaite
        for sommet in self.sommets:
            self.d[sommet] = 999;
        #djikstra general
        #init
        sommetDepart = self.sommets[0]
        self.visit.append(sommetDepart)
        self.d[sommetDepart] = 0
        self.djikstra[sommetDepart] = 0
        if self.grapheType==1:
            for arc in sommetDepart.arcs:
                if arc.source == sommetDepart:
                    v = arc.destination
                else:
                    v = arc.source
                self.d[v] = arc.poid
                self.p[v] = sommetDepart
        #boucle pour le reste
            while (len(self.visit)!=len(self.sommets)):
                sorted_d = sorted(self.d.items(), key=operator.itemgetter(1))
                minV = sorted_d[1][0]
                if minV not in self.visit:
                    self.visit.append(minV)
                for arc in minV.arcs:
                    if arc.source == minV:
                        v = arc.destination
                    else:
                        v = arc.source
                    if v not in self.visit:
                        save = self.d[v]
                        self.d[v] = min(self.d[v],self.d[minV]+arc.poid)
                        if (save==self.d[v]) and (save==999):
                            self.p[v] = minV
                        elif (save!=self.d[v]):
                            self.p[v] = minV
                self.djikstra[minV] = self.d[minV]
                del self.d[minV]
        else:
            for arc in sommetDepart.arcs:
                self.d[arc.destination] = arc.poid
                self.p[arc.destination] = sommetDepart
        #boucle pour le reste
            while (len(self.visit)!=len(self.sommets)):
                sorted_d = sorted(self.d.items(), key=operator.itemgetter(1))
                minV = sorted_d[1][0]
                if minV not in self.visit:
                    self.visit.append(minV)
                for arc in minV.arcs:
                    if arc.destination not in self.visit:
                        save = self.d[arc.destination]
                        self.d[arc.destination] = min(self.d[arc.destination],self.d[minV]+arc.poid)
                        if (save==self.d[arc.destination]) and (save==999):
                            self.p[arc.destination] = minV
                        elif (save!=self.d[arc.destination]):
                            self.p[arc.destination] = minV
                self.djikstra[minV] = self.d[minV]
                del self.d[minV]
        print 'Distances Djikstra:'
        print str(self.djikstra)
        print 'Chemin Sommet/Precedeur'
        print str(self.p)
        if self.grapheType==1:
            G = nx.Graph()
        else:
            G = nx.DiGraph()

        for arc in self.arcs:
            G.add_edges_from([(arc.source,arc.destination)],weight=arc.poid)

        edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])
        red_edges = []
        for key in self.p.keys():
            red_edges.append((self.p[key],key))
            if self.grapheType==1:
                red_edges.append((key,self.p[key]))
        for arc in red_edges:
            if arc not in G.edges():
                G.add_edges_from((arc[0],arc[1]))
        edge_colors = ['black' if not edge in red_edges else 'red' for edge in G.edges()]
        pos=nx.spring_layout(G)
        #les poids
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_size=14)
        nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
        nx.draw(G,pos,node_size=1000,edge_color=edge_colors)
        pylab.show()

    def bellmanfordAlgo(self):
        #ajoute a dicionnaite
        for sommet in self.sommets:
            self.bellmanford[sommet] = 999;
        #bellmanford general
        #init
        sommetDepart = self.sommets[0]
        self.bellmanford[sommetDepart] = 0
        #boucle pour le reste
        if self.grapheType==1:
            i = 0
            while (max(self.bellmanford.values())==999):
                if (i>len(self.sommets)-1):
                    print 'Circuit absorbant a ete detecte'
                    exit()
                for sommet in self.sommets:
                    for arc in sommet.arcs:
                        if arc.source!=sommet:
                            v = arc.source
                            arc.source = arc.destination
                            arc.destination = v
                        save = self.bellmanford[arc.destination]
                        self.bellmanford[arc.destination] = min(self.bellmanford[arc.destination],self.bellmanford[arc.source]+arc.poid)
                        if (save!=self.bellmanford[arc.destination]):
                            self.pbellman[arc.destination] = arc.source
                i=+1
        else:
            i = 0
            while (max(self.bellmanford.values())==999):
                if (i>len(self.sommets)-1):
                    print 'Circuit absorbant a ete detecte'
                    exit()
                for sommet in self.sommets:
                    for arc in sommet.arcs:
                        save = self.bellmanford[arc.destination]
                        self.bellmanford[arc.destination] = min(self.bellmanford[arc.destination],self.bellmanford[arc.source]+arc.poid)
                        if (save!=self.bellmanford[arc.destination]):
                            self.pbellman[arc.destination] = arc.source
                i=+1

        print 'Distance Bellman-Ford'
        print str(self.bellmanford)
        print 'Chemin Sommet/Precedeur'
        print str(self.pbellman)
        if self.grapheType==1:
            G = nx.Graph()
        else:
            G = nx.DiGraph()

        for arc in self.arcs:
            G.add_edges_from([(arc.source,arc.destination)],weight=arc.poid)

        edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])
        red_edges = []
        for key in self.pbellman.keys():
            red_edges.append((self.pbellman[key],key))
            if self.grapheType==1:
                red_edges.append((key,self.pbellman[key]))

        for arc in red_edges:
            if arc not in G.edges():
                G.add_edges_from((arc[0],arc[1]))
        edge_colors = ['black' if not edge in red_edges else 'red' for edge in G.edges()]
        pos=nx.spring_layout(G)
        #les poids
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_size=14)
        nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
        nx.draw(G,pos,node_size=1000,edge_color=edge_colors)
        pylab.show()

    def bellmanfordSimpleAlgo(self):
        #verification de la non-presence de circuit
        for sommet in self.sommets:
            for arc in sommet.arcs:
                for arcd in arc.destination.arcs:
                    if arcd.destination == arc.source:
                        print 'Circuit detecte'
                        exit()
        #Bellman-Ford Simplifie general
        #init
        sommetDepart = self.sommets[0]
        self.niveaux[1].append(sommetDepart)
        self.t.append(sommetDepart)
        #cherche les precedeurs
        for sommet in self.sommets:
            for arc in sommet.arcs:
                if arc.source!=sommet:
                    self.p[sommet].append(arc.source)
        #calculation des niveaux
        i = 2
        while(len(self.t)!=len(self.sommets)):
            tempNiveaux = []
            sommetPrAjout = []
            for niveau in self.niveaux.keys():
                for sommet in self.niveaux[niveau]:
                    tempNiveaux.append(sommet)
            for sommet in self.p.keys():
                tempNiveaux2 = []
                for precedeur in self.p[sommet]:
                    tempNiveaux2.append(precedeur)
                if (set(tempNiveaux2).issubset(tempNiveaux)):
                    if (sommet not in sommetPrAjout) and (sommet not in tempNiveaux):
                        sommetPrAjout.append(sommet)
                    if sommet not in self.t:
                        self.t.append(sommet)
            if sommetPrAjout!=[]:
                for sommet in sommetPrAjout:
                    self.niveaux[i].append(sommet)
                i+=1
        #2eme partie de l'algo
        #init
        self.dbellsimple[sommetDepart] = 0
        #boucle pour le reste
        i = 2
        while(len(self.dbellsimple)!=len(self.sommets)):
            for sommet in self.niveaux[i]:
                distanceValeurs = []
                for precedeur in self.p[sommet]:
                    for arc in precedeur.arcs:
                        if arc.destination==sommet:
                            distanceValeurs.append(self.dbellsimple[precedeur]+arc.poid)
                            self.sos[self.dbellsimple[precedeur]+arc.poid] = precedeur
                self.dbellsimple[sommet] = min(distanceValeurs)
                self.bp[sommet] = self.sos[min(distanceValeurs)]
            i+=1
        print 'Les Precedeurs'
        print str(self.p)
        print 'Les Niveaux'
        print str(self.niveaux)
        print 'Distance Bellman-Ford Simplifie'
        print str(self.dbellsimple)
        print 'Chemin Sommet/Precedeur'
        print str(self.bp)

        G = nx.DiGraph()
        for arc in self.arcs:
            G.add_edges_from([(arc.source,arc.destination)],weight=arc.poid)

        edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])
        red_edges = []
        for key in self.bp.keys():
            red_edges.append((self.bp[key],key))

        for arc in red_edges:
            if arc not in G.edges():
                G.add_edges_from((arc[0],arc[1]))
        edge_colors = ['black' if not edge in red_edges else 'red' for edge in G.edges()]
        pos=nx.spring_layout(G)
        #les poids
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_size=14)
        nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
        nx.draw(G,pos,node_size=1000,edge_color=edge_colors)
        pylab.show()

    def floydAlgo(self):
        shape = int(len(self.sommets))
        self.pfloyd = np.full((shape,shape), 0)
        self.matricePonderationGen()
        #Floyd general
        #init
        self.dfloyd = self.matricePonderation
        #diagonale p0(i,i)=i
        for i in range(0,shape):
            self.pfloyd[i][i] = i+1
        #init de p
        for i in range(0,shape):
            for j in range(0,shape):
                if self.dfloyd[i][j]!=999:
                    self.pfloyd[i][j] = i+1
                else:
                    self.pfloyd[i][j] = 0
        #le reste de l'algo
        for k in range(0,shape):
            d_1 = self.dfloyd
            p_1 = self.pfloyd
            #verification de circuit absorbant
            for i in range(0,shape):
                if self.dfloyd[i][i]<0:
                    print 'Circuit absorbant a ete detecte'
                    exit()
            #fixer la ligne et la colone de letape k
            for i in range(0,shape):
                self.dfloyd[i][k] = d_1[i][k]
                self.pfloyd[i][k] = p_1[i][k]
                self.dfloyd[k][i] = d_1[k][i]
                self.pfloyd[k][i] = p_1[k][i]
            for i in range(0,shape):
                for j in range(0,shape):
                    if i!=j:
                        self.dfloyd[i][j] = min(d_1[i][j],d_1[i][k]+d_1[k][j])
                        #si le minimum change
                        if (d_1[i][j]!=self.dfloyd[i][j]):
                            self.pfloyd[i][j] = p_1[k][j]

        print 'Matrice D'
        print self.dfloyd
        print 'Matrice P'
        print self.pfloyd
        self.matriceGUI(self.dfloyd,'Matrice Distance Floyd')
        self.matriceGUI(self.pfloyd,'Matrice Des Precedeurs Floyd')

def graphType():
    print '''
        [1] Graphe Non-Oriente
        [2] Graphe Oriente
    '''
    grapheT = int(raw_input("Le Type du Graphe [1/2] : "))
    return grapheT

gl = 1
def menu():
    global gl
    print '''
    </> Graph Algos
    [1]  Matrice Adjacence
    [2]  Matrice Incidence
    [3]  Liste Adjacence
    [4]  Matrice Ponderation
    [5]  Kruskal Algorithm
    [6]  Prim Algorithm
    [7]  Welsh & Powell Algorithm
    [8]  Djikstra Algorithm
    [9]  Bellman-Ford
    [10] Bellman-Ford Simplifie
    [11] Floyd Algorithm
    [99] Exit
    '''
    choix = int(raw_input("[+] Votre Choix : "))
    if choix==1:
        print '''
         ______________
        ||            ||
        ||  Matrice   ||
        ||  Adjacence ||
        ||            ||
        ||____________||
        |______________|
         \\############\\
          \\############\\
           \      ____  \
            \_____\___\___\

        '''
        typeg = graphType()
        gl = typeg
        graphe = Graphe(typeg)
        graphe.grapheRemplire()
        print 'Liste de sommets : '+str(graphe.sommets)
        graphe.matriceAdjacenceGen()
        menu()
    elif choix==2:
        print '''
         ______________
        ||            ||
        ||  Matrice   ||
        ||  Incidence ||
        ||            ||
        ||____________||
        |______________|
         \\############\\
          \\############\\
           \      ____  \
            \_____\___\___\

        '''
        typeg = graphType()
        gl = typeg
        graphe = Graphe(typeg)
        graphe.grapheRemplire()
        print 'Liste de sommets : '+str(graphe.sommets)
        graphe.matriceIncidenceGen()
        menu()
    elif choix==3:
        print '''
         ______________
        ||            ||
        ||  Liste     ||
        ||  Adjacence ||
        ||            ||
        ||____________||
        |______________|
         \\############\\
          \\############\\
           \      ____  \
            \_____\___\___\

        '''
        typeg = graphType()
        gl = typeg
        graphe = Graphe(typeg)
        graphe.grapheRemplire()
        print 'Liste de sommets : '+str(graphe.sommets)
        graphe.listeGen()
        menu()
    elif choix==4:
        print '''
         ______________
        ||            ||
        ||  Matrice   ||
        || Ponderation||
        ||            ||
        ||____________||
        |______________|
         \\############\\
          \\############\\
           \      ____  \
            \_____\___\___\

        '''
        typeg = graphType()
        gl = typeg
        graphe = Graphe(typeg)
        graphe.grapheRemplire()
        print 'Liste de sommets : '+str(graphe.sommets)
        graphe.matricePonderationGen()
        menu()
    elif choix==5:
        print '''
         ______________
        ||            ||
        ||            ||
        ||   Kruskal  ||
        ||            ||
        ||____________||
        |______________|
         \\############\\
          \\############\\
           \      ____  \
            \_____\___\___\

        '''
        typeg = 1
        gl = typeg
        graphe = Graphe(typeg)
        graphe.grapheRemplire()
        print 'Liste de sommets : '+str(graphe.sommets)
        graphe.kruskalAlgo()
        menu()
    elif choix==6:
        print '''
         ______________
        ||            ||
        ||            ||
        ||    Prim    ||
        ||            ||
        ||____________||
        |______________|
         \\############\\
          \\############\\
           \      ____  \
            \_____\___\___\

        '''
        typeg = 1
        gl = typeg
        graphe = Graphe(typeg)
        graphe.grapheRemplire()
        print 'Liste de sommets : '+str(graphe.sommets)
        graphe.primAlgo()
        menu()
    elif choix==7:
        print '''
         ______________
        ||            ||
        ||   Welsh    ||
        ||     &      ||
        ||   Powell   ||
        ||____________||
        |______________|
         \\############\\
          \\############\\
           \      ____  \
            \_____\___\___\

        '''
        typeg = 1
        gl = typeg
        graphe = Graphe(typeg)
        graphe.grapheRemplire()
        print 'Liste de sommets : '+str(graphe.sommets)
        graphe.welshNpowell()
        menu()
    elif choix==8:
        print '''
         ______________
        ||            ||
        ||            ||
        ||  Djikstra  ||
        ||            ||
        ||____________||
        |______________|
         \\############\\
          \\############\\
           \      ____  \
            \_____\___\___\

        '''
        typeg = graphType()
        gl = typeg
        graphe = Graphe(typeg)
        graphe.grapheRemplire()
        print 'Liste de sommets : '+str(graphe.sommets)
        graphe.djikstraAlgo()
        menu()
    elif choix==9:
        print '''
         ______________
        ||            ||
        ||   Bellman  ||
        ||     Ford   ||
        ||            ||
        ||____________||
        |______________|
         \\############\\
          \\############\\
           \      ____  \
            \_____\___\___\

        '''
        typeg = graphType()
        gl = typeg
        graphe = Graphe(typeg)
        graphe.grapheRemplire()
        print 'Liste de sommets : '+str(graphe.sommets)
        graphe.bellmanfordAlgo()
        menu()
    elif choix==10:
        print '''
         ______________
        ||            ||
        ||   Bellman  ||
        || Ford Simple||
        ||            ||
        ||____________||
        |______________|
         \\############\\
          \\############\\
           \      ____  \
            \_____\___\___\

        '''
        typeg = 2
        gl = typeg
        graphe = Graphe(typeg)
        graphe.grapheRemplire()
        print 'Liste de sommets : '+str(graphe.sommets)
        graphe.bellmanfordSimpleAlgo()
        menu()
    elif choix==11:
        print '''
         ______________
        ||            ||
        ||            ||
        ||    Floyd   ||
        ||            ||
        ||____________||
        |______________|
         \\############\\
          \\############\\
           \      ____  \
            \_____\___\___\

        '''
        typeg = graphType()
        gl = typeg
        graphe = Graphe(typeg)
        graphe.grapheRemplire()
        print 'Liste de sommets : '+str(graphe.sommets)
        graphe.floydAlgo()
        menu()
    elif choix==99:
        print '[!] Bye Bye!'
        exit()
    else:
        print '[!] Est-que vous etes sure que c\'est le bon choix?'
        menu()
print '''

             _____
          .-'.  ':'-.
        .''::: .:    '.
       /   :::::'      .
      ;.    ':' `       ;
      |       '..       |
      ; '      ::::.    ;
       \       '::::   /
        '.      :::  .'
          '-.___'_.-'

   </> Graph Tool | Author : Bond Benz
'''
menu()