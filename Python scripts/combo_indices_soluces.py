import csv

SOURCE_FILE_PATH = "indices.csv"
TARGET_FILE_PATH = "indices_combo_soluces.csv"
tab_clues = []
tab_soluces = []

# Python program to illustrate the intersection 
# of two lists in most simple way 
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3
    
def diff(lst1, lst2):
        lst1 = set([value["title"] for value in lst1])
        lst2 = set([value["title"] for value in lst2])
        return lst2 - lst1
    
def log(log_string, level):
    if level >= 2:
        print log_string

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
        i = i+1
        
def dig_solution(selected_clues, remaining_clues):
    log("\ndig_solution", 1)
    log("\tselected_clues : " + get_clues_string_list(selected_clues), 1)
    log("\tremaining_clues : " + get_clues_string_list(remaining_clues), 1)
    current_places_selected = get_selected_places(selected_clues)
    nb_selected_places = 0 if current_places_selected is None else len(current_places_selected)
    log("\tnb_selected_places = " + str(nb_selected_places), 1)
    if len(selected_clues) > 0 and nb_selected_places == 0:
        return
    elif nb_selected_places == 1:
        log("nb_selected_places==1", 1)
        log("\tselected_clues : " + get_clues_string_list(selected_clues), 1)
        if not is_clues_path_existing(selected_clues):
            tab_soluces.append({"place":current_places_selected[0],"clues":selected_clues})
            log("tab_soluces append ; length = " + str(len(tab_soluces)), 1)
        else:
            return
    else:
        for new_clue in remaining_clues:
            new_remaining_clues = list(remaining_clues)
            new_remaining_clues.remove(new_clue)
            new_selected_clues = list(selected_clues)
            new_selected_clues.append(new_clue)
            dig_solution(new_selected_clues, new_remaining_clues)
        return

def get_selected_places(selected_clues):
    log("\nget_selected_places", 1)
    log("\tselected_clues : " + get_clues_string_list(selected_clues), 0)
    selected_places = None
    for clue in selected_clues:
        log("\t\tclue : " + "|".join(clue["places"]), 0)
        if selected_places is None:
            log("\t\tselected_places : None", 0)
        else:
            log("\t\tselected_places : " + "|".join(selected_places), 0)
        if selected_places is None:
            selected_places = clue["places"]
        else:
            selected_places = intersection(selected_places, clue["places"])
    if selected_places is None:
        log("\tselected_places : None", 1)
    else:
        log("\tselected_places : " + "|".join(selected_places), 1)
    return selected_places

def is_clues_path_existing(clues_list):
    res = False
    for soluce in tab_soluces:
        soluce_clues = soluce["clues"]
        if len(diff(clues_list, soluce_clues)) == 0 or len(diff(soluce_clues, clues_list)) == 0:
            if len(soluce_clues) >= len(clues_list):
                tab_soluces.remove(soluce)
                return False
            else:
                return True
    return res
        
def get_clues_string_list(clues):
    list_clues_title = []
    for clue in clues:
        list_clues_title.append(clue["title"])
    return "|".join(list_clues_title)
        
#for clue_1 in tab_clues:
#    for clue_2 in tab_clues:
#        shared_places = intersection(clue_1["places"], clue_2["places"])
#        clue_1["combos"].append({"title":clue_2["title"],"count_places":clue_2["count_places"],"shared_places":";".join(shared_places),"count_shared_places":len(shared_places)})

dig_solution([], tab_clues)

log("tab_soluces length = " + str(len(tab_soluces)), 2)
        
with open(TARGET_FILE_PATH, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(["Lieu", "Indice_1", "Indice_2", "Indice_3", "Indice_4", "Indice_5", "Indice_6", "Indice_7", "Indice_8", "Indice_9", "Indice_10"])
    for soluce in tab_soluces:
        row = [soluce["place"]]
        for clue in soluce["clues"]:
            row.append(clue["title"])
        csvwriter.writerow(row)

