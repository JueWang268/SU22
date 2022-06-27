from music21 import *
import random as r
import typing

# TODO range of sounds, starting pitches, ascending/descending melody

def random_note(MIDI_lowerbound, MIDI_upperbound, quarterlength_l, quarterlength_u, key):
    '''returns a note of random pitch and duration.
        duration step hard coded as 0.25'''

    midi = r.randint(MIDI_lowerbound, MIDI_upperbound)
    pitches = [i.midi%12 for i in key.pitches]

    ''' make sure the note is in the right key'''

    while midi%12 not in pitches:
        midi += 1


    '''python random funcs can't take floats so we got to scale up the user input'''
    ql_lo_amplified = quarterlength_l * 1024
    ql_up_amplified = quarterlength_u * 1024

    sixteenth = 0.25*1024

    quarterlength = r.randrange(ql_lo_amplified, ql_up_amplified + sixteenth, sixteenth)
    quarterlength /= 1024
    res = note.Note(midi, quarterLength=quarterlength)

    return res


def random_rest(quarterlength_l, quarterlength_u):
    '''returns a rest of random duration'''
    '''python random funcs can't take floats so we got to scale up the user input'''
    ql_lo_amplified = quarterlength_l * 1024
    ql_up_amplified = quarterlength_u * 1024

    sixteenth = 0.25*1024

    quarterlength = r.randrange(ql_lo_amplified, ql_up_amplified + sixteenth, sixteenth)
    quarterlength /= 1024

    res = note.Rest(quarterLength = quarterlength)

    return res


def happy_song(numOfNotes: int = 100) -> stream.Part:
    song = stream.Part()

    kee = key.Key('C', 'major')

    song.append(meter.TimeSignature('4/4'))
    song.append(instrument.ElectricPiano())
    song.append(tempo.MetronomeMark(text=None, number=80, referent=note.Note(type='half')))
    song.keySignature = kee


    for _ in range(numOfNotes):
        if isinstance(song[-1], note.Rest) or r.random() < 0.8:
            noat = random_note(55, 70, 0.25, 1, song.keySignature)
            if r.random() < 0.5:
                noat.articulations.append(articulations.Staccato())
            if r.random() < 0.5:
                noat.articulations.append(articulations.Accent())

            song.append(noat)
        else:
            song.append(random_rest(0.25, 0.75))

    return song


def sad_song(numOfNotes:int = 100) -> stream.Part:
    song = stream.Part()

    kee = key.Key('F', 'minor')

    song.append(meter.TimeSignature('4/4'))
    song.append(instrument.ElectricPiano())
    song.append(tempo.MetronomeMark(text=None, number=60, referent=note.Note(type='half')))
    song.keySignature = kee


    for _ in range(numOfNotes):
        if isinstance(song[-1], note.Rest) or r.random() < 0.8:
            noat = random_note(55, 65, 0.75, 2, song.keySignature)
            if r.random() < 0.2:
                noat.articulations = [articulations.Tenuto()]
            song.append(noat)
                
        else:
            song.append(random_rest(0.5, 0.75))

    return song


if __name__ == "__main__":
    score = stream.Score()

    # bigSong = stream.Stream()
    # b = corpus.parse('bach/bwv66.6')

    score.append(sad_song(numOfNotes=20))
    
    score.show()
