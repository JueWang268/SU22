from music21 import *
import random
import typing
import sys
import subprocess

# positive low energy: 
# happy calm (content [slow sound in major, higher pitch]), 
# negative high energy: 
# sad excited (angry [fast sound in minor, lower pitch])

# all songs use electronic piano as instrument

def random_note(MIDI_lowerbound: int, 
                MIDI_upperbound: int, 
                quarterlength_l: int, 
                quarterlength_u: int, 
                key: key.Key) -> note.Note:
    """
    
    returns a note of random pitch and duration.
    duration step hard coded as 0.25
    

    Args:
        MIDI_lowerbound (int): lower bound for note in MIDI
        MIDI_upperbound (int): upper bound for note in MIDI
        quarterlength_l (int): lower bound for quarterlength
        quarterlength_u (int): upper bound for quarterlength
        key (key.Key): key where this note is expected to be on

    Returns:
        note.Note
    """
                
    midi = random.randint(MIDI_lowerbound, MIDI_upperbound)
    pitches = [i.midi%12 for i in key.pitches]

    ''' make sure the note is in the right key'''

    while midi%12 not in pitches:
        midi += 1


    '''python random funcs can't take floats so we got to scale up the user input'''
    ql_lo_amplified = quarterlength_l * 1024
    ql_up_amplified = quarterlength_u * 1024

    sixteenth = 0.25*1024

    quarterlength = random.randrange(int(ql_lo_amplified), int(ql_up_amplified + sixteenth), int(sixteenth))
    quarterlength /= 1024
    res = note.Note(midi, quarterLength=quarterlength)

    return res


def random_rest(quarterlength_l: int, quarterlength_u: int) -> note.Rest:
    """returns a rest of random duration

    Args:
        quarterlength_l (int): lower bound for quarterlength
        quarterlength_u (int): upper bound for quarterlength

    Returns:
        note.Rest
    """

    '''python random funcs can't take floats so we got to scale up the user input'''
    ql_lo_amplified = quarterlength_l * 1024
    ql_up_amplified = quarterlength_u * 1024

    sixteenth = 0.25*1024

    quarterlength = random.randrange(int(ql_lo_amplified), int(ql_up_amplified + sixteenth), int(sixteenth))
    quarterlength /= 1024

    res = note.Rest(quarterLength = quarterlength)

    return res


def main():
    instruments = ["string", "piano"]
    pattern = ["descending", "rising", "neutral"]
    mode = ["major" , "minor"]
    articulations = ["strong", "weak", "neutral"]
    rangeF = [5, 10, 15 ] 
    frequency = [30 , 50 , 60 , 70 , 90 ]
    speed = [ 60 , 100 , 150 ]
    for instrument1 in instruments:
        for pattern1 in pattern:
            for mode1 in mode:
                for articulation1 in articulations:
                    for rangeF1 in rangeF:
                        for freq1 in frequency:
                            for speed1 in speed:
                                writeSong(instrument1, articulation1, pattern1, mode1, rangeF1, freq1, speed1)

def writeSong(instrument1, articulation1, pattern1, mode1, rangeF1, freq1, speed1):
    score = stream.Score()
    score.append(song(instrument1, articulation1, pattern1, mode1, rangeF1, freq1, speed1))
    name = f'{instrument1}_{articulation1}_{pattern1}_{mode1}_{rangeF1}_{freq1}_{speed1}'
    score_name = f"{name}.musicxml"
    score.insert(0, metadata.Metadata())
    score.metadata.title = name
    # '/Applications/MuseScore\ 3.app/Contents/MacOS/mscore happy.musicxml -o happy.mp3'
    score.write('musicxml', fp = score_name)
    subprocess.run(["/Applications/MuseScore 3.app/Contents/MacOS/mscore", score_name, "-o", f'music/{name}.mp3'])


def song(instrument, articulation, pattern, mode, rangeF, freq, speed):
    """returns a happy (joyful excited) song of type stream.Part

    Args:
        numOfNotes (int, optional). Defaults to 20.

    Returns:
        stream.Part
    """

    # [XXX] Controlling number of notes based on tempo
    numOfNotes = int(speed / 3)

    song = stream.Part()

    # [XXX] Controlling mode
    kee = key.Key('C', mode)

    song.append(meter.TimeSignature('4/4'))

    # [XXX] Controlling instrument
    if (instrument == "piano"):
        song.append(instrument.ElectricPiano()) 
    else:
        song.append(instrument.StringInstrument()) 

    # [XXX] controlling speed
    song.append(tempo.MetronomeMark(text=None, number=speed, referent=note.Note(type='half')))
    song.keySignature = kee

    # adding notes or rests
    for i in range(numOfNotes):
        # if previous music21 object is of instance note.Rest, then append note.Note
        if isinstance(song[-1], note.Rest) or random.random() < 0.8:

            # [XXX] rangeF -> 70, 75+15
            # [XXX] freq -> 70
            # [XXX] pattern -> ascending because adding offset
            offset = int(i/numOfNotes*(rangeF))
            if pattern == "descending":
                offset *= -1
            if pattern == "neutral":
                offset = 0
            # each note will be generated within a higher pitch interval than the previous one
            noat = random_note(freq+offset, freq+5+offset, 0.5, 1, song.keySignature)

            # [XXX] articulation is controlled
            if random.random() < 0.4:
                if (articulations == "strong"):
                    noat.articulations.append(
                        random.choice(
                                    [articulations.Staccato(), 
                                     articulations.Spiccato(),
                                     articulations.Staccatissimo(),
                                     articulations.Spiccato()]
                                    ) # "strong" articulations 
                    )
                if (articulations == "weak"):
                    noat.articulations.append(
                        random.choice([articulations.Tenuto(),
                                        articulations.Unstress(),
                                        articulations.DetachedLegato()]
                                        ) # "weak" articulations
                    )

            song.append(noat)
        else:
            song.append(random_rest(0, 0.5))

    return song

if __name__ == "__main__":
	main()
