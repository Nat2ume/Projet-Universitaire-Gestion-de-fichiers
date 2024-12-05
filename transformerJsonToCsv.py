from json import loads
from csv import DictWriter
import fonctions as f

if __name__ == "__main__":   
    try :
        j = open("que-faire-a-paris-.json") # Ouverture du fichier json 
        liste = loads(j.read()) # Création de liste de dictionnaire a partir du fichier json
        # Liste des Cle qui ne sont pas voulu dans le csv mais qui sont dans la liste
        listeNonVoulu = ['occurrences','date_description','cover_url','cover_alt','cover_credit','tags', 'contact_facebook', 'contact_twitter', 'price_type', 'access_link', 'access_link_text', 'updated_at', 'image_couverture', 'programs', 'address_url', 'address_url_text','address_text','title_event','audience','childrens','group','locale']
        # Liste de lordre voulu dans les dictionnaires
        listeOrdonnee = ['id', 'url', 'title', 'lead_text', 'description', 'key_word', 'date_start', 'heure_start', 'date_end', 'heure_end', 'address_name', 'address_street', 'address_zipcode', 'address_city', 'lat_lon', 'pmr', 'blind', 'deaf', 'transport','contact_name','contact_phone','contact_mail', 'contact_url' , 'access_type','price_detail','URL of the cover image']
        # Liste dans l'odre voulu en français
        listeordonneeFr = ["ID" ,"URL" ,"Titre" ,"Chapeau" ,"Description" , "Mots clés" , "Date de début" ,"Heure de début" ,"Date de fin" ,"Heure de Fin" ,"Nom du lieu" ,"Adresse du lieu" ,"Code Postal" , "Ville" ,"Coordonnées géographiques" ,"Accès PMR" ,"Accès mal voyant" ,"Accès mal entendant" ,"Transport" ,"Nom de contact" ,"Téléphone de contact" ,"Email de contact" ,"Url de contact" , "Type d’accès", "Détail du prix" ,"URL de l’image de couverture."]
        # Liste vierge qui contiendra tous les dictionnaires en français
        listefr = []
        
        
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
            dico["key_word"] = None
            
            # Recherche des clés dans le disctionnaire
            for cle in dico:
                # Prendre le cas ou il y a des valeurs avec les clés
                if dico[cle] is not None:
                    # Modification pour les clés description et price_detail et enlever les trace HTML
                    if cle == "description" or cle == "price_detail":
                        dico[cle] = f.enleveTagsHtml(dico[cle])

                    # Modification des valeurs pour les clés afin d'avoir date et heure séparé 
                    if cle == "date_start":
                        dateHeure = f.dateVersDateEtHeures(dico[cle])
                        dico["date_start"] = dateHeure[0]
                        dico["heure_start"] = dateHeure[1]
                    if cle == "date_end":
                        dateHeure = f.dateVersDateEtHeures(dico[cle])
                        dico["date_end"] = dateHeure[0]
                        dico["heure_end"] = dateHeure[1]
        
        # Réordonner les clés des dictionnaire dans l'ordre voulu
        for i in range(len(liste)):
            liste[i] = {cle: liste[i][cle] for cle in listeOrdonnee}
            
        # Transformation en français de toutes les clés
        for dico in liste:
            dicofr = {}
            i = 0
            for cle in dico:
                dicofr[listeordonneeFr[i]] = dico[cle]
                i += 1
            listefr.append(dicofr)
        
        # Ouverture ou création de fichier csv au nom voulu en écriture au format text avec l'encodage utf-8
        fichier = open("que-faire-a-paris.csv", "wt",encoding='utf-8',newline="" ) 
        
        # Ajout de toutes les clés pour former la premiere ligne du fichier CSV
        ecritCSV = DictWriter(fichier,delimiter=";",fieldnames=listefr[0].keys())
        ecritCSV.writeheader() 
        
        # Ajout de toutes les valeurs dans le fichier CSV
        for dicofr in listefr:
            ecritCSV.writerow(dicofr)
        
        # fermeture des fichiers csv et json
        fichier.close()
        j.close()
        
    # Si le fichier json donner au début nes pas présent dans le dossier
    except FileNotFoundError: 
        print("Fichier introuvable")

        