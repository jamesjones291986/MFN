from glob import iglob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from util import Config

###########################################################
# Possessions
###########################################################

# One big file
print('Importing...')
big_one = pd.concat((pd.read_csv(f) for f in iglob(f'{Config.root}/**/*_pl.csv', recursive=True))).reset_index(drop=True)
big_one = pd.concat((pd.read_csv(f) for f in iglob(f'{Config.root}/norig/*_pl.csv', recursive=True))).reset_index(drop=True)
backup = big_one.copy()

big_one = backup.copy()

# Setup
print('Setup...')
big_one.HasBall.mask(big_one.OffensivePlay.eq('Kickoff'),
                     big_one.HasBall.shift(-1), inplace=True)
big_one.dropna(subset='HasBall', inplace=True)
big_one.YardsGained.fillna(0, inplace=True)
big_one.YardsGained.mask(big_one.OffensivePlay.eq('Field Goal'), 0, inplace=True)
big_one.YardsGained.mask(big_one.OffensivePlay.eq('Punt'), 0, inplace=True)

# Yards to Goal Line (YTGL)
print('YTGL...')
big_one.insert(big_one.shape[1], 'YTGL',
               big_one['Ball @'].str.partition(' ')[2].astype('Int64'))
big_one.YTGL.mask(big_one.HasBall.eq(big_one['Ball @'].str.partition(' ')[0]),
                  100 - big_one['Ball @'].str.partition(' ')[2].astype('Int64'), inplace=True)
big_one.YTGL.mask(big_one.Down.isin([6, 7]), pd.NA, inplace=True)

# Flag un-declined penalties (haha flag, get it?)
print('Penalties...')
big_one.insert(big_one.shape[1], 'penalty',
               big_one.Text.str.count('PENALTY') - big_one.Text.str.count('(Declined)')
               )
big_one.penalty.mask(big_one.Text.str.contains('replay down'), 1, inplace=True)

# Play points
print('Play points...')
big_one.insert(big_one.shape[1], 'pts', 0)
print('\tSafety...')
big_one.pts.mask(big_one.penalty.eq(0) &
                 big_one.Text.str.contains('SAFETY'), -2, inplace=True)  # safety
print('\tTouchdown...')
big_one.pts.mask(big_one.penalty.eq(0) &
                 big_one.Text.str.contains('TOUCHDOWN'), 6, inplace=True)  # normal touchdown by the offense
print('\tField Goals...')
big_one.pts.mask(big_one.penalty.eq(0) &
                 big_one.Text.str.contains('field goal') &
                 ~big_one.Text.str.contains('NO GOOD'), 3, inplace=True)  # field goal
print('\tTwo-point conversions...')
big_one.pts.mask(big_one.penalty.eq(0) &
                 big_one.Text.str.contains('CONVERSION') &
                 ~big_one.Text.str.contains('NO GOOD'), 2, inplace=True)  # two point conversion after TD
print('\tExtra Points...')
big_one.pts.mask(big_one.penalty.eq(0) &
                 big_one.Text.str.contains('Extra point') &
                 ~big_one.Text.str.contains('NO GOOD'), 1, inplace=True)  # extra point good after TD
print('\tFumble TDs...')
big_one.pts.mask(big_one.penalty.eq(0) &
                 big_one.Text.str.contains('FUMBLES') &
                 big_one.Text.str.contains('TOUCHDOWN'), -6, inplace=True)  # fumble returned for TD
print('\tPunt return TDs...')
big_one.pts.mask(big_one.penalty.eq(0) &
                 big_one.OffensivePlay.eq('Punt') &
                 ~big_one.Text.str.contains('FUMBLES') &
                 big_one.Text.str.contains('TOUCHDOWN'), -6, inplace=True)  # punt return TD
print('\tPunt return fumbled for TD...')
big_one.pts.mask(big_one.penalty.eq(0) &
                 big_one.OffensivePlay.eq('Punt') &
                 big_one.Text.str.contains('FUMBLES') &
                 big_one.Text.str.contains('TOUCHDOWN'), 6, inplace=True)  # punt return fumbled for TD
print('\tInterceptions returned for TD...')
big_one.pts.mask(big_one.penalty.eq(0) &
                 big_one.Text.str.contains('INTERCEPTED') &
                 ~big_one.Text.str.contains('FUMBLES') &
                 big_one.Text.str.contains('TOUCHDOWN'), -6, inplace=True)  # interception returned for TD

"""
Explanation: the below string only occurs when a turnover occurs.
While above captures straightforward cases, multiple turnovers can occur in a single play.
Hence, below, we search for any return TD, then match the team that was scored on to HasBall.
If they are not equal, then the offense ended up recovering and scoring; hence, the play is worth 6.
This will break if the team acronym is not exactly 3 characters long.
"""
print('\tEdge cases for TD (multiple turnovers, etc.)...')
pat = ' to ([A-Z][A-Z][A-Z]) 0 for '
ret = ~big_one.Text.str.extract(pat, expand=False).isna()  # tag returns for TD
check = (big_one.penalty.eq(0) & big_one.Text.str.contains('TOUCHDOWN') &  # still check for a TD
         big_one.Text.str.extract(pat, expand=False).ne(big_one.loc[ret, 'HasBall']))
big_one.pts.mask(check, 6, inplace=True)  # fumble return TD by the offense


print('Create possession table...')
# Create possession table
# big_one.insert(big_one.shape[1], 'poss_chg',
#                big_one.HasBall.ne(big_one.HasBall.shift()) &  # change of possession
#                ~big_one.HasBall.isna() &  # ignore timeouts, etc
#                ~big_one.HasBall.shift().isna() |  # ignore timeouts, etc
#                (big_one.Quarter.isin((3, 5)) & big_one.Quarter.shift().isin((2, 4))) |  # new half/OT
#                (big_one.Quarter.eq(1) & big_one.Quarter.shift().gt(1))  # new game
#                )
big_one.insert(big_one.shape[1], 'poss_chg',
               big_one.penalty.eq(0) &  # ignore penalties
               ~big_one.HasBall.isna() &  # ignore timeouts, etc.
               (big_one.OffensivePlay.eq('Kickoff') |
                big_one.OffensivePlay.eq('Onsides Kick Onside Kick') |
                big_one.HasBall.ne(big_one.HasBall.shift()))
               )
#############
# a = big_one.loc[big_one.pts.eq(-6)]

big_one.insert(big_one.shape[1], 'poss',
               big_one.poss_chg.cumsum())
big_one.drop('poss_chg', axis=1, inplace=True)
gb = big_one.groupby('poss')
gb_nxp = big_one.loc[big_one.Down.ne(7)].groupby('poss')  # possessions without extra point plays
big_pdf = pd.DataFrame(index=gb.indices.keys())

# possession start
print('\tPossession start...')
big_pdf.insert(big_pdf.shape[1], 'start',
               gb['YTGL'].first())

# possession yards gained
print('\tPossession yards gained...')
big_pdf.insert(big_pdf.shape[1], 'yards_gained',
               (gb_nxp['YTGL'].first() - gb_nxp['YTGL'].last() + gb_nxp['YardsGained'].last()).astype('Int64'))
# big_pdf.start.mask(big_pdf.yards_gained.isna(), pd.NA, inplace=True)
big_pdf.dropna(inplace=True)
big_pdf.reset_index(drop=True, inplace=True)

# possession points
print('\tPossession points...')
big_pdf.insert(big_pdf.shape[1], 'points',
               gb.pts.sum()
               )

########################################
# Plots
########################################


def my_plot(y, title='Title', xlabel='X-Axis', ylabel='Y-Axis'):
    x = y.index
    fig, ax = plt.subplots()
    ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)
    ax.set(xlim=(x.min(), x.max()), xticks=np.arange(x.min(), x.max(), (x.max() - x.min()) // 20),
           ylim=(0, y.max() * 1.05), yticks=np.arange(0, y.max(), y.max() * 1.05 / 10))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def bin_it(d, y, x, bins=20, r=0):
    """
    :param d: dataframe
    :param y: name of binned column
    :param x: name of binning column
    :param bins: number of bins
    :param r: number of digits to round x
    :return:
    """
    if type(bins) == int:
        size = round((1 + d[x].max() - d[x].min()) / bins, r)
        d['binned_' + y] = np.floor(d[y] / size, r)

    return 1


#############

# avg pts raw
y = big_pdf.groupby('start').points.mean()
chart_title = 'Average points per possession based on starting yards to goal line'
x_label = 'Yards to Goal Line'
y_label = 'Average Points'
my_plot(y, chart_title, x_label, y_label)

# avg pts zeroed
y = big_pdf.mask(big_pdf.points.lt(0), 0).groupby('start').points.mean()
chart_title = 'Average points per possession based on starting yards to goal line'
x_label = 'Yards to Goal Line'
y_label = 'Average Points'
my_plot(y, chart_title, x_label, y_label)

# field goal %
y = 100 * big_pdf.loc[big_pdf.points.eq(3)].groupby('start').points.count() / big_pdf.groupby('start').points.count()
chart_title = '% of possessions ending in a field goal based on starting YTGL'
x_label = 'Yards to Goal Line'
y_label = 'Field goal %'
my_plot(y, chart_title, x_label, y_label)

# TD %
df = big_pdf.loc[big_pdf.start.ne(0)]
y = 100 * df.loc[df.points.isin([6, 7, 8])].groupby('start').points.count() / df.groupby('start').points.count()
chart_title = '% of possessions ending in offensive touchdown based on starting YTGL'
x_label = 'Yards to Goal Line'
y_label = 'TD %'
my_plot(y, chart_title, x_label, y_label)

# TD % (binned)
df = big_pdf.loc[big_pdf.start.ne(0)]
df['binned_pts'] = df
y = 100 * df.loc[df.points.isin([6, 7, 8])].groupby('start').points.count() / df.groupby('start').points.count()
chart_title = '% of possessions ending in offensive touchdown based on starting YTGL'
x_label = 'Yards to Goal Line'
y_label = 'TD %'
my_plot(y, chart_title, x_label, y_label)


########################################
# error checking, temporary
########################################
big_pdf.isna().sum()
(gb_nxp['YTGL'].first() - gb_nxp['YTGL'].last() + gb_nxp['YardsGained'].last()).isna().sum()
gb_nxp['YTGL'].first().isna().sum()

b = big_one.loc[big_one.Text.str.contains('INTERCEPTED') & big_one.Text.str.contains('FUMBLES')]
big_one.loc[~big_one.Text.str.extract(' to ([A-Z][A-Z][A-Z]) 0 for ', expand=False).isna(),
            'Text'].str.extract(' to ([A-Z][A-Z][A-Z]) 0 for ', expand=False).eq(
    big_one.loc[~big_one.Text.str.extract(' to ([A-Z][A-Z][A-Z]) 0 for ', expand=False).isna(), 'HasBall'])

s = '3-6-NOS 42 (4:17) 7-John Swingle pass INTERCEPTED by 20-Kenneth Gage at NOS 41. 20-Kenneth Gage to PHI 0 for 59 yards. TOUCHDOWN! NOS 6 PHI 7'
import re
re.search(' to ([A-Z][A-Z][A-Z]) 0 for ', s)

big_one.loc[big_one.penalty.eq(0) &
            (big_one.Text.str.contains('INTERCEPTED') |
            big_one.Text.str.contains('FUMBLES')) &
            big_one.Text.str.contains('TOUCHDOWN')].shape[0]
big_one.loc[big_one.OffensivePlay.eq('Punt') &
            big_one.Text.str.contains('TOUCHDOWN')].shape[0]

p = 118954
a = big_one.loc[big_one.poss.ge(p - 1) & big_one.poss.le(p + 1)]

a = big_one.loc[big_one.poss.isin(big_pdf.loc[big_pdf.yards_gained.isna()].index)]
(~a.Down.isin([6, 7])).sum()
