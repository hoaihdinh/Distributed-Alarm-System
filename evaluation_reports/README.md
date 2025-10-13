# Evaluation Reports

These are reports generated using Locust. 

Evaluations for microservices architecture are under the `evaluation_reports/microservices/` directory.

Evaluations for resource-based architecture are under the `evaluation_reports/resource_based/` directory.

Files are named using this scheme:
```
<arch_acrynm>_<max_users>_<ramp>_<duration>
```
- arch_acrymn:
    - ms:  microservice architecture
    - rba: resource based architecture
- max_users: Max number of concurrent users
- ramp: Number of new users per second until max_users
- duration: All are 5m, for 5 minutes

These are the different scenarios covered, all are tested over a duration of approximately 5 minutes:
| Scenario | Number of users (peak concurrency) | Ramp up (users started/second) |
| --- | ---- | -- |
|  1  |    1 |  1 |
|  2  |   50 |  1 |
|  3  |  100 |  1 |
|  4  |  200 |  5 |
|  5  |  500 | 25 |
|  6  | 1000 | 75 |
