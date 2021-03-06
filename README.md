# ParkingLot

## Overview
### Purpose

This is a simple Django app that is meant to allow posting and answering questions, without requiring a login.

It's functionality is similar to [pigeonhole](http://pigeonhole.at/) but addresses the following shortcomings:

* This app allows you to write comments using Markdown syntax. For example, you can use embedded links.
* This app allows you to copy-and-paste from comments.
* This app allows editing of the last comment / post on a question.
* The questions and comments are not restricted once the course is over.

The decision was made to restrict editing to the most recent comment, as a comment in a thread might not make sense if
an earlier comment is edited. Because there is no required login, there has been no effort to restrict who can make
edits to the last post.

### Why no logins?

This application was made to assist with live trainings. The ability to set up new trainings (new "Parking lots") is
something that does require a login or use of the Django-admin panel. Because who signs up for trainings is often
considered private information, ability to view all "Parking Lots" also requires a log in.

Logins are _not_ required to do the following:
* View/submit questions in a parking lot
* View/submit comments or answers to questions

In order for a random user to gain access to a parking lot, it is required that she knows the parking lot's name. Again,
no causal browsing of lots is allowed!

### What is a ParkingLot?

A *ParkingLot* is a place where questions are collected. If using this for a specifc training, the idea is that there
should be one Parking Lot per training. There are dates attached to a Parking Lot, but these are for display purposes
only. A Parking Lot is still accessible once the training is complete.

## Installation

Once you have cloned/forked this repository, run the following commands (OSX/Linux)
```bash
conda env create -f environment.yaml
source activate ParkingLot
python manage.py runserver
```

On a windows machine, run
```bash
conda env create -f environment.yaml
activate ParkingLot
python manage.py runserver
```

Server should be up-and-running at http://127.0.0.1:8000

The database above comes with
* A superuser "admin", password "ParkingLot"
* There are two pre-made Parking Lots to play with:
  * "Acme", accessible either using "acme" on the homepage or via http://127.0.0.1:8000/acme/
  * "Stones'n'Swords", accessible either using the name on the homepage or via http://127.0.0.1:8000/stonesnswords/

### Built-in accounts

These are test accounts only for use on the demo system.

| Account name | Password | Privileges |
| --- | --- | --- |
| admin | ParkingLot | Superuser / admin privileges |
| damien | ParkingLot | Superuser / admin |
| voldemort | KillerCat | Staff user (can log into `/admin`) |
| delenn | OfTheGrey | Registered user |

At the moment, the only way to add or remove users is though the admin site http://127.0.0.1:8000/admin

The users `admin`, `damien` and `voldemort` have the ability to log on to the admin site.

The user `delenn` cannot, but should be able to view parking lots and add new ones.

The only restricted routes (i.e. off limits to non-logged in users) other than the admin panel are

* `/lots/` (i.e. an anonymous user cannot see all training groups)
* `/lots/new/` (i.e. an anonymous user cannot create new training groups)

Everything else is login agnostic.

## References

This project was largly based off the open sourced [Django tutorial](https://simpleisbetterthancomplex.com/series/beginners-guide/1.11/) by Vitor Freitas.
