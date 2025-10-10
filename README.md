# Distributed-Alarm-System

## How to Run Resource Based Arch
```
cd resource_based
docker compose up --build
```
Once the example_frontend_app container is running, then visit http://localhost:8080.

If this is the first time you start this application, then there will be no accounts available.

Get started by signing up with an account to then enter the Dashboard. 

Disclaimer: there is no password recovery option, so be sure to remember your credentials. Or you can make another account that does not have the same username.

From the Dashboard, you are able to add alarms for particular times along with a message. Once added, they will be scheduled, and then populate the Scheduled Alarms tab.

Under the Scheduled Alarms tab, you can see all alarms that are scheduled. You are able to delete alarms or edit their execution time and message.

Note that when you add alarms that are before the current time (e.g. adding an alarm for 5:00AM when it is 12:00PM), that alarm will be scheduled for the next day. The same principle applies when editing an alarm time to before the current time.

Adding alarms for the current time (e.g. adding an alarm for 12:00PM when it is 12:00PM) will result in an immediate notification.

Under the Notifications tab, this is where notifications are pushed when a Scheduled Alarm is due. 


## Clean Up after running Resource Based Arch
```
// assuming still in the resource_based directory
docker compose down
```

## How to run Arch2
```
cd arch_2
docker compose up --build
```

## Clean Up after running Arch2
```
// assuming still in the arch_2 directory
docker compose down
```

## Disclaimer
- As of right now, you must Clean Up if you want to switch arch