# Logic for the calculators
from math import pow


# Constants
NOTES = [
    "C",
    "C♯/D♭",
    "D",
    "D♯/E♭",
    "E",
    "F",
    "F♯/G♭",
    "G",
    "G♯/A♭",
    "A",
    "A♯/B♭",
    "B"
]


OCTAVES = list(range(9))


MULTIPLIERS = {
    '1/2': 2,
    '1/4d': 1.5,
    '1/4': 1,
    '1/8d': 1/2*1.5,
    '1/8': 1/2,
    '1/8t': 1/2*2/3,
    '1/16d': 1/4*1.5,
    '1/16': 1/4,
    '1/16t': 1/4*2/3,
    '1/32': 1/8,
}


INTONATION_NAME_MAP = {
    'equal_temp': 'equal temperament',
}


# Functions
def get_all_notes():
    """
    Generate a list of all names of notes in a standard 88 key piano (e.g. A0, E2, etc...)
    Ranges from A0 to C8

    :return: list of strings
    """
    all_notes = []
    stop = False
    reached_a0 = False
    for octave in OCTAVES:
        for note in NOTES:
            if octave == 0 and note != 'A' and not reached_a0:
                continue
            reached_a0 = True
            if "/" in note:
                all_notes.append(
                    '/'.join(
                        f"{accidental}{octave}" for accidental in note.split('/')
                    )
                )
                continue
            all_notes.append(f"{note}{octave}")
            if note == "C" and octave == 8:
                stop = True
                break
        if stop:
            break

    return all_notes


def eq_temp_freq(note, base_freq):
    """
    Equal temperament calculation of note frequency

    :param note: name of note (e.g. E2)
    :param base_freq: base tuning frequency in Hz (e.g. 440)

    :return: 2 decimal float representing the frequency of the note
    """
    all_notes = get_all_notes()
    diff = all_notes.index(note) - all_notes.index('A4')
    return base_freq * pow(2, diff/12)


def get_frequency(note, base_freq, intonation="equal_temp"):
    """
    Calculate the frequency of a note. Assumes equal temperament for now

    :param note: name of the note (e.g. E2)
    :param base_freq: base tuning frequency in Hz (e.g. 440)
    :param intonation: note intonation (e.g. 'equal_temp', other intonations TBI)

    :return: 2 decimal float representing the frequency of the note
    """
    if intonation == "equal_temp":
        return eq_temp_freq(note, float(base_freq))
    return None


def get_note_durations(time_sig_base, bpm):
    """
    Calculate the duration of different note lengths according to the time signature base
    of the measure and the beats per minute

    :param time_sig: denominator of time signature, i.e. 4 in 3/4, 8 in 12/8
    :param bpm: beats per minute

    :return: duration in miliseconds of most common notes
    """
    def _rel_duration(sig_base, multiplier):
        """
        Get ratio to beat of each note in MULTIPLIER.

        E.g.

        In x/4 time signatures, a minim is 2x the beat and a semiquaver 1/4 the beat
        In x/8, a crotchet is 2/3 the beat
        """
        return multiplier if sig_base == 4 else multiplier * 2/3

    return {
        note: 60/bpm * _rel_duration(time_sig_base, multiplier)
        for note, multiplier in MULTIPLIERS.items()
    }
