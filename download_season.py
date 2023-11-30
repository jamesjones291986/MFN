from GameLogDownloader import GameLogDownloader
from SeasonCompiler import SeasonCompiler

league = 'qad'
year = '2048'
path = f'/Users/jamesjones/game_logs/{league}/{year}/{league}_{year}.csv'

gdl = GameLogDownloader()
gdl.set_league_season(league, int(year))
gdl.download_season(path)

# Compile into a feather file

SeasonCompiler.compile(league, int(year), override_path=path)