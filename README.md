# Distributed-Alarm-System

There are two different distributed system architectures used to develop similar apps.
Microservice based architecture using gRPC to communicate between nodes
and a Resource Based architecture using HTTP to communicate between nodes.

The core required key functionalities provided in both apps are as follows:
1) Add alarms 
2) Update existing alarms
3) Delete alarms
4) List upcoming alarms
5) Notify user based on alarms data

Once the respective applications are up and running, users only need to interact with the provided frontend apps through http://localhost:8080 (microservices) or http://localhost:8081 (resource-based).

Both applications allow users to sign up or sign in. 
- **Disclaimer:** there is no password recovery option, so be sure to remember your credentials. Or you can make another account that does not have the same username.

Once signed in, the dashboard consists of:
* Section to add new alarms:
    * Adding a new alarm is as simple as filling out the corresponding fields for a title/message and time, then clicking the add button.
    * Adding alarms that are before the current time (e.g. adding an alarm for 5:00AM when it is 12:00PM) will be scheduled for the next day.
    * Adding alarms that are at the current time (e.g. adding an alarm for 12:00PM when it is 12:00PM) will be scheduled for the next day.
* Section listing scheduled alarms:
    * This section lists all alarms scheduled and not notified to the user yet. Users are able to edit alarms and change the title/message and/or the trigger time. Users are also able to remove scheduled alarms before the respective trigger times.
* Section listing notifications:
    * This section is how the application notifies its users when an alarm is triggered. When an alarm is due, it is removed from the table (in the Scheduled Alarms section) and a corresponding notification appears in this section. Users are able to dismiss received notifications.

## Microservice Architecture
### How to run Microservice Architecture
```
cd microservice_based
docker compose up --build
```
Once the api_gateway_MS container is running, then visit http://localhost:8080.

### How to run the Microservice Architecture with Locust
```
// In a terminal
cd microservice_based
docker compose up --build

// Open a new terminal
cd microservice_based
[locust command goes here]
```
Once the locust application is running visit [link goes here].


### Clean Up after running Microservice Based Architecture
```
// assuming still in the microservice_based directory
docker compose down
```

## Resource Based Architecture
### How to Run Resource Based Architecture
```
cd resource_based
docker compose up --build
```
Once the example_frontend_app_RBA container is running, then visit http://localhost:8081.

### How to Run Resource Based Architecture with Locust
```
cd resource_based/locust
docker compose up --build
```
Once the locust_app container is running, then visit http://localhost:8089.

Input the corresponding values into the given fields and start the test.
Details about the locust test/workers can be found in /resource_based/locust/src/locustfile.py

This file will simulate a user, create and account and login. Once the registration is successful, it then runs fetch commands on alarms and notifications every 0.5s (similar to the example_frontend_app_RBA).

Then the workers will run corresponding tasks based on the weight given to them (@task(weight_val)).
The current task distribution is as follows:
* 34.8% createAlarm
* 21.7% deleteNotification
* 21.7% deleteSpecificAlarm
* 21.7% updateAlarm

The tasks are created based on what the user is able to do in the example frontend app.

### Clean Up after running Resource Based Architecture
```
// assuming still in the resource_based directory
docker compose down

// if the locust file was ran, the same command can be run
// but you should be in the resource_based/locust directory
```
