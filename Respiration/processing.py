"""Dilate beam-enabled moments (binary)"""
"""To the same seq_length as data_Times"""
def dilate_beams(data_Times, beam_Times, beam_Amps):
    curr_state, beam_index = 0, 0
    dilated_beams = []
    for time in data_Times:
        if time > beam_Times[beam_index]:
            curr_state = beam_Amps[beam_index]
            if beam_index < len(beam_Times)-1:
                beam_index += 1
        dilated_beams.append(curr_state)
    return dilated_beams

"""Sectionize beam-enabled intervals"""
"""There are more than one beam session in even one field"""
def beam_enabling_intervals(data_Times, cutted_amps):
    total_intervals = []
    curr_interval = []
    for i in range(len(data_Times)-1):
        curr_amp, next_amp = cutted_amps[i], cutted_amps[i+1]
        if curr_amp != 0:
            curr_interval.append(curr_amp)
            if next_amp == 0:
                total_intervals.append(curr_interval)
                curr_interval = []
    return total_intervals, len(total_intervals)