import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_trackmate_xml_tracks(xml_file):
    """Reads tracks from trackmate xml track file and converts into a user-friendly DataFrame """
    
    from xml.etree import cElementTree as ET
    
    tracks = ET.parse(xml_file)
    frame_interval = float(tracks.getroot().attrib["frameInterval"])
    n_tracks = float(tracks.getroot().attrib["nTracks"])
    
    attributes = []
    for ti, track in enumerate(tracks.iterfind('particle')):
        for spots in track.iterfind('detection'):
            attributes.append([ti, int(spots.attrib.get('t')),
                                   float(spots.attrib.get('x')),
                                   float(spots.attrib.get('y'))])

    track_table = pd.DataFrame(attributes, columns=['TRACK_ID','FRAME','POSITION_X','POSITION_Y'])
    return track_table, frame_interval, n_tracks

def FilterTracks(traj_table, minlen):
    '''filter tracks shorter than minlen, in frames'''
    return traj_table.groupby('TRACK_ID').filter(lambda track: track.TRACK_ID.count() > minlen)

def PlotMultipleTracks(tracks_table, filter_tracks = 10, color = 'steelblue'):
    
    table = FilterTracks(tracks_table, filter_tracks)
    
    #n = len(table.groupby('TRACK_ID'))

    plt.subplots(figsize = (10,10), dpi = 120)

    for i, track in enumerate(np.random.choice(table.TRACK_ID.unique(), replace = True, size = 25)):

        traj = table[table.TRACK_ID == track]

        plt.subplot(5, 5, i+1)
        
        plt.plot(traj.POSITION_X, traj.POSITION_Y, '-o', lw = 1.2, c = color, 
                 markerfacecolor = 'w', markersize = 5, markeredgewidth = 0.5,
                 label = '{} steps'.format(len(traj)), clip_on = False)
        
        plt.plot(traj.POSITION_X.iloc[0], traj.POSITION_Y.iloc[0], 'o', color = color, markersize = 5)
        plt.plot(traj.POSITION_X.iloc[-1], traj.POSITION_Y.iloc[-1], 'o', color = color, markersize = 5)
        
        plt.legend(frameon = False, fontsize = 7, loc = 0, handlelength=0, markerscale=0)
        plt.tick_params(bottom = False)
        plt.axis('scaled')
        plt.axis('off')
		
def show_tracks(xml_file, filter_tracks = 30, color = 'steelblue'):

	PlotMultipleTracks(read_trackmate_xml_tracks(xml_file)[0], filter_tracks = filter_tracks, color = color)
	