#! /usr/bin/env python3
# coding: utf-8
import pandas as pd
from datetime import datetime
import random


class ClientUnique:
    def __init__(self, stat_boisson, stat_nourriture):
        self.client_id = "ID" + str(datetime.now().minute) + str(datetime.now().microsecond)
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
        return drinks.get(result, '/')

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
        return foods.get(result, '/')

    def payer(self, total):
        self.budget -= total

    def get_client_id(self):
        return self.client_id


class ClientTripAdvisor(ClientUnique):
    def _pourboire(self):
        return random.uniform(0, 10)

    def payer(self, total):
        self.budget -= self._pourboire()
        super().payer(total)


class ClientRegular(ClientUnique):
    def __init__(self, stat_boisson, stat_nourriture):
        super().__init__(stat_boisson, stat_nourriture)
        self.drink_history = {}
        self.food_history = {}
        self.budget = 250


class ClientHipster(ClientRegular):
    def __init__(self, stat_boisson, stat_nourriture):
        super().__init__(stat_boisson, stat_nourriture)
        self.budget = 500


def transforme_date(date_str):
    # Date format in the CSV file that we turn into a true datetime python type
    date_format = "%d/%m/%Y %H:%M"
    return datetime.strptime(date_str, date_format)


if __name__ == "__main__":
    chemin = "Coffeebar_2013-2017.csv"
    df = pd.read_csv(chemin, sep=";")
    lignes = df.to_dict('records')
    vente_heures_drinks = {}
    vente_heures_foods = {}
    for ligne_dict in lignes:
            # in the dictionnary, we recover the value of the column FOOD
        #the second parameter (an empty string) is the value that we want if the key "FOOD" is not in the dictionnary

            food = ligne_dict.get('FOOD', '')
            if str(food) == 'nan':
                food = '/'
            drink = ligne_dict.get('DRINKS', '')
            if str(drink) == 'nan':
                drink = '/'
            customer = ligne_dict.get('CUSTOMER', '')
            heure = ligne_dict.get('TIME', '')
            heure_format = "%H:%M"
            time = transforme_date(heure)
            heure = time.strftime(heure_format)
            # We recover the sales for this hour (to update with the line that we are reading)
            dict_drinks = vente_heures_drinks.get(heure, {})
            dict_foods = vente_heures_foods.get(heure, {})
            # We add 1 to the drink and food
            total_drink = dict_drinks.get(drink, 0) + 1
            total_food = dict_foods.get(food, 0) + 1
            #  We update this number in the dictionnary
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
    heure = '13:16'
    cli1 = ClientUnique(vente_heures_drinks, vente_heures_foods)
    cli2 = ClientTripAdvisor(vente_heures_drinks, vente_heures_foods)
    cli3 = ClientRegular(vente_heures_drinks, vente_heures_foods)
    cli4 = ClientHipster(vente_heures_drinks, vente_heures_foods)
    for x in range(0, 10):
        print("Customer ID %s buy %s and %s at %s" % (cli1.get_client_id(), cli1.get_nourriture(heure), cli1.get_boisson(heure), heure))
        print("Customer ID %s buy %s and %s at %s" % (cli2.get_client_id(), cli2.get_nourriture(heure), cli2.get_boisson(heure), heure))
        print("Customer ID %s buy %s and %s at %s" % (cli3.get_client_id(), cli3.get_nourriture(heure), cli3.get_boisson(heure), heure))
        print("Customer ID %s buy %s and %s at %s" % (cli4.get_client_id(), cli4.get_nourriture(heure), cli4.get_boisson(heure), heure))
