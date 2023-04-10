
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
Seahawks 13 @ Demons 41   
Monarchs 19 @ The Red Dragon 10   
Xtreme 3 @ Tigers 23   
Upside Down Sicilians 15 @ Shadow Dancers 3   
Devils 6 @ Thundercocks 23   
Lions 18 @ OrangeCrush 9   
Rumble Ponies 16 @ Barbarians 13   
Bears 12 @ Templars 3   
Fire Breathing Rubber Duckies 13 @ Rocky Mountain Bronx 16   
Invaders 23 @ Terror 10   
Anteaters 16 @ Holy Hand Grenades 13   
Argonauts 10 @ Wraiths 16   
Dildozers 6 @ Bandits 21   
Ravens 3 @ Raiders 16   
Kayfabe 34 @ Bangles 17   
Pirates 0 @ Thrashers 26   
Week 2
Kayfabe 6 @ Thundercocks 20   
The Red Dragon 7 @ Thrashers 20   
Bangles 14 @ Dildozers 9   
Ravens 0 @ Wraiths 21   
Barbarians 13 @ Devils 9   
Lions 23 @ Bears 9   
Demons 44 @ Pirates 10   
Monarchs 14 @ Invaders 16   
Rocky Mountain Bronx 10 @ Templars 20   
Fire Breathing Rubber Duckies 11 @ Upside Down Sicilians 23   
Holy Hand Grenades 13 @ Rumble Ponies 10   
Xtreme 19 @ Shadow Dancers 16   
OrangeCrush 9 @ Anteaters 28   
Seahawks 6 @ Tigers 31   
Bandits 10 @ Argonauts 17   
Terror 10 @ Raiders 23   
Week 3
Monarchs 36 @ Fire Breathing Rubber Duckies 12   
Demons 9 @ Upside Down Sicilians 36   
Thundercocks 23 @ Seahawks 20 (OT)   
Pirates 0 @ Tigers 29   
Bandits 12 @ Kayfabe 0   
The Red Dragon 6 @ Invaders 16   
Shadow Dancers 15 @ Templars 0   
Anteaters 33 @ Barbarians 20   
Lions 6 @ Terror 9 (OT)   
Raiders 14 @ Argonauts 24   
Rumble Ponies 3 @ Dildozers 24   
Devils 19 @ OrangeCrush 0   
Wraiths 20 @ Bangles 6   
Bears 6 @ Holy Hand Grenades 10   
Rocky Mountain Bronx 10 @ Ravens 13 (OT)   
Thrashers 0 @ Xtreme 29   
Week 4
Seahawks 16 @ Templars 10   
Demons 30 @ Fire Breathing Rubber Duckies 13   
Xtreme 26 @ Thundercocks 16   
Terror 17 @ Thrashers 22   
The Red Dragon 13 @ Rocky Mountain Bronx 6   
Upside Down Sicilians 9 @ Invaders 10   
Shadow Dancers 9 @ Monarchs 47   
Tigers 19 @ Kayfabe 0   
Pirates 23 @ Dildozers 42   
Bears 20 @ Raiders 26 (OT)   
OrangeCrush 19 @ Barbarians 29   
Lions 7 @ Ravens 3   
Bangles 0 @ Argonauts 9   
Anteaters 16 @ Wraiths 9   
Bandits 23 @ Rumble Ponies 6   
Holy Hand Grenades 10 @ Devils 13   
Week 5
Kayfabe 17 @ Monarchs 45   
Anteaters 16 @ Bears 6   
Bangles 13 @ Raiders 30   
Ravens 6 @ Holy Hand Grenades 9   
Barbarians 7 @ Rumble Ponies 19   
Thrashers 24 @ Pirates 0   
OrangeCrush 6 @ Wraiths 9   
Bandits 23 @ Dildozers 6   
Argonauts 20 @ Invaders 16   
Rocky Mountain Bronx 0 @ Tigers 25   
Templars 6 @ The Red Dragon 12   
Shadow Dancers 26 @ Fire Breathing Rubber Duckies 12   
Seahawks 10 @ Thundercocks 25   
Xtreme 30 @ Demons 17   
Upside Down Sicilians 30 @ Lions 3   
Devils 6 @ Terror 7   
Week 6
Dildozers 12 @ Ravens 6   
Raiders 17 @ Lions 20   
Wraiths 3 @ Bandits 0   
Devils 15 @ Holy Hand Grenades 13   
Bears 12 @ Rumble Ponies 15   
Terror 0 @ Bangles 10   
Anteaters 7 @ OrangeCrush 26   
Barbarians 10 @ Argonauts 16   
Upside Down Sicilians 13 @ Fire Breathing Rubber Duckies 18   
The Red Dragon 0 @ Monarchs 12   
Invaders 11 @ Kayfabe 3   
Rocky Mountain Bronx 3 @ Shadow Dancers 24   
Thrashers 7 @ Seahawks 10   
Tigers 29 @ Pirates 3   
Demons 37 @ Thundercocks 10   
Xtreme 17 @ Templars 0   
Week 7
Ravens 3 @ Bandits 13   
Fire Breathing Rubber Duckies 7 @ Devils 17   
Argonauts 20 @ OrangeCrush 17   
Templars 0 @ Shadow Dancers 17   
Thundercocks 33 @ Pirates 6   
Kayfabe 0 @ Thrashers 25   
Upside Down Sicilians 23 @ Seahawks 20   
Demons 17 @ Xtreme 33   
Bears 24 @ Barbarians 3   
Wraiths 3 @ Tigers 20   
Rumble Ponies 23 @ Anteaters 6   
Holy Hand Grenades 16 @ Lions 19   
Raiders 30 @ Bangles 3   
Dildozers 19 @ Terror 18   
Monarchs 31 @ Rocky Mountain Bronx 16   
Invaders 14 @ The Red Dragon 17   
Week 8
Dildozers 0 @ Argonauts 23   
Ravens 3 @ Terror 8   
Anteaters 9 @ Bandits 7   
Rumble Ponies 13 @ OrangeCrush 12   
Barbarians 3 @ Upside Down Sicilians 61   
Xtreme 16 @ Seahawks 0   
Shadow Dancers 30 @ Demons 13   
Templars 9 @ Thundercocks 19   
Fire Breathing Rubber Duckies 7 @ Invaders 35   
Rocky Mountain Bronx 0 @ Kayfabe 19   
Tigers 20 @ Thrashers 0   
The Red Dragon 13 @ Pirates 25   
Monarchs 16 @ Wraiths 13 (OT)   
Holy Hand Grenades 16 @ Raiders 20   
Bears 10 @ Devils 9   
Bangles 17 @ Lions 26   
Week 9
Kayfabe 11 @ The Red Dragon 16   
Rumble Ponies 10 @ Fire Breathing Rubber Duckies 9   
OrangeCrush 9 @ Xtreme 13   
Holy Hand Grenades 0 @ Shadow Dancers 13   
Bandits 0 @ Barbarians 14   
Raiders 17 @ Terror 23 (OT)   
Invaders 17 @ Tigers 38   
Pirates 10 @ Seahawks 26   
Lions 17 @ Anteaters 13   
Thundercocks 10 @ Demons 45   
Monarchs 30 @ Thrashers 20   
Upside Down Sicilians 38 @ Templars 0   
Dildozers 3 @ Rocky Mountain Bronx 23   
Wraiths 3 @ Argonauts 10   
Devils 16 @ Ravens 7   
Bears 21 @ Bangles 6   
Week 10
Raiders 20 @ Devils 27   
Seahawks 20 @ Bears 21   
Bangles 10 @ The Red Dragon 22   
Ravens 6 @ Pirates 10   
Argonauts 23 @ Bandits 7   
Terror 7 @ Wraiths 20   
Templars 6 @ Anteaters 16   
Monarchs 0 @ Upside Down Sicilians 26   
Demons 16 @ Thrashers 3   
Thundercocks 22 @ Rumble Ponies 19 (OT)   
Shadow Dancers 32 @ OrangeCrush 9   
Fire Breathing Rubber Duckies 6 @ Xtreme 23   
Kayfabe 0 @ Tigers 62   
Invaders 32 @ Rocky Mountain Bronx 9   
Barbarians 17 @ Dildozers 10   
Lions 12 @ Holy Hand Grenades 20   
Week 11
Templars 10 @ Demons 45   
Fire Breathing Rubber Duckies 8 @ Seahawks 18   
Thundercocks 7 @ Xtreme 17   
Thrashers 27 @ Rocky Mountain Bronx 16   
The Red Dragon 13 @ Upside Down Sicilians 30   
Invaders 17 @ Shadow Dancers 19   
Tigers 31 @ Monarchs 14   
Pirates 17 @ Kayfabe 6   
Raiders 17 @ Dildozers 24   
OrangeCrush 3 @ Bears 12   
Barbarians 16 @ Lions 19 (OT)   
Ravens 6 @ Bangles 23   
Argonauts 29 @ Anteaters 14   
Bandits 7 @ Wraiths 17   
Rumble Ponies 3 @ Devils 7   
Terror 8 @ Holy Hand Grenades 14   
Week 12
The Red Dragon 6 @ Bandits 0   
OrangeCrush 7 @ Rumble Ponies 16   
Fire Breathing Rubber Duckies 3 @ Shadow Dancers 22   
Xtreme 34 @ Kayfabe 10   
Holy Hand Grenades 25 @ Barbarians 27   
Bangles 13 @ Terror 12   
Tigers 14 @ Raiders 10   
Pirates 14 @ Invaders 52   
Anteaters 23 @ Seahawks 13   
Lions 10 @ Demons 48   
Thundercocks 10 @ Thrashers 3   
Templars 10 @ Monarchs 16   
Upside Down Sicilians 31 @ Rocky Mountain Bronx 7   
Dildozers 6 @ Wraiths 9   
Argonauts 20 @ Ravens 3   
Devils 0 @ Bears 27   
Week 13
Argonauts 34 @ Dildozers 6   
Bangles 10 @ Ravens 3   
Terror 0 @ Bandits 6   
Anteaters 39 @ Rumble Ponies 14   
Barbarians 15 @ OrangeCrush 0   
Upside Down Sicilians 12 @ Xtreme 10   
Demons 37 @ Seahawks 34   
Shadow Dancers 13 @ Thundercocks 16   
Fire Breathing Rubber Duckies 29 @ Templars 10   
Rocky Mountain Bronx 12 @ Invaders 24   
Thrashers 14 @ Kayfabe 6   
Tigers 40 @ The Red Dragon 10   
Monarchs 39 @ Pirates 15   
Wraiths 20 @ Raiders 18   
Holy Hand Grenades 37 @ Bears 6   
Lions 23 @ Devils 6   
Week 14
Dildozers 6 @ OrangeCrush 33   
Terror 20 @ Ravens 9   
Wraiths 3 @ Rumble Ponies 21   
Pirates 10 @ Rocky Mountain Bronx 0   
The Red Dragon 3 @ Fire Breathing Rubber Duckies 20   
Shadow Dancers 0 @ Upside Down Sicilians 19   
Invaders 26 @ Templars 0   
Tigers 27 @ Thundercocks 9   
Demons 6 @ Barbarians 10   
Xtreme 10 @ Holy Hand Grenades 38   
Seahawks 20 @ Kayfabe 6   
Bears 26 @ Lions 12   
Devils 20 @ Anteaters 16   
Raiders 23 @ Monarchs 27   
Thrashers 6 @ Argonauts 20   
Bandits 10 @ Bangles 17   
Week 15
Wraiths 9 @ Barbarians 27   
Rumble Ponies 27 @ Lions 30 (OT)   
Ravens 10 @ Bears 40   
Thrashers 16 @ Tigers 45   
Thundercocks 3 @ Upside Down Sicilians 45   
Dildozers 13 @ Anteaters 34   
Kayfabe 14 @ Demons 17   
OrangeCrush 3 @ Holy Hand Grenades 34   
Pirates 7 @ Xtreme 31   
Templars 0 @ Fire Breathing Rubber Duckies 14   
Bangles 13 @ Devils 10   
Seahawks 13 @ Shadow Dancers 24   
Argonauts 10 @ Terror 3   
Bandits 14 @ Raiders 10   
Invaders 16 @ Monarchs 13   
Rocky Mountain Bronx 13 @ The Red Dragon 10   
Week 16
Templars 0 @ Upside Down Sicilians 31   
Seahawks 13 @ Xtreme 20   
Thundercocks 13 @ Fire Breathing Rubber Duckies 25   
Rumble Ponies 10 @ Argonauts 33   
OrangeCrush 9 @ Bandits 16   
Terror 7 @ Bears 26   
Barbarians 18 @ Anteaters 44   
Devils 7 @ Lions 15   
Rocky Mountain Bronx 14 @ Monarchs 34   
Raiders 16 @ Ravens 3   
Wraiths 12 @ Dildozers 13   
Holy Hand Grenades 33 @ Bangles 9   
Shadow Dancers 20 @ The Red Dragon 6   
Thrashers 7 @ Invaders 25   
Kayfabe 12 @ Pirates 3   
Tigers 37 @ Demons 20         
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
