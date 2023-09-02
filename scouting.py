from main import format_df
from util import Config


# Scouting

# Bring in the league to scout
df = format_df(Config.load_feather('xfl', 2045)).reset_index(drop=True)


# Defensive Scouting
def def_scouting(defense, league, season):
    for p in df.OffPersonnel.unique():
        filtered_df = df.loc[
            df.DefTeam.eq(defense) &
            df.League.eq(league) &
            df.OffPersonnel.eq(p) &
            df.Season.astype(str).eq(season)
            ]
        grouped_data = filtered_df.groupby('DefensivePlay').size().sort_values(ascending=False).head(30)
        percentages = grouped_data / grouped_data.sum() * 100
        top_30 = percentages.head(30)
        print(p)
        print(top_30.apply(lambda x: f'{x:.1f}%'))
        print('')


def_scouting('ARZ', 'xfl', '2045')


##################################################

# Testing

# Offensive Scouting
def off_scouting(offenses, league, season):
    for offense in offenses:
        filtered_df = df.loc[
            df.DefTeam.eq(offense) &
            df.League.eq(league) &
            df.Season.astype(str).eq(season)
            ]
        grouped_data = filtered_df.groupby(['OffPersonnel', 'OffensivePlay']).size().reset_index(name='Count')
        grouped_data['Percentage'] = grouped_data.groupby('OffPersonnel')['Count'].transform(
            lambda x: x / x.sum() * 100)
        top_30 = grouped_data.groupby('OffPersonnel').apply(lambda x: x.nlargest(30, 'Percentage')).reset_index(
            drop=True)

        print(f"Offense: {offense}")
        for personnel in top_30['OffPersonnel'].unique():
            personnel_data = top_30[top_30['OffPersonnel'] == personnel]
            print(f"{personnel}:")
            print(personnel_data[['OffensivePlay', 'Percentage']].apply(
                lambda x: f"{x['OffensivePlay']:40s} {x['Percentage']:.1f}%", axis=1).to_string(index=False))
            print('')


off_scouting('NYM', 'pfl', '2029')