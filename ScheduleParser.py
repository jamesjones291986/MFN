
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
Mafia 41 @ Lightning 22   
Archers 15 @ Bayhawks 10   
Huskies 3 @ Motors 37   
Bombers 0 @ Hornets 7   
Founders 10 @ Hogs 29   
Miners 6 @ Legion 13   
Rattlers 0 @ Toros 20   
Apollos 49 @ Wyverns 13   
Medjays 0 @ Warships 51   
Pirates 3 @ Aliens 38   
Outlaws 7 @ Bearcats 36   
Grizzlies 10 @ Lumberjacks 26   
Bulldogs 3 @ Sharks 15   
Pioneers 10 @ Spartans 9   
Minutemen 17 @ Stallions 20 (OT)   
Brawlers 21 @ Reapers 16   
Week 2
Apollos 27 @ Archers 9   
Miners 2 @ Outlaws 13   
Hogs 27 @ Minutemen 0   
Mafia 24 @ Pirates 16   
Hornets 34 @ Rattlers 28   
Wyverns 17 @ Motors 31   
Bombers 12 @ Huskies 0   
Bayhawks 10 @ Founders 6   
Stallions 9 @ Legion 7   
Toros 16 @ Grizzlies 17   
Lightning 3 @ Lumberjacks 34   
Warships 18 @ Spartans 0   
Pioneers 6 @ Bearcats 13   
Sharks 10 @ Medjays 16   
Brawlers 0 @ Aliens 20   
Reapers 15 @ Bulldogs 0   
Week 3
Bulldogs 7 @ Grizzlies 48   
Outlaws 17 @ Warships 41   
Pioneers 0 @ Lightning 19   
Pirates 28 @ Sharks 16   
Wyverns 25 @ Archers 13   
Stallions 2 @ Apollos 20   
Spartans 6 @ Bearcats 22   
Motors 24 @ Rattlers 16   
Legion 0 @ Hornets 24   
Lumberjacks 10 @ Reapers 0   
Toros 17 @ Minutemen 10   
Founders 3 @ Bombers 30   
Hogs 6 @ Miners 15   
Huskies 23 @ Bayhawks 13   
Aliens 55 @ Medjays 3   
Mafia 42 @ Brawlers 16   
Week 4
Sharks 3 @ Bearcats 33   
Aliens 39 @ Spartans 0   
Legion 10 @ Apollos 47   
Mafia 42 @ Pioneers 5   
Grizzlies 10 @ Reapers 0   
Brawlers 0 @ Lumberjacks 27   
Bombers 20 @ Motors 15   
Founders 15 @ Bayhawks 3   
Minutemen 10 @ Wyverns 3   
Miners 16 @ Huskies 6   
Rattlers 30 @ Lightning 10   
Bulldogs 0 @ Hogs 16   
Pirates 3 @ Warships 40   
Hornets 12 @ Stallions 29   
Archers 0 @ Toros 17   
Medjays 6 @ Outlaws 3   
Week 5
Hogs 13 @ Bombers 25   
Minutemen 3 @ Archers 14   
Miners 23 @ Rattlers 10   
Motors 41 @ Legion 6   
Reapers 0 @ Lightning 12   
Hornets 19 @ Huskies 9   
Founders 11 @ Brawlers 3   
Warships 9 @ Apollos 24   
Sharks 11 @ Spartans 9   
Bearcats 6 @ Pirates 31   
Grizzlies 33 @ Outlaws 14   
Aliens 21 @ Mafia 15   
Bulldogs 3 @ Lumberjacks 31   
Pioneers 7 @ Stallions 9   
Toros 3 @ Wyverns 20   
Medjays 19 @ Bayhawks 13   
Week 6
Hogs 16 @ Medjays 22 (OT)   
Lumberjacks 16 @ Outlaws 3   
Bayhawks 24 @ Bulldogs 9   
Spartans 6 @ Warships 41   
Lightning 14 @ Pioneers 12   
Brawlers 3 @ Grizzlies 19   
Motors 29 @ Mafia 31   
Sharks 6 @ Reapers 19   
Bombers 24 @ Pirates 17   
Wyverns 12 @ Aliens 33   
Archers 9 @ Bearcats 13   
Hornets 13 @ Legion 10   
Toros 13 @ Miners 30   
Stallions 0 @ Founders 15   
Huskies 22 @ Rattlers 16   
Apollos 45 @ Minutemen 10   
Week 7
Toros 6 @ Hornets 29   
Miners 10 @ Stallions 20   
Rattlers 0 @ Apollos 52   
Pioneers 11 @ Lumberjacks 18   
Lightning 10 @ Grizzlies 34   
Aliens 39 @ Bearcats 7   
Warships 33 @ Outlaws 9   
Spartans 13 @ Medjays 10   
Mafia 82 @ Reapers 24   
Bulldogs 9 @ Brawlers 13   
Sharks 3 @ Pirates 13   
Archers 17 @ Legion 10   
Huskies 16 @ Hogs 27   
Bayhawks 2 @ Minutemen 20   
Motors 14 @ Bombers 9   
Founders 20 @ Wyverns 13   
Week 8
Pirates 23 @ Medjays 25   
Stallions 6 @ Spartans 9   
Legion 17 @ Miners 23   
Warships 14 @ Pioneers 7   
Founders 31 @ Toros 26   
Bulldogs 6 @ Aliens 25   
Minutemen 7 @ Sharks 9   
Lumberjacks 17 @ Hornets 15   
Reapers 15 @ Brawlers 9 (OT)   
Bearcats 15 @ Rattlers 17   
Hogs 10 @ Motors 53   
Outlaws 10 @ Lightning 30   
Huskies 17 @ Bombers 30   
Grizzlies 30 @ Mafia 33 (OT)   
Bayhawks 6 @ Wyverns 27   
Archers 3 @ Apollos 40   
Week 9
Grizzlies 6 @ Warships 28   
Rattlers 24 @ Hornets 17   
Apollos 52 @ Miners 14   
Aliens 25 @ Sharks 14   
Brawlers 16 @ Bulldogs 3   
Bearcats 3 @ Medjays 10   
Archers 20 @ Stallions 7   
Lumberjacks 44 @ Mafia 9   
Pirates 16 @ Outlaws 23   
Reapers 7 @ Pioneers 16   
Legion 16 @ Toros 13 (OT)   
Lightning 19 @ Spartans 6   
Bayhawks 9 @ Hogs 6 (OT)   
Minutemen 7 @ Motors 71   
Bombers 27 @ Wyverns 25   
Huskies 6 @ Founders 18   
Week 10
Stallions 20 @ Toros 30   
Bombers 13 @ Hogs 24   
Grizzlies 17 @ Lightning 20   
Sharks 19 @ Mafia 74   
Bulldogs 16 @ Reapers 23   
Wyverns 31 @ Bayhawks 7   
Medjays 0 @ Aliens 63   
Pirates 14 @ Brawlers 17 (OT)   
Spartans 7 @ Lumberjacks 26   
Outlaws 14 @ Pioneers 15   
Warships 33 @ Bearcats 21   
Founders 10 @ Minutemen 19   
Miners 10 @ Archers 13 (OT)   
Legion 7 @ Rattlers 37   
Motors 42 @ Huskies 10   
Apollos 41 @ Hornets 10   
Week 11
Bearcats 13 @ Outlaws 6   
Miners 23 @ Motors 26   
Hornets 30 @ Archers 24   
Spartans 15 @ Legion 21   
Pioneers 0 @ Grizzlies 38   
Lightning 3 @ Brawlers 7   
Lumberjacks 10 @ Warships 16   
Medjays 30 @ Sharks 3   
Mafia 48 @ Bulldogs 6   
Aliens 58 @ Reapers 0   
Pirates 11 @ Founders 6   
Wyverns 10 @ Huskies 14   
Stallions 10 @ Bayhawks 18   
Apollos 40 @ Toros 13   
Rattlers 31 @ Hogs 26   
Bombers 17 @ Minutemen 10   
Week 12
Wyverns 17 @ Stallions 10   
Founders 2 @ Apollos 44   
Reapers 3 @ Mafia 72   
Minutemen 6 @ Huskies 7   
Hogs 3 @ Hornets 40   
Motors 18 @ Bayhawks 3   
Toros 21 @ Archers 3   
Warships 30 @ Lightning 10   
Outlaws 6 @ Sharks 24   
Aliens 24 @ Pirates 6   
Spartans 16 @ Grizzlies 44   
Bearcats 3 @ Lumberjacks 26   
Legion 0 @ Pioneers 10   
Rattlers 27 @ Miners 18   
Brawlers 9 @ Bombers 31   
Medjays 9 @ Bulldogs 3   
Week 13
Pioneers 20 @ Bulldogs 14   
Brawlers 8 @ Sharks 21   
Mafia 48 @ Wyverns 7   
Bayhawks 0 @ Apollos 58   
Aliens 28 @ Motors 7   
Huskies 26 @ Reapers 10   
Lumberjacks 13 @ Lightning 7   
Bearcats 16 @ Spartans 3   
Legion 11 @ Hogs 17   
Minutemen 13 @ Founders 6   
Grizzlies 30 @ Miners 13   
Rattlers 6 @ Bombers 44   
Hornets 9 @ Warships 38   
Stallions 13 @ Archers 10 (OT)   
Outlaws 20 @ Toros 31   
Medjays 10 @ Pirates 13   
Week 14
Miners 2 @ Hornets 34   
Toros 10 @ Stallions 24   
Archers 30 @ Rattlers 6   
Apollos 6 @ Lumberjacks 13   
Grizzlies 31 @ Pioneers 3   
Lightning 3 @ Bearcats 6   
Warships 14 @ Aliens 17   
Spartans 21 @ Outlaws 16   
Reapers 10 @ Medjays 10 (OT)   
Brawlers 0 @ Mafia 68   
Pirates 34 @ Bulldogs 6   
Sharks 6 @ Huskies 26   
Motors 23 @ Founders 6   
Minutemen 25 @ Bayhawks 8   
Hogs 26 @ Wyverns 3   
Legion 3 @ Bombers 24   
Week 15
Wyverns 0 @ Founders 41   
Apollos 24 @ Stallions 6   
Bulldogs 18 @ Mafia 85   
Reapers 3 @ Minutemen 0   
Hogs 12 @ Huskies 10   
Hornets 31 @ Motors 55   
Bayhawks 6 @ Toros 20   
Lightning 33 @ Archers 3   
Warships 24 @ Sharks 10   
Outlaws 6 @ Aliens 34   
Spartans 7 @ Pirates 20   
Bearcats 15 @ Grizzlies 27   
Lumberjacks 13 @ Pioneers 3   
Rattlers 32 @ Legion 15   
Bombers 35 @ Miners 24   
Medjays 5 @ Brawlers 24   
Week 16
Wyverns 6 @ Minutemen 10   
Toros 0 @ Apollos 49   
Huskies 7 @ Legion 7 (OT)   
Stallions 3 @ Rattlers 30   
Motors 52 @ Hogs 10   
Pioneers 14 @ Brawlers 13   
Hornets 39 @ Miners 5   
Bayhawks 8 @ Bombers 33   
Archers 15 @ Founders 38   
Mafia 54 @ Medjays 9   
Lightning 18 @ Bulldogs 11   
Bearcats 14 @ Warships 35   
Lumberjacks 3 @ Grizzlies 19   
Outlaws 6 @ Spartans 13   
Sharks 0 @ Aliens 43   
Reapers 6 @ Pirates 27   
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
