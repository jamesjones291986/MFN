
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
Wheels 9 @ Wranglers 6   
Force 0 @ Storm 32   
Thunderbolts 20 @ Panthers 23 (OT)   
Federals 30 @ Stallions 27 (OT)   
Steamer 0 @ VooDoo 30   
Generals 20 @ Bell 10   
Renegades 23 @ Bandits 6   
Maulers 51 @ Hornets 0   
(NY) Stars 19 @ Breakers 3   
Blitz 33 @ Invaders 12   
Showboats 58 @ Gold 3   
Hawaiians 7 @ Outlaws 44   
Sun 10 @ SaberCats 42   
Express 3 @ Gunslingers 17   
Stars 3 @ Gamblers 26   
Blazers 3 @ Bulls 44   
Week 2
Blazers 17 @ Force 34   
Breakers 10 @ Generals 28   
Stars 13 @ Bandits 30   
Bell 35 @ Steamer 13   
Blitz 28 @ Gold 6   
Storm 0 @ Gunslingers 19   
VooDoo 15 @ Maulers 10   
Gamblers 0 @ Showboats 35   
Wranglers 6 @ Stallions 35   
Panthers 21 @ (NY) Stars 23   
Invaders 17 @ Hawaiians 10   
Bulls 24 @ Hornets 17   
Federals 0 @ Renegades 26   
SaberCats 29 @ Express 12   
Sun 0 @ Outlaws 14   
Thunderbolts 17 @ Wheels 17 (OT)   
Week 3
SaberCats 41 @ Bandits 32   
Express 23 @ Sun 31   
Wheels 13 @ Generals 23   
Federals 20 @ Stars 14   
Steamer 3 @ (NY) Stars 15   
Invaders 10 @ Force 37   
VooDoo 13 @ Wranglers 3   
Panthers 38 @ Thunderbolts 35 (OT)   
Storm 6 @ Gold 10   
Stallions 31 @ Bulls 51   
Hawaiians 0 @ Renegades 33   
Gamblers 41 @ Outlaws 20   
Hornets 13 @ Showboats 26   
Blazers 0 @ Maulers 55   
Bell 13 @ Breakers 25   
Gunslingers 13 @ Blitz 13 (OT)   
Week 4
Panthers 27 @ Express 17   
Blitz 12 @ SaberCats 8   
Wranglers 19 @ Steamer 23   
Storm 17 @ Invaders 15   
Thunderbolts 20 @ Bell 40   
(NY) Stars 20 @ Wheels 3   
Stallions 24 @ Force 14   
Renegades 7 @ VooDoo 26   
Gold 3 @ Sun 25   
Hawaiians 6 @ Showboats 33   
Gamblers 26 @ Gunslingers 14   
Hornets 7 @ Outlaws 62   
Stars 3 @ Maulers 38   
Bulls 17 @ Federals 13   
Bandits 9 @ Breakers 10   
Generals 27 @ Blazers 12   
Week 5
(NY) Stars 3 @ VooDoo 26   
Invaders 10 @ Wranglers 30   
Force 3 @ Bell 25   
Stallions 14 @ Breakers 24   
Bulls 17 @ Sun 21   
Express 23 @ Hawaiians 18   
Renegades 38 @ SaberCats 26   
Blazers 49 @ Bandits 7   
Maulers 31 @ Federals 6   
Hornets 10 @ Stars 22   
Showboats 26 @ Gamblers 24   
Outlaws 30 @ Gunslingers 27 (OT)   
Storm 7 @ Blitz 20   
Gold 3 @ Thunderbolts 50   
Panthers 12 @ Wheels 22   
Generals 6 @ Steamer 21   
Week 6
Bell 23 @ Panthers 20   
Gold 6 @ Wheels 24   
Wranglers 14 @ Storm 38   
Thunderbolts 12 @ Blitz 16   
Generals 12 @ Stallions 23   
Renegades 10 @ Maulers 13   
Express 13 @ Gamblers 31   
SaberCats 23 @ Bulls 29   
Hawaiians 37 @ Blazers 14   
Bandits 3 @ Sun 38   
Gunslingers 16 @ Federals 3   
Showboats 37 @ Stars 13   
Outlaws 27 @ Invaders 15   
VooDoo 30 @ Force 3   
Breakers 6 @ (NY) Stars 23   
Hornets 24 @ Steamer 17   
Week 7
Outlaws 16 @ SaberCats 20   
Wranglers 15 @ Gold 7   
Blazers 20 @ Express 17   
Invaders 12 @ Storm 9 (OT)   
Bandits 16 @ Federals 13   
Gunslingers 26 @ Hawaiians 7   
Showboats 6 @ Maulers 25   
Force 16 @ Stars 25   
VooDoo 31 @ Bell 12   
Blitz 20 @ Wheels 16   
Panthers 9 @ Breakers 13   
Thunderbolts 22 @ Generals 23   
Bulls 28 @ (NY) Stars 34 (OT)   
Sun 3 @ Renegades 34   
Gamblers 52 @ Hornets 16   
Steamer 14 @ Stallions 26   
Week 8
Stars 3 @ Gunslingers 61   
VooDoo 0 @ Stallions 20   
Federals 10 @ Outlaws 30   
Bandits 10 @ Hornets 29   
Renegades 31 @ Blazers 10   
Maulers 34 @ Bulls 0   
Showboats 13 @ Express 3   
SaberCats 6 @ Gamblers 34   
Storm 16 @ Panthers 13   
Wranglers 6 @ Blitz 37   
Wheels 10 @ Bell 20   
Generals 13 @ (NY) Stars 45   
Breakers 14 @ Force 30   
Steamer 9 @ Gold 17   
Invaders 18 @ Thunderbolts 13   
Hawaiians 23 @ Sun 16   
Week 9
Stallions 36 @ Gold 6   
Blitz 3 @ Thunderbolts 9   
Wheels 6 @ Storm 13   
Wranglers 23 @ Panthers 31   
Bell 22 @ Generals 13   
Maulers 5 @ Gamblers 6   
Express 3 @ Bulls 42   
SaberCats 17 @ Hawaiians 30   
Bandits 10 @ Blazers 19   
Gunslingers 43 @ Sun 7   
Federals 23 @ Showboats 36   
Outlaws 37 @ Stars 10   
Invaders 6 @ VooDoo 58   
(NY) Stars 26 @ Force 3   
Steamer 6 @ Breakers 0   
Hornets 3 @ Renegades 37   
Week 10
Express 3 @ Bandits 22   
Sun 5 @ Wheels 9   
Stars 3 @ Generals 17   
(NY) Stars 27 @ Federals 10   
Steamer 8 @ Invaders 27   
Force 10 @ VooDoo 37   
Thunderbolts 33 @ Wranglers 3   
Panthers 30 @ Gold 6   
Storm 17 @ Stallions 45   
Renegades 14 @ Bulls 23   
Gamblers 31 @ Hawaiians 14   
Outlaws 6 @ Showboats 21   
Hornets 16 @ Blazers 15   
Maulers 22 @ Bell 3   
Blitz 17 @ Breakers 26   
SaberCats 17 @ Gunslingers 50   
Week 11
Gunslingers 29 @ Hornets 13   
Stallions 44 @ Invaders 17   
Outlaws 17 @ Maulers 13   
Bandits 3 @ Bulls 40   
Showboats 40 @ SaberCats 36   
Wheels 14 @ Thunderbolts 23   
Blitz 6 @ Panthers 9   
Gold 7 @ Wranglers 12   
Hawaiians 23 @ Express 3   
Sun 7 @ Blazers 22   
Storm 19 @ Steamer 9   
Gamblers 55 @ Federals 20   
Renegades 41 @ Stars 7   
(NY) Stars 30 @ Bell 3   
Force 6 @ Generals 13   
Breakers 10 @ VooDoo 17   
Week 12
Gold 9 @ Force 16   
VooDoo 6 @ Storm 3   
Steamer 31 @ Bandits 26   
Maulers 17 @ Gunslingers 10   
Breakers 3 @ Bell 47   
Generals 13 @ Blitz 17   
Blazers 7 @ Stars 9   
Wheels 0 @ Showboats 34   
Wranglers 6 @ Gamblers 23   
Stallions 20 @ (NY) Stars 3   
Panthers 10 @ Invaders 13   
Bulls 40 @ Hawaiians 21   
Federals 33 @ Hornets 31   
Renegades 17 @ Express 6   
SaberCats 8 @ Sun 12   
Thunderbolts 9 @ Outlaws 40   
Week 13
Stars 29 @ Hornets 24   
Force 5 @ Steamer 10   
Stallions 12 @ VooDoo 24   
Bell 16 @ (NY) Stars 13   
Generals 10 @ Breakers 6   
Hawaiians 23 @ Thunderbolts 27   
Bulls 60 @ Blazers 16   
Express 18 @ SaberCats 20   
Gamblers 37 @ Panthers 17   
Wheels 7 @ Blitz 13   
Storm 29 @ Wranglers 3   
Invaders 24 @ Gold 6   
Gunslingers 6 @ Outlaws 23   
Federals 7 @ Maulers 57   
Bandits 7 @ Renegades 47   
Sun 14 @ Showboats 29   
Week 14
Outlaws 37 @ Express 16   
Blazers 6 @ SaberCats 28   
Wranglers 10 @ Invaders 33   
Gold 0 @ Storm 24   
Hornets 23 @ Federals 30   
Bandits 3 @ Hawaiians 9   
Gunslingers 40 @ Showboats 11   
Maulers 34 @ Stars 7   
Force 17 @ Stallions 31   
VooDoo 30 @ Steamer 7   
Bell 13 @ Blitz 20   
Breakers 12 @ Wheels 6   
Generals 17 @ Panthers 13   
(NY) Stars 38 @ Thunderbolts 35   
Bulls 25 @ Renegades 22   
Gamblers 39 @ Sun 3   
Week 15
Thunderbolts 0 @ Storm 37   
Force 13 @ Wranglers 16 (OT)   
Wheels 13 @ Panthers 23   
Stallions 36 @ Steamer 0   
VooDoo 33 @ Generals 27   
Bell 29 @ Renegades 27   
Maulers 37 @ Bandits 9   
Breakers 10 @ Hornets 15   
Blitz 6 @ (NY) Stars 29   
Gold 6 @ Invaders 20   
Showboats 35 @ Outlaws 12   
Hawaiians 3 @ SaberCats 28   
Sun 10 @ Express 15   
Gunslingers 17 @ Gamblers 10   
Stars 26 @ Bulls 51   
Federals 22 @ Blazers 16 (OT)   
Week 16
Invaders 29 @ Wheels 12   
(NY) Stars 20 @ Generals 24   
Bell 21 @ Stallions 58   
Breakers 0 @ Thunderbolts 6   
Bulls 57 @ Bandits 0   
Panthers 31 @ Blitz 30   
Express 7 @ Wranglers 17   
Sun 6 @ Hawaiians 37   
Blazers 3 @ Renegades 42   
Stars 3 @ Federals 34   
Outlaws 10 @ Gamblers 38   
Hornets 0 @ Maulers 37   
Showboats 13 @ Gunslingers 16 (OT)   
SaberCats 31 @ Storm 13   
Steamer 10 @ Force 6   
Gold 0 @ VooDoo 36          
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
