from .validation import validate_input_data
import numpy as np

def diff(series):
    """
    Compute the difference between consecutive elements in a series.
    """
    return series[1:] - series[:-1]

def smooth(x, window_len):
    """
    Smooth the input series using a moving average with a specified window length.
    """
    if window_len < 3:
        return x

    if window_len % 2 == 0:
        window_len += 1

    w = np.ones(window_len)
    y = np.convolve(w, x, mode='valid') / len(w)
    y = np.hstack((x[:window_len // 2], y, x[len(x) - window_len // 2:]))

    for i in range(0, window_len // 2):
        y[i] = np.sum(y[0: i + i]) / ((2 * i) + 1)

    for i in range(len(x) - window_len // 2, len(x)):
        y[i] = np.sum(y[i - (len(x) - i - 1): i + (len(x) - i - 1)]) / ((2 * (len(x) - i - 1)) + 1)

    return y

def detect_blinks(trial_data, sampling_freq=1000, concat_gap_interval=100):
    """
    Detect blink intervals based on missing data, smoothing, and monotonic trends.
    Adapted from: R. Hershman, A. Henik, and N. Cohen, 2018.
    
    Input:
        trial_data         : DataFrame with 'Pupil Size' column.
        sampling_freq      : Sampling frequency of the data.
        concat_gap_interval: Interval to concatenate consecutive blinks (default=100ms).
    Output:
        blink_intervals    : List of tuples with refined (start, end) indices of blinks.
    """
    validate_input_data(trial_data)
    pupil_sizes = np.asarray(trial_data['Pupil Size'])
    sampling_interval = 1000 // sampling_freq

    # Step 1: Identify missing data (zeros)
    missing_data = np.array(pupil_sizes == 0, dtype="float32")
    difference = diff(missing_data)

    blink_onset = np.where(difference == 1)[0]
    blink_offset = np.where(difference == -1)[0] + 1

    # Step 2: Edge case handling for start and end of data
    if pupil_sizes[0] == 0:
        blink_onset = np.hstack((0, blink_onset))
    if pupil_sizes[-1] == 0:
        blink_offset = np.hstack((blink_offset, len(pupil_sizes) - 1))

    # Step 3: Smooth data to reduce noise
    smoothing_window = 10 // sampling_interval
    smoothed_pupil = smooth(pupil_sizes, smoothing_window)
    smoothed_pupil[np.where(smoothed_pupil == 0)] = np.nan
    pupil_diff = diff(smoothed_pupil)

    monotonically_dec = pupil_diff <= 0
    monotonically_inc = pupil_diff >= 0

    # Step 4: Refine onset and offset indices based on monotonicity
    for i in range(len(blink_onset)):
        if blink_onset[i] != 0:
            j = blink_onset[i] - 1
            while j > 0 and monotonically_dec[j]:
                j -= 1
            blink_onset[i] = j + 1

        if blink_offset[i] != len(pupil_sizes) - 1:
            j = blink_offset[i]
            while j < len(monotonically_inc) and monotonically_inc[j]:
                j += 1
            blink_offset[i] = j

    # Step 5: Merge close blinks based on concat_gap_interval
    c = np.empty((len(blink_onset) + len(blink_offset),), dtype=blink_onset.dtype)
    c[0::2] = blink_onset
    c[1::2] = blink_offset
    c = list(c)

    i = 1
    while i < len(c) - 1:
        if c[i + 1] - c[i] <= concat_gap_interval:
            c[i:i + 2] = []
        else:
            i += 2

    temp = np.reshape(c, (-1, 2), order='C')

    # Step 6: Output refined blink intervals
    blink_intervals = [(int(temp[idx, 0]), int(temp[idx, 1])) for idx in range(temp.shape[0])]
    return blink_intervals


