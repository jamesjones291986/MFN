
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
Cincinnati Defenders 25 @ Titans 7   
Texas Hold'em 0 @ Michigan Wolverines 13   
Philadelphia Slayers 44 @ Brooklyn Hitmen 6   
Washington Warriors 10 @ Providence Islanders 33   
Seattle Barbarians 7 @ Vegas Black Aces 32   
Oakland Outlaws 31 @ Los Angeles Challengers 21   
Indiana Fog 32 @ New York Empire 14   
Buffalo Skull Crushers 14 @ Houston Roughnecks 12   
Dakota Blizzard 21 @ Daytona Beach Bull Sharks 3   
KC Chaos 20 @ Vancouver Vandals 34   
New England Crusaders 6 @ Montana Grizzlies 14   
Carolina Cobras 3 @ Atlanta Dominators 41   
Saint Paul Punishers 9 @ Zecken 23   
Miami Nemesis 3 @ Pittsburgh Blitzkrieg 31   
Gem City Gangsters 28 @ Tampa Bay Fireballs 6   
Memphis Maniacs 35 @ Arizona Wranglers 13   
Week 2
New York Empire 7 @ Miami Nemesis 8   
Vancouver Vandals 20 @ Indiana Fog 17 (OT)   
Arizona Wranglers 19 @ Los Angeles Challengers 10   
Providence Islanders 36 @ Daytona Beach Bull Sharks 9   
Pittsburgh Blitzkrieg 27 @ Michigan Wolverines 10   
Zecken 7 @ Atlanta Dominators 41   
Gem City Gangsters 13 @ Saint Paul Punishers 6   
Washington Warriors 7 @ Philadelphia Slayers 38   
Brooklyn Hitmen 3 @ Dakota Blizzard 17   
Houston Roughnecks 6 @ Titans 7   
New England Crusaders 6 @ Texas Hold'em 24   
KC Chaos 10 @ Buffalo Skull Crushers 16   
Oakland Outlaws 46 @ Vegas Black Aces 14   
Tampa Bay Fireballs 13 @ Montana Grizzlies 7   
Memphis Maniacs 29 @ Cincinnati Defenders 12   
Carolina Cobras 13 @ Seattle Barbarians 9   
Week 3
Memphis Maniacs 49 @ Tampa Bay Fireballs 12   
Atlanta Dominators 24 @ Carolina Cobras 3   
Titans 16 @ Pittsburgh Blitzkrieg 14   
Saint Paul Punishers 9 @ Montana Grizzlies 20   
Gem City Gangsters 34 @ New York Empire 13   
Zecken 12 @ New England Crusaders 7   
Oakland Outlaws 25 @ Miami Nemesis 0   
Buffalo Skull Crushers 9 @ Indiana Fog 21   
Daytona Beach Bull Sharks 0 @ Texas Hold'em 19   
Michigan Wolverines 32 @ Brooklyn Hitmen 15   
KC Chaos 7 @ Cincinnati Defenders 18   
Dakota Blizzard 14 @ Houston Roughnecks 9   
Washington Warriors 21 @ Los Angeles Challengers 6   
Vegas Black Aces 15 @ Vancouver Vandals 20   
Arizona Wranglers 49 @ Seattle Barbarians 3   
Providence Islanders 20 @ Philadelphia Slayers 33   
Week 4
Zecken 13 @ Montana Grizzlies 20   
Vegas Black Aces 10 @ Atlanta Dominators 27   
Memphis Maniacs 30 @ Carolina Cobras 10   
Tampa Bay Fireballs 17 @ Houston Roughnecks 37   
Titans 7 @ Cincinnati Defenders 14   
New England Crusaders 27 @ New York Empire 6   
Michigan Wolverines 13 @ Daytona Beach Bull Sharks 12   
Washington Warriors 13 @ Texas Hold'em 17   
Pittsburgh Blitzkrieg 24 @ Indiana Fog 17   
Providence Islanders 9 @ Arizona Wranglers 28   
Dakota Blizzard 12 @ Philadelphia Slayers 34   
Seattle Barbarians 12 @ Los Angeles Challengers 6   
Brooklyn Hitmen 10 @ Saint Paul Punishers 16   
Miami Nemesis 10 @ Gem City Gangsters 22   
Buffalo Skull Crushers 17 @ Vancouver Vandals 35   
KC Chaos 9 @ Oakland Outlaws 31   
Week 5
Miami Nemesis 23 @ Buffalo Skull Crushers 20   
Oakland Outlaws 23 @ Indiana Fog 24   
Montana Grizzlies 0 @ Memphis Maniacs 41   
Pittsburgh Blitzkrieg 22 @ Carolina Cobras 13   
Michigan Wolverines 24 @ Titans 19   
Brooklyn Hitmen 0 @ Philadelphia Slayers 43   
Vegas Black Aces 10 @ Providence Islanders 28   
Vancouver Vandals 43 @ Seattle Barbarians 3   
Arizona Wranglers 31 @ Gem City Gangsters 28   
New York Empire 10 @ KC Chaos 38   
Texas Hold'em 7 @ Cincinnati Defenders 20   
Daytona Beach Bull Sharks 8 @ Dakota Blizzard 31   
Atlanta Dominators 30 @ Houston Roughnecks 10   
Los Angeles Challengers 6 @ Tampa Bay Fireballs 17   
Zecken 13 @ Washington Warriors 16   
New England Crusaders 12 @ Saint Paul Punishers 6   
Week 6
Arizona Wranglers 26 @ Oakland Outlaws 18   
Philadelphia Slayers 14 @ Memphis Maniacs 44   
Seattle Barbarians 6 @ Washington Warriors 16   
Los Angeles Challengers 10 @ Vegas Black Aces 20   
Tampa Bay Fireballs 12 @ Carolina Cobras 7   
Saint Paul Punishers 16 @ Miami Nemesis 13 (OT)   
Indiana Fog 27 @ New England Crusaders 3   
Michigan Wolverines 10 @ Texas Hold'em 15   
Brooklyn Hitmen 3 @ Providence Islanders 38   
Vancouver Vandals 31 @ KC Chaos 28 (OT)   
Gem City Gangsters 17 @ Atlanta Dominators 24   
Cincinnati Defenders 17 @ Houston Roughnecks 20   
Titans 30 @ Daytona Beach Bull Sharks 8   
Dakota Blizzard 22 @ Pittsburgh Blitzkrieg 20   
Buffalo Skull Crushers 17 @ Zecken 13   
New York Empire 10 @ Montana Grizzlies 20   
Week 7
Indiana Fog 10 @ Vancouver Vandals 19   
Miami Nemesis 27 @ New York Empire 16   
Los Angeles Challengers 3 @ Providence Islanders 24   
Daytona Beach Bull Sharks 3 @ Michigan Wolverines 16   
Atlanta Dominators 30 @ Pittsburgh Blitzkrieg 6   
Zecken 17 @ Saint Paul Punishers 24   
Gem City Gangsters 17 @ Philadelphia Slayers 14   
Washington Warriors 13 @ Brooklyn Hitmen 3   
Titans 15 @ Dakota Blizzard 19   
Houston Roughnecks 31 @ Texas Hold'em 3   
New England Crusaders 0 @ Buffalo Skull Crushers 17   
Oakland Outlaws 26 @ KC Chaos 7   
Montana Grizzlies 3 @ Vegas Black Aces 25   
Cincinnati Defenders 21 @ Tampa Bay Fireballs 20   
Carolina Cobras 3 @ Memphis Maniacs 54   
Seattle Barbarians 3 @ Arizona Wranglers 52   
Week 8
Houston Roughnecks 9 @ Memphis Maniacs 26   
Carolina Cobras 23 @ Cincinnati Defenders 25   
Tampa Bay Fireballs 10 @ Atlanta Dominators 36   
Philadelphia Slayers 37 @ Los Angeles Challengers 3   
Brooklyn Hitmen 17 @ Seattle Barbarians 14   
Pittsburgh Blitzkrieg 21 @ Texas Hold'em 6   
Titans 13 @ New England Crusaders 7   
Oakland Outlaws 26 @ Buffalo Skull Crushers 22   
Miami Nemesis 15 @ Vancouver Vandals 29   
Indiana Fog 15 @ Arizona Wranglers 30   
Daytona Beach Bull Sharks 3 @ Washington Warriors 6 (OT)   
Providence Islanders 13 @ Dakota Blizzard 25   
Montana Grizzlies 6 @ Zecken 3 (OT)   
Saint Paul Punishers 3 @ Gem City Gangsters 31   
New York Empire 7 @ Michigan Wolverines 22   
KC Chaos 24 @ Vegas Black Aces 3   
Week 9
Saint Paul Punishers 13 @ Carolina Cobras 19   
Los Angeles Challengers 7 @ Seattle Barbarians 33   
Tampa Bay Fireballs 24 @ Brooklyn Hitmen 51   
Arizona Wranglers 24 @ Vegas Black Aces 9   
Pittsburgh Blitzkrieg 6 @ Houston Roughnecks 28   
Montana Grizzlies 17 @ Buffalo Skull Crushers 24   
Texas Hold'em 3 @ Dakota Blizzard 17   
Philadelphia Slayers 16 @ Washington Warriors 13   
Memphis Maniacs 37 @ Atlanta Dominators 40 (OT)   
Gem City Gangsters 11 @ Zecken 14   
Oakland Outlaws 3 @ Titans 22   
Michigan Wolverines 10 @ Providence Islanders 27   
KC Chaos 7 @ Indiana Fog 10   
Vancouver Vandals 26 @ New England Crusaders 15   
Cincinnati Defenders 24 @ New York Empire 12   
Daytona Beach Bull Sharks 6 @ Miami Nemesis 32   
Week 10
Montana Grizzlies 17 @ Saint Paul Punishers 10   
Michigan Wolverines 22 @ Dakota Blizzard 8   
Seattle Barbarians 3 @ KC Chaos 20   
Pittsburgh Blitzkrieg 23 @ Cincinnati Defenders 11   
Atlanta Dominators 14 @ Providence Islanders 12   
Gem City Gangsters 31 @ New England Crusaders 12   
Zecken 9 @ Tampa Bay Fireballs 10   
Houston Roughnecks 57 @ Carolina Cobras 14   
Memphis Maniacs 37 @ Titans 16   
Buffalo Skull Crushers 22 @ New York Empire 7   
Miami Nemesis 23 @ Indiana Fog 20   
Brooklyn Hitmen 10 @ Washington Warriors 16   
Daytona Beach Bull Sharks 0 @ Philadelphia Slayers 33   
Texas Hold'em 6 @ Oakland Outlaws 19   
Vancouver Vandals 17 @ Arizona Wranglers 31   
Vegas Black Aces 9 @ Los Angeles Challengers 0   
Week 11
Pittsburgh Blitzkrieg 27 @ Memphis Maniacs 34   
Carolina Cobras 20 @ Titans 17   
Atlanta Dominators 41 @ Tampa Bay Fireballs 7   
Providence Islanders 23 @ Montana Grizzlies 10   
New York Empire 20 @ Saint Paul Punishers 6   
Zecken 7 @ Gem City Gangsters 23   
New England Crusaders 14 @ Oakland Outlaws 24   
Buffalo Skull Crushers 17 @ Miami Nemesis 15   
Indiana Fog 9 @ Daytona Beach Bull Sharks 14   
Texas Hold'em 17 @ Brooklyn Hitmen 24   
Michigan Wolverines 13 @ KC Chaos 17   
Houston Roughnecks 15 @ Cincinnati Defenders 3   
Dakota Blizzard 58 @ Washington Warriors 3   
Seattle Barbarians 6 @ Philadelphia Slayers 38   
Vegas Black Aces 6 @ Arizona Wranglers 70   
Los Angeles Challengers 3 @ Vancouver Vandals 22   
Week 12
Los Angeles Challengers 13 @ Brooklyn Hitmen 17   
Arizona Wranglers 41 @ KC Chaos 14   
Oakland Outlaws 30 @ Vancouver Vandals 37   
Saint Paul Punishers 6 @ Memphis Maniacs 80   
Indiana Fog 22 @ Seattle Barbarians 0   
New England Crusaders 6 @ Miami Nemesis 18   
Philadelphia Slayers 34 @ Vegas Black Aces 13   
Carolina Cobras 27 @ Tampa Bay Fireballs 20   
Texas Hold'em 3 @ Providence Islanders 27   
Washington Warriors 17 @ Michigan Wolverines 26   
Cincinnati Defenders 6 @ Atlanta Dominators 27   
Titans 6 @ Houston Roughnecks 16   
Daytona Beach Bull Sharks 0 @ Pittsburgh Blitzkrieg 41   
Dakota Blizzard 28 @ Buffalo Skull Crushers 34   
Zecken 25 @ New York Empire 7   
Gem City Gangsters 19 @ Montana Grizzlies 17   
Week 13
Saint Paul Punishers 10 @ Los Angeles Challengers 3   
Arizona Wranglers 24 @ Washington Warriors 6   
Providence Islanders 23 @ Seattle Barbarians 3   
Philadelphia Slayers 20 @ Texas Hold'em 6   
Brooklyn Hitmen 18 @ Daytona Beach Bull Sharks 12   
Dakota Blizzard 14 @ Michigan Wolverines 33   
Houston Roughnecks 30 @ Vancouver Vandals 3   
Vegas Black Aces 27 @ Indiana Fog 10   
Buffalo Skull Crushers 22 @ New England Crusaders 20   
Memphis Maniacs 9 @ Zecken 16   
Cincinnati Defenders 11 @ Pittsburgh Blitzkrieg 28   
KC Chaos 38 @ Miami Nemesis 10   
New York Empire 13 @ Oakland Outlaws 31   
Carolina Cobras 0 @ Gem City Gangsters 30   
Titans 7 @ Tampa Bay Fireballs 3   
Atlanta Dominators 44 @ Montana Grizzlies 3   
Week 14
Titans 3 @ Atlanta Dominators 44   
Houston Roughnecks 38 @ Pittsburgh Blitzkrieg 43   
Tampa Bay Fireballs 2 @ Memphis Maniacs 33   
Montana Grizzlies 13 @ Gem City Gangsters 30   
Saint Paul Punishers 13 @ Buffalo Skull Crushers 66   
Dakota Blizzard 36 @ Texas Hold'em 12   
Philadelphia Slayers 24 @ Michigan Wolverines 10   
Providence Islanders 22 @ Washington Warriors 19   
Brooklyn Hitmen 0 @ Arizona Wranglers 48   
KC Chaos 17 @ Los Angeles Challengers 3   
Indiana Fog 19 @ Oakland Outlaws 17   
Vegas Black Aces 16 @ Seattle Barbarians 13   
Carolina Cobras 15 @ Zecken 6   
Miami Nemesis 3 @ New England Crusaders 12   
Vancouver Vandals 40 @ New York Empire 14   
Cincinnati Defenders 15 @ Daytona Beach Bull Sharks 20   
Week 15
Texas Hold'em 6 @ Titans 13   
Michigan Wolverines 30 @ Cincinnati Defenders 41   
Arizona Wranglers 21 @ Philadelphia Slayers 9   
Providence Islanders 52 @ Brooklyn Hitmen 6   
Washington Warriors 3 @ Vegas Black Aces 16   
Seattle Barbarians 0 @ Oakland Outlaws 30   
Los Angeles Challengers 22 @ Indiana Fog 37   
New York Empire 3 @ Buffalo Skull Crushers 73   
Daytona Beach Bull Sharks 3 @ Houston Roughnecks 25   
Vancouver Vandals 31 @ Dakota Blizzard 28   
New England Crusaders 7 @ KC Chaos 27   
Montana Grizzlies 6 @ Carolina Cobras 3   
Atlanta Dominators 79 @ Saint Paul Punishers 6   
Miami Nemesis 22 @ Zecken 31   
Tampa Bay Fireballs 13 @ Pittsburgh Blitzkrieg 30   
Memphis Maniacs 23 @ Gem City Gangsters 34   
Week 16
Cincinnati Defenders 22 @ Dakota Blizzard 21   
Philadelphia Slayers 9 @ Providence Islanders 2   
Los Angeles Challengers 3 @ Arizona Wranglers 38   
Indiana Fog 33 @ KC Chaos 7   
Vegas Black Aces 27 @ Brooklyn Hitmen 10   
Seattle Barbarians 0 @ Zecken 23   
Montana Grizzlies 3 @ Miami Nemesis 20   
Vancouver Vandals 7 @ Oakland Outlaws 12   
Buffalo Skull Crushers 20 @ Gem City Gangsters 34   
Tampa Bay Fireballs 20 @ Saint Paul Punishers 6   
Atlanta Dominators 25 @ Memphis Maniacs 16   
Washington Warriors 33 @ Carolina Cobras 7   
Texas Hold'em 25 @ Daytona Beach Bull Sharks 3   
Pittsburgh Blitzkrieg 7 @ Titans 31   
New York Empire 18 @ New England Crusaders 24   
Houston Roughnecks 10 @ Michigan Wolverines 24  """

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
