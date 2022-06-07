#for sound stuff
import wave
import struct
import math
import numpy
import random
import time
import os
# import MySQLdb

# keyboard frequency
piano = [16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87, 
         32.70, 34.65, 36.71, 38.89, 41.20, 43.65, 46.25, 49.00, 51.91, 55.00, 58.27, 61.74, 
         65.41, 69.30, 73.42, 77.78, 82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47, 
         130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 
         261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 
         523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77,
         1046.50, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.00, 1864.66, 1975.53,
         2093.00, 2217.46, 2349.32, 2489.02, 2637.02, 2793.83, 2959.96, 3135.96, 3322.44, 3520.00, 3729.31, 3951.07,
         4186.01, 4434.92, 4698.63, 4978.03, 5274.04, 5587.65, 5919.91, 6271.93, 6644.88, 7040.00, 7458.62, 7902.13]

cMajor = [ 
          0, 2, 4, 5, 7, 9,11,
          12,14,16,17,19,21,23,
          24,26,28,29,31,33,35,
          36,38,40,41,43,45,47,
          48,50,52,53,55,57,59,
          60,62,64,65,67,69,71,
          72,74,76,77,79,81,83,
          84,86,88,89,91,93,95,
          96,98,100,101,103,105,107
          ]
     
cMinor = [ 1, 3, 4, 6, 8, 9,11,
          13,15,16,18,20,21,23,
          25,27,28,30,32,33,35,
          37,39,40,42,44,45,47,
          49,51,52,54,56,57,59,
          61,63,64,66,68,69,71,
          73,75,76,78,80,81,83,
          85,87,88,90,92,93,95,
          97,99,100,102,104,105,107]

def create_Pause(pause, fs):
    pause = max(pause, 0)
    line = numpy.zeros(int(fs*pause))
    tone = b''.join(struct.pack('f', samp) for samp in line)
    return tone, pause


def create_toneADSR(frequency, sustainAmp, attackAmp, Aduration, Dduration, Sduration, Rduration, fs):
    print(frequency, sustainAmp, attackAmp, Aduration, Dduration, Sduration, Rduration)
    NTA = int(fs * Aduration)  
    NTD = int(fs * Dduration)  
    NTS = int(fs * Sduration) # repeat for T cycles
    NTR = int(fs * Rduration) 
    N = NTA+NTD+NTS+NTR
    dt = 1.0 / fs
    #logspace or linspace????
    line = numpy.concatenate((numpy.linspace(0, attackAmp, NTA, False), numpy.linspace(attackAmp, sustainAmp, NTD, False), numpy.linspace(sustainAmp, sustainAmp, NTS, False), numpy.linspace(sustainAmp, 0, NTR, False)))
    temp = (int(round(line[n] * math.sin(2 * math.pi * frequency * n * dt) * 128 * ((256 ** 1) -1))) for n in range(0,N))
    tone = b''.join(struct.pack('<h', samp) for samp in temp)
    return tone, Aduration+Dduration+Sduration+Rduration


def amplitude(value):  #62-90 dB range (Alexis' advice)
    x = 60.0*value-60.0
    if x == 0:
        return 0
    else:
        return 10**(x/10.0)

    
def createSong(song):
    fs = 44100
    note = song[0] % 12
    keys = cMajor
    if song[2]:
        keys = cMinor
    keys = [x+note for x in keys]
    if song[2]:
        noteIndex = keys.index(song[0]-1)
    else:
        noteIndex = keys.index(song[0])
    #select notes, check to make sure that the range does not go outside
    v=numpy.linspace(song[3],0,song[19]//2,False)
    f0Contour = numpy.concatenate((v,numpy.linspace(0, song[4], math.ceil(song[19]/2.0),False)))
    print(len(f0Contour), song[19])
    f0notes = [int(round(f0Contour[i])) + random.randint(max(0,noteIndex-song[1]),min(len(keys),noteIndex+song[1])) for i in range(0,song[19])]
    pausingFrequency = []
    while sum(pausingFrequency) < song[19]:
        pausingFrequency.append(random.randint(song[15]-song[16],song[15]+song[16]))
    pausingLength = [random.normalvariate(song[17],song[18]) for i in range(0,len(pausingFrequency))]
    sustain = [random.normalvariate(song[12],song[13]) for i in range(0,song[19])]
    ampContour = numpy.concatenate((numpy.linspace(song[8],0,song[19]//2,False),numpy.linspace(0, song[9], int(math.ceil(song[19]/2.0)),False)))
    tempS = [ampContour[i] + random.normalvariate(song[5],song[6]) for i in range(0,song[19])]
    amplitudeS = [amplitude(x) for x in tempS]  
    amplitudeA = [amplitude(x+song[7]) for x in tempS]
    nextPause = 0
    noise_output = wave.open(song[20], 'w')
    noise_output.setparams((1, 2, fs, 0, 'NONE', 'not compressed'))
    wait = 0
    for i in range(0,song[19]):
        tone, duration = create_toneADSR(piano[keys[f0notes[i]]], amplitudeS[i], amplitudeA[i], song[10], song[11], sustain[i], song[14], fs)
        wait += duration
        noise_output.writeframes(tone)
        #frequency, sustainAmp, attackAmp, Aduration, Dduration, Sduration, Rduration, fs, stream
        if i >= sum(pausingFrequency[0:nextPause]):
            pause, duration = create_Pause(pausingLength[nextPause],fs)
            wait += duration
            noise_output.writeframes(pause)
            nextPause = nextPause +1
    noise_output.close()
    
if __name__ == '__main__':
    #f0 center (0 to 107), variation, Minor Key (0 or 1), Contour 1 (int value giving max or min on that side), Contour 2
    #amp Sustain Mean (0-1 float) & Variance, Attack & sustain amplitude difference, Contour 1 (float value giving max or min on that side), Contour 2
    #articulation Attack, Decay, Sustain mean and variance, Release (milliseconds) 
    #pausing frequency, center and range (pause every x notes)
    #length, mean and variance (pause for x seconds)
    #songlength
    HappySong = [79,5,0,0,0,  .9,0,0,0,0,  .05,0,0,0,.2,  6,2,.2,.1,  19, ""]
    SadSong =   [57,3,1,0,5,  .9,0,0,0,0,  .2,0,.6,0,.2,  3,2,.4,.2,  5, ""]
    SurprisedSong = [85,10,1,0,0,  .9,0,0,0,0,  .02,0,0,0,.2,  6,2,.2,.1,  23, ""]
    AngrySong = [90,7,1,0,0,  .9,0,0,0,0,  .1,0,0,0,.2,  4,2,.2,.1,  10, ""]
    '''
    db = MySQLdb.connect(host="localhost", user="root", passwd="test!234", db="userstudy")
    cur = db.cursor()
        #f0 center (0 to 107), variation, Minor Key (0 or 1), Contour 1 (int value giving max or min on that side), Contour 2
        #amp Sustain Mean (0-1 float) & Variance, Attack & sustain amplitude difference, Contour 1 (float value giving max or min on that side), Contour 2
        #articulation Attack, Decay, Sustain mean and variance, Release (milliseconds) 
        #pausing frequency, center and range (pause every x notes)
        #length, mean and variance (pause for x seconds)
        #songlength
    cur.execute("DROP DATABASE userstudy;")
    cur.execute("CREATE DATABASE userstudy;")
    os.system("python2 manage.py makemigrations")
    os.system("python2 manage.py migrate")
    cur.execute("USE userstudy;")
    query_gene1 = "INSERT INTO study_soundgene (emotion) VALUES ('happy')"
    cur.execute(query_gene1)
    db.commit()
    query_gene2 = "INSERT INTO study_soundgene (emotion) VALUES ('sad')"
    cur.execute(query_gene2)
    db.commit()
    '''
    for i in range(100,110):
        s = format(i, '03')
        HappySong[20] = "audio/" + s + "h.wav"
        SadSong[20] = "audio/" + s + "s.wav"
        SurprisedSong[20] = "audio/" + s + "su.wav"
        AngrySong[20] = "audio/" + s + "a.wav"
        createSong(HappySong)
        createSong(SadSong)
        createSong(SurprisedSong)
        createSong(AngrySong)
        '''
        queryh = "INSERT INTO study_sound (sound, date_added, gene_id) VALUES ('{}', '{}', '{}');".format(HappySong[20], time.strftime('%Y-%m-%d %H:%M:%S'), 1)
        cur.execute(queryh)
        db.commit()
        querys = "INSERT INTO study_sound (sound, date_added, gene_id) VALUES ('{}', '{}', '{}');".format(SadSong[20], time.strftime('%Y-%m-%d %H:%M:%S'), 2)
        cur.execute(querys)
        db.commit()
    cur.close()
    del cur
    db.close()
    '''

