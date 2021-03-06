# musicxml2video
Convert an MusicXML score to play by your selected video sample

## Try it out!

### By scripts!
1. In debain based system: `apt-get install -y ffmpeg python python-pip`
2. `pip install pydub ffmpeg-python`
3. Try out **musiclxml2video** by `python main.py`
4. Play the video inside `tmp/{timestamp}/output.mp4`

### By docker!
1. Use this command `sudo docker build -t musicxml2video . && sudo docker run --name musicxml2video -t musicxml2video && sudo docker cp musicxml2video:/musicxml2video/tmp/. tmp && sudo docker rm musicxml2video`
2. Play the video inside `tmp/{timestamp}/output.mp4`

## How to setup your own video Manually
1. edit the `config.py` to change parameter!
2. To add instrument, go to `input` folder, then add an folder name of your instrument. Change the `input/{instrument}/{octave}/{note}.mp3` audio to match the request, for for which notes correspond to which sound, see below:

```
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
```

3. Copy the video into `input/{instrument}/video.mp4`

Note: You can see `input/woah/` as an example for how the folder shouold be layout

## How to setup your own video Automatically (Linux only) (One video input only)
1. You need to download Audacity first, it will be the software to help us do the batch auto tunning
2. Locate the Audacity Macro folder, for mind is located on `~/snap/audacity/190/.audacity-data/Macros`
3. Move the `utiles/audacity_batch_change_pitch_macro.txt` into the macro folder above, for how I genearte the Macro you can read the `utils/audacity_macro_generator.py`.
4. Execute the Marco using Audacity Marco by file, choose the file of your choice, and wait a bit
5. The file executed should be from `file_name`001 to `file_name`096, play the files to make sure it is ok
6. Finally, reformat the audio from Audacity format to the format this program can handle, you can use the `utils/audio_file_reformatter.py`, you probably need to change some config before using it

Have fun!
