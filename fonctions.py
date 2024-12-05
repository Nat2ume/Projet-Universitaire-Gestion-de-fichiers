from bs4 import BeautifulSoup

def enleveTagsHtml(texte : str) -> str:
    '''
    Objectif
    ----------
    Fonction qui permet de transformer un programme HTML (au format str) à un texte (au format str)

    Parameters
    ----------
    texte : str , Texte initial avec les <> de HTML

    Returns
    -------
    str , Texte renvoyer sans aucune trace de HTML
    
    Exemple d'appel
    ----------
    remove_html_tags("<body><p>Bienvenue sur mon site web ! Visitez ce lien pour plus d'informations.</p></body>") renvoie "Bienvenue sur mon site web ! Visitez ce lien pour plus d'informations."

    '''
    textTransforme = BeautifulSoup(texte, "html.parser")
    return textTransforme.get_text()

def estBissextile(annee : int) -> bool:
    '''
    Objectif
    ----------
    Fonction qui permet de savoir si une année est bissextille

    Parameters
    ----------
    annee : int , une année que l'on veut savoir si elle est bissextille

    Returns
    -------
    bool , qui est True si l'année est bissextille False sinon
    
    Exemple d'appel
    ----------
    estBissextile(2020) renvoie True 
    
    '''
    
    # Vérification de toutes les conditions pour que se soit une année bissextille
    # Divisible par 4 et 100 ou alors divisible par 400
    if (annee % 4 == 0 and annee % 100 != 0) or (annee % 400 == 0):
        return True
    else:
        return False
    
def dateVersDateEtHeures(dateHeures : str) -> tuple():
    '''
    Objectif
    ---------- 
    Fonction permettant de convertir une unique chaine de caractère avec date et heure au format "AAAA-MM-JJTHH:MM:SS+0n:00" en un tuple (date, heure)
    
    Parameters
    ----------
    dateHeures : str , au format "AAAA-MM-JJThh:mm:ss+0n:00"
        
    Returns
    -------
    tuple , au format (date, heure)
        
    Exemple d'appel
    ----------
    dateVersDateEtHeures("2024-11-23T16:00:00+01:00") renvoie ('23-11-2024', '16:00:00')
    
    
    '''
    
    # Séparation et mise au format français de la date et de l'heure grâce aux fonction dateFr() et heurefr()
    date = dateFr(dateHeures)
    heure  = heureFr(dateHeures)
    
    # Indices qui séparent les heures des minutes 
    pointH = heure.find(":")
    # Indices qui séparent les jours des mois
    tiretD = date.find("-")
    
    
    anneeBi = estBissextile(int(date[8:]))
    # Vérification si l'année donnée est bissextille
    # Si oui février a 29 jours
    if anneeBi:
        listeMois = [31,29,31,30,31,30,31,31,30,31,30,31]
    # Si non février a 28 jours
    else:
        listeMois = [31,28,31,30,31,30,31,31,30,31,30,31]

    # Modification si l'heure donner par heurefr() est supérieur à 24h
    if int(heure[:pointH]) >= 24:
        heure = str(int(heure[:pointH]) - 24) + heure[pointH:]
        
        # Rajout de 1 jour à la date en gardant le format d'origine de la date
        if int(date[:tiretD]) >= 10:
            date = str(int(date[:tiretD]) + 1) + date[tiretD:]
        else :
            date = "0" + str(int(date[:tiretD]) + 1) + date[tiretD:]
        
        
        if int(date[:tiretD]) > listeMois[int(date[3:5]) - 1]:
            # Rajout de 1 moi à la date en gardant le format d'origine de la date
            if int(date[3:5]) >= 10 :
                date = "01" + "-" + str(int(date[3:5]) + 1) + date[5:]
            else :
                date = "01" + "-0" + str(int(date[3:5]) + 1) + date[5:]
            
            if int(date[3:5]) > 12:
                # Rajout de 1 année à la date en gardant le format d'origine de la date
                date = date[:3] + "0" + str(int(date[3:5]) - 12) +  "-" +str(int(date[6:]) + 1)
                
                
    # Modification si l'heure donner par heurefr() est inférieur à 0h         
    elif int(heure[:pointH]) < 0:
        heure = str(24 + int(heure[:pointH])) + heure[pointH:]
        # Diminution de 1 jour à la date
        date = "0" + str(int(date[:tiretD]) - 1) + date[tiretD:]
        
        if int(date[:tiretD]) < 1:
            # Modification du jour et diminution du mois de 1 en gardant le format d'origine de la date
            if int(date[3:5]) >= 10:
                date = str(listeMois[int(date[3:5]) - 2] + int(date[:tiretD])) + "-" + str(int(date[3:5]) - 1) + date[5:]
            else :
                date = str(listeMois[int(date[3:5]) - 2] + int(date[:tiretD])) + "-0" + str(int(date[3:5]) - 1) + date[5:]
            
            # Modification du mois et diminution de l'année de 1 en gardant le format d'origine de la date
            if int(date[3:5]) < 1:
                date = date[:3] + str(12 - int(date[3:5])) + "-" + str(int(date[6:]) -1)
        
    return date,heure


    
def dateFr(dateHeures : str) -> str:
    '''
    Objectif
    ---------- 
    Fonction permettant de convertir une unique chaine de caractère avec date et heure au format "AAAA-MM-JJTHH:MM:SS+0n:00" et en donner seulement la date au format français

    Parameters
    ----------
    dateHeures : str , au format "AAAA-MM-JJThh:mm:ss+0n:00"

    Returns
    -------
    date : str , au format "JJ-MM-AAAA"
    
    Exemple d'appel
    ----------
    dateFr("2024-11-23T16:00:00+01:00") renvoie "23-11-2024"

    '''
    # Isolation de la date
    date = list(dateHeures[:10])
    
    # Modification de la date au format francais
    date[8:10],date[5:7],date[:4] = date[:4],date[5:7],date[8:10]
    date = ''.join(date)
    
    return date


def heureFr(dateHeures : str) -> str:
    '''
    Objectif
    ---------- 
    Fonction permettant de convertir une unique chaine de caractère avec date et heure au format "AAAA-MM-JJTHH:MM:SS+0n:00" et en donner seulement l'heure au format français

    Parameters
    ----------
    dateHeures : str , au format "AAAA-MM-JJThh:mm:ss+0n:00"

    Returns
    -------
    heure : str , au format "hh:mm:ss"
    
    Exemple d'appel
    ----------
    heureFr("2024-11-23T16:00:00+01:00") renvoie "16:00:00"

    '''
    # Isolation de l'heure
    heureTotal = dateHeures[11:]
    
    # Séparation heure et utc
    heure = heureTotal[:8]
    utc = heureTotal[8:]
    
    # Indices qui séparent les heures des minutes 
    pointH = heure.find(":")
    pointU = utc.find(":")
    
    # Modification de l'heure au format français
    heure = str(int(heure[:pointH]) + int(utc[:pointU]) - 1) + heure[pointH:]
      
    return heure

