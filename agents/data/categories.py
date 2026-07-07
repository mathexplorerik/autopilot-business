ANIMAL_NICHES = {
    "jungle animals",
    "farm animals",
    "ocean animals",
    "dinosaurs",
    "dogs",
    "cats",
    "birds",
    "insects",
    "wild animals",
    "zoo animals",
    "pets",
    "forest animals"
}

FESTIVAL_NICHES = {
    "diwali",
    "holi",
    "eid",
    "christmas",
    "navratri",
    "dussehra",
    "onam",
    "halloween",
    "easter"
}

FANTASY_NICHES = {
    "unicorn",
    "princess",
    "mermaid",
    "dragon",
    "fairy"
}

VEHICLE_NICHES = {
    "cars",
    "trucks",
    "construction vehicles",
    "airplanes",
    "boats",
    "trains"
}

EDUCATION_NICHES = {
    "alphabet",
    "numbers",
    "shapes",
    "fruits",
    "vegetables"
}

OCCUPATION_NICHES = {
    "doctor",
    "firefighter",
    "chef",
    "police",
    "teacher"
}
def get_engine(niche: str):
    niche = niche.lower().strip()

    if niche in ANIMAL_NICHES:
        return "animal"

    if niche in FESTIVAL_NICHES:
        return "festival"

    if niche in FANTASY_NICHES:
        return "fantasy"

    if niche in VEHICLE_NICHES:
        return "vehicle"

    if niche in EDUCATION_NICHES:
        return "education"

    if niche in OCCUPATION_NICHES:
        return "occupation"

    return "default"