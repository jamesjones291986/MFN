
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
Wheels 3 @ Steamer 23   
Panthers 20 @ Thunderbolts 6   
SaberCats 46 @ Storm 33   
Express 27 @ Sun 30 (OT)   
Maulers 24 @ Hawaiians 3   
Bell 13 @ Invaders 10   
Gunslingers 27 @ Showboats 9   
Bandits 7 @ Force 9   
VooDoo 9 @ Stallions 3   
Blazers 27 @ Bulls 13   
Renegades 0 @ Generals 3   
Wranglers 9 @ Gamblers 14   
Outlaws 16 @ Blitz 18   
Breakers 23 @ Gold 10   
Hornets 0 @ (NY) Stars 52   
Federals 36 @ Stars 10   
Week 2
Thunderbolts 13 @ Wheels 6   
Steamer 0 @ Panthers 21   
Storm 19 @ Sun 13   
Express 6 @ Hawaiians 10   
Maulers 24 @ Bell 53   
Invaders 6 @ Gunslingers 40   
Showboats 27 @ Bandits 10   
Force 10 @ VooDoo 16   
Stallions 13 @ Bulls 16   
Renegades 45 @ Blazers 19   
Wranglers 3 @ Generals 20   
Gamblers 35 @ Outlaws 21   
Gold 22 @ Blitz 6   
(NY) Stars 30 @ Breakers 3   
Federals 45 @ Hornets 9   
Stars 0 @ SaberCats 50   
Week 3
Federals 24 @ Maulers 25   
Express 7 @ Gold 10   
Invaders 10 @ Storm 5   
(NY) Stars 13 @ Generals 19   
Wheels 3 @ Panthers 7   
Thunderbolts 19 @ Showboats 32   
Breakers 14 @ Bell 41   
Sun 10 @ Wranglers 16   
SaberCats 38 @ Hornets 17   
Renegades 10 @ Outlaws 31   
Hawaiians 24 @ Stars 6   
Gamblers 19 @ Blazers 20   
Bulls 9 @ Bandits 13   
Force 10 @ Stallions 17   
Steamer 0 @ VooDoo 39   
Blitz 13 @ Gunslingers 34   
Week 4
Panthers 12 @ Gamblers 17   
Blitz 20 @ Thunderbolts 17   
Outlaws 28 @ Showboats 16   
Gunslingers 29 @ Wheels 6   
Blazers 12 @ Renegades 18 (OT)   
Bell 10 @ (NY) Stars 34   
Bandits 3 @ Hornets 24   
Bulls 24 @ VooDoo 31   
Force 9 @ Steamer 4   
Stallions 23 @ Stars 7   
Generals 21 @ Breakers 6   
Sun 9 @ Federals 37   
Storm 24 @ Gold 7   
Invaders 20 @ Wranglers 6   
Hawaiians 26 @ Express 0   
SaberCats 31 @ Maulers 22   
Week 5
Blazers 3 @ Outlaws 9   
Force 22 @ Renegades 14   
Bandits 9 @ VooDoo 35   
Gamblers 6 @ Gunslingers 25   
Breakers 7 @ Maulers 23   
Express 16 @ SaberCats 30   
Blitz 6 @ Wheels 23   
Hornets 0 @ Hawaiians 36   
Stallions 13 @ Panthers 17   
Showboats 31 @ Bulls 35   
Thunderbolts 0 @ Steamer 10   
Sun 16 @ Stars 13 (OT)   
(NY) Stars 7 @ Invaders 24   
Bell 6 @ Federals 16   
Wranglers 3 @ Gold 17   
Generals 14 @ Storm 24   
Week 6
(NY) Stars 3 @ Bell 9   
Generals 9 @ Maulers 26   
Stars 3 @ Breakers 13   
Federals 17 @ Express 16   
Sun 10 @ Invaders 12   
SaberCats 12 @ Gold 19   
Hawaiians 7 @ Wranglers 7 (OT)   
Outlaws 34 @ Storm 17   
Showboats 0 @ Gunslingers 44   
Wheels 3 @ Stallions 38   
Hornets 0 @ Force 18   
Bulls 17 @ Renegades 22   
Blazers 3 @ Steamer 17   
VooDoo 31 @ Thunderbolts 9   
Panthers 28 @ Blitz 21   
Bandits 13 @ Gamblers 16   
Week 7
Force 10 @ Wheels 12   
Hawaiians 20 @ Sun 13   
Bandits 7 @ Renegades 36   
Panthers 0 @ VooDoo 31   
Maulers 10 @ Federals 24   
Hornets 6 @ Stars 17   
Bell 34 @ Generals 13   
Gold 14 @ (NY) Stars 28   
Wranglers 3 @ Invaders 28   
SaberCats 38 @ Express 24   
Breakers 3 @ Storm 26   
Steamer 6 @ Blitz 21   
Gamblers 17 @ Showboats 10   
Gunslingers 16 @ Outlaws 17   
Thunderbolts 10 @ Stallions 35   
Bulls 45 @ Blazers 7   
Week 8
Breakers 17 @ Hornets 33   
Maulers 26 @ Stars 0   
Sun 17 @ Express 10   
Hawaiians 44 @ SaberCats 21   
Storm 20 @ Invaders 23   
(NY) Stars 23 @ Federals 26 (OT)   
Bell 27 @ Wranglers 22   
Generals 21 @ Gold 6   
Wheels 7 @ Outlaws 37   
Bulls 28 @ Force 9   
Steamer 8 @ Stallions 17   
Renegades 34 @ Showboats 30   
Thunderbolts 3 @ Panthers 27   
Blitz 3 @ VooDoo 27   
Blazers 6 @ Bandits 20   
Gunslingers 20 @ Gamblers 30   
Week 9
Sun 16 @ SaberCats 29   
Panthers 20 @ Wheels 9   
Wranglers 3 @ Express 12   
Hornets 6 @ Maulers 38   
Bell 58 @ Stars 3   
Gold 0 @ Storm 15   
Hawaiians 38 @ Thunderbolts 6   
Showboats 22 @ Gamblers 43   
Federals 27 @ Blazers 23   
Invaders 16 @ Generals 28   
Breakers 6 @ (NY) Stars 16   
Outlaws 24 @ Bandits 7   
Gunslingers 34 @ Renegades 29   
Steamer 17 @ Bulls 27   
VooDoo 21 @ Force 0   
Stallions 21 @ Blitz 16   
Week 10
Stars 2 @ Federals 48   
Generals 5 @ Hornets 3   
Gold 7 @ Bell 20   
(NY) Stars 10 @ Wranglers 16   
Breakers 6 @ Steamer 31   
Sun 13 @ Wheels 6   
Maulers 13 @ VooDoo 16 (OT)   
Bandits 13 @ Bulls 44   
Renegades 30 @ Stallions 35   
Gunslingers 35 @ Blazers 10   
Thunderbolts 10 @ Invaders 15   
Panthers 26 @ SaberCats 29   
Blitz 10 @ Force 16   
Outlaws 3 @ Gamblers 24   
Express 6 @ Showboats 23   
Storm 19 @ Hawaiians 24   
Week 11
Bulls 10 @ Gunslingers 30   
Wheels 9 @ Blitz 23   
Blazers 32 @ Breakers 3   
Showboats 0 @ Gold 23   
Thunderbolts 10 @ Outlaws 27   
Gamblers 40 @ Renegades 0   
Generals 13 @ Bell 35   
Hawaiians 16 @ Invaders 13   
Maulers 10 @ Sun 24   
Stars 9 @ Express 9 (OT)   
Hornets 0 @ Federals 30   
Force 8 @ (NY) Stars 18   
Stallions 21 @ Bandits 16   
VooDoo 21 @ Steamer 0   
Storm 26 @ Panthers 40   
Wranglers 15 @ SaberCats 28   
Week 12
Express 6 @ Maulers 37   
Gold 16 @ Invaders 31   
Storm 3 @ (NY) Stars 20   
Generals 15 @ Stallions 31   
Steamer 3 @ Bandits 20   
Force 13 @ Blazers 10 (OT)   
Bulls 17 @ Gamblers 16   
Panthers 17 @ Gunslingers 35   
Wheels 6 @ Thunderbolts 17   
Showboats 23 @ Blitz 14   
VooDoo 3 @ Bell 39   
Wranglers 34 @ Breakers 15   
Hornets 9 @ Sun 20   
SaberCats 25 @ Outlaws 23   
Stars 16 @ Renegades 23   
Hawaiians 22 @ Federals 17   
Week 13
SaberCats 46 @ Sun 13   
Wheels 10 @ Wranglers 16   
Express 13 @ Hornets 17   
Stars 7 @ Maulers 33   
Storm 16 @ Bell 22 (OT)   
Gold 13 @ Hawaiians 26   
Gamblers 50 @ Thunderbolts 10   
Blazers 7 @ Showboats 27   
Federals 19 @ Generals 13   
Invaders 12 @ Breakers 17   
(NY) Stars 9 @ Bandits 10   
Outlaws 12 @ Gunslingers 3   
Renegades 22 @ Bulls 31   
Steamer 9 @ Force 0   
Stallions 20 @ VooDoo 24   
Blitz 0 @ Panthers 32   
Week 14
Gamblers 44 @ Sun 22   
Gunslingers 20 @ Hawaiians 10   
Force 13 @ Thunderbolts 12   
Wheels 0 @ Showboats 27   
Outlaws 7 @ Panthers 15   
VooDoo 21 @ Renegades 9   
Bandits 17 @ Blazers 9   
Stallions 26 @ Steamer 14   
Breakers 10 @ Generals 17   
Maulers 35 @ Hornets 6   
Bell 9 @ Bulls 36   
Invaders 10 @ Gold 17   
Federals 33 @ SaberCats 75   
(NY) Stars 17 @ Stars 12   
Wranglers 20 @ Storm 23   
Blitz 17 @ Express 9   
Week 15
Gold 9 @ Wranglers 31   
Stars 0 @ Hornets 9   
Bell 26 @ Breakers 3   
Steamer 12 @ Federals 23   
Generals 37 @ (NY) Stars 17   
VooDoo 37 @ Wheels 0   
Bulls 16 @ Maulers 10   
Renegades 14 @ Bandits 7   
Blazers 20 @ Stallions 27   
Gunslingers 47 @ Thunderbolts 3   
Invaders 58 @ SaberCats 74   
Panthers 27 @ Force 18   
Blitz 6 @ Gamblers 23   
Showboats 10 @ Outlaws 28   
Express 3 @ Storm 22   
Sun 3 @ Hawaiians 18   
Week 16
Hornets 0 @ Bell 24   
Federals 43 @ Breakers 3   
Gold 18 @ Sun 10   
Invaders 20 @ Express 9   
Storm 0 @ Wranglers 16   
Stars 16 @ Generals 13 (OT)   
SaberCats 12 @ Hawaiians 3   
Maulers 34 @ (NY) Stars 16   
Outlaws 23 @ Bulls 34   
Stallions 3 @ Force 23   
Renegades 16 @ Steamer 2   
Showboats 22 @ Panthers 33   
Thunderbolts 0 @ Blitz 20   
VooDoo 22 @ Blazers 0   
Bandits 9 @ Gunslingers 26   
Gamblers 23 @ Wheels 10   
"""

print(parse_scores(s))