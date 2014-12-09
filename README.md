# webapp-up-keeper 
---------------------

## Why ?

Some cloud platform (one in particular) offer a free plan to run cloud web
application, but shut them down when no requests are received for a certain
amount of time.

This python application tries to keep them up, by sending an HTTP request
from time to time, in order to prevent the platform from shutting the web 
application down and preventing users from experiencing huge load times (which
would be actually due to application load times more than application response
time instead).

## What is this, actually ?

This is a unix daemon. Written in Python.

## How do i run it ?

Basically, five steps:

1. Copy the init-script: `cp init-script.sh /etc/init.d/webapp-up-keeper`
2. Make the init-script executable: `chmod +x /etc/init.d/webapp-up-keeper`
3. Copy the `webapp-up-keeper.conf` script to etc: `cp webapp-up-keeper.conf /etc/`
4. Adjust settings (mostly set the `WEB_APP` variable)
5. Run it: `/etc/init.d/webapp-up-keeper start`
