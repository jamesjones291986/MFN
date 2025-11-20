from GameLogDownloader import GameLogDownloader
from SeasonCompiler import SeasonCompiler

league = 'USFL'
year = '2018'
path = '/Users/jamesjones/projects/mfn/USFL_2018_schedule.csv'

gdl = GameLogDownloader()
gdl.set_league_season(league, int(year))
gdl.download_season(path)

# Compile into a feather file

SeasonCompiler.compile(league, int(year), override_path = '/Users/jamesjones/projects/mfn/USFL_2018_schedule.csv'