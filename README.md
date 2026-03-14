# Podcast Splitter

Another CLI utility by Gabriele Murara for splitting an MP3 file into smaller files based either on a specified number of seconds or on detected silence.

It can be useful, for example, when listening to long podcasts on devices such as older MP3 players that handle fast-forwarding within a track poorly.

---

## ✨ Features

- Split long MP3 files into smaller tracks.
- Split audio either by a fixed duration (seconds) or by detected silence.
- Useful for podcasts, DJ sets, and long recordings.
- Command-line interface designed for quick batch processing.
- Generates multiple audio segments while preserving the original audio quality.

## 📦 Installation

### 💻 Install in development mode

```bash
git clone https://github.com/gabriele-murara/podcast-splitter.git
cd podcast-splitter
pip install -e .
```

### 🚀 Build a wheel

```bash
python update_project.py
python -m build
pip install dist/podcast_splitter-<version>-py3-none-any.whl
```

### 🔗 Install for use in another project

```bash
pip install --extra-index-url https://pip.murara.computer \
            --trusted-host pip.murara.computer \
            podcast-splitter
```

### 📝 Adding to requirements.txt

```
--index-url https://pypi.org/simple
--extra-index-url https://pip.murara.computer
--trusted-host pip.murara.computer

podcast-splitter==1.2.0
```

### 🛠️ Requirements

- python>=3.6
- ffmpeg

## 📦 Dependencies

### ℹ️ Installation Note

This project depends on two small libraries maintained by the same author:

- [`boolifyer==1.0.0`](https://pip.murara.computer/boolifyer/) – used to convert string values from environment variables into booleans.
- [`nano-logger==1.2.0`](https://pip.murara.computer/nano-logger/) – used for logging messages to the console or to a file.

These dependencies are available through the author's **public Python package index** (served over HTTPS) and can therefore be installed automatically during the normal installation process.

For full transparency, the source code of both libraries is also publicly available on GitHub. If you prefer, you can review, download, and install them directly from their respective repositories:

- [`boolifyer` GitHub repository](https://github.com/gabriele-murara/boolifyer)  
- [`nano-logger` GitHub repository](https://github.com/gabriele-murara/py-nano-logger)

This allows users to choose the installation method they trust the most.

---

## ⚙️ Configuration

The application supports multiple configuration sources with the following priority order (highest to lowest):

1. Command-line arguments  
2. Values defined in a `.env` file  
3. Environment variables  
4. Built-in default values  

This means that command-line parameters always override everything else.

---

### 🔁 Configuration Priority Example

If `--seconds` is passed via CLI, it will be used.  
Otherwise:

- If `SPLIT_SECONDS` exists in `.env`, it will be used.
- Else if `SPLIT_SECONDS` exists as an environment variable, it will be used.
- Otherwise, the default value will be applied.

---

### 📄 `.env` File

You can create a `.env` file in the project root.

A sample configuration file named `.env.sample` is included in the repository so you can create your own configuration file by copying it:

```bash
cp .env.sample .env
```

Then edit the `.env` file with your configuration values:

```
OUTPUT_DIRECTORY=/path/to/splitted_files/
SPLIT_SECONDS=60
SPLIT_BY_SILENCE=0

NANO_LOGGER_NAME=nano_logger_from_env
NANO_LOGGER_LOG_FILE_PATH=/var/log/my-project/nano_logger_from_env.log
NANO_LOGGER_LOG_LEVEL=INFO
NANO_LOGGER_WRITE_TO_CONSOLE=true
NANO_LOGGER_FORMAT="%(asctime)s %(process)d: %(levelname)s - %(message)s"
NANO_LOGGER_SUPPRESS_WARNINGS=true
```

---

### 🌍 Environment Variables

The same values can be provided as environment variables:

```bash
export OUTPUT_DIRECTORY=/path/to/splitted_files/
export SPLIT_SECONDS=60
export SPLIT_BY_SILENCE=0

export NANO_LOGGER_NAME=nano_logger_from_env
export NANO_LOGGER_LOG_FILE_PATH=/var/log/my-project/nano_logger_from_env.log
export NANO_LOGGER_LOG_LEVEL=INFO
export NANO_LOGGER_WRITE_TO_CONSOLE=true
export NANO_LOGGER_FORMAT="%(asctime)s %(process)d: %(levelname)s - %(message)s"
export NANO_LOGGER_SUPPRESS_WARNINGS=true

```

---

### 🧾 Default Values

| Parameter     | Shortcut | Environment Variable | Default      |
|--------------|----------|--------------|--------------|
| `--filename`     | `-f`     | None           | *(required)* |
| `--output_directory`     | `-o`     | `OUTPUT_DIRECTORY`           | *(required)* |
| `--seconds`     | `-s`     | `SPLIT_SECONDS`           | 60           |
| `--by-silence`     | `-b`     | `SPLIT_BY_SILENCE`           | False        |
| `--verbose` | `-v`     | `NANO_LOGGER_WRITE_TO_CONSOLE`       | False        |

> Parameters marked as *(required)* must be provided through one of the configuration sources.

Configuration of `nano-logger` is outside the scope of this project.  
For full details, please refer to the README in the `nano-logger` repository.


By default, log messages are written to the file `nano_logger.log` in the operating system's temporary directory.

If you want to change the file location or adjust the logger's behavior, configure the environment variables related to `NANO_LOGGER`.

## 📖 Help

```commandline
podcast-splitter --help
```

```
usage: Podcast Splitter [-h] [--version] -f FILENAME [-d DIRECTORY] [-s SECONDS] [-b] [-o OUTPUT_DIRECTORY] [-v] [--envs]

A program that splits audio tracks and applies metadata.

options:
  -h, --help            show this help message and exit
  --version             Show the version number
  -f FILENAME, --filename FILENAME
                        The filename of the track to split.
  -d DIRECTORY, --directory DIRECTORY
                        The directory containing tracks to split.
  -s SECONDS, --seconds SECONDS
                        The duration in seconds of each split track.
  -b, --by-silence      Split the track by detected silence. If this flag is used, --seconds is ignored.
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        The destination directory for split files.
  -v, --verbose         Show log messages in the console.
  --envs                Print environment variables.
```


## 📌 Usage Examples

### 1. Split a single track by duration

Split an audio track into smaller files of a specific length (in seconds):

```commandline
podcast-splitter -f episode1.mp3 -s 600 -o /path/to/output/
```

Splits `episode1.mp3` into 10-minute segments (600 seconds each) and saves the resulting files in the 
`/path/to/output/episode1_splitted` directory.

Each track's title tag is `episode1_01.mp3`, `episode1_02.mp3`, etc.
The album's title tag is `episode1`.

### 2. Split a track by silence

```commandline
podcast-splitter -f episode2.mp3 -b -o /path/to/output/
```

Splits `episode2.mp3` wherever silence is detected. The --seconds option is ignored in this mode. 
Results are saved in /path/to/output/episode2_splitted.

Each track's title tag is `episode2_01.mp3`, `episode2_02.mp3`, etc.
The album's title tag is `episode2`.

### 3. Enable verbose logging

```commandline
podcast-splitter -f episode3.mp3 -s 300 -v
```

Shows detailed log messages in the console while splitting episode3.mp3 into 5-minute segments (300 seconds). 
The files are saved in the folder specified by `OUTPUT_DIRECTORY`.


### 4. Print environment variables

```commandline
podcast-splitter --envs
```

---

## ⚖️ License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🤝 Contributing

Contributions are welcome! If you’d like to improve NanoLogger, feel free to open an issue or submit a pull request.

---

## 👤 Author

Developed by Gabriele Murara

---

## ✉️ Contact

For any questions or support, please reach out to [gabriele@murara.computer].

---
