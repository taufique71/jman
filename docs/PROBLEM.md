### Background
In widespace we manage terabytes of data. Everyday we run lots of computation jobs on those data. Some of those do machine learning to get meaningful insight from data. Others do some ad hoc work to facilitate other systems. Apart from computation jobs we also have jobs that reads data from sources and then imports that data to a database (RDBMS, or NOSQL DB). 

We have a dedicated machine that fire jobs everyday at a fixed time or interval. One job may depend on one or more jobs for its processing. Almost all jobs indeed run on remote clusters and some jobs which need less CPU or IO run in the machine itself. Any job can fail at any time. The job status of each job whether it is succeeded or failed is notified to the interested parties. Your job is to develope an application that will automate this process that otherwise will be tedious. 


### Problem
A job will run on a day at a fixed time for once or interval. The application you will develop will run jobs when needed. You can consider all jobs are nothing but shell scripts and a script may or may not wait for completion of the job. Your application will not have any knowledge about the script or internal processing of the job. For simplicity you can also consider each job will run on a day for once.

Firing a job at once or regular interval everyday is not a problem. The problem here is a job may depends on one or more jobs to run its processing and some other jobs depend on the job too and vice versa. If a scheduled time is not mentioned, dependent jobs should run automatically after the finish of the jobs on which they depend. Dependent jobs should not run even if a schedule time is mentioned until all of their upstream jobs are not finished. A job will not depend on its dependent jobs anyway.

After running a job it may fail at any time. Once any job failed the further downstream job processing should get stopped and interested parties notified automatically. There should have a mechanism to start the failed jobs from where it stopped. You should also implement a mechanism so that the job can notify your application or your application can detect automatically if it finished processing successfully or not. A failed job may not able to notify that it failed. For each successful processing a job may write an entry to a database about the size of the data it generates. The interested parties should get notified if less or excessive amount of data are generated or any job takes time more than expected.

The application should be enough user friendly so that those who will use can add, remove, restart job execution etc. easily. It should maintain all the states somewhere so that we can understand about the status of the job.

### Implementation Criteria
* It should handle hundreds of jobs without any kind of manual intervention.
* It should take minimum time to trigger any job or notify parties.
* It can be a simple python app, java app or shell script as long as we can run it easily in our machine.
* Code composing and structure should be good and well documented.
* Vanilla MySQL


### Deliverables
* A shell script to deploy and run the application.
* Source code with a readme how to run.
* Document about the approach how you solve the problem.
* Necessary sql scripts to generate required tables and sample data.

