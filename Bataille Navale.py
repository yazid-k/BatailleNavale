#Constantes
N=10
COLONNES=[str(i) for i in range(N)]
LIGNES = [' '] + list(map(chr, range(97, 107)))
DICT_LIGNES_INT = {LIGNES[i]:i-1 for i in range(len(LIGNES))}
VIDE = '.'
EAU='o'
TOUCHE='x'
BATEAU='#'
DETRUIT='@'
NOMS=['Transporteur','Cuirassé','Croiseur','Sous-marin','Destructeur']
TAILLES=[5,4,3,3,2]

from random import*
from typing import Tuple

def create_grid():
    l=[]
    for i in range(N):
        l.append([])
    for i in l:
        for j in range(N):
            i.append(VIDE)
    return l

def plot_grid(m):
    s=''
    s+=LIGNES[0]+' '
    for i in range(N):
        s+=COLONNES[i]+' '
    s+='\n'
    for i in range(N):
        s+=LIGNES[i+1]+' '
        for j in range(N):
            s+=m[i][j]+' '
        s+='\n'
    return s

def tir(m,pos,flotte):
    if m[pos[0]][pos[1]]==EAU or m[pos[0]][pos[1]]== TOUCHE:
        print("Case déja touchée ")
        return False
    if presence_bateau(pos,flotte):
        m[pos[0]][pos[1]]=TOUCHE
        flotte[id_bateau_at_pos(pos,flotte)]["cases touchées"]+=1
        if flotte[id_bateau_at_pos(pos,flotte)]["cases touchées"]==flotte[id_bateau_at_pos(pos,flotte)]["taille"]:
            print(flotte[id_bateau_at_pos(pos,flotte)]["nom"]+' touché-coulé ! ')
            for i in flotte[id_bateau_at_pos(pos,flotte)]["positions"]:
                m[i[0]][i[1]]=DETRUIT
            flotte.pop(id_bateau_at_pos(pos,flotte))
        else :
            print('Touché ! ')
    else :
        m[pos[0]][pos[1]]=EAU
        print("Manqué ! ")
    return True

def random_position():
    return (randint(0,N-1),randint(0,N-1))

def pos_from_string(s):
    if len(s)==3 and s[0] in LIGNES and s[2] in COLONNES :
        return (LIGNES.index(s[0])-1,int(s[2]))
    else:
        s=str(input("Erreur, entrez un couple valide : "))
        return pos_from_string(s)

def nouveau_bateau(flotte,nom,taille,pos,orientation):
    cases=[]
    for i in range(taille):
        if orientation=='h':
            cases.append((pos[0],pos[1]+i))
        if orientation=='v':
            cases.append((pos[0]+i,pos[1]))
    flotte.append({"nom":nom,"taille":taille,"cases touchées":0,"positions":cases})

def presence_bateau(pos,flotte):
    for i in flotte:
        for j in i["positions"]:
            if j==pos:
                return True
    return False

def plot_flotte_grid(m,flotte):
    s=''
    s+=LIGNES[0]+' '
    for i in range(N):
        s+=COLONNES[i]+' '
    s+='\n'
    for i in range(N):
        s+=LIGNES[i+1]+' '
        for j in range(N):
            if presence_bateau((i,j),flotte):
                if m[i][j]==TOUCHE:
                    s+=TOUCHE+' '
                else :
                    s+=BATEAU+' '
            else :
                s+=m[i][j]+' '
        s+='\n'
    return s

def input_ajout_bateau(flotte,nom,taille):

    position=str(input())
    pos=pos_from_string(position)
    orientation=str(input("Entrez une orientation (h ou v) : "))
    while not(orientation=='h' or orientation=='v'):
        orientation=str(input("Erreur, entrez une orientation valide (h ou v) : "))

    cases=[]
    for i in range(taille):
        if orientation=='h':
            cases.append((pos[0],pos[1]+i))
        if orientation=='v':
            cases.append((pos[0]+i,pos[1]))

    for i in cases:
        if i[0]>N-1 or i[1]>N-1:
            print("Bateau ajouté hors du champ de bataille, veuillez réessayer : ",end="")
            return input_ajout_bateau(flotte,nom,taille)
        if presence_bateau(i,flotte):
            print("Bateau ajouté sur un autre bateau, veuillez réessayer : ",end="")
            return input_ajout_bateau(flotte,nom,taille)

    nouveau_bateau(flotte,nom,taille,pos,orientation)

def init_joueur():
    m=create_grid()
    flotte=[]
    for i in range(len(NOMS)):
        print("Entrez une position pour placer votre "+NOMS[i]+" de taille "+str(TAILLES[i])+" : ",end="")
        input_ajout_bateau(flotte,NOMS[i],TAILLES[i])
    return m,flotte

def init_ia():
    m=create_grid()
    flotte=[]
    s="vh"
    i=0
    while i<len(NOMS):
        pos=random_position()
        orientation=choice(s)
        a=False
        j=0
        for j in range(TAILLES[i]):
            if orientation=='h':
                if presence_bateau((pos[0],pos[1]+j),flotte) or pos[0]>N-1 or pos[1]+j>N-1:
                    a=True
            if orientation=='v':
                if presence_bateau((pos[0]+j,pos[1]),flotte) or pos[0]+j>N-1 or pos[1]>N-1:
                    a=True
        if not a:
            nouveau_bateau(flotte,NOMS[i],TAILLES[i],pos,orientation)
            i+=1
    return m,flotte

def id_bateau_at_pos(pos,flotte):
    for i in flotte:
        if pos in i["positions"]:
            return flotte.index(i)
    return None

def tour_ia_random(m,flotte):
    a=False
    while not a:
        pos=random_position()
        if m[pos[0]][pos[1]]!=EAU and m[pos[0]][pos[1]]!=TOUCHE and m[pos[0]][pos[1]]!=DETRUIT:
            tir(m,pos,flotte)
            a=True

def tour_ia_better_random(m,flotte):
    tir_potentiel=[]
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j]==TOUCHE:
                if i!=N-1:
                    tir_potentiel.append((1,0))
                if i!=0:
                    tir_potentiel.append((-1,0))
                if j!=N-1:
                    tir_potentiel.append((0,1))
                if j!=0:
                    tir_potentiel.append((0,-1))
                for k in tir_potentiel:
                    if m[i+k[0]][j+k[1]]==VIDE:
                        return tir(m,(i+k[0],j+k[1]),flotte)
    tour_ia_random(m,flotte)
                    
def tour_joueur(m,flotte):
    s=str(input("Tir : "))
    tour=tir(m,pos_from_string(s),flotte)
    while not tour:
        return tour_joueur(m,flotte)

def test_fin_partie(nom,flotte,nb_tour):
    if flotte==[]:
        print(nom+" a gagné en "+str(nb_tour)+" tours ! ")
        exit()

def joueur_vs_ia():
    m_joueur,flotte_joueur=init_joueur()
    m_ia,flotte_ia=init_ia()
    nb_tour=1
    while True:
        print(hide(plot_flotte_grid(m_ia,flotte_ia)))
        tour_joueur(m_ia,flotte_ia)
        test_fin_partie("Joueur 1",flotte_ia,nb_tour)
        tour_ia_better_random(m_joueur,flotte_joueur)
        test_fin_partie("IA",flotte_joueur,nb_tour)
        nb_tour+=1

def hide(str):
    return str.replace(BATEAU,VIDE)

def joueur_vs_joueur():
    m_joueur1,flotte_joueur1=init_joueur()
    m_joueur2,flotte_joueur2=init_joueur()
    nb_tour=1
    while True:
        print(hide(plot_flotte_grid(m_joueur1,flotte_joueur1)))
        tour_joueur(m_joueur1,flotte_joueur1)
        test_fin_partie("Joueur 1",flotte_joueur1,nb_tour)
        print(hide(plot_flotte_grid(m_joueur2,flotte_joueur2)))
        tour_joueur(m_joueur2,flotte_joueur2)
        test_fin_partie("Joueur2 ",flotte_joueur2,nb_tour)
        nb_tour+=1

def choix():
    a=input("1 ou 2 joueurs ? ")
    while a!='1' and a!='2':
        print("Choix erroné ")
        return choix()
    if a=='1':
        joueur_vs_ia()
    if a=='2':
        joueur_vs_joueur()
choix()
