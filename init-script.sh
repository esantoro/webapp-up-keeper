#!/bin/bash
### BEGIN INIT INFO
# Provides:          webapp-up-keeper
# Required-Start:    networking
# Required-Stop:     
# Should-Start:      
# Should-Stop:       
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Enabling webapp-up-keeper
# Description:       Keeps up web application on some cloud platforms.
### END INIT INFO

case "$1" in
start)  echo "Enabling webapp-up-keeper:"

	source /etc/webapp-up-keeper.conf
	cd $WEBAPP_UP_KEEPER_PATH
	source bin/activate
	python keeper.py --pidfile=$WEBAPP_UP_KEEPER_PIDFILE
        ;;
stop)   echo "Disabling webapp-up-keeper"
	source /etc/webapp-up-keeper.conf
	kill -9 `cat $WEBAPP_UP_KEEPER_PIDFILE`
        ;;
restart) echo "Not implemented yet: do stop and then start again."
        ;;
reload|force-reload) echo "Not implemented yet."
        ;;
*)      echo "Usage: /etc/init.d/mio_start_script.sh {start|stop|restart|reload|force-reload}"
        exit 2
        ;;
esac
exit 0
