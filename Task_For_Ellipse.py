"""
Adapted from https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking

@author: Will Fenwick

"""

import Metrica_IO as mio
import Metrica_Viz as mviz

# set up initial path to data
DATADIR = 'C:/Users/fenwickw/Documents/Python_Scripts/data/Metrica/sample-data-master/data'
game_id = 1 # let's look at sample match 1

# read in the event data
events = mio.read_event_data(DATADIR,game_id)

# Unit conversion from metric data units to meters
events = mio.to_metric_coordinates(events)

# Get events by team
home_events = events[events['Team']=='Home']
away_events = events[events['Team']=='Away']


# Get all shots
shots = events[events['Type']=='SHOT']
home_shots = home_events[home_events.Type=='SHOT']
away_shots = away_events[away_events.Type=='SHOT']

# Get all first half shots
first_half_shots = events[(events['Type']=='SHOT') & (events['Period']==1)]
first_half_home_shots = home_events[(home_events['Type']=='SHOT') & (home_events['Period']==1)]
first_half_away_shots = away_events[(away_events['Type']=='SHOT') & (away_events['Period']==1)]
fig,ax = mviz.plot_events( first_half_home_shots, indicators = ['Marker','Arrow'])
mviz.plot_events( first_half_away_shots, figax=(fig,ax ), color='b', indicators = ['Marker','Arrow'])
fig.suptitle('Home Shots (red) and Away Shots (blue) in the First Half', fontsize=24)


# Reading in the tracking data
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')


# Convert positions from metrica units to meters 
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)


# Plot first goal and run up
fig,ax = mviz.plot_events( events.loc[32:34], indicators = ['Marker','Arrow'], annotate=True )
goal_frame = events.loc[34]['Start Frame']
fig,ax = mviz.plot_frame( tracking_home.loc[goal_frame], tracking_away.loc[goal_frame], figax = (fig,ax), team_colors=('r','b'), PlayerMarkerSize=7, PlayerAlpha=0.5 )
ax.plot( tracking_home['Home_9_x'].iloc[2038:2288], tracking_home['Home_9_y'].iloc[2038:2288], 'm', markersize=10)
fig.suptitle('First Goal', fontsize=24)

#Plot passes and interceptions of player 7
first_half_passes_player7 = events[(events['Type']=='PASS') & (events['Period']==1) & (events['From']=='Player7') ]
first_half_unsuscessfull_passes_player7 = events[(events['Type']=='BALL LOST') & (events['Period']==1) & (events['From']=='Player7') &(events['Subtype'][12:]=='INTERCEPTION') ]
fig,ax = mviz.plot_pitch(field_color ='white' )
mviz.plot_events( first_half_passes_player7, figax=(fig,ax ), indicators = ['Marker','Arrow'], color='g')
mviz.plot_events( first_half_unsuscessfull_passes_player7, figax=(fig,ax ), indicators = ['Marker','Arrow'], color='r')
fig.suptitle('Player 7 Passes (green) and Intercepted Passes (red) in the First Half', fontsize=24)