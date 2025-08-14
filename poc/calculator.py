# Logic for the calculators
from math import pow


# Constants
NOTES = [
    "C",
    "C#/Db",
    "D",
    "D#/Eb",
    "E",
    "F",
    "F#/Gb",
    "G",
    "G#/Ab",
    "A",
    "A#/Bb",
    "B"
]

OCTAVES = list(range(9))

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
                all_notes.append('/'.join(f"{accidental}{octave}" for accidental in note.split('/')))
                continue
            all_notes.append(f"{note}{octave}")
            if note == "C" and octave == 8:
                stop = True
                break
        if stop:
            break
    return all_notes


ALL_NOTES = get_all_notes()

INTONATION_NAME_MAP = {
    'equal_temp': 'equal temperament',
}

# Functions
def eq_temp_freq(note, base_freq):
    """
    Equal temperament calculation of note frequency

    :param note: name of note (e.g. E2)
    :param base_freq: base tuning frequency in Hz (e.g. 440)

    :return: 2 decimal float representing the frequency of the note
    """
    diff = ALL_NOTES.index(note) - ALL_NOTES.index('A4')
    return base_freq * pow(2, diff/12)


def get_frequency(note, base_freq, intonation="equal_temp"):
    """
    Calculate the frequency of a note. Assumes equal temperament for now

    :param note: name of the note (e.g. E2)
    :param base_freq: base tuning frequency in Hz (e.g. 440)
    :param intonation: note intonation (e.g. 'equal_temp', other intonations TBI)

    :return: 2 decimal float representing the frequency of the note
    """
    base_freq = float(base_freq)
    if intonation == "equal_temp":
        return eq_temp_freq(note, base_freq)
    return None
