# neatify

A command-line tool that scans and organizes files from a messy folder (like Downloads) into categorized subfolders (like Documents, Images, Code, etc.).

Useful for keeping your system clean and automating the boring parts of file management.

## Installation

Clone the repo:

```bash
git clone https://github.com/izaaksarnecki1/neatify.git
cd neatify
```

Create a virtual enviornment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Running:

```bash
python3 main.py --source {source_folder} --dest {destination_folder}
```
