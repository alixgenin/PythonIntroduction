import pandas as pd
from datetime import datetime
#tranform the date format in the CSV file into a real datetime python type.
def transforme_date(date_str):
    date_format = "%d/%m/%Y %H:%M"
    return datetime.strptime(date_str, date_format)

#The len () function is used to obtain the size of the list.
def imprimer_data(customers, drinks, foods, total_foods, total_drinks, vente_heures):
    global food, total, drink, heure
    nombre_clients = len(customers)
#In our case, we have deleted duplicates
# so the number of items in the list corresponds to the number of customers, foods and drinks
#The join () function (applied on a string) allows to attach the elements of the list
# with each time this string between the elements
    boissons = "\n\t- ".join([d for d in drinks if str(d) != 'non'])
    nourritures = "\n\t- ".join([f for f in foods if str(f) != 'non'])
    print("Part 1")
    print("Number of customers: %s" % nombre_clients)
    print("Foods:\n\t- %s" % nourritures)
    print("Drinks:\n\t- %s" % boissons)
    print("Part 2")
    print("Total nourriture vendue:")
#On a dictionary, the items () function is used to obtain a list with both the key and the value.
    for food, total in total_foods.items():
        print("\t- %s\t%s" % (food, total))
    print("Total boissons vendues")
    for drink, total in total_drinks.items():
        print("\t- %s\t%s" % (drink, total))
    print("Part 3")
    for heure, sous_dict in vente_heures.items():
        print("%s" % heure)
        print("Part 3")
# la fonction pop() permet d'obtenir la valeur de la clef et de la supprimer du dictionnaire
        total = float(sous_dict.pop('Total', 1))
        for type_article, articles in sous_dict.items():
            print("%s" % type_article)
            for article, nb in articles.items():
                print("\t%s: %.2f%%" % (article, nb / total * 100))
#We count the number of foods and we put that in a dictionary where the key=food and the value=number
def main():
    foods = []
    drinks = []
    customers = []
    total_foods = {}
    total_drinks = {}
    total_customers = {}
#part : sales/hours
    vente_heures = {}
#We use a loop on each element of the list (each element is a dictionary)
    cpt = 0
    chemin = "Coffeebar_2013-2017.csv"
    df = pd.read_csv(chemin, sep=';')
    lignes = df.to_dict('records')
#The to_dict ('records') allows to read each line of the file like a dictionary.
    for ligne_dict in lignes:
        cpt += 1
        print("Traitement ligne %s" % cpt)
        # Dans le dictionnaire, on récupère la valeur de la colonne FOOD.
        # Le deuxième paramètre (un string vide) est la valeur qu'on souhaite si la clef "FOOD" n'est pas dans le dict
        food = ligne_dict.get('FOOD', '')
        if str(food) == 'nan':
            food = 'Rien'
        drink = ligne_dict.get('DRINKS', '')
        if str(drink) == 'nan':
            drink = 'Rien'
        customer = ligne_dict.get('CUSTOMER', '')
        heure = ligne_dict.get('TIME', '')
        # Si la food n'est pas déjà dans la liste, on l'ajoute.
        # Ca permet d'éviter les doublons
        if food not in foods:
            foods.append(food)
        # Pareil pour drink
        if drink not in drinks:
            drinks.append(drink)
        # Et aussi pour les clients
        if customer not in customers:
            customers.append(customer)
        # Partie comptage
        total_food = total_foods.get(food, 0) + 1
        total_drink = total_drinks.get(drink, 0) + 1
        total_customer = total_customers.get(customer, 0) + 1
        # Maintenant on remet ce nombre dans le dictionnaire (vu qu'on l'a modifié)
        total_foods.update({
            food: total_food,
        })
        total_drinks.update({
            drink: total_drink,
        })
        total_customers.update({
            customer: total_customer,
        })

        # Partie vente/heure
        heure_format = "%H:%M"
        time = transforme_date(heure)
        heure = time.strftime(heure_format)
        # On récupère les ventes de cette heure là (pour les mettre à jour avec la ligne qu'on est en train de lire)
        vente_cette_heure = vente_heures.get(heure, {})
        # Ensuite pour cette heure précise, on récupère le sous-dictionnaire des foods et drinks
        vente_cette_heure_food = vente_cette_heure.get('foods', {})
        vente_cette_heure_drink = vente_cette_heure.get('drinks', {})
        # On ajoute 1 à la drink et food
        total_drink = vente_cette_heure_drink.get(drink, 0) + 1
        total_food = vente_cette_heure_food.get(food, 0) + 1
        # On met à jour ce nombre dans le dictionnaire
        vente_cette_heure_drink.update({
            drink: total_drink,
        })
        vente_cette_heure_food.update({
            food: total_food,
        })
        total = vente_cette_heure.get('Total', 0) + 1
        vente_cette_heure.update({
            'foods': vente_cette_heure_food,
            'drinks': vente_cette_heure_drink,
            'Total': total,
        })
        vente_heures.update({
            heure: vente_cette_heure,
        })
    imprimer_data(customers, drinks, foods, total_foods, total_drinks, vente_heures)

    # Voici la structure de vente_heures après la boucle:
    {
        '08:00': {
            'drinks': {
                'tea': 50,
                'cafe': 30,
            },
            'foods': {
                'sandwich': 2,
            },
            'Total': 82,
        },
        '09:00': {
            # ...
        }
    }

if __name__ == "__main__":
    main()
