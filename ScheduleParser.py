
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
Bulldogs 21 @ Wyverns 28   
Toros 0 @ Outlaws 17   
Rattlers 14 @ Bayhawks 24   
Apollos 21 @ Warships 9   
Miners 5 @ Hornets 20   
Legion 30 @ Minutemen 3   
Mafia 17 @ Brawlers 29   
Grizzlies 18 @ Sharks 3   
Founders 6 @ Bombers 15   
Bearcats 24 @ Reapers 8   
Spartans 12 @ Lumberjacks 29   
Pioneers 7 @ Lightning 23   
Archers 26 @ Stallions 14   
Pirates 2 @ Hogs 0   
Aliens 3 @ Medjays 6   
Motors 48 @ Huskies 31   
Week 2
Miners 38 @ Toros 0   
Pioneers 36 @ Sharks 7   
Bearcats 6 @ Apollos 12   
Medjays 13 @ Motors 34   
Hogs 6 @ Bombers 9   
Archers 40 @ Rattlers 31   
Huskies 46 @ Pirates 24   
Lumberjacks 17 @ Lightning 3   
Aliens 17 @ Grizzlies 16   
Brawlers 30 @ Reapers 3   
Bulldogs 3 @ Warships 23   
Spartans 27 @ Outlaws 3   
Legion 12 @ Stallions 6   
Hornets 34 @ Wyverns 22   
Mafia 28 @ Minutemen 0   
Founders 21 @ Bayhawks 11   
Week 3
Legion 17 @ Miners 14   
Wyverns 18 @ Founders 3   
Hornets 6 @ Spartans 37   
Huskies 16 @ Motors 42   
Bombers 15 @ Medjays 3   
Lightning 18 @ Aliens 21   
Lumberjacks 71 @ Rattlers 0   
Grizzlies 36 @ Pirates 13   
Minutemen 7 @ Reapers 32   
Bulldogs 27 @ Sharks 10   
Bayhawks 9 @ Brawlers 32   
Mafia 20 @ Bearcats 30   
Toros 17 @ Pioneers 10   
Hogs 12 @ Apollos 45   
Outlaws 13 @ Warships 20   
Stallions 3 @ Archers 40   
Week 4
Motors 17 @ Bayhawks 27   
Medjays 23 @ Mafia 70   
Stallions 0 @ Outlaws 31   
Miners 15 @ Lightning 3   
Pioneers 3 @ Lumberjacks 63   
Bombers 9 @ Apollos 13   
Rattlers 27 @ Legion 24   
Hornets 7 @ Grizzlies 21   
Warships 52 @ Toros 14   
Hogs 8 @ Archers 21   
Minutemen 17 @ Wyverns 19   
Brawlers 17 @ Bearcats 16   
Reapers 18 @ Spartans 13   
Founders 35 @ Bulldogs 3   
Pirates 9 @ Aliens 19   
Huskies 41 @ Sharks 3   
Week 5
Outlaws 17 @ Legion 12   
Wyverns 25 @ Miners 0   
Founders 31 @ Hornets 16   
Spartans 6 @ Warships 16   
Archers 40 @ Huskies 0   
Bombers 13 @ Motors 16 (OT)   
Medjays 3 @ Aliens 10   
Lightning 37 @ Rattlers 7   
Grizzlies 0 @ Lumberjacks 23   
Reapers 33 @ Pirates 7   
Sharks 16 @ Minutemen 10   
Bulldogs 3 @ Bayhawks 30   
Brawlers 3 @ Mafia 34   
Pioneers 24 @ Bearcats 49   
Apollos 46 @ Toros 6   
Stallions 4 @ Hogs 17   
Week 6
Stallions 0 @ Bombers 16   
Legion 0 @ Lightning 22   
Rattlers 10 @ Hornets 44   
Pioneers 3 @ Miners 12   
Bayhawks 25 @ Mafia 27   
Apollos 31 @ Motors 40   
Grizzlies 6 @ Outlaws 13   
Lumberjacks 23 @ Medjays 6   
Huskies 19 @ Toros 0   
Archers 10 @ Warships 22   
Minutemen 10 @ Hogs 11   
Wyverns 3 @ Brawlers 26   
Spartans 32 @ Bearcats 13   
Reapers 3 @ Bulldogs 6   
Pirates 3 @ Founders 25   
Aliens 8 @ Sharks 22   
Week 7
Lightning 28 @ Hornets 35   
Legion 10 @ Founders 30   
Rattlers 23 @ Pioneers 6   
Medjays 10 @ Grizzlies 13   
Lumberjacks 37 @ Aliens 6   
Brawlers 41 @ Bulldogs 0   
Reapers 22 @ Mafia 27   
Bayhawks 21 @ Wyverns 20   
Miners 10 @ Minutemen 7   
Bearcats 3 @ Warships 11   
Outlaws 0 @ Spartans 31   
Apollos 61 @ Stallions 0   
Archers 52 @ Motors 48   
Toros 0 @ Bombers 26   
Hogs 0 @ Huskies 17   
Pirates 15 @ Sharks 13   
Week 8
Bombers 20 @ Reapers 30   
Hornets 23 @ Legion 19   
Bayhawks 9 @ Founders 20   
Minutemen 27 @ Rattlers 3   
Huskies 17 @ Wyverns 20   
Medjays 13 @ Pioneers 3   
Pirates 10 @ Lightning 16   
Sharks 7 @ Hogs 43   
Mafia 24 @ Bulldogs 17   
Warships 13 @ Outlaws 24   
Apollos 36 @ Archers 3   
Motors 56 @ Toros 17   
Aliens 7 @ Brawlers 52   
Spartans 48 @ Stallions 6   
Bearcats 19 @ Miners 10   
Lumberjacks 20 @ Grizzlies 12   
Week 9
Lightning 31 @ Archers 7   
Outlaws 19 @ Reapers 28   
Wyverns 21 @ Bayhawks 20   
Sharks 7 @ Medjays 36   
Bombers 10 @ Huskies 3   
Motors 62 @ Stallions 13   
Hogs 6 @ Aliens 10   
Pioneers 7 @ Pirates 26   
Miners 19 @ Legion 13   
Lumberjacks 51 @ Apollos 7   
Spartans 38 @ Toros 5   
Warships 13 @ Bearcats 24   
Bulldogs 9 @ Brawlers 31   
Mafia 7 @ Founders 17   
Minutemen 7 @ Hornets 26   
Rattlers 10 @ Grizzlies 41   
Week 10
Brawlers 40 @ Minutemen 3   
Sharks 0 @ Lumberjacks 46   
Pioneers 7 @ Grizzlies 66   
Outlaws 7 @ Bearcats 22   
Bayhawks 27 @ Legion 10   
Bulldogs 6 @ Spartans 28   
Warships 12 @ Lightning 13   
Miners 23 @ Rattlers 28   
Founders 15 @ Wyverns 14   
Apollos 33 @ Hornets 11   
Bombers 19 @ Archers 0   
Aliens 13 @ Huskies 6   
Hogs 0 @ Medjays 17   
Toros 3 @ Stallions 16   
Motors 17 @ Pirates 30   
Mafia 31 @ Reapers 3   
Week 11
Legion 20 @ Hornets 23   
Founders 58 @ Rattlers 7   
Reapers 11 @ Wyverns 17   
Minutemen 7 @ Bayhawks 26   
Huskies 23 @ Bombers 10   
Lumberjacks 64 @ Pioneers 3   
Medjays 9 @ Pirates 28   
Sharks 0 @ Lightning 36   
Hogs 23 @ Bulldogs 7   
Warships 26 @ Mafia 29   
Outlaws 17 @ Apollos 30   
Archers 22 @ Toros 7   
Aliens 6 @ Motors 31   
Spartans 22 @ Brawlers 41   
Stallions 0 @ Bearcats 26   
Grizzlies 6 @ Miners 0   
Week 12
Motors 32 @ Bombers 31   
Toros 10 @ Hogs 13   
Medjays 23 @ Sharks 7   
Lightning 40 @ Pioneers 16   
Pirates 6 @ Lumberjacks 28   
Bayhawks 34 @ Aliens 0   
Wyverns 8 @ Legion 3   
Hornets 19 @ Miners 22 (OT)   
Founders 26 @ Minutemen 7   
Reapers 7 @ Brawlers 44   
Outlaws 9 @ Bulldogs 17   
Spartans 23 @ Mafia 38   
Apollos 37 @ Huskies 3   
Stallions 6 @ Grizzlies 31   
Rattlers 0 @ Warships 36   
Bearcats 37 @ Archers 20   
Week 13
Bulldogs 15 @ Reapers 0   
Wyverns 13 @ Mafia 21   
Bayhawks 20 @ Minutemen 2   
Legion 3 @ Lumberjacks 51   
Lightning 7 @ Grizzlies 8   
Sharks 14 @ Pirates 38   
Hogs 7 @ Motors 23   
Bombers 16 @ Aliens 17   
Brawlers 16 @ Founders 20   
Rattlers 14 @ Miners 33   
Bearcats 19 @ Outlaws 0   
Warships 24 @ Spartans 10   
Stallions 0 @ Toros 6   
Archers 6 @ Apollos 52   
Medjays 24 @ Huskies 35   
Hornets 34 @ Pioneers 0   
Week 14
Reapers 12 @ Warships 20   
Minutemen 15 @ Bulldogs 12   
Motors 24 @ Sharks 30   
Mafia 19 @ Huskies 22   
Bearcats 3 @ Spartans 17   
Hornets 20 @ Bayhawks 7   
Brawlers 41 @ Outlaws 10   
Stallions 0 @ Apollos 66   
Bombers 16 @ Hogs 6   
Pirates 46 @ Medjays 21   
Grizzlies 9 @ Legion 0   
Miners 0 @ Founders 36   
Rattlers 14 @ Wyverns 57   
Lightning 0 @ Lumberjacks 23   
Aliens 15 @ Pioneers 13   
Toros 21 @ Archers 24   
Week 15
Grizzlies 7 @ Lightning 14   
Outlaws 10 @ Archers 39   
Reapers 16 @ Bayhawks 0   
Wyverns 13 @ Medjays 6   
Sharks 3 @ Bombers 33   
Huskies 31 @ Stallions 3   
Motors 45 @ Hogs 7   
Aliens 10 @ Pirates 41   
Pioneers 19 @ Legion 16 (OT)   
Miners 0 @ Lumberjacks 27   
Apollos 12 @ Spartans 6   
Toros 0 @ Bearcats 30   
Warships 25 @ Brawlers 34   
Bulldogs 10 @ Mafia 6   
Minutemen 0 @ Founders 33   
Hornets 46 @ Rattlers 0   
Week 16
Sharks 6 @ Aliens 30   
Lightning 17 @ Medjays 19   
Legion 43 @ Rattlers 0   
Mafia 56 @ Outlaws 15   
Brawlers 24 @ Motors 3   
Toros 3 @ Apollos 29   
Archers 14 @ Spartans 47   
Warships 38 @ Stallions 3   
Huskies 12 @ Hogs 7   
Pirates 6 @ Bombers 3   
Founders 13 @ Reapers 15   
Lumberjacks 7 @ Hornets 24   
Grizzlies 30 @ Pioneers 17   
Bearcats 24 @ Bulldogs 7   
Bayhawks 20 @ Miners 6   
Wyverns 19 @ Minutemen 3   """

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
