# Term Project for CS300 | Winter 2022 | Portland State University #

Group Members | Github
------------- | -------------
Alana Gilston | [abluescarab](https://github.com/abluescarab)
Alex Harris   | [LazG7](https://github.com/LazG7)
Alissa Friel  | [xuvea](https://github.com/xuvea)
Evan La Fleur | [evanlafleur](https://github.com/evanlafleur)
Henry Kaus    | [henrykaus](https://github.com/henrykaus)
Nate Callon   | [ncallonpsu](https://github.com/ncallonpsu)

## Brief Description ##
**Chocoholics Anonymous**, or ChocAn, is a service that provides support and rehabilitation for chocolate addicts. Our term project is to design a system that allows employees to manage, provide, and bill services to ChocAn members.

## How to Compile/Run ##
The program requires Python 3.8.10 or newer to run. Ensure that the `faker` library is installed before running.
```bash
# Install the "faker" library
$ pip install faker
# Run the program
$ python3 main.py
# Run unit tests
$ python3 -m unittest main.py
```
The program also may be run with the `--help` flag to check any command line arguments.

## Invalid or Suspended User IDs ##
**NOTE**: Members are in the ranges of 1-7 in the starting digit possition, Providers start with 8 and Managers start with 9.

* Suspended - User ID that is temporarily disabled and can be renabled either by ChocAn IT or when a Member has paid dues.

* Invalid - The User ID ***cannot*** ever be reused in the future as this status is to indicate that the ID has been essentially deleted from the system.

List of "Suspended" or "Invalid" user IDs|
------------------------------------------
208281605 | Invalid |
294811466 | Invalid |
326194733 | Suspended |
831410219 | Suspended |
836251779 | Invalid |
841330483 | Suspended |
925747948 | Invalid |
963818730 | Suspended |