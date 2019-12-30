import csv

SOURCE_FILE_PATH = "indices.csv"
TARGET_FILE_PATH = "indices_combo.csv"
tab_clues = []

# Python program to illustrate the intersection 
# of two lists in most simple way 
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

with open(SOURCE_FILE_PATH, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",", quotechar="\"")
    i = 0
    for line in csvreader:
        if i > 0:
            clue = {}
            clue["title"] = line[0]
            clue["desc"] = line[1]
            clue["places"] = line[2].split(";")
            clue["count_places"] = line[3]
            clue["combos"] = []
            tab_clues.append(clue)
            print clue["title"]
            print "|".join(clue["places"])
        i = i+1
        
tab_combos = []
for clue_1 in tab_clues:
    for clue_2 in tab_clues:
        shared_places = intersection(clue_1["places"], clue_2["places"])
        clue_1["combos"].append({"title":clue_2["title"],"count_places":clue_2["count_places"],"shared_places":";".join(shared_places),"count_shared_places":len(shared_places)})
        
with open(TARGET_FILE_PATH, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(["Indice_1", "Nb_lieux", "Indice_2", "Nb_Lieux_2", "Lieux_communs", "Nb_lieux_communs"])
    for main_clue in tab_clues:
        for secondary_clue in main_clue["combos"]:
            if secondary_clue["title"] != main_clue["title"]:
                csvwriter.writerow([main_clue["title"], main_clue["count_places"], secondary_clue["title"], secondary_clue["count_places"], secondary_clue["shared_places"], secondary_clue["count_shared_places"]])
            else:
                csvwriter.writerow([main_clue["title"], main_clue["count_places"], "X", secondary_clue["count_places"], "X", secondary_clue["count_shared_places"]])

