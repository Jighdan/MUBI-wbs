# MUBI-wbs
"Film of the Week" based on MUBI.com/showing page

### Flow
mubilifier.py extracts the movie data > storage_dude.py filters the films and updates de database > delivery_guy.py ships the movie via email

### Requeriments
requests, re, bs4, csv, smtplib, email, random, datetime
