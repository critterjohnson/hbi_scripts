import json
import hackbi_eventbrite as he

with open("secret.json", "r") as file:
    secrets = json.load(file)
event_id = secrets["event_id"]
token = secrets["token"]

hs = ["Freshman / 9th grade", 
      "Sophomore / 10th grade", 
      "Junior / 11th grade", 
      "Senior / 12th grade"]

attendees = he.get_attendee_list(event_id, token)
hs_atts = []
for grade in hs:
    hs_atts.extend(he.get_people_answered(attendees, grade, "26350001"))
ms_atts = [attendee for attendee in attendees if attendee not in hs_atts]

def count_names(atts):
    alph = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    dist = {}
    for letter in alph:
        dist[letter] = 0
    for att in atts:
        last = att["profile"]["last_name"].lower()
        dist[last[0]] += 1
    return dist

def split(dist, total, splits):
    per = total // splits
    split_dist = []
    cur = 0
    items = tuple(dist.items())
    for i in range(splits):
        split = []
        cur_total = 0
        while cur_total < per:
            try:
                cur_total += items[cur][1]
            except IndexError:
                break
            split.append(items[cur][0])
            cur += 1
        split_dist.append(split)
    dist_totals = {}
    for split in split_dist:
        key = f"{split[0]}-{split[-1]}"
        dist_totals[key] = 0
        for letter in split:
            dist_totals[key] += dist[letter]
    return dist_totals
        

print(split(count_names(hs_atts), len(hs_atts), 5))
print(split(count_names(ms_atts), len(ms_atts), 2))
