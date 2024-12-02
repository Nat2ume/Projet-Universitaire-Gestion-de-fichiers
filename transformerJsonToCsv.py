from json import loads
from csv import DictWriter
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


def dateVersDateEtHeures(dateHeures : str) -> tuple():
    '''
    Objectif
    ---------- 
    Fonction permettant de convertir une unique chaine de caractère avec date et heure au format (AAAA-MM-JJTHH:MM:SS+0n:00) en un tuple (date, heure)
    
    Parameters
    ----------
    dateHeures : str , au format (AAAA-MM-JJThh:mm:ss+0n:00)
        
    Returns
    -------
    tuple , au format (date, heure)
        
    Exemple d'appel
    ----------
    dateVersDateEtHeures("2024-11-23T16:00:00+01:00") renvoie ('23-11-2024', '16:00:00')
    
    
    '''
    
    # Elimination du cas ou il n'y a pas de date
    if dateHeures == None:
        return None
    
    # Séparation de la date et l'heure
    date = list(dateHeures[:10])
    heure = dateHeures[11:]
    
    # Modification de la date au format francais
    date[8:10],date[5:7],date[:4] = date[:4],date[5:7],date[8:10]
    date = ''.join(date)
    
    # Modification de l'heure au format français
    # Modification pour un UTC positif
    if heure[8] == "+":
        heure = str(int(heure[:2]) + int(heure[9:11]) - 1) + heure[2:8]
    # Modification pour un UTC négatif
    elif heure[8] == "-":
        heure = str(int(heure[:2]) - int(heure[9:11]) - 1) + heure[2:8]

    # Séparateur pour les heures
    point = heure.find(":")
    
    # Modification si l'heure devient négative 
    if heure[0] == "-":
        # Changement de l'heure pour compter a partir de 24h pour soustraire
        heure = str(24 - int(heure[:point])) + heure[2:]
        # Baisse de 1 jour
        date = str(int(date[:2])-1) + date[2:]
    
    
    # Modification si l'heure dépace 23:59:59 
    elif int(heure[:point]) > 23:
        # Changement de l'heure pour soustraire 24h a une heure trop élevé
        heure = str(int(heure[:point]) - 24) + heure[2:]
        # Rajout de 1 jour a la date
        date = str(int(date[:2])+1) + date[2:]
            

    return date,heure
    

if __name__ == "__main__":   
    try :
        j = open("que-faire-a-paris-.json") # Ouverture du fichier json 
        liste = loads(j.read()) # Création de liste de dictionnaire a partir du fichier json
        # Liste des Cle qui ne sont pas voulu dans le csv mais qui sont dans la liste
        listeNonVoulu = ['occurrences','date_description','cover_url','cover_alt','cover_credit','tags', 'contact_facebook', 'contact_twitter', 'price_type', 'access_link', 'access_link_text', 'updated_at', 'image_couverture', 'programs', 'address_url', 'address_url_text','address_text','title_event','audience','childrens','group','locale']
        # Liste de lordre voulu dans les dictionnaires
        listeOrdonnee = ['id', 'url', 'title', 'lead_text', 'description', 'date_start', 'heure_start', 'date_end', 'heure_end', 'address_name', 'address_street', 'address_zipcode', 'address_city', 'lat_lon', 'pmr', 'blind', 'deaf', 'transport','contact_name','contact_phone','contact_mail', 'contact_url' , 'access_type','price_detail','URL of the cover image']
        
        
        # Enlever les clé qui ne sont pas voulu 
        for dico in liste:
            for element in listeNonVoulu:
                del(dico[element])

        for dico in liste:
            # Création dans tous les dictionnaire, les clés qui sont demandé mais pas dedans
            dico["heure_start"] = None
            dico["heure_end"] = None
            dico["contact_name"] = None
            dico["URL of the cover image"] = None
            
            # Recherche des clés dans le disctionnaire
            for cle in dico:
                # Prendre le cas ou il y a des valeurs avec les clés
                if dico[cle] is not None:
                    # Modification pour les clés description et price_detail et enlever les trace HTML
                    if cle == "description" or cle == "price_detail":
                        dico[cle] = enleveTagsHtml(dico[cle])

                    # Modification des valeurs pour les clés afin d'avoir date et heure séparé 
                    if cle == "date_start":
                        dateHeure = dateVersDateEtHeures(dico[cle])
                        dico["date_start"] = dateHeure[0]
                        dico["heure_start"] = dateHeure[1]
                    if cle == "date_end":
                        dateHeure = dateVersDateEtHeures(dico[cle])
                        dico["date_end"] = dateHeure[0]
                        dico["heure_end"] = dateHeure[1]
        
        # Réordonner les clés des dictionnaire dans l'ordre voulu
        for i in range(len(liste)):
            liste[i] = {cle: liste[i][cle] for cle in listeOrdonnee}
        
        # Ouverture ou création de fichier csv au nom voulu en écriture au format text avec l'encodage utf-8
        fichier = open("que-faire-a-paris.csv", "wt",encoding='utf-8',newline="" ) 
        
        # Ajout de toutes les clés pour former la premiere ligne du fichier CSV
        ecritCSV = DictWriter(fichier,delimiter=";",fieldnames=liste[0].keys())
        ecritCSV.writeheader() 
        
        # Ajout de toutes les valeurs dans le fichier CSV
        for dico in liste:
            ecritCSV.writerow(dico)
        
    # Si le fichier json donner au début nes pas présent dans le dossier
    except FileNotFoundError: 
        print("Fichier introuvable")
    
    finally:
        # fermeture des fichiers csv et json
        fichier.close()
        j.close()