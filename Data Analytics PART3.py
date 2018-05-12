import pandas as pd
from datetime import datetime
import random

class Nourriture:
    def __init__(self, name, prix=3):
        self.prix = prix
        self.name = name

    def get_name(self):
        return self.name

    def get_prix(self):
        if self.name == '':
            return 0
        return self.prix

class Boisson:
    def __init__(self, name, prix=3):
        self.prix = prix
        self.name = name

    def get_name(self):
        return self.name

    def get_prix(self):
        if self.name == '':
            return 0
        return self.prix

class Cookie(Nourriture):
    def __init__(self):
        super().__init__("Cookie", 2)

class Sandwich(Nourriture):
    def __init__(self):
        super().__init__("Sandwich", 5)

class Milkshake(Boisson):
    def __init__(self):
        super().__init__("Milkshake", 5)

class Frappucino(Boisson):
    def __init__(self):
        super().__init__("Frappucino", 4)

class Water(Boisson):
    def __init__(self):
        super().__init__("Water", 2)

class ClientUnique:
    def __init__(self, stat_boisson, stat_nourriture):
        self.client_id = "CID" + str(datetime.now().minute) + str(datetime.now().microsecond)
        self.budget = 100
        self.csv_nourriture = stat_nourriture
        self.csv_boisson = stat_boisson

    def get_boisson(self, heure):
        nbr = 1
        csv_boisson = self.csv_boisson
        stat = csv_boisson.get(heure)
        if not stat:
            return '/'
        values = stat.values()
        total = sum([nb for nb in values])
        probs = {}
        drinks = {}
        for name, nb in stat.items():
            if name not in drinks.keys():
                drinks.update({
                    nbr: name,
                })
                nbr += 1
            prob = 0
            if total:
                prob = nb / float(total)
            probs.update({
                name: prob,
            })
        result = '/'
        if probs:
            result = random.choices(list(drinks.keys()), list(probs.values()))[0]
        drink_txt = drinks.get(result, '').lower()
        if drink_txt == 'milkshake':
            drink = Milkshake()
        elif drink_txt == 'frappucino':
            drink = Frappucino()
        elif drink_txt == 'water':
            drink = Water()
        else:
            drink = Boisson(drink_txt)
        return drink

    def get_budget(self):
        return self.budget

    def get_nourriture(self, heure):
        csv_nourriture = self.csv_nourriture
        stat = csv_nourriture.get(heure)
        if not stat:
            return '/'
        values = stat.values()
        total = sum([nb for nb in values])
        probs = {}
        foods = {}
        cpt = 1
        for name, nb in stat.items():
            if name not in foods.keys():
                foods.update({
                    cpt: name,
                })
                cpt += 1
            prob = 0
            if total:
                prob = nb / float(total)
            probs.update({
                name: prob,
            })
        result = ''
        if probs:
            result = random.choices(list(foods.keys()), list(probs.values()))[0]
        food_txt = foods.get(result, '').lower()
        if food_txt == 'sandwich':
            food = Sandwich()
        elif food_txt == 'cookie':
            food = Cookie()
        else:
            food = Nourriture(food_txt)
        return food

    def payer(self, drink, food, date):
        self.budget -= drink.get_prix() + food.get_prix()

    def get_client_id(self):
        return self.client_id

class ClientTripAdvisor(ClientUnique):
    def _pourboire(self):
        return random.uniform(0, 10)

    def payer(self, drink, food, date):
        super().payer(drink, food, date)
        self.budget -= self._pourboire()

class ClientRegular(ClientUnique):
    def __init__(self, stat_boisson, stat_nourriture):
        super().__init__(stat_boisson, stat_nourriture)
        self.drink_history = {}
        self.food_history = {}
        self.budget = 250

    def payer(self, drink, food, date):
        super().payer(drink, food, date)
        self.drink_history.update({
            date: drink.get_name(),
        })
        self.food_history.update({
            date: food.get_name()
        })

class ClientHipster(ClientRegular):
    def __init__(self, stat_boisson, stat_nourriture):
        super().__init__(stat_boisson, stat_nourriture)
        self.budget = 500

def transforme_date(date_str):
    # date format in the CSV file that we turn into a true datetime python type

    date_format = "%d/%m/%Y %H:%M"
    return datetime.strptime(date_str, date_format)

if __name__ == "__main__":
    chemin = "Coffeebar_2013-2017.csv"
    vente_heures_drinks = {}
    vente_heures_foods = {}
    dates = []
    df = pd.read_csv(chemin, sep=';')
    lignes = df.to_dict('records')
    for ligne_dict in lignes:
        #in the dictionnary, we recover the value of the column FOOD
        #the second parameter (an empty string) is the value that we want if the key "FOOD" is not in the dictionnary

        food = ligne_dict.get('FOOD', '')
        if str(food) == 'nan':
            food = '/'
        drink = ligne_dict.get('DRINKS', '')
        if str(drink) == 'nan':
            drink = '/'
        customer = ligne_dict.get('CUSTOMER', '')
        heure = ligne_dict.get('TIME', '')
        dates.append(heure)
        heure_format = "%H:%M"
        time = transforme_date(heure)
        heure = time.strftime(heure_format)
        #We recover the sales for this hour (to update with the line that we are reading)

        dict_drinks = vente_heures_drinks.get(heure, {})
        dict_foods = vente_heures_foods.get(heure, {})
        #We add 1 to the drink and food

        total_drink = dict_drinks.get(drink, 0) + 1
        total_food = dict_foods.get(food, 0) + 1
        #We update this number in the dictionnary

        dict_drinks.update({
            drink: total_drink,
        })
        dict_foods.update({
            food: total_food,
        })
        vente_heures_drinks.update({
            heure: dict_drinks,
        })
        vente_heures_foods.update({
            heure: dict_foods,
        })
    #We generate the 1000 returning customers

    clients_fideles = []
    for x in range(0, 999):
        nombre = random.uniform(0, 1)
        if nombre > 0.66666666666:
            clients_fideles.append(ClientRegular(vente_heures_drinks, vente_heures_foods))
        else:
            clients_fideles.append(ClientHipster(vente_heures_drinks, vente_heures_foods))

    #We create a csv file to simulate the 5 next years

    chemin = "nouveau_bar.csv"
    colonnes = ["TIME", "CUSTOMER", "DRINKS", "FOOD"]
    lignes = []
    with open(chemin, "w") as csv_file:
        for date in dates:
            time = transforme_date(date)
            heure = time.strftime(heure_format)
            nombre = int(random.uniform(0, 100))
            if nombre > 80:
                client = False
                #We have to generate a number until havind a client with enough money (for the returning clients)

                while not client:
                    index = int(random.uniform(0, 999))
                    client = clients_fideles[index]
                    #If the client doesn't have enough money, we ignore him et we take another one

                    if client.get_budget() < 5:
                        client = False
            else:
                nombre = int(random.uniform(0, 100))
                if nombre < 1:
                    client = ClientTripAdvisor(vente_heures_drinks, vente_heures_foods)
                else:
                    client = ClientUnique(vente_heures_drinks, vente_heures_foods)
            food = client.get_nourriture(heure)
            drink = client.get_boisson(heure)
            amount = food.get_prix() + drink.get_prix()
            client.payer(drink, food, date)
            values = {
                'TIME': date,
                'CUSTOMER': client.get_client_id(),
                'DRINKS': drink.get_name(),
                'FOOD': food.get_name(),
            }
            lignes.append(values)
    df = pd.DataFrame(lignes, columns=colonnes)
    df.to_csv("nouveau_bar.csv")
