# import package
from datetime import datetime


def convert_timestamps(timestamps): #  panda series ==to==> [Hours][Minutes] (list)
    """
        This function converts a pandas series of timestamps into a list of hours and minutes.
        
        Args:
            timestamps (pd.Series): A pandas series of timestamps.

        Returns:
            list: A list of tuples where each tuple contains the hour and minute of the timestamp.
    """
    # rest of your function here
    hh_mm = [0, 0]*len(timestamps)   
    for i in range(len(timestamps)):
        t = timestamps.iloc[i][0]
        d = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')       
        h,m = d.hour, d.minute
        hh_mm[i] = h, m       
    return hh_mm