
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
New England Patriots 12 @ Green Bay Packers 27   
Chicago Bears 10 @ Minnesota Vikings 20   
Denver Broncos 6 @ San Francisco 49ers 0   
Carolina Panthers 29 @ Los Angeles Rams 13   
Arizona Cardinals 16 @ Tampa Bay Buccaneers 12   
Seattle Seahawks 0 @ Atlanta Falcons 14   
Saints 0 @ Cincinnati Bengals 13   
Indianapolis Colts 6 @ Tennessee Titans 27   
Buffalo Bills 13 @ New York Jets 19   
Cleveland Browns 10 @ San Diego Chargers 13   
Pittsburgh Steelers 17 @ Baltimore Ravens 3   
Oakland Raiders 17 @ Kansas City Chiefs 21   
Houston Texans 7 @ Jacksonville Jaguars 23   
Dallas Cowboys 10 @ New York Giants 19   
Philadelphia Eagles 14 @ Washington Redskins 17   
Miami Dolphins 44 @ Detroit Lions 17   
Week 2
Houston Texans 7 @ Tennessee Titans 65   
New England Patriots 13 @ Indianapolis Colts 13 (OT)   
Baltimore Ravens 10 @ Cleveland Browns 30   
Oakland Raiders 10 @ Denver Broncos 20   
Kansas City Chiefs 0 @ Arizona Cardinals 33   
Philadelphia Eagles 3 @ Seattle Seahawks 20   
Jacksonville Jaguars 24 @ New York Giants 17   
Miami Dolphins 17 @ New York Jets 3   
Detroit Lions 11 @ Minnesota Vikings 9   
Washington Redskins 7 @ Dallas Cowboys 22   
Green Bay Packers 19 @ Buffalo Bills 30   
San Diego Chargers 39 @ San Francisco 49ers 0   
Atlanta Falcons 3 @ Los Angeles Rams 10   
Carolina Panthers 17 @ Saints 7   
Cincinnati Bengals 27 @ Pittsburgh Steelers 24 (OT)   
Chicago Bears 6 @ Tampa Bay Buccaneers 25   
Week 3
Chicago Bears 3 @ Philadelphia Eagles 30   
Jacksonville Jaguars 13 @ Washington Redskins 3   
Houston Texans 10 @ Indianapolis Colts 15   
San Diego Chargers 17 @ Denver Broncos 0   
Cincinnati Bengals 24 @ Oakland Raiders 17   
Seattle Seahawks 26 @ Kansas City Chiefs 33   
Atlanta Falcons 0 @ Cleveland Browns 2   
Saints 23 @ Tampa Bay Buccaneers 24   
Los Angeles Rams 9 @ Arizona Cardinals 38   
Dallas Cowboys 6 @ San Francisco 49ers 14   
Tennessee Titans 31 @ New York Giants 8   
Detroit Lions 19 @ New York Jets 7   
New England Patriots 17 @ Buffalo Bills 13   
Baltimore Ravens 10 @ Carolina Panthers 13   
Pittsburgh Steelers 0 @ Miami Dolphins 19   
Minnesota Vikings 17 @ Green Bay Packers 9   
Week 4
Los Angeles Rams 6 @ Seattle Seahawks 10   
Tampa Bay Buccaneers 17 @ Philadelphia Eagles 13   
Oakland Raiders 11 @ New England Patriots 31   
Tennessee Titans 45 @ Washington Redskins 9   
Baltimore Ravens 11 @ Jacksonville Jaguars 19   
San Francisco 49ers 7 @ Arizona Cardinals 51   
Denver Broncos 0 @ Houston Texans 16   
New York Jets 7 @ Buffalo Bills 13   
Green Bay Packers 7 @ Miami Dolphins 52   
Minnesota Vikings 27 @ New York Giants 20   
Chicago Bears 3 @ Detroit Lions 21   
Indianapolis Colts 10 @ Dallas Cowboys 31   
San Diego Chargers 37 @ Cincinnati Bengals 23   
Kansas City Chiefs 3 @ Cleveland Browns 26   
Carolina Panthers 24 @ Pittsburgh Steelers 6   
Saints 16 @ Atlanta Falcons 9   
Week 5
Jacksonville Jaguars 6 @ Tennessee Titans 27   
Washington Redskins 0 @ Philadelphia Eagles 16   
New England Patriots 10 @ Baltimore Ravens 21   
Los Angeles Rams 9 @ Tampa Bay Buccaneers 10   
Seattle Seahawks 7 @ Oakland Raiders 12   
Saints 10 @ San Francisco 49ers 15   
Arizona Cardinals 24 @ Denver Broncos 20   
Houston Texans 6 @ Buffalo Bills 21   
New York Jets 8 @ Miami Dolphins 20   
Green Bay Packers 7 @ Minnesota Vikings 30   
New York Giants 21 @ Chicago Bears 16   
Detroit Lions 10 @ Dallas Cowboys 27   
San Diego Chargers 34 @ Indianapolis Colts 10   
Cincinnati Bengals 38 @ Kansas City Chiefs 29   
Cleveland Browns 13 @ Pittsburgh Steelers 13 (OT)   
Atlanta Falcons 10 @ Carolina Panthers 31   
Week 6
Tennessee Titans 46 @ Houston Texans 10   
Chicago Bears 12 @ New England Patriots 16   
Indianapolis Colts 16 @ Cleveland Browns 6   
Baltimore Ravens 20 @ Oakland Raiders 17   
Kansas City Chiefs 17 @ Denver Broncos 10   
Philadelphia Eagles 6 @ New York Giants 28   
Jacksonville Jaguars 9 @ New York Jets 40   
Minnesota Vikings 3 @ Miami Dolphins 30   
Washington Redskins 6 @ Detroit Lions 17   
Dallas Cowboys 15 @ Green Bay Packers 0   
Buffalo Bills 0 @ San Diego Chargers 41   
Cincinnati Bengals 16 @ Carolina Panthers 31   
Pittsburgh Steelers 9 @ Tampa Bay Buccaneers 31   
San Francisco 49ers 13 @ Los Angeles Rams 6   
Saints 3 @ Seattle Seahawks 9   
Atlanta Falcons 19 @ Arizona Cardinals 33   
Week 7
Denver Broncos 0 @ San Diego Chargers 28   
Cincinnati Bengals 36 @ Baltimore Ravens 10   
San Francisco 49ers 6 @ Carolina Panthers 24   
Oakland Raiders 10 @ Arizona Cardinals 29   
Kansas City Chiefs 14 @ Pittsburgh Steelers 10   
Seattle Seahawks 20 @ Los Angeles Rams 0   
Atlanta Falcons 3 @ Tampa Bay Buccaneers 33   
Cleveland Browns 10 @ Saints 6   
Detroit Lions 27 @ Green Bay Packers 3   
Buffalo Bills 24 @ Chicago Bears 34   
Minnesota Vikings 14 @ Washington Redskins 3   
New York Jets 19 @ Houston Texans 19 (OT)   
Tennessee Titans 13 @ New England Patriots 6   
Miami Dolphins 39 @ Jacksonville Jaguars 7   
New York Giants 6 @ Indianapolis Colts 13   
Dallas Cowboys 20 @ Philadelphia Eagles 3   
Week 8
Minnesota Vikings 34 @ Detroit Lions 31 (OT)   
Tampa Bay Buccaneers 6 @ Carolina Panthers 32   
Seattle Seahawks 6 @ Chicago Bears 3   
New York Giants 20 @ Washington Redskins 24   
Arizona Cardinals 32 @ Saints 0   
Houston Texans 13 @ Dallas Cowboys 23   
Cleveland Browns 14 @ Buffalo Bills 13   
Cincinnati Bengals 30 @ Atlanta Falcons 6   
Philadelphia Eagles 6 @ Green Bay Packers 23   
Jacksonville Jaguars 24 @ Indianapolis Colts 13   
San Francisco 49ers 13 @ Oakland Raiders 10   
Los Angeles Rams 0 @ San Diego Chargers 36   
Baltimore Ravens 24 @ Pittsburgh Steelers 7   
Denver Broncos 6 @ Kansas City Chiefs 9 (OT)   
New England Patriots 6 @ Miami Dolphins 49   
Tennessee Titans 9 @ New York Jets 12   
Week 9
New England Patriots 20 @ New York Jets 38   
Denver Broncos 6 @ Seattle Seahawks 3   
Miami Dolphins 44 @ Buffalo Bills 17   
Atlanta Falcons 12 @ Saints 10   
Baltimore Ravens 3 @ Cincinnati Bengals 23   
Houston Texans 9 @ Pittsburgh Steelers 20   
Arizona Cardinals 23 @ New York Giants 9   
Tennessee Titans 23 @ Indianapolis Colts 9   
Tampa Bay Buccaneers 7 @ San Francisco 49ers 3   
Washington Redskins 13 @ Chicago Bears 23   
Green Bay Packers 6 @ Detroit Lions 34   
Dallas Cowboys 3 @ Minnesota Vikings 30   
Philadelphia Eagles 12 @ Jacksonville Jaguars 11   
San Diego Chargers 31 @ Oakland Raiders 3   
Kansas City Chiefs 28 @ Los Angeles Rams 20   
Carolina Panthers 20 @ Cleveland Browns 13   
Week 10
Washington Redskins 10 @ Indianapolis Colts 23   
Houston Texans 9 @ Philadelphia Eagles 11   
Dallas Cowboys 12 @ Jacksonville Jaguars 0   
Miami Dolphins 29 @ New England Patriots 10   
Buffalo Bills 3 @ Tennessee Titans 34   
Cleveland Browns 18 @ Cincinnati Bengals 27   
New York Jets 13 @ Minnesota Vikings 16   
Arizona Cardinals 28 @ San Diego Chargers 24   
Kansas City Chiefs 20 @ Oakland Raiders 13   
Seattle Seahawks 3 @ San Francisco 49ers 9   
Tampa Bay Buccaneers 13 @ Baltimore Ravens 7   
Detroit Lions 28 @ Saints 7   
New York Giants 17 @ Carolina Panthers 31   
Atlanta Falcons 0 @ Pittsburgh Steelers 16   
Los Angeles Rams 7 @ Denver Broncos 24   
Chicago Bears 6 @ Green Bay Packers 10   
Week 11
New York Jets 29 @ Green Bay Packers 13   
New York Giants 20 @ Houston Texans 13   
Oakland Raiders 24 @ Los Angeles Rams 16   
Kansas City Chiefs 3 @ San Diego Chargers 44   
Arizona Cardinals 23 @ San Francisco 49ers 9   
Miami Dolphins 34 @ Chicago Bears 6   
Philadelphia Eagles 3 @ Minnesota Vikings 0   
Detroit Lions 15 @ New England Patriots 14   
Seattle Seahawks 7 @ Carolina Panthers 27   
Washington Redskins 23 @ Atlanta Falcons 3   
Indianapolis Colts 22 @ Buffalo Bills 16   
Pittsburgh Steelers 13 @ Cleveland Browns 23   
Denver Broncos 12 @ Baltimore Ravens 3   
Saints 7 @ Dallas Cowboys 19   
Tennessee Titans 30 @ Jacksonville Jaguars 8   
Tampa Bay Buccaneers 28 @ Cincinnati Bengals 14   
Week 12
Saints 3 @ Carolina Panthers 31   
Seattle Seahawks 9 @ Arizona Cardinals 28   
New York Giants 16 @ Dallas Cowboys 17   
Minnesota Vikings 13 @ Chicago Bears 20   
Cleveland Browns 25 @ Tampa Bay Buccaneers 7   
Buffalo Bills 3 @ Detroit Lions 7   
Washington Redskins 22 @ Houston Texans 7   
Atlanta Falcons 10 @ Green Bay Packers 7   
Indianapolis Colts 21 @ Philadelphia Eagles 0   
Jacksonville Jaguars 0 @ Oakland Raiders 14   
Los Angeles Rams 3 @ San Francisco 49ers 23   
Pittsburgh Steelers 10 @ San Diego Chargers 31   
Baltimore Ravens 10 @ Kansas City Chiefs 3   
Miami Dolphins 25 @ Denver Broncos 0   
New York Jets 24 @ New England Patriots 9   
Cincinnati Bengals 14 @ Tennessee Titans 28   
Week 13
Dallas Cowboys 9 @ Washington Redskins 26   
Indianapolis Colts 17 @ Jacksonville Jaguars 24   
Houston Texans 3 @ Miami Dolphins 30   
Cincinnati Bengals 16 @ Cleveland Browns 22   
Buffalo Bills 17 @ New England Patriots 20 (OT)   
Philadelphia Eagles 6 @ Tennessee Titans 68   
Minnesota Vikings 7 @ Arizona Cardinals 35   
Oakland Raiders 3 @ San Diego Chargers 34   
San Francisco 49ers 14 @ Kansas City Chiefs 3   
Tampa Bay Buccaneers 13 @ Seattle Seahawks 6   
Saints 3 @ Baltimore Ravens 13   
New York Giants 34 @ Detroit Lions 27   
Carolina Panthers 13 @ Atlanta Falcons 7   
Pittsburgh Steelers 13 @ Denver Broncos 6   
Green Bay Packers 6 @ Los Angeles Rams 21   
Chicago Bears 13 @ New York Jets 17   
Week 14
Detroit Lions 26 @ Philadelphia Eagles 3   
Pittsburgh Steelers 0 @ Cincinnati Bengals 3   
Carolina Panthers 25 @ Tampa Bay Buccaneers 7   
Washington Redskins 28 @ New York Giants 13   
Buffalo Bills 3 @ Miami Dolphins 48   
Jacksonville Jaguars 0 @ Houston Texans 19   
Denver Broncos 24 @ Oakland Raiders 3   
Green Bay Packers 0 @ Chicago Bears 3   
New York Jets 10 @ Indianapolis Colts 27   
New England Patriots 13 @ Minnesota Vikings 34   
San Diego Chargers 29 @ Kansas City Chiefs 14   
Cleveland Browns 24 @ Baltimore Ravens 16   
Dallas Cowboys 13 @ Tennessee Titans 14   
Los Angeles Rams 26 @ Saints 3   
Arizona Cardinals 10 @ Seattle Seahawks 13   
San Francisco 49ers 19 @ Atlanta Falcons 0   
Week 15
Indianapolis Colts 6 @ Miami Dolphins 30   
New England Patriots 13 @ Houston Texans 2   
New York Giants 28 @ Philadelphia Eagles 34   
San Francisco 49ers 14 @ Detroit Lions 7   
Tennessee Titans 43 @ Kansas City Chiefs 3   
Buffalo Bills 16 @ Jacksonville Jaguars 23   
Chicago Bears 3 @ Dallas Cowboys 14   
New York Jets 17 @ Cincinnati Bengals 23   
Cleveland Browns 3 @ Denver Broncos 9   
Oakland Raiders 9 @ Pittsburgh Steelers 24   
San Diego Chargers 34 @ Seattle Seahawks 0   
Tampa Bay Buccaneers 24 @ Saints 10   
Baltimore Ravens 13 @ Atlanta Falcons 6   
Carolina Panthers 18 @ Minnesota Vikings 6   
Arizona Cardinals 17 @ Los Angeles Rams 20   
Green Bay Packers 0 @ Washington Redskins 10   
Week 16
Indianapolis Colts 21 @ Houston Texans 9   
Los Angeles Rams 0 @ Washington Redskins 34   
Minnesota Vikings 14 @ Buffalo Bills 30   
Jacksonville Jaguars 14 @ New England Patriots 3   
Philadelphia Eagles 16 @ Dallas Cowboys 34   
Oakland Raiders 3 @ Cleveland Browns 18   
Miami Dolphins 20 @ Tennessee Titans 23 (OT)   
San Francisco 49ers 20 @ Seattle Seahawks 9   
Kansas City Chiefs 7 @ New York Jets 20   
Denver Broncos 6 @ Cincinnati Bengals 15   
Pittsburgh Steelers 34 @ Saints 8   
Detroit Lions 27 @ Chicago Bears 24   
Green Bay Packers 3 @ New York Giants 6   
Carolina Panthers 24 @ Arizona Cardinals 7   
San Diego Chargers 19 @ Baltimore Ravens 0   
Tampa Bay Buccaneers 35 @ Atlanta Falcons 10   
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
