
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
Cavaliers 42 @ Bullets 24   
Spurs 0 @ Jazz 47   
Celtics 24 @ Heat 0   
Thunder 17 @ Warriors 32   
Nuggets 17 @ Nets 38   
Suns 16 @ Lakers 13   
Bulls 13 @ Timberwolves 3   
Kings 13 @ Bucks 18   
Pistons 12 @ Trail Blazers 16   
Royals 34 @ Knicks 52   
Rockets 10 @ Grizzlies 14   
Magic 23 @ Wizards 3   
76ers 0 @ Globetrotters 7   
Pelicans 3 @ Hornets 45   
Mavericks 10 @ Hawks 6   
Clippers 0 @ Raptors 56   
Week 2
Heat 9 @ Clippers 17   
Nuggets 6 @ Warriors 30   
Grizzlies 0 @ Royals 26   
Celtics 13 @ Rockets 18   
76ers 20 @ Kings 5   
Mavericks 6 @ Thunder 19   
Trail Blazers 18 @ Globetrotters 0   
Hornets 9 @ Lakers 0   
Hawks 13 @ Wizards 3   
Magic 24 @ Pelicans 6   
Spurs 0 @ Raptors 76   
Cavaliers 10 @ Nets 21   
Bucks 20 @ Timberwolves 0   
Bullets 10 @ Pistons 34   
Bulls 20 @ Jazz 0   
Suns 44 @ Knicks 52   
Week 3
Spurs 3 @ Cavaliers 26   
Clippers 19 @ Warriors 0   
Thunder 16 @ Nuggets 7   
Rockets 3 @ Royals 9   
Grizzlies 20 @ Magic 31   
Wizards 6 @ Globetrotters 3   
Pelicans 6 @ 76ers 28   
Hornets 10 @ Mavericks 3   
Hawks 0 @ Raptors 27   
Bucks 10 @ Bulls 13   
Trail Blazers 28 @ Kings 14   
Knicks 65 @ Lakers 17   
Heat 0 @ Nets 35   
Bullets 14 @ Jazz 34   
Celtics 10 @ Suns 28   
Pistons 10 @ Timberwolves 17   
Week 4
Bullets 6 @ Bucks 20   
Trail Blazers 3 @ Nets 16   
Warriors 27 @ Thunder 17   
Grizzlies 10 @ Clippers 30   
Globetrotters 11 @ Timberwolves 14   
Knicks 22 @ Cavaliers 16   
Lakers 9 @ Bulls 13   
76ers 0 @ Wizards 7   
Spurs 0 @ Celtics 68   
Kings 22 @ Heat 3   
Hawks 16 @ Pelicans 0   
Mavericks 7 @ Suns 31   
Raptors 22 @ Nuggets 3   
Jazz 16 @ Pistons 20   
Royals 6 @ Hornets 24   
Rockets 10 @ Magic 38   
Week 5
Pelicans 13 @ Magic 44   
Jazz 13 @ Warriors 16   
Royals 19 @ Nuggets 20   
Clippers 28 @ Thunder 7   
Mavericks 9 @ Wizards 7   
Hawks 27 @ Pistons 10   
Timberwolves 13 @ Bullets 17   
Bucks 60 @ Spurs 3   
Rockets 0 @ Raptors 27   
Hornets 12 @ Grizzlies 15   
Lakers 27 @ Kings 0   
Globetrotters 10 @ 76ers 13   
Trail Blazers 17 @ Bulls 20   
Suns 57 @ Heat 0   
Cavaliers 11 @ Celtics 20   
Nets 32 @ Knicks 38   
Week 6
Warriors 16 @ Clippers 13   
Pistons 23 @ Mavericks 17   
Globetrotters 20 @ Nuggets 3   
Magic 35 @ Hawks 13   
Timberwolves 0 @ Kings 12   
Spurs 3 @ Bullets 32   
Bucks 21 @ Trail Blazers 24   
Hornets 24 @ 76ers 10   
Lakers 10 @ Wizards 0   
Bulls 9 @ Suns 23   
Heat 7 @ Cavaliers 37   
Royals 14 @ Raptors 28   
Pelicans 17 @ Grizzlies 10   
Rockets 27 @ Jazz 7   
Nets 23 @ Celtics 3   
Knicks 52 @ Thunder 13   
Week 7
Pistons 10 @ Lakers 13   
Clippers 7 @ Royals 25   
Grizzlies 16 @ Thunder 0   
Jazz 6 @ Cavaliers 27   
Trail Blazers 29 @ Celtics 17   
Suns 22 @ Bucks 9   
Timberwolves 0 @ Bulls 26   
Wizards 13 @ 76ers 16 (OT)   
Pelicans 6 @ Hawks 3   
Mavericks 14 @ Magic 11   
Raptors 19 @ Hornets 3   
Nuggets 24 @ Rockets 25   
Globetrotters 6 @ Warriors 6 (OT)   
Nets 26 @ Bullets 0   
Heat 10 @ Spurs 19   
Kings 38 @ Knicks 2   
Week 8
Knicks 12 @ Nets 3   
Pistons 41 @ Spurs 6   
Kings 3 @ Lakers 31   
Royals 20 @ Grizzlies 23   
Thunder 7 @ Cavaliers 22   
Celtics 21 @ Jazz 22   
Suns 23 @ Trail Blazers 34   
Timberwolves 6 @ Bucks 40   
Wizards 3 @ Bulls 10   
76ers 13 @ Hawks 9   
Pelicans 22 @ Mavericks 36   
Magic 22 @ Hornets 25   
Raptors 14 @ Heat 0   
Bullets 21 @ Nuggets 0   
Warriors 21 @ Rockets 33   
Clippers 24 @ Globetrotters 10   
Week 9
Nuggets 19 @ Clippers 7   
Royals 12 @ Warriors 20   
Grizzlies 24 @ Rockets 19   
Heat 0 @ Celtics 38   
Suns 18 @ Kings 0   
Mavericks 3 @ 76ers 20   
Thunder 7 @ Globetrotters 12   
Lakers 24 @ Trail Blazers 41   
Hawks 3 @ Hornets 41   
Wizards 14 @ Pelicans 20 (OT)   
Magic 3 @ Raptors 10   
Spurs 0 @ Nets 77   
Cavaliers 0 @ Timberwolves 13   
Pistons 21 @ Bucks 3   
Bulls 24 @ Bullets 3   
Jazz 13 @ Knicks 32   
Week 10
Cavaliers 30 @ Jazz 15   
Nuggets 10 @ Mavericks 16   
Lakers 10 @ Celtics 17   
Magic 31 @ Bucks 22   
Trail Blazers 16 @ Suns 34   
Timberwolves 6 @ Pelicans 10   
Bulls 6 @ Pistons 23   
Warriors 10 @ Grizzlies 18   
Raptors 19 @ Royals 3   
Wizards 10 @ Hornets 17   
Rockets 6 @ Thunder 9 (OT)   
Hawks 13 @ Globetrotters 13 (OT)   
76ers 14 @ Clippers 17 (OT)   
Bullets 7 @ Heat 15   
Knicks 44 @ Spurs 6   
Nets 39 @ Kings 6   
Week 11
Globetrotters 10 @ Pelicans 32   
Hornets 3 @ Magic 35   
Thunder 3 @ Wizards 10   
Warriors 3 @ Mavericks 20   
Hawks 24 @ Royals 13   
Raptors 10 @ Grizzlies 17   
Nuggets 14 @ 76ers 3   
Rockets 22 @ Clippers 8   
Cavaliers 25 @ Spurs 10   
Bulls 49 @ Kings 7   
Knicks 48 @ Trail Blazers 7   
Lakers 3 @ Nets 26   
Jazz 6 @ Heat 3   
Celtics 26 @ Bullets 0   
Timberwolves 10 @ Suns 27   
Bucks 0 @ Pistons 44   
Week 12
Jazz 21 @ Spurs 14   
Nets 38 @ Heat 0   
Raptors 20 @ Warriors 9   
Pistons 26 @ Bulls 6   
Grizzlies 20 @ Bullets 3   
Cavaliers 35 @ Royals 7   
Hornets 3 @ Pelicans 9   
Trail Blazers 38 @ Timberwolves 17   
Kings 10 @ Suns 14   
Celtics 3 @ Knicks 76   
Bucks 16 @ Lakers 14   
76ers 16 @ Magic 50   
Mavericks 15 @ Clippers 10   
Nuggets 7 @ Thunder 10   
Rockets 16 @ Hawks 9   
Globetrotters 6 @ Wizards 3 (OT)   
Week 13
Jazz 20 @ Bullets 7   
Clippers 16 @ Nuggets 6   
Nets 20 @ Grizzlies 13   
Royals 9 @ Rockets 14   
Warriors 13 @ 76ers 14   
Globetrotters 10 @ Hornets 6   
Hawks 3 @ Magic 58   
Celtics 13 @ Kings 33   
Lakers 14 @ Timberwolves 0   
Bucks 10 @ Cavaliers 28   
Thunder 0 @ Raptors 40   
Knicks 88 @ Heat 0   
Spurs 6 @ Bulls 37   
Wizards 0 @ Mavericks 15   
Pelicans 10 @ Trail Blazers 40   
Suns 25 @ Pistons 21   
Week 14
Lakers 6 @ Suns 13   
Hornets 23 @ Hawks 3   
Timberwolves 3 @ Pistons 9   
Bucks 7 @ 76ers 0   
Bullets 13 @ Spurs 31   
Heat 3 @ Trail Blazers 34   
Kings 2 @ Magic 25   
Warriors 13 @ Nuggets 3   
Cavaliers 24 @ Bulls 7   
Mavericks 19 @ Globetrotters 17   
Clippers 10 @ Wizards 6   
Thunder 20 @ Royals 34   
Grizzlies 0 @ Raptors 80   
Pelicans 18 @ Rockets 28   
Nets 10 @ Jazz 3   
Knicks 58 @ Celtics 12   
Week 15
Kings 19 @ Trail Blazers 6   
Spurs 0 @ Timberwolves 26   
Pistons 17 @ Cavaliers 31   
Warriors 20 @ Celtics 23 (OT)   
Nets 9 @ Suns 15   
Heat 7 @ Lakers 24   
Bullets 16 @ Knicks 96   
Jazz 15 @ Bucks 6   
Bulls 0 @ Hornets 18   
Magic 31 @ Globetrotters 0   
Royals 20 @ Pelicans 40   
Grizzlies 15 @ Hawks 20   
Raptors 19 @ Rockets 34   
Thunder 13 @ Clippers 16   
Wizards 10 @ Nuggets 0   
76ers 19 @ Mavericks 0   
Week 16
Raptors 7 @ Pelicans 7 (OT)   
Nuggets 0 @ Grizzlies 9   
Globetrotters 3 @ Mavericks 17   
Bulls 14 @ Bucks 6   
Timberwolves 3 @ Jazz 13   
Bullets 16 @ Cavaliers 27   
76ers 3 @ Thunder 10   
Wizards 3 @ Warriors 10   
Celtics 6 @ Nets 39   
Kings 14 @ Pistons 20   
Trail Blazers 10 @ Lakers 16   
Suns 47 @ Hawks 3   
Clippers 26 @ Spurs 0   
Heat 0 @ Knicks 38   
Magic 57 @ Royals 0   
Hornets 14 @ Rockets 0    
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
