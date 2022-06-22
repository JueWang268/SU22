from music21 import *
import random as r

'''returns a note of random pitch and duration
    duration accurate to a sixteenth note'''
def random_note(MIDI_lowerbound, MIDI_upperbound, quarterlength_l, quarterlength_u):
    midi = r.randint(MIDI_lowerbound, MIDI_upperbound)

    '''python random funcs can't take floats so we got to scale up the user input'''
    ql_lo_amplified = quarterlength_l * 1024
    ql_up_amplified = quarterlength_u * 1024

    sixteenth = 0.25*1024

    quarterlength = r.randrange(ql_lo_amplified, ql_up_amplified + sixteenth, sixteenth)
    quarterlength /= 1024
    res = note.Note(midi, quarterLength=quarterlength)
    res.storedInstrument = instrument.Viola()
    return res


'''returns a rest of random duration'''
def random_rest(quarterlength_l, quarterlength_u):
    '''python random funcs can't take floats so we got to scale up the user input'''
    ql_lo_amplified = quarterlength_l * 1024
    ql_up_amplified = quarterlength_u * 1024

    sixteenth = 0.25*1024

    quarterlength = r.randrange(ql_lo_amplified, ql_up_amplified + sixteenth, sixteenth)
    quarterlength /= 1024

    res = note.Rest(quarterLength = quarterlength)

    return res


if __name__ == "__main__":
    score = stream.Score()
    song = stream.Part()

    song.append(meter.TimeSignature('6/8'))
    song.append(instrument.Viola())
    song.append(tempo.MetronomeMark(text=None, number=60, referent=note.Note(type='half')))
    song.keySignature = key.Key('C', 'major')


    for i in range(40):
        if r.random() < 0.8:
            song.append(random_note(55, 80, 0.25, 2))
        elif song[-1] is not note.Rest:
            song.append(random_rest(0.25, 0.5))
        else:
            song.append(random_note(55, 80, 0.25, 2))



    # bigSong = stream.Stream()
    # b = corpus.parse('bach/bwv66.6')

    score.append(song)
    
    score.show()