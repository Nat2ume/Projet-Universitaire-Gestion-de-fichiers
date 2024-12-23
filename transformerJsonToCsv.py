from json import loads
from csv import DictWriter
import fonctions as f

# Vérification que le nom du fichier actuel est bien celui du programme lancé
if __name__ == "__main__":   
    try :
        j = open("que-faire-a-paris-.json") # Ouverture du fichier json 
        liste = loads(j.read()) # Création d'une liste de dictionnaires à partir du fichier json
        # Liste des clés qui ne sont pas voulues dans le csv mais qui sont dans la liste
        listeNonVoulu = ['occurrences','date_description','cover_url','cover_alt','cover_credit','tags', 'contact_facebook', 'contact_twitter', 'price_type', 'access_link', 'access_link_text', 'updated_at', 'image_couverture', 'programs', 'address_url', 'address_url_text','address_text','title_event','audience','childrens','group','locale']
        # Liste de l'ordre voulu dans les dictionnaires
        listeOrdonnee = ['id', 'url', 'title', 'lead_text', 'description', 'key_word', 'date_start', 'heure_start', 'date_end', 'heure_end', 'address_name', 'address_street', 'address_zipcode', 'address_city', 'lat_lon', 'pmr', 'blind', 'deaf', 'transport','contact_name','contact_phone','contact_mail', 'contact_url' , 'access_type','price_detail','URL of the cover image']
        # Liste dans l'ordre voulu en français
        listeordonneeFr = ["ID" ,"URL" ,"Titre" ,"Chapeau" ,"Description" , "Mots clés" , "Date de début" ,"Heure de début" ,"Date de fin" ,"Heure de Fin" ,"Nom du lieu" ,"Adresse du lieu" ,"Code Postal" , "Ville" ,"Coordonnées géographiques" ,"Accès PMR" ,"Accès mal voyant" ,"Accès mal entendant" ,"Transport" ,"Nom de contact" ,"Téléphone de contact" ,"Email de contact" ,"Url de contact" , "Type d’accès", "Détail du prix" ,"URL de l’image de couverture."]
        # Liste vierge qui contiendra tous les dictionnaires en français
        listefr = []
        
        
        # Enlever les clés qui ne sont pas voulues
        for dico in liste:
            for element in listeNonVoulu:
                del(dico[element])

        for dico in liste:
            # Création dans tous les dictionnaires, les clés qui sont demandées mais pas dedans
            dico["heure_start"] = None
            dico["heure_end"] = None
            dico["contact_name"] = None
            dico["URL of the cover image"] = None
            dico["key_word"] = None
            
            # Recherche des clés dans le dictionnaire
            for cle in dico:
                # Prendre le cas où il y a des valeurs avec les clés
                if dico[cle] is not None:
                    # Modification pour les clés description et price_detail pour enlever les traces HTML
                    if cle == "description" or cle == "price_detail":
                        dico[cle] = f.enleveTagsHtml(dico[cle])
                    
                    # Modification pour les clés pmr, blind et deaf pour remplacer le binaire en mot français
                    if cle == "pmr" or cle == "blind" or cle == "deaf":
                        dico[cle] = f.binaireToFrancais(dico[cle])

                    # Modification pour les clés date_start et date_end afin d'avoir les dates et les heures séparées 
                    if cle == "date_start":
                        dateHeure = f.dateVersDateEtHeures(dico[cle])
                        dico["date_start"] = dateHeure[0]
                        dico["heure_start"] = dateHeure[1]
                    if cle == "date_end":
                        dateHeure = f.dateVersDateEtHeures(dico[cle])
                        dico["date_end"] = dateHeure[0]
                        dico["heure_end"] = dateHeure[1]
        
        # Réordonner les clés des dictionnaires dans l'ordre voulu
        for i in range(len(liste)):
            liste[i] = {cle: liste[i][cle] for cle in listeOrdonnee}
            
        # Traduction en français de toutes les clés
        for dico in liste:
            # Création d'un nouveau dictionnaire pour chaque dictionnaire pris dans la liste
            dicofr = {}
            # Indice pour parcourir la liste française
            i = 0
            # Parcours des clés dans le dico en anglais
            for cle in dico:
                # Création de chaque élément dans le dictionnaire français avec la clé en français et la valeur qui est celle du dictionnaire en anglais
                dicofr[listeordonneeFr[i]] = dico[cle]
                i += 1
            # Ajout de chaque nouveau dictionnaire dans une liste
            listefr.append(dicofr)
        
        # Ouverture ou création de fichier csv au nom voulu en écriture au format texte avec l'encodage utf-8
        fichier = open("que-faire-a-paris.csv", "wt",encoding='utf-8',newline="" ) 
        
        # Ajout de toutes les clés pour former la première ligne du fichier csv
        ecritCSV = DictWriter(fichier,delimiter=";",fieldnames=listefr[0].keys())
        ecritCSV.writeheader() 
        
        # Ajout de toutes les valeurs dans le fichier csv
        for dicofr in listefr:
            ecritCSV.writerow(dicofr)
        
        # Fermeture des fichiers csv et json
        fichier.close()
        j.close()
        
    # Affiche un message à l'utilisateur si le fichier json n'est pas présent dans le dossier
    except FileNotFoundError: 
        print("Fichier introuvable")