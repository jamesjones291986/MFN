import pandas as pd
from util import Config
from SheetsRef import SheetsRef

# Config
targets = ['RB1', 'RB2', 'FB2', 'FB1', 'TE1', 'TE2', 'WR1', 'WR3', 'WR2', 'WR4', 'WR5']
global_off_ref = SheetsRef(Config.sheet_lookup['global_file'], 'OffPlays').get_dataframe()

# Load data
df = pd.concat((Config.load_feather_with_players(k, y)
                for k, v in Config.ls_dictionary.items()
                for y in v)).reset_index(drop=True)

# Add play type/personnel and filter
df[['OffPlayType', 'OffPersonnel']] = df.merge(
    global_off_ref, how='left', left_on='OffensivePlay', right_on='OffPlay')[['OffPlayType', 'OffPersonnel']]
df = df.loc[df.OffPlayType.isin(('Short Pass', 'Medium Pass', 'Long Pass'))]

# Set versions
df['version'] = pd.concat([df.League, df.Season.astype(str)], axis=1).apply(
    lambda x: Config.version_map[x['League']][int(x['Season'])], axis=1)

# OPTIONAL 0.4.6 only
df = df.loc[df.version.eq('0.4.6')]

# Set up modified target columns
for t in targets:
    df[t + '_tar'] = df[t].str.partition(' - ')[0].str.partition(' ')[2].str.partition('.')[0].str.encode('ascii', errors='replace').str.decode('ascii')

# Parse the Text field to pull the intended target.
# Note that no target is specified if the ball is thrown away or intercepted.
df['tgt'] = ''
df.tgt.mask(df.Text.str.contains('pass complete to '),
            df.Text.str.partition('pass complete to ')[2].str.partition(' to ')[0],
            inplace=True)
df.tgt.mask(df.tgt.str.contains('TOUCHDOWN') | df.tgt.str.contains('CONVERSION GOOD') | df.tgt.str.contains('SAFETY'),
            df.Text.str.partition('pass complete to ')[2].str.partition(' to ')[0],
            inplace=True)
df.tgt.mask(df.tgt.str.contains('yards'),
            df.tgt.str.partition(' for ')[0],
            inplace=True)
df.tgt.mask(df.Text.str.contains('intended for '),
            df.Text.str.partition('intended for ')[2].str.partition('.')[0],
            inplace=True)
df.tgt.mask(df.Text.str.contains('dropped by '),
            df.Text.str.partition('dropped by ')[2].str.partition('.')[0],
            inplace=True)
df.loc[:, 'tgt'] = df.tgt.str.partition('-')[2]
df.loc[:, 'tgt'] = df.tgt.str.encode('ascii', errors='replace').str.decode('ascii')
df.loc[:, 'tgt'] = df.tgt.str.partition('.')[0]

# Look for equalities between tgt and _tar columns
df['target'] = ''
for t in targets:
    df.target.mask(df.tgt.eq(df[t + '_tar']), t, inplace=True)

# Test for unknown targets, should print 0
misses = (df.Text.str.contains('pass') &
          (df.target.isna() | df.target.eq(' ') | df.target.eq('')) &
          ~df.Text.str.contains('INTERCEPT') &
          ~df.Text.str.contains('thrown away')).sum()
print(f'Unknown targets: {misses} (should be 0)')

cm = df.loc[~(df.target.isna() | df.target.isin(('', ' ')))]


# Rack and stack by offensive play and target, sort, and export
cnt = cm.groupby(['OffensivePlay', 'OffPlayType', 'target']).tgt.count()
cnt = pd.DataFrame(index=cnt.index, data=cnt)
cnt.sort_index(inplace=True)
cnt.insert(cnt.shape[1], 'tgt %', cnt.tgt / cm.groupby('OffensivePlay').tgt.count())
cnt.to_csv(Config.root + '/targets.csv')


exclude = ('Kickoff', 'Punt', 'Field Goal')
norig = df.loc[df.League.eq('norig') & df.Season.eq('2026') & ~df.OffensivePlay.isin(exclude)]
k = norig.groupby(['HasBall', 'OffensivePlay']).Text.count().sort_values(ascending=False)
a = pd.concat((k.index.to_frame(), k), axis=1).reset_index(drop=True)
aa = a.drop_duplicates('HasBall', keep='first')
aa.sort_values('OffensivePlay', ascending=True, inplace=True)


k = norig.groupby('OffensivePlay').Text.count().sort_values(ascending=False)
a = pd.concat((k.index.to_frame(), k), axis=1).reset_index(drop=True)
aa.sort_values('OffensivePlay', ascending=True, inplace=True)
