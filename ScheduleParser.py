
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
s = """ Week 1
Rampage 10 @ Stars 21   
Rattlesnakes 20 @ Treasure 6   
Monarchs 27 @ Rancors 28   
Hammers 33 @ Borealis 3   
Virgins 10 @ Autobots 17   
Blizzard 9 @ Corsairs 6   
Heisenbergs 20 @ Storm 12   
Leviathan 17 @ Ukraine United 20   
Ravens 38 @ Muskies 9   
Quicksilver 22 @ Regulators 9   
Cut Throat’s 3 @ Mellotrons 38   
Bakers 21 @ Airborne 15   
Far East 27 @ Timbers 3   
Black Sharks 7 @ Fighting DeLucias 22   
Mallards 24 @ Chips 3   
Foghorn Leghorns 9 @ Fightin' Amish 50   
Week 2
Storm 3 @ Leviathan 29   
Cut Throat’s 6 @ Ukraine United 15   
Black Sharks 3 @ Foghorn Leghorns 40   
Mallards 21 @ Regulators 29   
Fightin' Amish 26 @ Muskies 6   
Blizzard 17 @ Treasure 29   
Ravens 21 @ Corsairs 10   
Stars 0 @ Rattlesnakes 39   
Borealis 17 @ Rancors 27   
Far East 9 @ Virgins 7   
Monarchs 17 @ Rampage 3   
Airborne 15 @ Autobots 12 (OT)   
Chips 27 @ Heisenbergs 20   
Timbers 24 @ Bakers 37   
Mellotrons 41 @ Fighting DeLucias 6   
Hammers 14 @ Quicksilver 10   
Week 3
Stars 26 @ Corsairs 3   
Fightin' Amish 17 @ Quicksilver 27   
Timbers 20 @ Far East 11   
Borealis 0 @ Airborne 23   
Rancors 6 @ Monarchs 55   
Hammers 59 @ Muskies 10   
Ravens 13 @ Blizzard 16 (OT)   
Black Sharks 26 @ Storm 12   
Foghorn Leghorns 43 @ Regulators 66   
Heisenbergs 12 @ Mallards 31   
Leviathan 14 @ Chips 22   
Autobots 13 @ Treasure 31   
Rampage 30 @ Virgins 10   
Rattlesnakes 27 @ Bakers 0   
Mellotrons 17 @ Ukraine United 3   
Fighting DeLucias 6 @ Cut Throat’s 31   
Week 4
Fightin' Amish 25 @ Corsairs 3   
Fighting DeLucias 37 @ Foghorn Leghorns 31   
Cut Throat’s 6 @ Regulators 48   
Blizzard 6 @ Storm 15   
Hammers 24 @ Stars 0   
Ukraine United 44 @ Muskies 28   
Mallards 10 @ Monarchs 36   
Treasure 22 @ Borealis 3   
Rattlesnakes 34 @ Virgins 0   
Quicksilver 47 @ Autobots 6   
Rancors 27 @ Ravens 0   
Timbers 10 @ Rampage 26   
Leviathan 0 @ Bakers 21   
Heisenbergs 9 @ Airborne 25   
Far East 13 @ Chips 32   
Mellotrons 48 @ Black Sharks 3   
Week 5
Corsairs 17 @ Black Sharks 13   
Rattlesnakes 33 @ Rampage 17   
Borealis 3 @ Blizzard 24   
Storm 3 @ Foghorn Leghorns 14   
Airborne 9 @ Mallards 30   
Leviathan 20 @ Treasure 16   
Autobots 3 @ Monarchs 52   
Virgins 13 @ Quicksilver 59   
Fightin' Amish 52 @ Fighting DeLucias 7   
Far East 10 @ Bakers 20   
Cut Throat’s 17 @ Chips 34   
Regulators 3 @ Hammers 29   
Stars 16 @ Ukraine United 27   
Muskies 12 @ Ravens 30   
Rancors 12 @ Heisenbergs 20   
Timbers 0 @ Mellotrons 35   
Week 6
Corsairs 3 @ Fightin' Amish 56   
Foghorn Leghorns 23 @ Cut Throat’s 6   
Regulators 62 @ Storm 30   
Hammers 31 @ Blizzard 0   
Muskies 10 @ Stars 37   
Mallards 40 @ Ukraine United 12   
Monarchs 34 @ Treasure 7   
Borealis 0 @ Rattlesnakes 41   
Autobots 10 @ Virgins 0   
Quicksilver 41 @ Ravens 10   
Rampage 24 @ Rancors 27   
Bakers 30 @ Timbers 16   
Leviathan 0 @ Airborne 13   
Heisenbergs 20 @ Far East 24   
Chips 30 @ Black Sharks 6   
Fighting DeLucias 0 @ Mellotrons 41   
Week 7
Ukraine United 20 @ Airborne 35   
Regulators 21 @ Heisenbergs 26   
Treasure 35 @ Timbers 3   
Rampage 34 @ Leviathan 16   
Bakers 23 @ Black Sharks 6   
Muskies 14 @ Cut Throat’s 20   
Corsairs 10 @ Hammers 29   
Autobots 7 @ Fightin' Amish 73   
Rancors 32 @ Blizzard 13   
Fighting DeLucias 32 @ Ravens 13   
Foghorn Leghorns 23 @ Storm 0   
Mellotrons 47 @ Quicksilver 17   
Virgins 0 @ Stars 18   
Rattlesnakes 9 @ Monarchs 18   
Far East 10 @ Mallards 29   
Chips 41 @ Borealis 7   
Week 8
Black Sharks 10 @ Timbers 20   
Storm 8 @ Ukraine United 29   
Fightin' Amish 17 @ Hammers 33   
Cut Throat’s 15 @ Bakers 31   
Virgins 14 @ Rancors 27   
Corsairs 21 @ Muskies 23   
Borealis 0 @ Treasure 35   
Rampage 7 @ Quicksilver 17   
Chips 24 @ Fighting DeLucias 11   
Ravens 0 @ Monarchs 32   
Rattlesnakes 52 @ Autobots 0   
Stars 16 @ Blizzard 14   
Mellotrons 26 @ Regulators 54   
Airborne 18 @ Far East 21   
Heisenbergs 44 @ Leviathan 16   
Foghorn Leghorns 7 @ Mallards 34   
Week 9
Rattlesnakes 41 @ Corsairs 0   
Rampage 41 @ Borealis 13   
Airborne 29 @ Foghorn Leghorns 7   
Leviathan 9 @ Mallards 28   
Treasure 6 @ Monarchs 22   
Fightin' Amish 56 @ Virgins 0   
Fighting DeLucias 16 @ Far East 12   
Bakers 13 @ Chips 33   
Heisenbergs 17 @ Timbers 14   
Storm 3 @ Mellotrons 59   
Black Sharks 3 @ Cut Throat’s 16   
Ukraine United 12 @ Regulators 27   
Muskies 3 @ Hammers 74   
Quicksilver 37 @ Stars 10   
Rancors 20 @ Autobots 6   
Blizzard 6 @ Ravens 20   
Week 10
Stars 12 @ Fightin' Amish 14   
Quicksilver 41 @ Corsairs 6   
Rancors 24 @ Borealis 6   
Monarchs 45 @ Muskies 3   
Hammers 32 @ Ravens 21   
Black Sharks 3 @ Blizzard 9   
Storm 9 @ Regulators 84   
Autobots 9 @ Chips 32   
Treasure 10 @ Rampage 16 (OT)   
Virgins 13 @ Rattlesnakes 52   
Mellotrons 38 @ Bakers 27   
Ukraine United 25 @ Fighting DeLucias 13   
Timbers 6 @ Cut Throat’s 23   
Mallards 36 @ Airborne 10   
Far East 16 @ Leviathan 13   
Heisenbergs 9 @ Foghorn Leghorns 6   
Week 11
Autobots 12 @ Corsairs 13   
Quicksilver 16 @ Rattlesnakes 36   
Cut Throat’s 8 @ Fighting DeLucias 20   
Foghorn Leghorns 28 @ Mellotrons 37   
Airborne 27 @ Leviathan 20   
Muskies 12 @ Rancors 24   
Stars 17 @ Ravens 13   
Treasure 6 @ Hammers 36   
Monarchs 31 @ Borealis 2   
Virgins 3 @ Rampage 17   
Blizzard 3 @ Fightin' Amish 26   
Bakers 27 @ Far East 19   
Mallards 23 @ Heisenbergs 14   
Ukraine United 12 @ Storm 24   
Regulators 44 @ Black Sharks 6   
Chips 14 @ Timbers 3   
Week 12
Ukraine United 6 @ Foghorn Leghorns 24   
Chips 16 @ Far East 26   
Mellotrons 40 @ Cut Throat’s 7   
Fighting DeLucias 15 @ Black Sharks 3   
Storm 10 @ Corsairs 13   
Rampage 22 @ Autobots 7   
Stars 10 @ Quicksilver 34   
Blizzard 16 @ Muskies 3   
Treasure 14 @ Virgins 3   
Timbers 3 @ Mallards 25   
Regulators 34 @ Airborne 31 (OT)   
Leviathan 10 @ Heisenbergs 13 (OT)   
Rattlesnakes 26 @ Fightin' Amish 21   
Borealis 2 @ Ravens 20   
Monarchs 21 @ Hammers 17   
Bakers 3 @ Rancors 27   
Week 13
Rancors 9 @ Treasure 31   
Bakers 32 @ Heisenbergs 6   
Far East 3 @ Mellotrons 38   
Chips 11 @ Airborne 24   
Fightin' Amish 20 @ Stars 9   
Rampage 5 @ Rattlesnakes 33   
Borealis 8 @ Autobots 7   
Muskies 6 @ Quicksilver 58   
Corsairs 12 @ Virgins 6   
Blizzard 0 @ Monarchs 38   
Ravens 3 @ Hammers 39   
Fighting DeLucias 21 @ Timbers 15 (OT)   
Cut Throat’s 19 @ Black Sharks 3   
Regulators 46 @ Ukraine United 6   
Foghorn Leghorns 33 @ Leviathan 14   
Storm 9 @ Mallards 30   
Week 14
Timbers 3 @ Chips 30   
Rancors 20 @ Rattlesnakes 34   
Autobots 13 @ Rampage 28   
Monarchs 22 @ Far East 3   
Quicksilver 27 @ Fightin' Amish 41   
Corsairs 10 @ Stars 17   
Hammers 8 @ Mellotrons 13   
Muskies 9 @ Blizzard 34   
Bakers 10 @ Fighting DeLucias 17   
Virgins 0 @ Borealis 6   
Airborne 7 @ Heisenbergs 16   
Ravens 12 @ Treasure 24   
Ukraine United 24 @ Black Sharks 0   
Regulators 62 @ Foghorn Leghorns 16   
Mallards 31 @ Leviathan 17   
Storm 3 @ Cut Throat’s 30   
Week 15
Foghorn Leghorns 26 @ Ukraine United 21   
Far East 16 @ Cut Throat’s 10   
Black Sharks 0 @ Mellotrons 51   
Fighting DeLucias 9 @ Storm 7   
Corsairs 10 @ Rampage 13 (OT)   
Stars 16 @ Autobots 9   
Quicksilver 55 @ Blizzard 3   
Treasure 45 @ Muskies 13   
Virgins 0 @ Mallards 31   
Airborne 16 @ Timbers 19 (OT)   
Leviathan 13 @ Regulators 55   
Heisenbergs 26 @ Rattlesnakes 45   
Ravens 10 @ Fightin' Amish 39   
Borealis 0 @ Monarchs 61   
Hammers 6 @ Rancors 24   
Chips 24 @ Bakers 6   
Week 16
Cut Throat’s 5 @ Stars 19   
Corsairs 7 @ Quicksilver 38   
Fightin' Amish 36 @ Rampage 17   
Treasure 17 @ Rancors 21   
Muskies 6 @ Borealis 24   
Monarchs 23 @ Virgins 9   
Autobots 0 @ Rattlesnakes 58   
Mellotrons 34 @ Chips 3   
Mallards 48 @ Bakers 13   
Ravens 0 @ Foghorn Leghorns 25   
Blizzard 3 @ Hammers 30   
Black Sharks 0 @ Far East 22   
Airborne 17 @ Storm 3   
Regulators 44 @ Fighting DeLucias 17   
Ukraine United 20 @ Heisenbergs 23   
Timbers 3 @ Leviathan 25     
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
