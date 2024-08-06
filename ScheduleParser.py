
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
Hornets 3 @ Bulls 17   
Blazers 6 @ Wheels 20   
Maulers 14 @ Renegades 16   
Stars 23 @ Wranglers 6   
Panthers 13 @ Gamblers 27   
SaberCats 39 @ Showboats 50   
Invaders 0 @ Storm 19   
Federals 10 @ VooDoo 42   
Breakers 0 @ Steamer 17   
(NY) Stars 7 @ Outlaws 20   
Bell 22 @ Generals 0   
Sun 7 @ Gunslingers 44   
Thunderbolts 3 @ Gold 20   
Blitz 6 @ Hawaiians 34   
Stallions 9 @ Express 26   
Force 7 @ Bandits 17   
Week 2
Bulls 37 @ Bandits 20   
Wranglers 3 @ Panthers 33   
Federals 53 @ Stars 6   
Showboats 10 @ Gamblers 23   
Force 3 @ VooDoo 18   
Express 6 @ Hawaiians 20   
Invaders 18 @ SaberCats 14   
Blazers 3 @ Hornets 9   
Blitz 20 @ Thunderbolts 16   
Gold 7 @ Sun 27   
Renegades 22 @ Wheels 0   
Maulers 7 @ Storm 28   
Steamer 19 @ Stallions 13   
Breakers 0 @ (NY) Stars 20   
Generals 6 @ Gunslingers 24   
Bell 16 @ Outlaws 7   
Week 3
Stallions 13 @ (NY) Stars 6   
Hawaiians 14 @ Storm 27   
Force 6 @ Generals 25   
Steamer 21 @ Stars 2   
Express 13 @ VooDoo 51   
Blazers 9 @ Federals 62   
Panthers 7 @ Renegades 16   
SaberCats 6 @ Gunslingers 13   
Blitz 20 @ Bandits 17   
Bulls 10 @ Maulers 31   
Hornets 13 @ Gold 7   
Wranglers 10 @ Invaders 13   
Thunderbolts 13 @ Wheels 19 (OT)   
Outlaws 27 @ Sun 12   
Breakers 17 @ Showboats 23   
Bell 7 @ Gamblers 27   
Week 4
Federals 31 @ Bulls 22   
Bandits 15 @ Panthers 14   
Gold 10 @ Stars 19   
Thunderbolts 3 @ Invaders 25   
Renegades 22 @ Blazers 31   
Wheels 3 @ Storm 15   
Maulers 21 @ Hornets 3   
Blitz 3 @ Wranglers 33   
Express 3 @ Outlaws 31   
Generals 31 @ Showboats 37 (OT)   
(NY) Stars 14 @ Force 9   
Bell 34 @ Breakers 23   
VooDoo 20 @ Sun 17   
Stallions 7 @ Steamer 3   
SaberCats 8 @ Hawaiians 28   
Gamblers 0 @ Gunslingers 16   
Week 5
Bandits 6 @ Stars 0   
Renegades 6 @ Federals 28   
Thunderbolts 0 @ Panthers 48   
Gamblers 10 @ Showboats 23   
SaberCats 44 @ Steamer 20   
Force 14 @ Stallions 32   
Hawaiians 13 @ VooDoo 35   
Sun 20 @ Express 6   
Wheels 20 @ Wranglers 13   
Gold 20 @ Blitz 14   
Invaders 14 @ Maulers 14 (OT)   
Storm 36 @ Hornets 0   
Blazers 16 @ Bulls 38   
Outlaws 30 @ Breakers 3   
(NY) Stars 27 @ Generals 19   
Gunslingers 20 @ Bell 2   
Week 6
VooDoo 17 @ Force 12   
Panthers 24 @ Blitz 20   
Bell 0 @ (NY) Stars 31   
Express 0 @ Gamblers 44   
Showboats 43 @ Wheels 7   
Bandits 47 @ Thunderbolts 0   
Breakers 0 @ Stallions 52   
Maulers 17 @ Wranglers 0   
Federals 17 @ Hornets 3   
Stars 10 @ Blazers 19   
Bulls 17 @ Renegades 13   
Generals 13 @ Steamer 9   
Gunslingers 27 @ Hawaiians 3   
Sun 22 @ SaberCats 47   
Outlaws 14 @ Gold 19   
Storm 22 @ Invaders 3   
Week 7
Renegades 15 @ Bandits 12   
Thunderbolts 7 @ Blazers 22   
Breakers 7 @ Bell 38   
Sun 13 @ Showboats 23   
Hornets 13 @ Force 18   
Invaders 20 @ Stars 0   
Blitz 0 @ Bulls 19   
Wheels 3 @ Panthers 34   
Storm 19 @ Gold 24   
Wranglers 7 @ Federals 65   
Stallions 19 @ Maulers 22   
Hawaiians 17 @ Express 7   
Steamer 10 @ (NY) Stars 16   
Gunslingers 38 @ Outlaws 20   
Gamblers 6 @ SaberCats 22   
VooDoo 30 @ Generals 3   
Week 8
Gold 24 @ Wranglers 10   
Generals 20 @ Breakers 13   
VooDoo 27 @ Bulls 10   
Thunderbolts 0 @ Outlaws 59   
Hawaiians 24 @ SaberCats 36   
Steamer 13 @ Force 12   
(NY) Stars 29 @ Bell 13   
Gamblers 31 @ Sun 28   
Showboats 13 @ Express 20   
Storm 13 @ Gunslingers 44   
Wheels 12 @ Blitz 7   
Bandits 17 @ Maulers 20   
Panthers 36 @ Blazers 19   
Federals 14 @ Invaders 31   
Hornets 3 @ Stars 6   
Renegades 39 @ Stallions 14   
Week 9
Stars 3 @ Storm 40   
Generals 3 @ (NY) Stars 24   
Steamer 10 @ Hawaiians 17   
Stallions 23 @ VooDoo 49   
Express 16 @ Force 26   
Bell 24 @ Federals 41   
Blazers 7 @ Renegades 40   
SaberCats 47 @ Panthers 32   
Gunslingers 27 @ Blitz 9   
Bandits 10 @ Bulls 13   
Gold 23 @ Maulers 20   
Wranglers 13 @ Hornets 3   
Invaders 35 @ Wheels 9   
Sun 21 @ Thunderbolts 20   
Outlaws 7 @ Showboats 9   
Gamblers 24 @ Breakers 9   
Week 10
Wranglers 20 @ Gold 30   
VooDoo 67 @ Breakers 0   
Bulls 6 @ Thunderbolts 3 (OT)   
Hawaiians 17 @ Outlaws 0   
Force 14 @ SaberCats 30   
Steamer 20 @ Bell 13   
(NY) Stars 3 @ Gamblers 31   
Express 3 @ Sun 41   
Showboats 6 @ Gunslingers 31   
Blitz 6 @ Storm 27   
Wheels 3 @ Bandits 29   
Maulers 23 @ Blazers 9   
Panthers 24 @ Invaders 6   
Hornets 10 @ Federals 64   
Stars 10 @ Renegades 38   
Generals 23 @ Stallions 12   
Week 11
Hawaiians 40 @ Force 14   
VooDoo 40 @ Steamer 3   
Federals 23 @ Maulers 16   
Hornets 6 @ Invaders 34   
Gold 23 @ Storm 14   
Wranglers 18 @ Thunderbolts 0   
Bandits 16 @ Blazers 13   
Bulls 56 @ Panthers 31   
Renegades 13 @ Blitz 19 (OT)   
Outlaws 24 @ Generals 0   
SaberCats 22 @ Sun 20   
Gunslingers 23 @ Gamblers 26   
Wheels 10 @ Express 12   
Showboats 28 @ (NY) Stars 13   
Stallions 25 @ Bell 28   
Stars 0 @ Breakers 12   
Week 12
Panthers 45 @ Wheels 7   
Invaders 17 @ Gold 20   
Storm 22 @ Wranglers 7   
Generals 13 @ Renegades 31   
Hornets 0 @ Maulers 21   
Hawaiians 0 @ Gamblers 32   
Showboats 10 @ Outlaws 17   
Thunderbolts 0 @ Blitz 33   
(NY) Stars 0 @ VooDoo 20   
Bell 14 @ Force 23   
Breakers 3 @ Gunslingers 34   
Express 13 @ SaberCats 42   
Sun 3 @ Stallions 9   
Blazers 0 @ Steamer 31   
Bulls 6 @ Stars 10   
Federals 16 @ Bandits 16 (OT)   
Week 13
Outlaws 10 @ Gamblers 16   
Showboats 6 @ Hawaiians 27   
Invaders 19 @ Wranglers 20   
Blitz 14 @ Panthers 34   
Storm 9 @ Thunderbolts 10   
Gold 38 @ Wheels 0   
Renegades 34 @ Hornets 0   
Maulers 17 @ Generals 13   
Bandits 9 @ (NY) Stars 13   
Bell 10 @ VooDoo 40   
Force 3 @ Breakers 10   
Gunslingers 36 @ Express 6   
SaberCats 16 @ Stallions 22 (OT)   
Sun 6 @ Steamer 15   
Bulls 48 @ Blazers 3   
Stars 9 @ Federals 34   
Week 14
VooDoo 31 @ Stallions 0   
Sun 7 @ Hawaiians 37   
Gamblers 36 @ Invaders 17   
(NY) Stars 21 @ Breakers 3   
Wranglers 6 @ Showboats 13   
Outlaws 3 @ Gunslingers 20   
SaberCats 44 @ Express 12   
Storm 10 @ Panthers 17   
Wheels 30 @ Thunderbolts 17   
Federals 27 @ Gold 24   
Hornets 10 @ Bandits 20   
Renegades 20 @ Bulls 23   
Maulers 20 @ Stars 24   
Generals 20 @ Bell 30   
Force 0 @ Steamer 9   
Blazers 0 @ Blitz 19   
Week 15
Breakers 0 @ Generals 27   
Stars 13 @ Hornets 7   
Steamer 3 @ Express 0   
Force 9 @ Sun 27   
Gamblers 24 @ Outlaws 16   
Thunderbolts 7 @ Renegades 42   
Stallions 23 @ Hawaiians 7   
VooDoo 7 @ SaberCats 18   
Wheels 7 @ Bulls 33   
Invaders 19 @ Blitz 9   
Maulers 27 @ Federals 24   
Blazers 6 @ Bandits 37   
Panthers 17 @ Gold 33   
Wranglers 13 @ Storm 17   
Gunslingers 23 @ (NY) Stars 0   
Showboats 17 @ Bell 16   
Week 16
Storm 25 @ Federals 24   
Steamer 2 @ VooDoo 37   
Stars 6 @ Maulers 37   
Stallions 25 @ Force 3   
(NY) Stars 17 @ Hornets 13   
Gamblers 28 @ Generals 12   
Gunslingers 31 @ Showboats 9   
Bulls 10 @ Bell 17   
Bandits 7 @ Renegades 26   
Blitz 20 @ Wheels 17 (OT)   
Panthers 23 @ Thunderbolts 6   
Express 10 @ Wranglers 12   
Hawaiians 20 @ Sun 9   
Gold 28 @ Invaders 6   
Outlaws 27 @ SaberCats 35   
Breakers 13 @ Blazers 30   
"""

print(parse_scores(s))