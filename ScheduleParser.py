
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
Borealis 0 @ Quicksilver 28   
Stars 19 @ Cut Throat’s 13   
Fightin' Amish 34 @ Corsairs 0   
Ukraine United 19 @ Storm 14   
Ravens 31 @ Muskies 17   
Treasure 16 @ Timbers 14   
Chips 3 @ Hammers 43   
Airborne 14 @ Virgins 0   
Bakers 10 @ Rancors 31   
Rampage 33 @ Heisenbergs 20   
Foghorn Leghorns 24 @ Regulators 31   
Rattlesnakes 63 @ Autobots 0   
Fighting DeLucias 0 @ Mellotrons 18   
Black Sharks 13 @ Blizzard 27   
Far East 3 @ Monarchs 64   
Leviathan 3 @ Mallards 38   
Week 2
Leviathan 6 @ Heisenbergs 10   
Timbers 16 @ Virgins 13   
Bakers 10 @ Far East 13   
Fighting DeLucias 23 @ Muskies 19   
Blizzard 12 @ Hammers 31   
Ukraine United 7 @ Rampage 41   
Rattlesnakes 34 @ Regulators 23   
Foghorn Leghorns 31 @ Autobots 14   
Airborne 13 @ Mallards 37   
Mellotrons 17 @ Ravens 6   
Chips 27 @ Treasure 13   
Stars 3 @ Fightin' Amish 13   
Quicksilver 0 @ Monarchs 40   
Corsairs 15 @ Storm 27   
Cut Throat’s 18 @ Black Sharks 12   
Rancors 26 @ Borealis 9   
Week 3
Mellotrons 48 @ Heisenbergs 5   
Storm 29 @ Regulators 48   
Ravens 27 @ Black Sharks 9   
Leviathan 6 @ Rattlesnakes 21   
Far East 12 @ Airborne 10   
Quicksilver 20 @ Blizzard 14   
Timbers 20 @ Muskies 7   
Rancors 13 @ Chips 6   
Rampage 10 @ Foghorn Leghorns 37   
Virgins 9 @ Autobots 13   
Fighting DeLucias 14 @ Mallards 32   
Cut Throat’s 9 @ Hammers 27   
Monarchs 48 @ Bakers 13   
Stars 19 @ Borealis 13   
Corsairs 6 @ Treasure 16   
Fightin' Amish 24 @ Ukraine United 10   
Week 4
Storm 14 @ Foghorn Leghorns 27   
Fightin' Amish 16 @ Quicksilver 13   
Regulators 52 @ Corsairs 14   
Hammers 55 @ Black Sharks 10   
Monarchs 38 @ Timbers 3   
Borealis 3 @ Treasure 20   
Muskies 12 @ Far East 37   
Mallards 3 @ Mellotrons 31   
Heisenbergs 24 @ Bakers 20   
Rampage 25 @ Rattlesnakes 27   
Virgins 6 @ Leviathan 39   
Autobots 9 @ Airborne 16   
Cut Throat’s 13 @ Ukraine United 30   
Fighting DeLucias 17 @ Blizzard 10   
Chips 27 @ Ravens 3   
Stars 6 @ Rancors 33   
Week 5
Borealis 3 @ Leviathan 13   
Timbers 13 @ Bakers 13 (OT)   
Chips 7 @ Far East 13   
Monarchs 56 @ Rancors 13   
Treasure 3 @ Stars 23   
Regulators 17 @ Quicksilver 48   
Corsairs 0 @ Fightin' Amish 29   
Rattlesnakes 27 @ Ukraine United 6   
Muskies 9 @ Storm 40   
Ravens 0 @ Hammers 54   
Blizzard 20 @ Mellotrons 49   
Airborne 19 @ Cut Throat’s 6   
Heisenbergs 9 @ Black Sharks 27   
Foghorn Leghorns 39 @ Fighting DeLucias 16   
Autobots 0 @ Virgins 10   
Mallards 45 @ Rampage 24   
Week 6
Timbers 17 @ Chips 19   
Treasure 14 @ Monarchs 26   
Bakers 10 @ Borealis 13   
Rancors 28 @ Far East 6   
Muskies 7 @ Hammers 73   
Ravens 21 @ Blizzard 31   
Ukraine United 9 @ Corsairs 15 (OT)   
Stars 25 @ Regulators 31   
Storm 0 @ Fightin' Amish 47   
Rattlesnakes 16 @ Mallards 15   
Cut Throat’s 14 @ Leviathan 13   
Black Sharks 7 @ Airborne 9   
Heisenbergs 20 @ Autobots 15   
Rampage 27 @ Virgins 3   
Quicksilver 19 @ Foghorn Leghorns 37   
Mellotrons 45 @ Fighting DeLucias 24   
Week 7
Far East 17 @ Ravens 20   
Timbers 33 @ Blizzard 45   
Rancors 20 @ Quicksilver 21   
Regulators 63 @ Storm 58   
Rattlesnakes 28 @ Chips 6   
Airborne 7 @ Mellotrons 38   
Black Sharks 13 @ Muskies 19   
Heisenbergs 19 @ Leviathan 26   
Ukraine United 7 @ Foghorn Leghorns 44   
Rampage 17 @ Autobots 0   
Mallards 47 @ Virgins 10   
Fighting DeLucias 21 @ Cut Throat’s 27   
Hammers 33 @ Bakers 3   
Borealis 7 @ Monarchs 46   
Stars 13 @ Corsairs 16   
Treasure 10 @ Fightin' Amish 19   
Week 8
Far East 28 @ Bakers 20   
Chips 0 @ Mallards 44   
Autobots 0 @ Rattlesnakes 34   
Airborne 16 @ Heisenbergs 17   
Leviathan 10 @ Black Sharks 12   
Muskies 23 @ Cut Throat’s 20   
Hammers 68 @ Fighting DeLucias 0   
Fightin' Amish 3 @ Mellotrons 19   
Storm 13 @ Ukraine United 17   
Corsairs 0 @ Foghorn Leghorns 26   
Quicksilver 20 @ Stars 9   
Regulators 21 @ Rampage 20   
Virgins 0 @ Borealis 20   
Monarchs 23 @ Treasure 7   
Timbers 3 @ Rancors 21   
Blizzard 26 @ Ravens 38   
Week 9
Regulators 60 @ Virgins 26   
Foghorn Leghorns 30 @ Rattlesnakes 24 (OT)   
Quicksilver 51 @ Storm 10   
Stars 19 @ Ukraine United 20   
Monarchs 30 @ Fightin' Amish 22   
Borealis 13 @ Chips 16 (OT)   
Rampage 3 @ Rancors 38   
Airborne 6 @ Treasure 10   
Autobots 9 @ Far East 34   
Leviathan 14 @ Timbers 9   
Mellotrons 20 @ Cut Throat’s 3   
Ravens 20 @ Fighting DeLucias 14 (OT)   
Heisenbergs 13 @ Mallards 31   
Black Sharks 25 @ Corsairs 3   
Bakers 16 @ Muskies 27   
Hammers 49 @ Blizzard 6   
Week 10
Timbers 17 @ Far East 24   
Treasure 13 @ Rancors 45   
Monarchs 55 @ Borealis 6   
Chips 13 @ Bakers 16   
Mellotrons 16 @ Hammers 24   
Blizzard 41 @ Muskies 35 (OT)   
Ukraine United 16 @ Ravens 6   
Corsairs 3 @ Stars 17   
Fightin' Amish 15 @ Regulators 17   
Storm 9 @ Rattlesnakes 38   
Mallards 55 @ Leviathan 3   
Black Sharks 12 @ Cut Throat’s 6   
Heisenbergs 24 @ Airborne 21   
Autobots 13 @ Rampage 17   
Virgins 7 @ Foghorn Leghorns 45   
Fighting DeLucias 3 @ Quicksilver 59   
Week 11
Muskies 10 @ Chips 14   
Virgins 6 @ Rampage 15   
Rattlesnakes 27 @ Airborne 13   
Cut Throat’s 12 @ Heisenbergs 17   
Hammers 51 @ Ravens 9   
Ukraine United 35 @ Regulators 36   
Storm 32 @ Autobots 6   
Fightin' Amish 20 @ Rancors 23   
Bakers 22 @ Timbers 10   
Treasure 3 @ Borealis 19   
Quicksilver 16 @ Corsairs 13   
Foghorn Leghorns 10 @ Stars 13   
Leviathan 16 @ Fighting DeLucias 19   
Mellotrons 20 @ Black Sharks 6   
Blizzard 36 @ Far East 20   
Mallards 0 @ Monarchs 12   
Week 12
Leviathan 16 @ Airborne 3   
Hammers 0 @ Fightin' Amish 9   
Rampage 10 @ Storm 9   
Stars 9 @ Quicksilver 38   
Foghorn Leghorns 37 @ Ukraine United 12   
Mellotrons 29 @ Regulators 12   
Rancors 31 @ Corsairs 9   
Muskies 9 @ Ravens 28   
Blizzard 6 @ Cut Throat’s 19   
Treasure 14 @ Bakers 25   
Autobots 0 @ Mallards 35   
Fighting DeLucias 9 @ Black Sharks 20   
Virgins 0 @ Heisenbergs 23   
Monarchs 13 @ Rattlesnakes 10   
Far East 0 @ Chips 21   
Timbers 20 @ Borealis 13   
Week 13
Fighting DeLucias 16 @ Airborne 9   
Foghorn Leghorns 10 @ Fightin' Amish 36   
Mallards 31 @ Cut Throat’s 3   
Rancors 30 @ Heisenbergs 16   
Regulators 32 @ Ukraine United 23   
Quicksilver 17 @ Treasure 29   
Leviathan 12 @ Autobots 13   
Hammers 30 @ Timbers 3   
Borealis 20 @ Far East 17 (OT)   
Corsairs 6 @ Monarchs 30   
Ravens 9 @ Stars 51   
Bakers 10 @ Rampage 19   
Rattlesnakes 23 @ Virgins 3   
Storm 27 @ Black Sharks 13   
Muskies 12 @ Mellotrons 35   
Blizzard 19 @ Chips 24   
Week 14
Quicksilver 0 @ Fightin' Amish 43   
Regulators 36 @ Foghorn Leghorns 31   
Rancors 24 @ Treasure 10   
Mallards 15 @ Heisenbergs 13   
Airborne 6 @ Leviathan 10   
Autobots 0 @ Ukraine United 23   
Cut Throat’s 13 @ Fighting DeLucias 14   
Chips 17 @ Timbers 3   
Far East 6 @ Hammers 69   
Borealis 17 @ Corsairs 0   
Monarchs 21 @ Stars 0   
Ravens 3 @ Bakers 23   
Rattlesnakes 20 @ Rampage 3   
Virgins 20 @ Storm 25   
Black Sharks 0 @ Mellotrons 30   
Muskies 6 @ Blizzard 34   
Week 15
Mallards 40 @ Airborne 10   
Cut Throat’s 13 @ Mellotrons 26   
Black Sharks 10 @ Fighting DeLucias 13   
Hammers 54 @ Muskies 3   
Ukraine United 14 @ Virgins 16   
Autobots 6 @ Regulators 70   
Storm 14 @ Stars 35   
Corsairs 9 @ Quicksilver 21   
Far East 10 @ Treasure 13   
Ravens 10 @ Timbers 16   
Blizzard 35 @ Foghorn Leghorns 28   
Rampage 33 @ Leviathan 3   
Heisenbergs 6 @ Rattlesnakes 47   
Bakers 20 @ Chips 41   
Rancors 9 @ Monarchs 37   
Fightin' Amish 43 @ Borealis 9   
Week 16
Virgins 0 @ Rattlesnakes 60   
Foghorn Leghorns 36 @ Storm 25   
Ukraine United 9 @ Quicksilver 10   
Fightin' Amish 29 @ Stars 10   
Chips 3 @ Monarchs 27   
Borealis 0 @ Rancors 44   
Airborne 3 @ Rampage 14   
Treasure 30 @ Autobots 7   
Far East 13 @ Timbers 17   
Mellotrons 52 @ Leviathan 6   
Cut Throat’s 7 @ Ravens 28   
Heisenbergs 12 @ Fighting DeLucias 6   
Black Sharks 10 @ Mallards 29   
Corsairs 27 @ Muskies 12   
Bakers 29 @ Blizzard 45   
Regulators 3 @ Hammers 55        
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
