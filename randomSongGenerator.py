from music21 import *
import random
import typing

# TODO range of sounds, starting pitches, ascending/descending melody, intensity arrow things
# TODO Other quadrants of emotoin: 

# positive low energy: 
# happy calm (content [slow sound in major, higher pitch]), 
# negative high energy: 
# sad excited (angry [fast sound in minor, lower pitch])

def random_note(MIDI_lowerbound, MIDI_upperbound, quarterlength_l, quarterlength_u, key):
    '''returns a note of random pitch and duration.
        duration step hard coded as 0.25'''

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


def random_rest(quarterlength_l, quarterlength_u):
    '''returns a rest of random duration'''
    '''python random funcs can't take floats so we got to scale up the user input'''
    ql_lo_amplified = quarterlength_l * 1024
    ql_up_amplified = quarterlength_u * 1024

    sixteenth = 0.25*1024

    quarterlength = random.randrange(ql_lo_amplified, ql_up_amplified + sixteenth, sixteenth)
    quarterlength /= 1024

    res = note.Rest(quarterLength = quarterlength)

    return res


def happy_song(numOfNotes: int = 100) -> stream.Part:
    song = stream.Part()

    kee = key.Key('C', 'major')

    song.append(meter.TimeSignature('4/4'))
    song.append(instrument.ElectricPiano())
    song.append(tempo.MetronomeMark(text=None, number=120, referent=note.Note(type='half')))
    song.keySignature = kee

    for i in range(numOfNotes):
        if isinstance(song[-1], note.Rest) or random.random() < 0.8:

            offset = int(i/numOfNotes*15)

            noat = random_note(70+offset, 75+offset, 0.5, 1, song.keySignature)
            if random.random() < 0.4:
                noat.articulations.append(
                    random.choice(
                                [articulations.Staccato(), 
                                 articulations.Spiccato(),
                                 articulations.Staccatissimo(),
                                 articulations.Spiccato()]
                                )
                )

            song.append(noat)
        else:
            song.append(random_rest(0, 0.5))

    


    return song

def content_song(numOfNotes: int = 100) -> stream.Part:
    '''happy and calm, major, slow but with high pitch'''
    song = stream.Part()

    kee = key.Key('F', 'major')

    song.append(meter.TimeSignature('4/4'))
    song.append(instrument.ElectricPiano())
    song.append(tempo.MetronomeMark(text=None, number=70, referent=note.Note(type='half')))
    song.keySignature = kee

    for i in range(numOfNotes):
        if isinstance(song[-1], note.Rest) or random.random() < 0.9:

            offset = int(i/numOfNotes*10)
            noat = random_note(70+offset, 75+offset, 0.5, 1, song.keySignature)
            if random.random() < 0.4:
                noat.articulations.append(random.choice([articulations.Tenuto(),
                                                        articulations.Unstress(),
                                                        articulations.DetachedLegato()]
                                                        )
                                        )
            song.append(noat)
        else:
            song.append(random_rest(0.5,1))

    return song

def sad_song(numOfNotes:int = 100) -> stream.Part:
    song = stream.Part()

    kee = key.Key('C', 'minor')

    song.append(meter.TimeSignature('4/4'))
    song.append(instrument.ElectricPiano())
    song.append(tempo.MetronomeMark(text=None, number=60, referent=note.Note(type='half')))
    song.keySignature = kee


    for i in range(numOfNotes):
        if isinstance(song[-1], note.Rest) or random.random() < 0.8:

            offset = int(i/numOfNotes*10)

            noat = random_note(55-offset, 60-offset, 1, 2, song.keySignature)
            if random.random() < 0.5:
                noat.articulations.append(
                    random.choice([articulations.Tenuto()])
                    )
            song.append(noat)
                
        else:
            song.append(random_rest(0.5, 0.75))

    return song


def angry_song(numOfNotes:int = 100) -> stream.Part:
    song = stream.Part()

    kee = key.Key('C', 'minor')

    song.append(meter.TimeSignature('4/4'))
    song.append(instrument.ElectricPiano())
    song.append(tempo.MetronomeMark(text=None, number=100, referent=note.Note(type='half')))
    song.keySignature = kee

    for i in range(numOfNotes):
        if isinstance(song[-1], note.Rest) or random.random() < 0.9:

            offset = int(i/numOfNotes*5)

            noat = random_note(50-offset, 55-offset, 0.25, 0.75, song.keySignature)
            if random.random() < 0.7:
                noat.articulations.append(
                    random.choice(
                                [articulations.Staccato(), 
                                 articulations.Spiccato(),
                                 articulations.Staccatissimo(),
                                 articulations.Spiccato(),
                                 articulations.StrongAccent()]
                                )
                )
            song.append(noat)
                
        else:
            song.append(random_rest(0.25, 0.5))

    return song


if __name__ == "__main__":
    score = stream.Score()

    score.append(angry_song(numOfNotes=20))


    percussionPart = stream.Part()

    percussionPart.append(instrument.Percussion()) 
    # better when changed to Percussion()

    for i in range(2*int(score.duration.quarterLength)):
        if i % 8 == 0:
            percussionPart.append(note.Note(45, quarterLength = 0.5))
        else:
            percussionPart.append(note.Note(40, quarterLength = 0.5))


    # score.append(percussionPart)
    score.write('midi',fp = "/Users/baronwang/Desktop/Colby/SU22/happy_song.mid")
    score.show()
