
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
Clippers 3 @ Thunder 33   
Trail Blazers 0 @ Kings 37   
Timberwolves 12 @ Bulls 21   
Nuggets 10 @ Hawks 13   
Royals 30 @ Spurs 8   
Bullets 0 @ Lakers 45   
Suns 13 @ Jazz 3   
Cavaliers 33 @ Grizzlies 6   
Rockets 10 @ Raptors 23   
Bucks 34 @ Pistons 37   
Pelicans 10 @ Warriors 15   
Heat 6 @ Wizards 31   
Globetrotters 3 @ Mavericks 16   
Celtics 3 @ Knicks 78   
Nets 13 @ 76ers 17   
Magic 23 @ Hornets 6   
Week 2
Bullets 13 @ Jazz 6   
Kings 30 @ Suns 3   
Spurs 0 @ Raptors 54   
Warriors 0 @ Hornets 23   
Hawks 3 @ Magic 35   
Trail Blazers 12 @ Lakers 9 (OT)   
Thunder 19 @ Pelicans 3   
Cavaliers 29 @ Clippers 7   
Bulls 7 @ Royals 9   
Bucks 6 @ Grizzlies 13   
Nuggets 3 @ Knicks 42   
Mavericks 7 @ 76ers 17   
Globetrotters 7 @ Nets 30   
Wizards 6 @ Timberwolves 0   
Pistons 31 @ Rockets 24   
Heat 6 @ Celtics 9   
Week 3
Spurs 7 @ Bullets 28   
Knicks 53 @ Thunder 23   
Nets 33 @ Heat 7   
Jazz 0 @ Kings 64   
76ers 28 @ Lakers 16   
Mavericks 10 @ Globetrotters 5   
Bulls 44 @ Grizzlies 13   
Rockets 10 @ Royals 50   
Timberwolves 3 @ Magic 26   
Trail Blazers 10 @ Hornets 13   
Wizards 0 @ Suns 33   
Raptors 17 @ Cavaliers 16   
Pistons 23 @ Bucks 20   
Hawks 17 @ Pelicans 30   
Nuggets 6 @ Clippers 0   
Warriors 17 @ Celtics 17 (OT)   
Week 4
Thunder 12 @ Nuggets 0   
Cavaliers 29 @ Bullets 7   
Raptors 6 @ Knicks 36   
Globetrotters 13 @ Heat 9   
Trail Blazers 7 @ 76ers 15   
Mavericks 6 @ Wizards 7   
Celtics 12 @ Nets 17   
Clippers 28 @ Warriors 13   
Pelicans 6 @ Magic 33   
Lakers 27 @ Suns 0   
Kings 31 @ Hawks 10   
Bulls 16 @ Bucks 10   
Royals 17 @ Pistons 40   
Hornets 18 @ Timberwolves 13   
Grizzlies 13 @ Spurs 7   
Jazz 20 @ Rockets 7   
Week 5
Kings 70 @ Bullets 6   
Celtics 8 @ Thunder 22   
Suns 54 @ Spurs 0   
Jazz 6 @ Cavaliers 27   
Heat 3 @ 76ers 23   
Nets 26 @ Wizards 3   
Magic 20 @ Nuggets 13   
Lakers 27 @ Globetrotters 9   
Mavericks 27 @ Trail Blazers 17   
Warriors 28 @ Knicks 39   
Royals 7 @ Grizzlies 24   
Pelicans 3 @ Bulls 23   
Raptors 30 @ Rockets 7   
Pistons 0 @ Timberwolves 7   
Hornets 8 @ Clippers 6   
Bucks 13 @ Hawks 26   
Week 6
Nuggets 7 @ Warriors 19   
76ers 3 @ Pistons 62   
Timberwolves 31 @ Pelicans 24   
Bucks 19 @ Bulls 7   
Clippers 20 @ Magic 74   
Knicks 78 @ Heat 7   
Celtics 26 @ Globetrotters 0   
Kings 34 @ Wizards 10   
Hornets 6 @ Hawks 16   
Thunder 16 @ Nets 17   
Grizzlies 14 @ Raptors 59   
Royals 21 @ Jazz 3   
Rockets 0 @ Bullets 9   
Spurs 3 @ Cavaliers 43   
Lakers 7 @ Trail Blazers 6   
Suns 27 @ Mavericks 17   
Week 7
Hawks 3 @ Clippers 23   
76ers 6 @ Celtics 17   
Suns 27 @ Globetrotters 10   
Trail Blazers 21 @ Cavaliers 30   
Wizards 17 @ Knicks 76   
Heat 0 @ Nets 52   
Nuggets 10 @ Spurs 37   
Magic 16 @ Pelicans 0   
Bucks 17 @ Hornets 20   
Timberwolves 3 @ Raptors 37   
Grizzlies 18 @ Rockets 9   
Bullets 0 @ Royals 46   
Warriors 6 @ Thunder 31   
Lakers 28 @ Jazz 13   
Mavericks 0 @ Kings 45   
Bulls 6 @ Pistons 24   
Week 8
Warriors 14 @ Clippers 19   
Celtics 16 @ Bullets 7   
Spurs 13 @ Jazz 20   
Kings 31 @ 76ers 9   
Wizards 10 @ Lakers 37   
Trail Blazers 13 @ Suns 59   
Knicks 44 @ Cavaliers 16   
Thunder 29 @ Magic 26 (OT)   
Pelicans 6 @ Hornets 27   
Nets 23 @ Nuggets 3   
Mavericks 13 @ Heat 3   
Rockets 15 @ Bulls 9   
Hawks 19 @ Timberwolves 7   
Grizzlies 3 @ Pistons 41   
Royals 26 @ Raptors 23   
Bucks 10 @ Globetrotters 19   
Week 9
Celtics 9 @ Clippers 19   
Globetrotters 12 @ 76ers 7   
Cavaliers 10 @ Suns 40   
Trail Blazers 9 @ Wizards 6   
Knicks 6 @ Nets 15   
Spurs 3 @ Heat 15   
Pelicans 3 @ Nuggets 9   
Hornets 0 @ Magic 53   
Raptors 31 @ Bucks 9   
Timberwolves 9 @ Rockets 7   
Grizzlies 13 @ Royals 20   
Bullets 3 @ Thunder 63   
Warriors 10 @ Jazz 16 (OT)   
Kings 16 @ Lakers 9   
Bulls 7 @ Mavericks 9   
Hawks 16 @ Pistons 38   
Week 10
Warriors 12 @ Nuggets 30   
Pistons 35 @ Pelicans 6   
Bucks 5 @ Timberwolves 0   
Magic 35 @ Bulls 3   
Knicks 64 @ Clippers 13   
Celtics 16 @ Heat 0   
Globetrotters 0 @ Kings 52   
Hawks 17 @ Wizards 2   
Hornets 10 @ Thunder 41   
Nets 13 @ Grizzlies 6   
Raptors 26 @ Royals 0   
Jazz 27 @ Bullets 6   
Rockets 6 @ Cavaliers 23   
Spurs 7 @ Trail Blazers 34   
Lakers 7 @ Mavericks 28   
76ers 3 @ Suns 41   
Week 11
Grizzlies 3 @ Jazz 34   
Cavaliers 17 @ Royals 21   
Clippers 10 @ Raptors 44   
Bullets 11 @ Spurs 30   
Thunder 41 @ Warriors 6   
Bulls 21 @ Hornets 17   
Magic 61 @ Bucks 10   
Pelicans 0 @ Hawks 30   
Lakers 16 @ Kings 23   
Suns 29 @ Trail Blazers 27   
Heat 13 @ Nuggets 10   
76ers 7 @ Knicks 56   
Mavericks 0 @ Nets 54   
Globetrotters 9 @ Wizards 21   
Timberwolves 10 @ Pistons 27   
Rockets 13 @ Celtics 38   
Week 12
76ers 9 @ Mavericks 12 (OT)   
Spurs 0 @ Kings 67   
Wizards 7 @ Celtics 13   
Suns 42 @ Bulls 28   
Warriors 10 @ Hawks 13   
Pistons 20 @ Magic 41   
Nuggets 9 @ Hornets 13   
Thunder 44 @ Rockets 0   
Clippers 13 @ Nets 44   
Pelicans 7 @ Lakers 43   
Bullets 0 @ Cavaliers 49   
Globetrotters 7 @ Trail Blazers 23   
Heat 3 @ Knicks 98   
Bucks 3 @ Royals 17   
Grizzlies 20 @ Timberwolves 3   
Jazz 0 @ Raptors 26   
Week 13
Heat 3 @ Warriors 17   
Bulls 26 @ Timberwolves 17   
Royals 10 @ Nuggets 10 (OT)   
Magic 47 @ Hawks 3   
Thunder 22 @ Clippers 12   
Kings 27 @ Trail Blazers 2   
Bullets 20 @ Suns 88   
Pelicans 0 @ Bucks 16   
Raptors 33 @ Grizzlies 0   
Hornets 27 @ Pistons 13   
76ers 7 @ Wizards 17   
Knicks 40 @ Globetrotters 28   
Celtics 17 @ Mavericks 3   
Jazz 11 @ Nets 9 (OT)   
Cavaliers 7 @ Lakers 24   
Spurs 12 @ Rockets 7   
Week 14
Nuggets 10 @ Thunder 38   
Magic 19 @ Warriors 3   
Suns 14 @ Kings 33   
Bulls 15 @ Hawks 3   
Clippers 23 @ Pelicans 29   
Trail Blazers 23 @ Bullets 6   
Heat 7 @ Royals 41   
Timberwolves 3 @ Bucks 13   
Rockets 14 @ Grizzlies 16   
Pistons 10 @ Raptors 30   
Hornets 3 @ 76ers 14   
Wizards 3 @ Globetrotters 20   
Knicks 62 @ Mavericks 20   
Nets 22 @ Celtics 35   
Cavaliers 31 @ Jazz 9   
Lakers 24 @ Spurs 3   
Week 15
Lakers 19 @ Bucks 10   
Hornets 7 @ Pelicans 3   
Timberwolves 3 @ Kings 26   
Jazz 21 @ Trail Blazers 17   
Magic 23 @ Suns 26   
Raptors 33 @ Bullets 0   
Cavaliers 36 @ Spurs 0   
Hawks 16 @ Thunder 41   
Pistons 26 @ Bulls 42   
Royals 23 @ Rockets 17   
76ers 19 @ Globetrotters 23   
Wizards 12 @ Mavericks 10   
Clippers 17 @ Heat 7   
Nuggets 3 @ Celtics 30   
Grizzlies 3 @ Warriors 22   
Nets 3 @ Knicks 28   
Week 16
Royals 7 @ Timberwolves 16   
Globetrotters 11 @ Pelicans 17   
Mavericks 14 @ Magic 55   
Raptors 16 @ Bulls 10   
Hawks 13 @ Hornets 34   
Rockets 0 @ Bucks 20   
Thunder 29 @ Heat 6   
Kings 40 @ Cavaliers 6   
Wizards 21 @ 76ers 3   
Suns 25 @ Lakers 10   
Pistons 20 @ Trail Blazers 25   
Bullets 6 @ Grizzlies 20   
Jazz 24 @ Spurs 13   
Nets 3 @ Warriors 9   
Clippers 9 @ Nuggets 2   
Knicks 33 @ Celtics 6   
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
