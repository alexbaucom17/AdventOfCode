import operator

def load_data(filename):
    with open(filename) as f:
        data = []
        for line in f:
            line = line.strip()
            line = line.replace('(', '')
            line = line.replace(')','')
            ingredients_str, allergens_str = line.split("contains")
            ingredients = [i.strip() for i in ingredients_str.split()]
            allergens = [a.strip() for a in allergens_str.replace(",",'').split()]
            data.append((ingredients, allergens))
        return data

INGREDIENT_ID = 0
ALLERGEN_ID = 1

def count_all_items(data, id):
    counts = {}
    ingredient_counts = {}
    for line in data:
        item = line[id]
        for i in item:
            if i in counts.keys():
                counts[i] += 1
            else:
                counts[i] = 1
    return counts

def preprocess_counts(data):
    ingredient_counts = count_all_items(data, INGREDIENT_ID)
    allergen_counts = count_all_items(data, ALLERGEN_ID)
    return (ingredient_counts, allergen_counts)

def try_identify_allergen_blind(allergen, data):
    
    # Find all rows with the specific allergen
    rows_with_allergen = []
    for row in data:
        if allergen in row[ALLERGEN_ID]:
            rows_with_allergen.append(row)

    # Get counts of ingredients with that allergen
    ingredient_counts = count_all_items(rows_with_allergen, INGREDIENT_ID)

    # If any ingredients appear in every allergen row, then there is a match
    n_allergens = len(rows_with_allergen)
    matching_ingredients = []
    for key,num in ingredient_counts.items():
        if n_allergens == num:
            matching_ingredients.append(key)

    # Return info about matches
    found_match = False
    if len(matching_ingredients) > 0:
        found_match = True

    return (found_match, matching_ingredients)

# Simple first pass to match allergens
def match_allergens_blind(data):
    
    # Get allergens and sort by most occurences
    allergen_counts = count_all_items(data, ALLERGEN_ID)
    sorted_counts = sorted(allergen_counts.items(), key=operator.itemgetter(1))

    matches = {}
    for allergen,_ in sorted_counts:
        match, matching_ingredients = try_identify_allergen_blind(allergen, data)
        if match:
            matches[allergen] = matching_ingredients

    # If these lengths match, it means that we have found at least one match for each allergen
    all_allergens_matched = False
    if len(matches) == len(allergen_counts):
        all_allergens_matched = True

    return (all_allergens_matched, matches)

def match_allergens(data):

    # Do initial matches blindly
    all_allergens_matched, initial_matches = match_allergens_blind(data)
    if not all_allergens_matched:
        print("ERROR: Did not match all allergens in blind search")
        return

    # Now sort out which matches are unabiguous
    matches = {}
    count = 0
    max_count = 50
    while count < max_count:

        count += 1

        # Figure out which ones are unabiguous
        for allergen, ingredient_matches in initial_matches.items():
            if len(ingredient_matches) == 1:
                matches[allergen] = ingredient_matches[0]
                
        # Clear out unabiguous matches from initial_matches
        for k in matches.keys():
            try:
                del initial_matches[k]
            except KeyError:
                pass

        # Now that unabiguous ones are picked out, remove those ingredients from other match lists
        for allergen, ingredient_matches in initial_matches.items():
            for ingredient in matches.values():
                if ingredient in ingredient_matches:
                    ingredient_matches.remove(ingredient)

            if len(ingredient_matches) == 0:
                raise ValueError("Removed all potential matches from initial matches for {}".format(allergen))

        if len(initial_matches) == 0:
            break

    if count == max_count:
        print("Didn't finish loop")

    return matches


def count_non_allergen_ingredients(data):

    allergens = match_allergens(data)
    print(allergens)

    ingredient_counts = count_all_items(data, INGREDIENT_ID)
    print(ingredient_counts)

    ingredients_with_allergens = [a for a in allergens.values()]
    print(ingredients_with_allergens)

    total = 0
    for i,n in ingredient_counts.items():
        if i not in ingredients_with_allergens:
            total += n

    return total


def get_dangerous_list(data):
    allergens = match_allergens(data)
    sorted_allergens = sorted(allergens.items(), key=operator.itemgetter(0))

    dangerous_list = ','.join([i for a,i in sorted_allergens])
    return dangerous_list


if __name__ == '__main__':

    sample_data = load_data("day21/sample_input.txt")
    data = load_data("day21/input.txt") 

    print(count_non_allergen_ingredients(data))
    print(get_dangerous_list(data))