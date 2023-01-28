# podcast-splitter
A simple command line tool for split long audio files (like a podcast) into smaller tracks.

## Application

### Requirements

python-3.9

### Install

Create a virtual-env with:

```commandline
$ python3 -m venv your_virtual_env
$ cd your_virtual_env
$ . bin/activate
```

go to application directory and install requirements via pip

```commandline
$ cd podcast-splitter
$ pip install -r requirements.txt
```

### Configuration

By default, log messages are written to the file tracce_a_pezzi.log in 
the system's temp dir.
If you want to change the log path, copy .env.sample to .env and valorize
the LOG_FILE_PATH variable.

```commandline
$ cp .env.sample .env
```

Otherwise you can set the environment variable LOG_FILE_PATH 

```commandline
$ LOG_FILE_PATH=/tmp/from_env.log
$ export LOG_FILE_PATH
```

### Help

```commandline
$ python main.py --help
```

### Simple use

```commandline
$ python main.py -f /path/to/your/long_audio_file.mp3 -s 600 -o /path/to/output/ 
```

Split `long_audio_file.mp3` into tracks of 600 seconds (10 minutes). Output files 
are stored to `/path/to/output/long_audio_file_splitted`. 
Each track's title tag is `long_audio_file_1.mp3`, `long_audio_file_2.mp3`, etc.
The album's title tag is `long_audio_file`.




