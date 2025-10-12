# Distributed-Alarm-System

## How to Run Resource Based Arch
```
cd resource_based
docker compose up --build
```

## Using the Example Fontend App

Once the example_frontend_app container is running, then visit http://localhost:8080.

If this is the first time you start this application, then there will be no accounts available.

Get started by signing up with an account to then enter the Dashboard. 

Disclaimer: there is no password recovery option, so be sure to remember your credentials. Or you can make another account that does not have the same username.

From the Dashboard, you are able to add alarms for particular times along with a message. Once added, they will be scheduled, and then populate the Scheduled Alarms section.

Under the Scheduled Alarms section, you can see all alarms that are scheduled. You are able to delete alarms or edit their execution time and message.

Note that when you add alarms that are before the current time (e.g. adding an alarm for 5:00AM when it is 12:00PM), that alarm will be scheduled for the next day. The same principle applies when editing an alarm time to before the current time.

Adding alarms for the current time (e.g. adding an alarm for 12:00PM when it is 12:00PM) it will be registered at that time and a notification will be sent within around 1-2 seconds.

Under the Notifications section, this is where notifications are pushed when a Scheduled Alarm is due. 

## How to Run Resource Based Arch with Locust
```
cd resource_based/locust
docker compose up --build
```

## Using the Resource Based Arch with Locust

Once the locust_app container is running, then visit http://localhost:8089.

Input the corresponding values into the given fields and start the test.
Details about the locust test/workers can be found in /resource_based/locust/src/locustfile.py

This file will simulate a user, create and account and login. Once the registration is successful,
it then runs fetch commands on alarms and notifications every 0.5s (similar to the fontend app).

Then the workers will run corresponding tasks based on the weight given to them (@task(weight_val)).
The current task distribution is as follows:
* 34.8% createAlarm
* 21.7% deleteNotification
* 21.7% deleteSpecificAlarm
* 21.7% updateAlarm

The tasks are created based on what the user is able to do in the example frontend app.

## Clean Up after running Resource Based Arch
```
// assuming still in the resource_based directory
docker compose down

// if the locust file was ran, the same command can be run
// but you should be in the resource_based/locust directory
```

## How to run Microservice Based Arch
```
cd microservice_based
docker compose up --build
```

## Clean Up after running Microservice Based Arch
```
// assuming still in the microservice_based directory
docker compose down
```
