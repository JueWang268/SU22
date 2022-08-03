# SUMMER RESEARCH 2022 - Sound Generator

### *BARON WANG (Git username: ChenxuMurong)*


## Required Libraries

The sound generator requires toolkit [music21](https://web.mit.edu/music21) to run. Run
```sudo pip3 install music21``` on Mac or ```pip install music21``` on Windows to [install](https://web.mit.edu/music21/doc/installing/).

## Usage

randomSongGenerator.py is script that is used to generate random sound clips capable of expressing a certain emotion (happy, sad, content, or angry).

Use command line argument to specify which emotion to be associated with the sound. It defaults to happy songs.

```python3 randomSongGenerator.py [happy|sad|content|angry|h|s|c|a]```



## Reference Table

|                               |Content Happy|Excited Happy|Sad        |Angry    |Neutral (2 notes)|Reason / Theory|
|:-----------------------------:|:-----------:|:-----------:|:---------:|:-------:|:---------------:|:-------------:|
|Ascending / Descending / Random|ascending    |ascending    |descending|descending|Ascending        |               |
|Range F0                       | B-4 to C#6  |B-4 to F#6   | A2 to C4 | A2 to G3 |C4, G4(just 2 notes)|higher range => happier|
|Tempo (referent = half note)   |70           |  150        |   60     |    150   |  100            |higher tempo => more excitement|
|Key Signature                  |C Major      |     C Major |C Minor   |   C Minor| C Major         |Major sounds happy, minor sounds sad|
|Articulations                  |Tenuto, Unstress, DetachedLegato|Staccato, Spiccato, Staccatissimo|Tenuto, Unstress, DetachedLegato|Staccato, Spiccato, Staccatissimo, Strong accent|No|Short, detached articulations are better at expressing happy, excited emotions|
|Probability of generating notes or rest|90% for notes, 10% for rests|80% for notes, 20% for rests|90% for notes, 10% for rests|90% for notes, 10% for rests|No rests|works in conjunction with rest lengths|
|Number of notes|20|20|10|30|2|slower songs have fewer notes|






