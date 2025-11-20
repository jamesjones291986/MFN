
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
(NY) Stars 10 @ Breakers 16   
Steamer 13 @ Panthers 6   
Generals 24 @ Bandits 0   
Gamblers 10 @ Renegades 36   
Blazers 7 @ Bulls 13   
Stallions 30 @ Force 16   
VooDoo 6 @ Hornets 23   
Maulers 21 @ Stars 19   
Federals 21 @ Bell 20   
Wranglers 6 @ Outlaws 27   
Invaders 13 @ Showboats 45   
Gold 51 @ Storm 7   
Gunslingers 10 @ SaberCats 9   
Thunderbolts 54 @ Wheels 3   
Blitz 25 @ Sun 6   
Express 7 @ Hawaiians 26   
Week 2
(NY) Stars 17 @ Invaders 14   
Wheels 17 @ Force 38   
SaberCats 24 @ Blitz 3   
Steamer 6 @ Thunderbolts 25   
Generals 31 @ Wranglers 10   
Stars 3 @ Sun 13   
Panthers 16 @ Hawaiians 13   
Stallions 16 @ Federals 30   
VooDoo 10 @ Bandits 6   
Outlaws 24 @ Bulls 31   
Bell 20 @ Blazers 23 (OT)   
Gold 21 @ Gamblers 16   
Storm 3 @ Gunslingers 46   
Renegades 26 @ Showboats 14   
Hornets 20 @ Breakers 24   
Maulers 3 @ Express 20   
Week 3
Hawaiians 20 @ Blitz 3   
Invaders 38 @ Storm 6   
Outlaws 6 @ Showboats 38   
Thunderbolts 6 @ SaberCats 12   
Gold 26 @ Gunslingers 22   
Steamer 29 @ Force 7   
Generals 19 @ (NY) Stars 17 (OT)   
Wranglers 20 @ Breakers 14   
Bulls 10 @ Bell 30   
Panthers 27 @ Stallions 12   
Wheels 10 @ Express 28   
Sun 13 @ Hornets 20   
Stars 17 @ Blazers 22   
Bandits 0 @ Gamblers 16   
Maulers 6 @ Renegades 3   
VooDoo 13 @ Federals 28   
Week 4
Bell 16 @ (NY) Stars 10   
Renegades 13 @ Generals 17   
Bulls 14 @ Gamblers 7   
Wranglers 6 @ Showboats 49   
Storm 3 @ Gold 62   
Invaders 37 @ Breakers 13   
VooDoo 30 @ Wheels 16   
Blitz 0 @ Gunslingers 49   
Bandits 24 @ Blazers 13   
Hornets 0 @ Federals 28   
Stallions 10 @ Steamer 44   
Stars 6 @ Express 15   
Hawaiians 13 @ Sun 7   
Outlaws 10 @ Thunderbolts 21   
Panthers 7 @ SaberCats 27   
Force 27 @ Maulers 37   
Week 5
Express 16 @ Thunderbolts 39   
Federals 10 @ Stars 6   
Stallions 17 @ Hornets 9   
Hawaiians 31 @ Maulers 13   
SaberCats 19 @ Sun 0   
Showboats 38 @ Panthers 3   
Generals 6 @ Invaders 23   
Gold 24 @ Blitz 13   
Force 6 @ VooDoo 19   
Wheels 3 @ Steamer 10   
Storm 9 @ Wranglers 18   
Gunslingers 24 @ Gamblers 3   
Renegades 27 @ Outlaws 20   
Bulls 9 @ Bandits 9 (OT)   
Breakers 0 @ Bell 7   
Blazers 13 @ (NY) Stars 18   
Week 6
Hawaiians 7 @ SaberCats 30   
Maulers 15 @ Federals 24   
Thunderbolts 15 @ Stallions 3   
Express 7 @ Showboats 24   
Sun 7 @ Panthers 26   
Hornets 33 @ Stars 30 (OT)   
Gold 13 @ Invaders 27   
VooDoo 25 @ Blitz 3   
Force 13 @ Steamer 14   
Storm 17 @ Wheels 13   
Gunslingers 44 @ Wranglers 7   
Gamblers 26 @ Outlaws 21   
Bandits 6 @ Renegades 10   
Bulls 0 @ Breakers 21   
(NY) Stars 14 @ Bell 15   
Blazers 7 @ Generals 26   
Week 7
Sun 3 @ Hawaiians 16   
Blitz 20 @ Steamer 34   
Force 0 @ Thunderbolts 61   
SaberCats 8 @ Stars 3   
Wheels 0 @ Panthers 31   
Invaders 16 @ Wranglers 14   
(NY) Stars 16 @ Generals 14   
Express 0 @ Federals 24   
VooDoo 3 @ Stallions 21   
Bandits 6 @ Bulls 13   
Blazers 23 @ Outlaws 23 (OT)   
Bell 20 @ Gold 37   
Storm 10 @ Gamblers 20   
Showboats 10 @ Gunslingers 6   
Breakers 6 @ Renegades 25   
Maulers 25 @ Hornets 0   
Week 8
SaberCats 44 @ Hawaiians 25   
Thunderbolts 30 @ Blitz 0   
Outlaws 19 @ Storm 0   
Showboats 7 @ Gold 34   
Gunslingers 34 @ Invaders 16   
VooDoo 22 @ Force 17   
Steamer 13 @ Generals 20   
Breakers 0 @ (NY) Stars 24   
Wranglers 3 @ Bell 23   
Stallions 16 @ Bulls 22 (OT)   
Express 9 @ Panthers 13   
Wheels 21 @ Sun 2   
Stars 23 @ Hornets 6   
Gamblers 31 @ Blazers 27   
Renegades 27 @ Bandits 3   
Federals 13 @ Maulers 12   
Week 9
Force 0 @ (NY) Stars 59   
Bell 0 @ Generals 16   
Renegades 22 @ Bulls 10   
Gamblers 0 @ Showboats 23   
Wranglers 6 @ Storm 13   
Invaders 6 @ Gold 17   
Breakers 10 @ VooDoo 16   
Blitz 18 @ Wheels 10   
Gunslingers 34 @ Blazers 13   
Bandits 13 @ Hornets 14   
Federals 10 @ Steamer 16   
Stars 10 @ Stallions 26   
Hawaiians 17 @ Express 23   
Sun 0 @ Outlaws 13   
Panthers 30 @ Thunderbolts 24   
SaberCats 22 @ Maulers 29   
Week 10
Showboats 32 @ Storm 13   
Bandits 11 @ Bell 24   
Gunslingers 3 @ Renegades 13   
Generals 10 @ Bulls 6   
Hornets 0 @ SaberCats 43   
Federals 0 @ Hawaiians 26   
(NY) Stars 34 @ Stars 0   
Gamblers 16 @ Wranglers 0   
Invaders 23 @ Outlaws 0   
Breakers 3 @ Gold 20   
Blazers 12 @ Force 7   
Blitz 10 @ Thunderbolts 13   
Panthers 17 @ Wheels 5   
Steamer 3 @ VooDoo 10   
Maulers 30 @ Stallions 6   
Sun 0 @ Express 25   
Week 11
Thunderbolts 9 @ Panthers 11   
Bulls 27 @ Blazers 7   
Sun 6 @ Federals 42   
Steamer 2 @ Maulers 34   
Renegades 23 @ (NY) Stars 19   
Stars 13 @ VooDoo 7   
Bell 20 @ Stallions 6   
Wheels 6 @ Blitz 27   
Generals 26 @ Breakers 0   
Gold 48 @ Wranglers 19   
Storm 3 @ Invaders 38   
Outlaws 26 @ Bandits 13   
Hornets 26 @ Force 7   
Gamblers 21 @ Hawaiians 17   
SaberCats 19 @ Express 3   
Gunslingers 17 @ Showboats 13   
Week 12
VooDoo 16 @ Steamer 12   
Bell 31 @ Storm 14   
Bandits 13 @ Breakers 7   
Force 14 @ Panthers 52   
Hawaiians 39 @ Stars 0   
Sun 0 @ Thunderbolts 21   
Wranglers 3 @ Invaders 26   
Outlaws 14 @ Gunslingers 26   
Showboats 41 @ Gamblers 10   
Blazers 6 @ Renegades 41   
Generals 6 @ Maulers 27   
Gold 27 @ (NY) Stars 15   
Bulls 13 @ Federals 20   
SaberCats 20 @ Wheels 0   
Stallions 10 @ Blitz 18   
Express 27 @ Hornets 10   
Week 13
Bulls 6 @ Gunslingers 33   
Showboats 21 @ Bandits 0   
Bell 14 @ Renegades 21   
Storm 13 @ Generals 43   
Express 0 @ SaberCats 19   
Hornets 6 @ Hawaiians 40   
Stars 13 @ Federals 27   
(NY) Stars 35 @ Wranglers 13   
Gamblers 16 @ Invaders 37   
Outlaws 6 @ Gold 37   
Breakers 13 @ Blazers 37   
Blitz 13 @ Force 0   
Wheels 3 @ Thunderbolts 43   
Panthers 23 @ VooDoo 20   
Steamer 0 @ Stallions 12   
Maulers 38 @ Sun 3   
Week 14
Renegades 24 @ Blazers 3   
Force 3 @ Stallions 20   
Maulers 28 @ VooDoo 9   
Steamer 32 @ Stars 26 (OT)   
Showboats 19 @ Bulls 16   
Federals 31 @ Hornets 0   
Panthers 20 @ Blitz 12   
Express 16 @ Sun 5   
SaberCats 18 @ Gold 40   
Thunderbolts 10 @ Wranglers 6   
Hawaiians 19 @ Wheels 0   
Outlaws 34 @ Gamblers 19   
Bandits 3 @ Gunslingers 34   
Storm 21 @ (NY) Stars 25   
Breakers 9 @ Generals 37   
Invaders 9 @ Bell 13   
Week 15
Bell 40 @ Breakers 28   
Blazers 3 @ Bandits 27   
Renegades 24 @ Steamer 0   
Force 6 @ Stars 36   
Wranglers 13 @ Sun 3   
Showboats 20 @ Outlaws 6   
Hawaiians 50 @ Storm 7   
Thunderbolts 41 @ VooDoo 9   
Panthers 16 @ Invaders 20   
Gamblers 0 @ Gunslingers 30   
Hornets 17 @ Maulers 38   
Gold 34 @ Generals 15   
(NY) Stars 21 @ Bulls 16   
Federals 0 @ SaberCats 52   
Stallions 6 @ Wheels 13   
Blitz 13 @ Express 30   
Week 16
Stallions 14 @ VooDoo 10   
Federals 53 @ Force 7   
Blazers 3 @ Showboats 41   
Blitz 6 @ Panthers 38   
Bulls 23 @ Renegades 20   
Hornets 6 @ Steamer 28   
Stars 12 @ Maulers 30   
Sun 19 @ SaberCats 22   
Wranglers 9 @ Gold 39   
Thunderbolts 10 @ Hawaiians 24   
Wheels 9 @ Gamblers 32   
Gunslingers 30 @ Outlaws 13   
(NY) Stars 9 @ Bandits 7   
Breakers 16 @ Storm 3   
Generals 30 @ Bell 9   
Invaders 23 @ Express 25   
"""

print(parse_scores(s))