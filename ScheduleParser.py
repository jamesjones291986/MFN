
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
Texans 6 @ Jaguars 23   
Chargers 3 @ Spotted Cows 15   
Clout Chasers 38 @ Vikings 16   
Superhawks 8 @ Wraiths 31   
Hammerheads 17 @ Colts 7   
Larceny 24 @ Nonsayins 17   
Chiefs 34 @ Raiders 10   
Broncos 17 @ Bears 27   
Buccaneers 6 @ Patriots 21   
Dolphins 30 @ Dinos 9   
Ravens 10 @ Stillers 3   
Browns 12 @ Dongers 23   
Giants 48 @ Cheesesteaks 24   
Redwolves 44 @ Aliens 17   
Panthers 14 @ Saints 38   
Buffalo 13 @ Jets 19   
Week 2
Dolphins 0 @ Buffalo 36   
Dinos 20 @ Stillers 20 (OT)   
Browns 7 @ Ravens 22   
Patriots 2 @ Jets 49   
Saints 22 @ Clout Chasers 13   
Wraiths 52 @ Nonsayins 3   
Superhawks 45 @ Spotted Cows 24   
Colts 9 @ Larceny 23   
Hammerheads 24 @ Jaguars 38   
Chiefs 27 @ Texans 26   
Chargers 14 @ Broncos 31   
Raiders 27 @ Bears 26   
Vikings 10 @ Aliens 24   
Dongers 76 @ Redwolves 33   
Cheesesteaks 13 @ Buccaneers 71   
Giants 13 @ Panthers 3   
Week 3
Browns 50 @ Cheesesteaks 9   
Ravens 23 @ Dinos 10   
Stillers 17 @ Jets 19   
Chiefs 9 @ Buffalo 6   
Chargers 7 @ Clout Chasers 57   
Raiders 24 @ Colts 13   
Texans 18 @ Broncos 3   
Larceny 3 @ Hammerheads 26   
Saints 3 @ Redwolves 9   
Buccaneers 12 @ Spotted Cows 15   
Vikings 9 @ Bears 7   
Nonsayins 13 @ Giants 30   
Dolphins 17 @ Aliens 12   
Panthers 13 @ Dongers 12   
Wraiths 6 @ Superhawks 22   
Jaguars 28 @ Patriots 16   
Week 4
Stillers 20 @ Browns 11   
Jaguars 37 @ Colts 14   
Chiefs 30 @ Hammerheads 16   
Chargers 0 @ Raiders 38   
Nonsayins 3 @ Texans 35   
Spotted Cows 6 @ Vikings 16   
Dolphins 9 @ Broncos 32   
Patriots 19 @ Panthers 7   
Aliens 3 @ Buffalo 45   
Dongers 3 @ Saints 53   
Giants 7 @ Redwolves 13   
Ravens 38 @ Cheesesteaks 12   
Bears 17 @ Wraiths 20   
Clout Chasers 40 @ Larceny 6   
Superhawks 24 @ Buccaneers 13   
Dinos 3 @ Jets 30   
Week 5
Larceny 7 @ Texans 17   
Spotted Cows 3 @ Raiders 9   
Clout Chasers 21 @ Bears 14   
Vikings 3 @ Chiefs 48   
Superhawks 11 @ Jaguars 32   
Colts 24 @ Nonsayins 0   
Broncos 10 @ Dinos 19   
Ravens 20 @ Chargers 3   
Panthers 3 @ Aliens 9   
Cheesesteaks 29 @ Redwolves 26   
Hammerheads 3 @ Wraiths 24   
Buccaneers 14 @ Saints 28   
Buffalo 28 @ Browns 3   
Giants 13 @ Dongers 3   
Patriots 16 @ Stillers 20   
Jets 22 @ Dolphins 3   
Week 6
Clout Chasers 28 @ Spotted Cows 3   
Nonsayins 9 @ Vikings 19   
Giants 3 @ Ravens 21   
Panthers 3 @ Buffalo 26   
Aliens 2 @ Saints 6   
Patriots 10 @ Dolphins 18   
Colts 13 @ Chiefs 59   
Broncos 17 @ Jaguars 22   
Chargers 16 @ Texans 24   
Hammerheads 10 @ Superhawks 12   
Larceny 13 @ Bears 19 (OT)   
Cheesesteaks 24 @ Wraiths 49   
Redwolves 13 @ Dongers 6   
Jets 22 @ Buccaneers 13   
Dinos 10 @ Browns 27   
Raiders 16 @ Stillers 0   
Week 7
Browns 13 @ Dolphins 20   
Redwolves 6 @ Ravens 41   
Texans 13 @ Wraiths 27   
Aliens 43 @ Nonsayins 0   
Buccaneers 22 @ Giants 13   
Saints 7 @ Patriots 10   
Dinos 7 @ Buffalo 42   
Cheesesteaks 14 @ Dongers 79   
Stillers 2 @ Jaguars 33   
Colts 3 @ Hammerheads 17   
Spotted Cows 26 @ Broncos 16   
Bears 31 @ Chargers 3   
Panthers 0 @ Jets 14   
Larceny 19 @ Vikings 14   
Raiders 13 @ Chiefs 19   
Superhawks 13 @ Clout Chasers 19   
Week 8
Stillers 20 @ Giants 12   
Aliens 3 @ Buccaneers 26   
Nonsayins 14 @ Larceny 24   
Vikings 6 @ Superhawks 38   
Texans 19 @ Hammerheads 14   
Wraiths 43 @ Colts 3   
Browns 3 @ Chiefs 48   
Redwolves 0 @ Panthers 45   
Dolphins 10 @ Jets 33   
Dinos 6 @ Ravens 16   
Buffalo 28 @ Patriots 10   
Cheesesteaks 17 @ Saints 52   
Spotted Cows 6 @ Dongers 20   
Bears 20 @ Clout Chasers 35   
Jaguars 50 @ Chargers 19   
Broncos 13 @ Raiders 27   
Week 9
Saints 26 @ Aliens 5   
Hammerheads 3 @ Raiders 15   
Chiefs 52 @ Spotted Cows 10   
Broncos 45 @ Vikings 18   
Jaguars 41 @ Nonsayins 2   
Dolphins 12 @ Stillers 6   
Patriots 6 @ Dinos 0   
Ravens 13 @ Browns 17   
Redwolves 6 @ Giants 31   
Dongers 77 @ Cheesesteaks 14   
Wraiths 19 @ Clout Chasers 33   
Superhawks 46 @ Larceny 0   
Bears 19 @ Panthers 7   
Buffalo 13 @ Buccaneers 6   
Jets 16 @ Texans 23   
Colts 28 @ Chargers 24   
Week 10
Nonsayins 0 @ Bears 31   
Vikings 16 @ Spotted Cows 6   
Wraiths 13 @ Jaguars 34   
Colts 3 @ Texans 41   
Hammerheads 17 @ Broncos 14   
Chargers 0 @ Chiefs 86   
Patriots 3 @ Raiders 31   
Saints 23 @ Buccaneers 16   
Larceny 27 @ Redwolves 6   
Dongers 17 @ Superhawks 15   
Giants 12 @ Aliens 16   
Dolphins 6 @ Panthers 15   
Clout Chasers 38 @ Cheesesteaks 16   
Stillers 17 @ Buffalo 64   
Jets 9 @ Ravens 7   
Browns 38 @ Dinos 10   
Week 11
Redwolves 0 @ Browns 66   
Ravens 19 @ Dolphins 13   
Nonsayins 0 @ Wraiths 51   
Buccaneers 27 @ Aliens 30   
Saints 26 @ Giants 0   
Patriots 6 @ Buffalo 47   
Dongers 10 @ Dinos 7   
Cheesesteaks 6 @ Stillers 41   
Jaguars 37 @ Hammerheads 16   
Broncos 24 @ Colts 13   
Spotted Cows 7 @ Bears 12   
Chargers 0 @ Jets 38   
Panthers 6 @ Larceny 6 (OT)   
Raiders 28 @ Vikings 7   
Chiefs 19 @ Clout Chasers 26   
Texans 3 @ Superhawks 24   
Week 12
Spotted Cows 13 @ Nonsayins 12   
Giants 3 @ Vikings 10   
Buffalo 52 @ Ravens 10   
Saints 36 @ Panthers 10   
Patriots 19 @ Aliens 27   
Colts 16 @ Dolphins 18   
Chiefs 27 @ Broncos 12   
Jaguars 37 @ Texans 3   
Chargers 17 @ Hammerheads 41   
Bears 10 @ Superhawks 26   
Larceny 3 @ Wraiths 25   
Redwolves 96 @ Cheesesteaks 3   
Dongers 16 @ Buccaneers 6   
Jets 23 @ Browns 3   
Stillers 19 @ Dinos 13 (OT)   
Clout Chasers 30 @ Raiders 19   
Week 13
Raiders 20 @ Broncos 3   
Browns 6 @ Stillers 24   
Cheesesteaks 0 @ Giants 56   
Ravens 6 @ Dongers 22   
Nonsayins 56 @ Superhawks 7   
Bears 3 @ Chiefs 42   
Spotted Cows 13 @ Clout Chasers 56   
Vikings 10 @ Chargers 13   
Texans 10 @ Colts 3   
Wraiths 24 @ Saints 22   
Jaguars 38 @ Larceny 6   
Dinos 37 @ Redwolves 36   
Buffalo 22 @ Hammerheads 16   
Panthers 3 @ Buccaneers 9   
Dolphins 10 @ Patriots 6   
Aliens 0 @ Jets 20   
Week 14
Superhawks 14 @ Colts 10   
Redwolves 0 @ Bears 55   
Chiefs 28 @ Chargers 3   
Texans 16 @ Ravens 10   
Cheesesteaks 0 @ Dinos 72   
Raiders 12 @ Jaguars 10   
Vikings 6 @ Wraiths 45   
Clout Chasers 62 @ Broncos 31   
Aliens 9 @ Panthers 10   
Spotted Cows 13 @ Larceny 20   
Nonsayins 0 @ Hammerheads 94   
Buffalo 10 @ Saints 19   
Giants 21 @ Browns 31   
Dongers 9 @ Stillers 27   
Jets 40 @ Patriots 10   
Buccaneers 25 @ Dolphins 10   
Week 15
Buffalo 23 @ Dolphins 10   
Stillers 19 @ Ravens 13   
Browns 0 @ Patriots 13   
Jets 17 @ Saints 22   
Clout Chasers 126 @ Nonsayins 0   
Wraiths 9 @ Spotted Cows 6   
Larceny 6 @ Superhawks 28   
Colts 19 @ Jaguars 28   
Hammerheads 23 @ Texans 26 (OT)   
Broncos 10 @ Chiefs 52   
Raiders 29 @ Chargers 0   
Bears 6 @ Vikings 19   
Aliens 3 @ Dongers 24   
Buccaneers 44 @ Redwolves 3   
Panthers 45 @ Cheesesteaks 0   
Dinos 10 @ Giants 6   
Week 16
Bears 28 @ Spotted Cows 0   
Dinos 6 @ Colts 13   
Broncos 21 @ Chargers 33   
Jets 13 @ Buffalo 16   
Ravens 17 @ Patriots 13   
Stillers 29 @ Redwolves 23   
Aliens 46 @ Cheesesteaks 0   
Buccaneers 10 @ Panthers 17   
Wraiths 10 @ Larceny 20   
Superhawks 2 @ Nonsayins 18   
Texans 3 @ Raiders 9   
Vikings 7 @ Clout Chasers 46   
Jaguars 17 @ Chiefs 31   
Hammerheads 21 @ Browns 7   
Saints 13 @ Dolphins 21   
Dongers 5 @ Giants 11      
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
