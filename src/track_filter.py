# this code has the table output of my read_xml_function as input (track table )

def FilterTracks(traj_table, minlen):
    '''filter tracks shorter than minlen, in frames'''
    
    traj_table = traj_table.groupby('TRACK_ID').filter(lambda track: track.TRACK_ID.count() > minlen)
    
    # create a dictionary to attribute a new number to each track ID
    new_ids = {}
    for i, value in enumerate(traj_table.TRACK_ID.unique()):
        new_ids[value] = i
    
    # replace existent IDs with new ID's using the dicitonary above
    traj_table['TRACK_ID'].replace(new_ids, inplace = True)
    
    # reset index (just in case)
    traj_table.reset_index(drop = True, inplace = True)
    
    # THIS WAS SUPER SMART BTW!
    return traj_table