# musicxml2video
Convert an MusicXML score to play by your selected video sample

# Try it out!

1. `pip install ffmpeg and pydub`
2. Install `ffmpeg` in your system!
3. Try out the convertion by `python main.py`

# How to setup your own video
1. edit the `config.py` to change parameter!
2. To add instrument, go to `input` folder, then add an folder name of your instrument. Change the `input/{instrument}/{octave}/{note}.mp4` videos to match the request, for for which notes correspond to which sound, see below:

`
C => 1
C# => 2
D => 3
D# => 4
E => 5
F => 6
F# => 7
G => 8
G# => 9
A => 10
A# => 11
B => 12
`
3. Have fun!
