# Tournament Manager

[Roundnet](https://en.wikipedia.org/wiki/Roundnet) is a game played between two teams of two players. Roundnet
tournaments are run with one to many divisions (skill levels). A division has many teams sign up for it. A team can only
sign up for one division. A division has many matches amongst teams within a division. Each match consists of one to
many games where the team that wins the majority of the games wins the match.

Tournament Manager is a native Python application leveraging Python's Tk GUI toolkit
([Tkinter](https://docs.python.org/3/library/tkinter.html)) and using MySQL interface
([PyMySQL](https://pypi.org/project/PyMySQL/)) to communicate with the designed SQL storage database. The app allows
users to create/update/delete tournaments, tournament divisions, division teams, division matches, and game scores
within a match.

## Requirements

### Python >= 3.6

Most systems will have Python installed, to verify your version run `python3 --version` in your command line. If your
version is lower than 3.6 or the command does not return a version number, visit the Python [downloads page](https://www.python.org/downloads/) and download
the latest version.

### Tkinter

Tkinter comes pre-installed with the Python installer binaries, but if you don't have Tkinter installed you can run
`pip3 install tk` in your command line.

### PyMySQL

PyMySQL does not come pre-installed and can be installed by running `pip3 install PyMySQL` in your command line.

## Installation

Clone the repository using your preferred cloning method or download the ZIP.

## Setup

### Backend
Utilize the included database dump `/back_end/dump.sql` to setup the MySQL database using your preferred database
management tool.

### Frontend
Adjust `host` and `db_name` in `front_end/main.py` based on the results of the previous section. 

## Usage

Navigate to the `front_end` directory and run `python3 main.py` in your command line.

## Project Status

The project is fully functional and meets all the set goals. As this was my first time creating a python application,
using Tkinter, and working with a SQL storage database there is significant room for improvement. However, as this was
for a course project and there exists competing solutions I am unlikely to continue work on the project. This project
was a fantastic learning experience and I hope to bring my newfound knowledge to future endeavours.

Note: I worked on this project with https://github.com/bradleybares/ locally on their machine, then copied the repository from their github.
