import pandas as pd
from util import Config


# Yards Per Play

df = pd.concat((Config.load_feather(k, y) for k, v in Config.ls_dictionary.items() for y in v)).fillna(0)

# 5

off_plays_5 = ['Shotgun 5 Wide Parallel Slants']
def_ypp_5 = df.loc[df.OffensivePlay.isin(off_plays_5)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_5.columns[0]])

# 014

off_plays_014 = ['Empty 4 Wide Spread Corner Post']
def_ypp_014 = df.loc[df.OffensivePlay.isin(off_plays_014)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_014.columns[0]])

# 104

off_plays_104 = ['Singleback 4 Wide Quick Outs']
def_ypp_104 = df.loc[df.OffensivePlay.isin(off_plays_104)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_104.columns[0]])

# 113

off_plays_113 = ['Shotgun Normal HB Flare', 'Singleback Normal TE Quick Out', 'Singleback Normal WR Quick In',
                 'Shotgun Normal TE Out', 'Singleback Normal FL Post', 'Singleback Normal HB Release Mid',
                 'Singleback Normal SE Quick Hit']
def_ypp_113 = df.loc[df.OffensivePlay.isin(off_plays_113)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_113.columns[0]])

# 122

off_plays_122 = ['Singleback Big WR Deep', 'Singleback Big Ins and Outs']
def_ypp_122 = df.loc[df.OffensivePlay.isin(off_plays_122)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_122.columns[0]])

# 203

off_plays_203 = ['Split Backs 3 Wide Drag In', 'Split Backs 3 Wide Slot Post', 'Split Backs 3 Wide WR Quick Out']
def_ypp_203 = df.loc[df.OffensivePlay.isin(off_plays_203)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_203.columns[0]])

# 212

pass_plays_212 = ['I Formation Twin WR Hard Slants', 'I Formation Twin WR Quick Outs',
                  'Weak I Normal WR Corner TE Middle', 'I Formation Normal Max Protect', 'I Formation Normal FL Hitch',
                  ]
run_plays_212 = ['Weak I Normal HB Inside Weak', 'I Formation Normal HB Dive', 'I Formation Normal HB Blast',
                 'I Formation Normal HB Counter']
total_plays_212 = pass_plays_212 + run_plays_212
def_ypp_pass_212 = df.loc[df.OffensivePlay.isin(pass_plays_212)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_pass_212.columns[0]])
def_ypp_run_212 = df.loc[df.OffensivePlay.isin(run_plays_212)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_run_212.columns[0]])
def_ypp_total_212 = df.loc[df.OffensivePlay.isin(total_plays_212)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_total_212.columns[0]])

# 221

pass_plays_221 = ['Strong I Big TE Post', 'Strong I Big Backfield Drag']
run_plays_221 = []
total_plays_221 = pass_plays_221 + run_plays_221
def_ypp_pass_221 = df.loc[df.OffensivePlay.isin(pass_plays_221)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_pass_221.columns[0]])
def_ypp_run_221 = df.loc[df.OffensivePlay.isin(run_plays_221)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_run_221.columns[0]])
def_ypp_total_221 = df.loc[df.OffensivePlay.isin(total_plays_221)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_total_221.columns[0]])


# Yards Per Play - Best Offense

# 113

def_plays_113 = ['4-3 Normal Man Under 1']
off_ypp_113 = df.loc[df.DefensivePlay.isin(def_plays_113)].groupby('OffensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[off_ypp_113.columns[0]], ascending=False)

# 203

def_plays_203 = ['4-3 Normal Man Under 1']
off_ypp_203 = df.loc[df.DefensivePlay.isin(def_plays_203)].groupby('OffensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[off_ypp_203.columns[0]], ascending=False)

# 212

def_plays_212 = ['3-4 Normal Double WR2']
off_ypp_212 = df.loc[df.DefensivePlay.isin(def_plays_212)].groupby('OffensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[off_ypp_212.columns[0]], ascending=False)

# 311

def_plays_311 = ['Dime Flat MLB SS Blitz']
off_ypp_311 = df.loc[df.DefensivePlay.isin(def_plays_311)].groupby('OffensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[off_ypp_311.columns[0]], ascending=False)

# 122

def_plays_122 = ['Nickel Strong 2 Deep Man Under']
off_ypp_122 = df.loc[df.DefensivePlay.isin(def_plays_122)].groupby('OffensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[off_ypp_122.columns[0]], ascending=False)
