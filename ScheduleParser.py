
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

s = """BrooklynHitmen	3	PhiladelphiaSlayers	30
MontanaGrizzlies	16	IndianaFog	24
VegasBlackAces	27	SaintPaulPunishers	0
LosAngelesChallengers	17	DaytonaBeachBullSharks	20
ArizonaWranglers	28	TexasHold'em	27
TampaBayFireballs	10	NewEnglandCrusaders	17
AtlantaDominators	7	MemphisManiacs	22
CincinnatiDefenders	18	BuffaloSkullCrushers	36
Zecken	21	SeattleBarbarians	0
KCChaos	10	MichiganWolverines	34
GemCityGangsters	10	OaklandOutlaws	7
DakotaBlizzard	25	VancouverVandals	19
HoustonRoughnecks	17	WashingtonWarriors	6
ProvidenceIslanders	29	PittsburghBlitzkrieg	7
NewYorkEmpire	0	Titans	20
CarolinaCobras	23	MiamiNemesis	9
Titans	33	CincinnatiDefenders	2
IndianaFog	24	MichiganWolverines	15
ProvidenceIslanders	39	MontanaGrizzlies	7
GemCityGangsters	23	PhiladelphiaSlayers	29
MiamiNemesis	3	AtlantaDominators	17
TexasHold'em	10	DakotaBlizzard	15
VegasBlackAces	9	ArizonaWranglers	17
HoustonRoughnecks	19	NewYorkEmpire	0
PittsburghBlitzkrieg	24	WashingtonWarriors	3
BrooklynHitmen	23	SaintPaulPunishers	13
VancouverVandals	26	KCChaos	7
OaklandOutlaws	16	DaytonaBeachBullSharks	18
CarolinaCobras	7	SeattleBarbarians	30
BuffaloSkullCrushers	23	NewEnglandCrusaders	21
TampaBayFireballs	5	MemphisManiacs	38
LosAngelesChallengers	6	Zecken	22
DaytonaBeachBullSharks	14	MichiganWolverines	20
KCChaos	19	DakotaBlizzard	30
VancouverVandals	3	IndianaFog	9
SaintPaulPunishers	11	GemCityGangsters	23
ProvidenceIslanders	38	BrooklynHitmen	3
Zecken	3	VegasBlackAces	30
MontanaGrizzlies	19	LosAngelesChallengers	23
ArizonaWranglers	52	SeattleBarbarians	0
AtlantaDominators	38	CarolinaCobras	6
PittsburghBlitzkrieg	26	NewYorkEmpire	6
WashingtonWarriors	3	TampaBayFireballs	13
NewEnglandCrusaders	9	MemphisManiacs	43
MiamiNemesis	13	BuffaloSkullCrushers	64
PhiladelphiaSlayers	16	Titans	10
HoustonRoughnecks	13	CincinnatiDefenders	6
OaklandOutlaws	16	TexasHold'em	19
PhiladelphiaSlayers	7	CincinnatiDefenders	10
SeattleBarbarians	24	SaintPaulPunishers	21
Zecken	6	GemCityGangsters	24
OaklandOutlaws	6	MontanaGrizzlies	6
DaytonaBeachBullSharks	25	IndianaFog	6
DakotaBlizzard	8	ArizonaWranglers	26
MichiganWolverines	10	VancouverVandals	14
KCChaos	13	BuffaloSkullCrushers	33
BrooklynHitmen	6	MemphisManiacs	28
TampaBayFireballs	8	AtlantaDominators	37
TexasHold'em	7	NewEnglandCrusaders	22
LosAngelesChallengers	3	VegasBlackAces	53
MiamiNemesis	6	HoustonRoughnecks	48
WashingtonWarriors	0	ProvidenceIslanders	32
PittsburghBlitzkrieg	12	Titans	12
NewYorkEmpire	6	CarolinaCobras	23
CincinnatiDefenders	9	PittsburghBlitzkrieg	32
WashingtonWarriors	22	BrooklynHitmen	13
AtlantaDominators	14	ProvidenceIslanders	17
VegasBlackAces	18	SeattleBarbarians	10
SaintPaulPunishers	7	CarolinaCobras	26
BuffaloSkullCrushers	62	MiamiNemesis	27
NewEnglandCrusaders	27	NewYorkEmpire	24
VancouverVandals	9	Titans	13
TexasHold'em	17	KCChaos	7
ArizonaWranglers	24	LosAngelesChallengers	3
TampaBayFireballs	9	Zecken	3
MemphisManiacs	28	PhiladelphiaSlayers	45
DakotaBlizzard	3	HoustonRoughnecks	7
MichiganWolverines	10	DaytonaBeachBullSharks	6
IndianaFog	13	OaklandOutlaws	14
MontanaGrizzlies	16	GemCityGangsters	21
WashingtonWarriors	0	AtlantaDominators	38
ProvidenceIslanders	0	MemphisManiacs	22
CarolinaCobras	6	PhiladelphiaSlayers	35
TampaBayFireballs	19	BrooklynHitmen	0
MichiganWolverines	6	DakotaBlizzard	33
VegasBlackAces	30	LosAngelesChallengers	3
Zecken	20	SaintPaulPunishers	12
SeattleBarbarians	14	MontanaGrizzlies	17
ArizonaWranglers	26	DaytonaBeachBullSharks	14
VancouverVandals	20	TexasHold'em	3
NewEnglandCrusaders	0	OaklandOutlaws	9
KCChaos	7	GemCityGangsters	14
PittsburghBlitzkrieg	20	IndianaFog	14
CincinnatiDefenders	13	Titans	23
BuffaloSkullCrushers	19	HoustonRoughnecks	31
MiamiNemesis	16	NewYorkEmpire	0
CarolinaCobras	6	MemphisManiacs	35
AtlantaDominators	31	TampaBayFireballs	6
KCChaos	7	OaklandOutlaws	20
MichiganWolverines	13	PittsburghBlitzkrieg	27
NewEnglandCrusaders	3	CincinnatiDefenders	20
IndianaFog	23	MiamiNemesis	3
MontanaGrizzlies	17	Zecken	18
SeattleBarbarians	10	VegasBlackAces	34
SaintPaulPunishers	0	ArizonaWranglers	47
GemCityGangsters	19	VancouverVandals	16
DakotaBlizzard	34	LosAngelesChallengers	14
DaytonaBeachBullSharks	3	TexasHold'em	9
BrooklynHitmen	6	WashingtonWarriors	22
Titans	17	HoustonRoughnecks	21
PhiladelphiaSlayers	34	ProvidenceIslanders	11
NewYorkEmpire	12	BuffaloSkullCrushers	46
DakotaBlizzard	46	MichiganWolverines	10
IndianaFog	0	GemCityGangsters	22
VegasBlackAces	9	ProvidenceIslanders	10
MontanaGrizzlies	13	ArizonaWranglers	27
AtlantaDominators	17	NewYorkEmpire	6
Titans	34	MiamiNemesis	0
HoustonRoughnecks	20	PhiladelphiaSlayers	37
CincinnatiDefenders	11	TexasHold'em	16
Zecken	16	WashingtonWarriors	31
BrooklynHitmen	9	PittsburghBlitzkrieg	37
SaintPaulPunishers	7	KCChaos	14
OaklandOutlaws	9	VancouverVandals	28
DaytonaBeachBullSharks	20	SeattleBarbarians	17
NewEnglandCrusaders	21	CarolinaCobras	9
MemphisManiacs	27	BuffaloSkullCrushers	24
LosAngelesChallengers	6	TampaBayFireballs	28
PittsburghBlitzkrieg	14	NewEnglandCrusaders	15
BuffaloSkullCrushers	46	NewYorkEmpire	23
CincinnatiDefenders	3	HoustonRoughnecks	20
MichiganWolverines	0	TexasHold'em	16
VegasBlackAces	6	MontanaGrizzlies	17
ArizonaWranglers	38	Zecken	3
ProvidenceIslanders	3	PhiladelphiaSlayers	27
CarolinaCobras	13	TampaBayFireballs	7
AtlantaDominators	39	GemCityGangsters	15
VancouverVandals	18	SaintPaulPunishers	0
IndianaFog	10	KCChaos	6
DakotaBlizzard	44	OaklandOutlaws	6
Titans	7	DaytonaBeachBullSharks	19
SeattleBarbarians	0	BrooklynHitmen	30
WashingtonWarriors	0	LosAngelesChallengers	6
MemphisManiacs	42	MiamiNemesis	9
NewYorkEmpire	6	VancouverVandals	29
TexasHold'em	22	IndianaFog	7
BuffaloSkullCrushers	14	DakotaBlizzard	36
MiamiNemesis	9	PittsburghBlitzkrieg	34
CincinnatiDefenders	28	BrooklynHitmen	3
PhiladelphiaSlayers	34	WashingtonWarriors	3
HoustonRoughnecks	29	Titans	21
ProvidenceIslanders	14	CarolinaCobras	6
MemphisManiacs	20	TampaBayFireballs	6
MontanaGrizzlies	12	KCChaos	30
DaytonaBeachBullSharks	3	VegasBlackAces	25
GemCityGangsters	27	Zecken	10
OaklandOutlaws	23	SaintPaulPunishers	17
LosAngelesChallengers	6	SeattleBarbarians	21
MichiganWolverines	0	ArizonaWranglers	33
AtlantaDominators	31	NewEnglandCrusaders	3
IndianaFog	3	VancouverVandals	24
DakotaBlizzard	40	TexasHold'em	17
BuffaloSkullCrushers	8	PittsburghBlitzkrieg	49
CincinnatiDefenders	3	MiamiNemesis	6
PhiladelphiaSlayers	41	BrooklynHitmen	3
WashingtonWarriors	6	Titans	27
ProvidenceIslanders	10	HoustonRoughnecks	13
TampaBayFireballs	23	CarolinaCobras	24
MontanaGrizzlies	2	MemphisManiacs	73
DaytonaBeachBullSharks	3	KCChaos	23
GemCityGangsters	23	VegasBlackAces	9
Zecken	20	OaklandOutlaws	23
SaintPaulPunishers	6	LosAngelesChallengers	17
SeattleBarbarians	20	MichiganWolverines	17
ArizonaWranglers	14	AtlantaDominators	12
NewYorkEmpire	3	NewEnglandCrusaders	24
NewYorkEmpire	0	MiamiNemesis	36
Titans	20	PittsburghBlitzkrieg	17
SaintPaulPunishers	3	IndianaFog	28
DaytonaBeachBullSharks	3	DakotaBlizzard	36
ArizonaWranglers	17	GemCityGangsters	3
KCChaos	19	Zecken	17
BuffaloSkullCrushers	12	AtlantaDominators	44
PhiladelphiaSlayers	31	TampaBayFireballs	7
CarolinaCobras	7	WashingtonWarriors	31
BrooklynHitmen	6	ProvidenceIslanders	40
MemphisManiacs	35	VegasBlackAces	6
MichiganWolverines	6	LosAngelesChallengers	16
VancouverVandals	23	MontanaGrizzlies	14
OaklandOutlaws	13	CincinnatiDefenders	0
HoustonRoughnecks	13	NewEnglandCrusaders	24
TexasHold'em	41	SeattleBarbarians	7
Titans	21	BuffaloSkullCrushers	34
WashingtonWarriors	3	PhiladelphiaSlayers	34
TexasHold'em	25	DaytonaBeachBullSharks	6
KCChaos	7	IndianaFog	19
MemphisManiacs	44	CarolinaCobras	24
TampaBayFireballs	13	NewYorkEmpire	3
SaintPaulPunishers	26	Zecken	25
NewEnglandCrusaders	3	MiamiNemesis	20
PittsburghBlitzkrieg	10	HoustonRoughnecks	20
AtlantaDominators	26	BrooklynHitmen	3
GemCityGangsters	19	MontanaGrizzlies	0
LosAngelesChallengers	3	ArizonaWranglers	48
VancouverVandals	20	OaklandOutlaws	13
CincinnatiDefenders	20	ProvidenceIslanders	27
VegasBlackAces	9	MichiganWolverines	13
SeattleBarbarians	0	DakotaBlizzard	37
PittsburghBlitzkrieg	7	CincinnatiDefenders	14
IndianaFog	3	Zecken	48
ProvidenceIslanders	13	WashingtonWarriors	16
LosAngelesChallengers	10	GemCityGangsters	15
BrooklynHitmen	0	HoustonRoughnecks	42
PhiladelphiaSlayers	17	AtlantaDominators	38
SeattleBarbarians	0	ArizonaWranglers	42
MontanaGrizzlies	24	SaintPaulPunishers	10
CarolinaCobras	22	BuffaloSkullCrushers	31
MiamiNemesis	9	TampaBayFireballs	6
NewYorkEmpire	0	MemphisManiacs	39
NewEnglandCrusaders	6	Titans	34
VancouverVandals	9	DaytonaBeachBullSharks	12
OaklandOutlaws	28	KCChaos	14
TexasHold'em	31	MichiganWolverines	7
VegasBlackAces	10	DakotaBlizzard	31
NewEnglandCrusaders	30	BuffaloSkullCrushers	38
NewYorkEmpire	0	CincinnatiDefenders	32
HoustonRoughnecks	17	PittsburghBlitzkrieg	13
MiamiNemesis	3	MichiganWolverines	27
TexasHold'em	7	VegasBlackAces	9
Zecken	14	MontanaGrizzlies	17
PhiladelphiaSlayers	10	ArizonaWranglers	3
TampaBayFireballs	10	ProvidenceIslanders	26
CarolinaCobras	0	AtlantaDominators	38
GemCityGangsters	7	SaintPaulPunishers	13
KCChaos	14	VancouverVandals	23
OaklandOutlaws	25	IndianaFog	9
DakotaBlizzard	20	DaytonaBeachBullSharks	0
Titans	13	BrooklynHitmen	18
SeattleBarbarians	3	LosAngelesChallengers	6
MemphisManiacs	23	WashingtonWarriors	10
ArizonaWranglers	27	VegasBlackAces	24
BuffaloSkullCrushers	18	TampaBayFireballs	16
MemphisManiacs	16	AtlantaDominators	30
MiamiNemesis	12	NewEnglandCrusaders	3
BrooklynHitmen	13	CarolinaCobras	16
PittsburghBlitzkrieg	13	PhiladelphiaSlayers	7
GemCityGangsters	17	SeattleBarbarians	31
DaytonaBeachBullSharks	14	NewYorkEmpire	31
HoustonRoughnecks	31	KCChaos	17
SaintPaulPunishers	13	MontanaGrizzlies	13
Titans	26	ProvidenceIslanders	20
WashingtonWarriors	7	CincinnatiDefenders	12
Zecken	13	VancouverVandals	30
MichiganWolverines	14	OaklandOutlaws	24
IndianaFog	3	DakotaBlizzard	41
LosAngelesChallengers	13	TexasHold'em	23     """

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
