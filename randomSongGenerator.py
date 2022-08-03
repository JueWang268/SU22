from music21 import *
import random
import typing
import sys


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

    quarterlength = random.randrange(ql_lo_amplified, ql_up_amplified + sixteenth, sixteenth)
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

    quarterlength = random.randrange(ql_lo_amplified, ql_up_amplified + sixteenth, sixteenth)
    quarterlength /= 1024

    res = note.Rest(quarterLength = quarterlength)

    return res


def happy_song(numOfNotes: int = 20) -> stream.Part:
    """returns a happy (joyful excited) song of type stream.Part

    Args:
        numOfNotes (int, optional). Defaults to 20.

    Returns:
        stream.Part
    """

    song = stream.Part()

    kee = key.Key('C', 'major')

    song.append(meter.TimeSignature('4/4'))
    song.append(instrument.ElectricPiano())
    song.append(tempo.MetronomeMark(text=None, number=150, referent=note.Note(type='half')))
    song.keySignature = kee

    # adding notes or rests
    for i in range(numOfNotes):
        # if previous music21 object is of instance note.Rest, then append note.Note
        if isinstance(song[-1], note.Rest) or random.random() < 0.8:

            offset = int(i/numOfNotes*15)
            # each note will be generated within a higher pitch interval than the previous one
            noat = random_note(70+offset, 75+offset, 0.5, 1, song.keySignature)
            if random.random() < 0.4:
                noat.articulations.append(
                    random.choice(
                                [articulations.Staccato(), 
                                 articulations.Spiccato(),
                                 articulations.Staccatissimo(),
                                 articulations.Spiccato()]
                                ) # "strong" articulations 
                )

            song.append(noat)
        else:
            song.append(random_rest(0, 0.5))

    return song


def content_song(numOfNotes: int = 20) -> stream.Part:
    """returns a content (joyful calm) song of type stream.Part
    
    Args:
        numOfNotes (int, optional). Defaults to 20.

    Returns:
        stream.Part
    """

    song = stream.Part()

    kee = key.Key('C', 'major')

    song.append(meter.TimeSignature('4/4'))
    song.append(instrument.ElectricPiano())
    song.append(tempo.MetronomeMark(text=None, number=70, referent=note.Note(type='half')))
    song.keySignature = kee

    for i in range(numOfNotes):
        # if previous music21 object is of instance note.Rest, then append note.Note
        if isinstance(song[-1], note.Rest) or random.random() < 0.9:

            offset = int(i/numOfNotes*10)
            # each note will be generated within a higher pitch interval than the previous one
            noat = random_note(70+offset, 75+offset, 0.5, 1, song.keySignature)
            if random.random() < 0.4:
                noat.articulations.append(random.choice([articulations.Tenuto(),
                                                        articulations.Unstress(),
                                                        articulations.DetachedLegato()]
                                                        ) # "weak" articulations
                                        )
            song.append(noat)
        else:
            song.append(random_rest(0.5,1))

    return song

def sad_song(numOfNotes:int = 10) -> stream.Part:
    """returns a sad (sorrowful calm) song of type stream.Part
    
    Args:
        numOfNotes (int, optional). Defaults to 10 due to longer note lengths.

    Returns:
        stream.Part
    """
    song = stream.Part()

    kee = key.Key('C', 'minor')

    song.append(meter.TimeSignature('4/4'))
    song.append(instrument.ElectricPiano())
    song.append(tempo.MetronomeMark(text=None, number=60, referent=note.Note(type='half')))
    song.keySignature = kee


    for i in range(numOfNotes):
        # if previous music21 object is of instance note.Rest, then append note.Note
        if isinstance(song[-1], note.Rest) or random.random() < 0.9:

            offset = int(i/numOfNotes*10)
            # each note will be generated within a lower pitch interval than the previous one
            noat = random_note(55-offset, 60-offset, 1, 2, song.keySignature)
            if random.random() < 0.5:
                noat.articulations.append(
                    random.choice([articulations.Tenuto(),
                                   articulations.Unstress(),
                                   articulations.DetachedLegato()])
                                # "weak" articulations
                    )
            song.append(noat)
                
        else:
            song.append(random_rest(0.5, 0.75))

    return song


def angry_song(numOfNotes:int = 30) -> stream.Part:
    """returns a angry (sorrowful excited) song of type stream.Part
    
    Args:
        numOfNotes (int, optional). Defaults to 30 due to shorter note lengths.

    Returns:
        stream.Part
    """
    song = stream.Part()

    kee = key.Key('C', 'minor')

    song.append(meter.TimeSignature('4/4'))
    song.append(instrument.ElectricPiano())
    song.append(tempo.MetronomeMark(text=None, number=150, referent=note.Note(type='half')))
    song.keySignature = kee

    for i in range(numOfNotes):
        # if previous music21 object is of instance note.Rest, then append note.Note
        if isinstance(song[-1], note.Rest) or random.random() < 0.8:

            offset = int(i/numOfNotes*5)
            # each note will be generated within a lower pitch interval than the previous one
            noat = random_note(50-offset, 55-offset, 0.25, 0.75, song.keySignature)
            if random.random() < 0.7:
                noat.articulations.append(
                    random.choice(
                                [articulations.Staccato(), 
                                 articulations.Spiccato(),
                                 articulations.Staccatissimo(),
                                 articulations.Spiccato(),
                                 articulations.StrongAccent()]
                                ) # strong accented articulations
                )
            song.append(noat)
                
        else:
            song.append(random_rest(0.25, 0.5))

    return song

def neutral_sound(ascending: bool = True) -> stream.Part:
    """returns a neutral sound consisting of two individual notes

    Returns:
        stream.Part
    """
    song = stream.Part()

    kee = key.Key('C', 'major')

    song.append(meter.TimeSignature('2/4'))
    song.append(instrument.ElectricPiano())
    song.append(tempo.MetronomeMark(text=None, number=150, referent=note.Note(type='half')))
    song.keySignature = kee

    if ascending:
        song.append(note.Note('C4', quarterLength = 1))
        song.append(note.Note('G4', quarterLength = 1))
    else:
        song.append(note.Note('G4', quarterLength = 1))
        song.append(note.Note('C4', quarterLength = 1))

    return song


if __name__ == "__main__":

    score = stream.Score()

    if len(sys.argv) == 2:
        emotion = sys.argv[1]
        if emotion == "happy" or emotion == "h":
            score.append(happy_song(numOfNotes=20))
        elif emotion == "sad" or emotion == "s":
            score.append(sad_song(numOfNotes=10))
        elif emotion == "content" or emotion == "c":
            score.append(content_song(numOfNotes=20))
        elif emotion == "angry" or emotion == "a":
            score.append(angry_song(numOfNotes=30))
        else:
            print("USAGE: python3 randomSongGenerator.py [happy/sad/content/angry]")
            exit()
    # happy song by default
    else:
        score.append(happy_song(numOfNotes=20))
        

    score.write('midi',fp = "/Users/baronwang/Desktop/Colby/SU22/song.mid")

    score.show()