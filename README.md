# Pypopro.py

Post-processing tool used by the french-speaking podcast
[NipSource](http://nipcast.com/category/nipsource/).

Jitsi Meet supports recording but it splits each speaker's track in different
mp3 files.

This script can create a bash script which will use sox to make one file per
speaker.

## Workflow

1. Put this script in the directory of the jitsi recoring (it contains
 metadata.json and mp3 files)

2. Call `./pypopro.py > extract.sh` to create the script.

3. Review the script: `view extract.sh`

4. Execute the script if it works: `chmod +x extract.sh && ./extract.sh`

5. The files are called `final_*.wav`

6. Import the wav files in audacity and do the post-processing.

## Requirements

* python 2.7
* sox

## License

This work is published under GPL-2.

## See also

* [Jisti Meet](https://jitsi.org/Projects/JitsiMeet)
* [Jipopro](https://github.com/jitsi/jipopro): an alternative in Java, which
 inspired this work
