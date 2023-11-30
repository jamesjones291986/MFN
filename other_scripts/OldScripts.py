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


def_scouting('ARZ', 'xfl', '2046')