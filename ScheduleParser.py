
def parse_scores(schedule):
    new_schedule = ''
    for line in schedule.splitlines():
        if 'Week' in line:
            continue
        away, home = line.replace('(OT)', '').split('@')
        away, home = away.strip().rsplit(' ', 1), home.strip().rsplit(' ', 1)
        new_schedule += f'{away[0].replace(" ", "")}\t{away[1]}\t{home[0].replace(" ", "")}\t{home[1]}\n'
    return new_schedule.strip()


def parse_schedule(schedule):
    new_schedule = ''
    for line in schedule.splitlines():
        if 'Week' in line and 'Game' not in line:
            continue
        away, home = line.replace('Game of the Week', '').replace('(OT)', '').split('@')
        away, home = away.strip().rsplit('(', 1), home.strip().rsplit('(', 1)
        new_schedule += f'{away[0].strip().replace(" ", "")}\t\t{home[0].strip().replace(" ", "")}\n'
    return new_schedule.strip()


def retro_schedule(schedule, tabs=2):
    new_schedule = ''
    for line in schedule.splitlines():
        if 'Week' in line and 'Game' not in line:
            continue
        away, home = line.replace('Game of the Week', '').replace('(OT)', '').split('@')
        away, home = away.strip().rsplit('(', 1), home.strip().rsplit('(', 1)
        new_schedule += f'{away[0].strip().replace(" ", "")}\t{home[0].strip().replace(" ", "")}\n'
    return new_schedule.strip()

# Copy schedules from the league schedule page. Paste them below and run the parse_scores.
s = """Week 1
Stallions 14 @ Sabretooths 29   
Blarney Stones 19 @ Bulls 6   
Crocodiles 7 @ Diamonds 31   
Assassins 10 @ Red Dragons 10 (OT)   
Hex 9 @ Sphinx 23   
Rhino 6 @ Hawkeyes 23   
Barbarians 3 @ Jumbos 10   
Ice 13 @ Eskimos 26   
Daggers 10 @ Lightning 24   
Blue 10 @ Labradors 24   
Smoke 10 @ Riot 6   
Chilli Peppers 13 @ Flying Serpents 24   
Poison Dart Frogs 13 @ Zweig 28   
Bite 24 @ Settlers 3   
Gold Nuggets 7 @ Royals 38   
Conjurors 6 @ Admirals 25   
Week 2
Zweig 14 @ Smoke 19   
Red Dragons 0 @ Diamonds 38   
Hex 7 @ Chilli Peppers 26   
Jumbos 8 @ Sphinx 13   
Bite 3 @ Flying Serpents 20   
Conjurors 11 @ Daggers 7   
Barbarians 3 @ Blarney Stones 13   
Hawkeyes 9 @ Blue 25   
Riot 26 @ Gold Nuggets 21   
Eskimos 0 @ Labradors 16   
Royals 29 @ Admirals 7   
Crocodiles 10 @ Rhino 25   
Poison Dart Frogs 17 @ Assassins 21   
Settlers 0 @ Stallions 19   
Sabretooths 6 @ Bulls 12 (OT)   
Ice 14 @ Lightning 42   
Week 3
Smoke 13 @ Poison Dart Frogs 3   
Bite 0 @ Chilli Peppers 20   
Hex 0 @ Zweig 34   
Diamonds 31 @ Rhino 9   
Red Dragons 3 @ Assassins 6   
Riot 10 @ Sphinx 31   
Labradors 10 @ Lightning 20   
Eskimos 43 @ Conjurors 17   
Gold Nuggets 3 @ Stallions 19   
Royals 19 @ Blarney Stones 16 (OT)   
Settlers 17 @ Sabretooths 16   
Admirals 19 @ Barbarians 22   
Ice 13 @ Blue 24   
Bulls 16 @ Daggers 3   
Hawkeyes 22 @ Crocodiles 16   
Flying Serpents 17 @ Jumbos 20   
Week 4
Blarney Stones 10 @ Admirals 3   
Sabretooths 23 @ Red Dragons 9   
Crocodiles 3 @ Jumbos 8   
Assassins 6 @ Royals 13   
Blue 24 @ Bulls 12   
Barbarians 7 @ Lightning 20   
Conjurors 6 @ Labradors 30   
Daggers 14 @ Ice 6   
Settlers 29 @ Smoke 10   
Chilli Peppers 26 @ Riot 17   
Flying Serpents 25 @ Bite 10   
Diamonds 66 @ Hex 6   
Rhino 28 @ Sphinx 10   
Hawkeyes 10 @ Poison Dart Frogs 16   
Zweig 26 @ Stallions 10   
Eskimos 35 @ Gold Nuggets 7   
Week 5
Stallions 19 @ Conjurors 3   
Crocodiles 17 @ Riot 5   
Labradors 13 @ Settlers 0   
Gold Nuggets 13 @ Flying Serpents 31   
Hex 0 @ Smoke 14   
Rhino 37 @ Chilli Peppers 27   
Poison Dart Frogs 6 @ Bite 27   
Assassins 0 @ Zweig 29   
Sphinx 10 @ Diamonds 39   
Hawkeyes 20 @ Red Dragons 10   
Jumbos 13 @ Admirals 0   
Blarney Stones 3 @ Blue 12   
Daggers 3 @ Eskimos 26   
Royals 21 @ Barbarians 3   
Ice 20 @ Sabretooths 16   
Lightning 19 @ Bulls 17   
Week 6
Daggers 0 @ Settlers 18   
Hex 0 @ Bite 31   
Flying Serpents 24 @ Riot 16   
Sphinx 3 @ Hawkeyes 26   
Stallions 6 @ Eskimos 40   
Crocodiles 13 @ Assassins 18   
Red Dragons 3 @ Jumbos 17   
Rhino 15 @ Diamonds 31   
Chilli Peppers 24 @ Smoke 12   
Zweig 35 @ Poison Dart Frogs 3   
Bulls 3 @ Royals 26   
Admirals 19 @ Ice 7   
Labradors 3 @ Barbarians 26   
Sabretooths 3 @ Blue 32   
Blarney Stones 33 @ Conjurors 0   
Lightning 20 @ Gold Nuggets 7   
Week 7
Conjurors 0 @ Stallions 51   
Royals 16 @ Sabretooths 13   
Bulls 13 @ Crocodiles 17   
Labradors 16 @ Riot 6   
Gold Nuggets 3 @ Settlers 26   
Smoke 3 @ Flying Serpents 24   
Hex 0 @ Rhino 12   
Chilli Peppers 20 @ Poison Dart Frogs 3   
Zweig 13 @ Bite 3   
Diamonds 20 @ Assassins 13   
Sphinx 13 @ Red Dragons 10 (OT)   
Jumbos 0 @ Hawkeyes 21   
Admirals 3 @ Blarney Stones 21   
Blue 17 @ Daggers 10   
Eskimos 24 @ Lightning 13   
Barbarians 21 @ Ice 23   
Week 8
Smoke 10 @ Crocodiles 10 (OT)   
Zweig 34 @ Flying Serpents 13   
Ice 3 @ Assassins 20   
Bite 23 @ Poison Dart Frogs 13   
Lightning 16 @ Daggers 6   
Diamonds 51 @ Sphinx 3   
Bulls 3 @ Labradors 17   
Riot 9 @ Hex 13   
Blue 20 @ Barbarians 3   
Chilli Peppers 10 @ Eskimos 21   
Red Dragons 6 @ Hawkeyes 30   
Jumbos 0 @ Rhino 35   
Gold Nuggets 39 @ Conjurors 20   
Royals 27 @ Settlers 2   
Admirals 13 @ Sabretooths 41   
Stallions 3 @ Blarney Stones 9   
Week 9
Sphinx 7 @ Smoke 12   
Rhino 31 @ Crocodiles 22   
Jumbos 13 @ Red Dragons 6   
Bite 16 @ Hawkeyes 14   
Flying Serpents 24 @ Assassins 14   
Gold Nuggets 3 @ Labradors 24   
Stallions 3 @ Chilli Peppers 16   
Blue 20 @ Diamonds 25   
Admirals 9 @ Royals 29   
Sabretooths 35 @ Conjurors 19   
Settlers 0 @ Blarney Stones 44   
Bulls 48 @ Ice 17   
Daggers 11 @ Barbarians 6   
Poison Dart Frogs 24 @ Hex 3   
Riot 7 @ Zweig 41   
Lightning 7 @ Eskimos 18   
Week 10
Gold Nuggets 17 @ Daggers 14   
Smoke 17 @ Lightning 3   
Red Dragons 19 @ Poison Dart Frogs 13   
Assassins 3 @ Rhino 31   
Crocodiles 6 @ Sphinx 16   
Jumbos 0 @ Bite 3   
Settlers 19 @ Conjurors 14   
Hex 6 @ Riot 30   
Chilli Peppers 24 @ Diamonds 31   
Ice 7 @ Blarney Stones 36   
Barbarians 9 @ Bulls 13   
Sabretooths 21 @ Admirals 18   
Blue 14 @ Royals 11   
Eskimos 13 @ Zweig 12   
Hawkeyes 7 @ Flying Serpents 9   
Labradors 19 @ Stallions 17   
Week 11
Chilli Peppers 23 @ Crocodiles 0   
Smoke 3 @ Diamonds 47   
Blarney Stones 23 @ Hawkeyes 3   
Assassins 9 @ Jumbos 15   
Zweig 27 @ Red Dragons 13   
Riot 16 @ Bite 3   
Flying Serpents 29 @ Poison Dart Frogs 3   
Daggers 11 @ Hex 6   
Labradors 17 @ Eskimos 20   
Barbarians 7 @ Sabretooths 27   
Stallions 19 @ Gold Nuggets 7   
Admirals 22 @ Rhino 10   
Sphinx 20 @ Ice 0   
Bulls 6 @ Blue 24   
Settlers 12 @ Lightning 13   
Conjurors 3 @ Royals 33   
Week 12
Diamonds 17 @ Crocodiles 12   
Smoke 6 @ Chilli Peppers 13   
Assassins 0 @ Hawkeyes 32   
Jumbos 0 @ Zweig 30   
Bite 13 @ Red Dragons 19   
Poison Dart Frogs 3 @ Riot 6   
Flying Serpents 21 @ Hex 3   
Daggers 9 @ Labradors 16   
Barbarians 14 @ Eskimos 35   
Sabretooths 14 @ Gold Nuggets 19   
Admirals 16 @ Stallions 9   
Sphinx 0 @ Rhino 34   
Ice 20 @ Bulls 26   
Lightning 10 @ Blue 20   
Conjurors 28 @ Settlers 32   
Blarney Stones 20 @ Royals 19   
Week 13
Crocodiles 2 @ Hex 0   
Zweig 23 @ Chilli Peppers 6   
Assassins 0 @ Bite 33   
Poison Dart Frogs 9 @ Flying Serpents 23   
Diamonds 17 @ Riot 0   
Hawkeyes 9 @ Jumbos 3   
Eskimos 24 @ Daggers 0   
Rhino 30 @ Smoke 5   
Red Dragons 3 @ Bulls 28   
Royals 29 @ Sphinx 7   
Stallions 23 @ Settlers 10   
Gold Nuggets 0 @ Admirals 16   
Labradors 16 @ Ice 10 (OT)   
Barbarians 6 @ Blue 27   
Sabretooths 9 @ Blarney Stones 58   
Lightning 78 @ Conjurors 6   
Week 14
Lightning 26 @ Labradors 6   
Settlers 0 @ Eskimos 30   
Conjurors 6 @ Poison Dart Frogs 41   
Royals 27 @ Ice 7   
Sphinx 14 @ Chilli Peppers 36   
Smoke 27 @ Hex 3   
Daggers 10 @ Stallions 13   
Blarney Stones 18 @ Gold Nuggets 16   
Hawkeyes 14 @ Assassins 6   
Diamonds 17 @ Jumbos 0   
Crocodiles 3 @ Sabretooths 24   
Bulls 16 @ Barbarians 6   
Blue 45 @ Admirals 3   
Riot 15 @ Rhino 20   
Bite 7 @ Zweig 12   
Red Dragons 3 @ Flying Serpents 23   
Week 15
Zweig 13 @ Hawkeyes 37   
Diamonds 7 @ Blarney Stones 24   
Sabretooths 20 @ Royals 18   
Stallions 10 @ Lightning 20   
Bite 14 @ Smoke 6   
Riot 6 @ Chilli Peppers 32   
Hex 26 @ Conjurors 9   
Settlers 12 @ Gold Nuggets 3   
Bulls 21 @ Admirals 27   
Eskimos 20 @ Blue 17   
Ice 13 @ Barbarians 6   
Rhino 10 @ Red Dragons 7   
Sphinx 12 @ Crocodiles 13   
Jumbos 29 @ Assassins 9   
Poison Dart Frogs 10 @ Daggers 23   
Flying Serpents 20 @ Labradors 6   
Week 16
Flying Serpents 22 @ Zweig 19 (OT)   
Hawkeyes 24 @ Diamonds 17   
Blarney Stones 9 @ Sabretooths 13   
Royals 24 @ Stallions 9   
Lightning 13 @ Bite 17   
Riot 10 @ Smoke 15   
Chilli Peppers 9 @ Hex 3   
Conjurors 6 @ Gold Nuggets 17   
Admirals 9 @ Settlers 13   
Eskimos 27 @ Bulls 26   
Blue 16 @ Ice 3   
Rhino 18 @ Barbarians 9   
Red Dragons 23 @ Crocodiles 6   
Assassins 10 @ Sphinx 23   
Poison Dart Frogs 23 @ Jumbos 6   
Labradors 27 @ Daggers 23   
"""

print(parse_scores(s))

print(parse_schedule(s))

s = """Preseason Week 1
Cheesesteaks 13 @ Titans 3   
Eggball Team 26 @ Texans 18   
49ers 13 @ Chargers 6   
Lions 19 @ Jaguars 3   
Aliens 17 @ Broncos 7   
Lillys 6 @ Dinos 0   
Panthers 27 @ Chiefs 23   
Nonsayins 6 @ Stillers 28   
Bears 0 @ Jets 17   
Buccaneers 13 @ Ravens 10 (OT)   
Giants 3 @ Buffalo 19   
Superhawks 30 @ Browns 12   
Dryer Vlads 24 @ Raiders 9   
Packers 12 @ Colts 14   
Vikings 7 @ Patriots 15   
Saints 0 @ Dolphins 27   
Preseason Week 2
Texans 6 @ Cheesesteaks 10   
Chargers 25 @ Eggball Team 13   
Jaguars 6 @ 49ers 3 (OT)   
Broncos 3 @ Lions 30   
Dinos 9 @ Aliens 6   
Chiefs 13 @ Lillys 16   
Stillers 19 @ Panthers 24   
Jets 20 @ Nonsayins 15   
Ravens 12 @ Bears 9   
Buffalo 9 @ Buccaneers 14   
Browns 30 @ Giants 13   
Raiders 15 @ Superhawks 12   
Colts 22 @ Dryer Vlads 37   
Patriots 6 @ Packers 3   
Dolphins 16 @ Vikings 3   
Titans 23 @ Saints 7   
Preseason Week 3
Cheesesteaks 17 @ Chargers 27   
Eggball Team 3 @ Jaguars 27   
49ers 16 @ Broncos 9   
Lions 31 @ Dinos 0   
Aliens 29 @ Chiefs 12   
Lillys 23 @ Stillers 16   
Panthers 3 @ Jets 37   
Nonsayins 6 @ Ravens 17   
Bears 13 @ Buffalo 20   
Buccaneers 24 @ Browns 19   
Giants 42 @ Raiders 26   
Superhawks 45 @ Colts 13   
Dryer Vlads 49 @ Patriots 25   
Packers 3 @ Dolphins 25   
Vikings 0 @ Titans 29   
Saints 6 @ Texans 5   """

print(retro_schedule(s))
