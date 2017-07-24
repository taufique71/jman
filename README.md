# widespace-job-manager

This app was developed as a test project for Widespace Bangladesh



### Prerequisites
* Python 3 [Obigatory]
* MySQL (up and running) [Obligatory]
* Virtualenv [Suggested]



### How to run

##### If `Virtualenv` is installed

Virtualenv helps to avoid version related problems of pip packages.
That is why it is suggested here.

* `git pull git@github.com:taufique71/widespace-job-manager.git`
* `cd widespace-job-manager`
* `virtualenv -p <path of python executable> ./`
* `source ./bin/activate`
* `pip install -r requirement.txt`
* `python main.py`

##### If `Virtualenv` is not installed

Now you are responsible if pip packages conflict due to version.

* `git pull git@github.com:taufique71/widespace-job-manager.git`
* `cd widespace-job-manager`
* `pip install -r requirement.txt`
* `python main.py`


The app should be up and running. To learn about how to use it please refer to the usage section.



### Configure
`config.json` file should hold the configurations needed for the app. 
Both job configuration and database configuration should reside in this file.
A sample configuration is give with this project.
Just editing this file would suffice for configuration.


### Usage
Once configuration is done it's time for usage.
It's a command line application.
When the app runs command can be given from the console. 
The app takes following commands -
* `start` - Starts all job processing from current state
* `start <job_key>` - Starts processing specific job from current state
* `stop` - Stops all job processing but save current state so that again it can be started from where it was stopped
* `stop <job_key>` - Stops processing specific job
* `status` - Prints status of all jobs. Following are possible status of a job -
    * `queued` - Queued for processing but not started yet for some reason. May be due to dependency, may be due to scheduled time. Can be stopped by stop command.
    * `processing` - Execution is ongoing. Can be stopped by stop command. Once stopped can't be resumed. Starting it again means processing would restart.
    * `success` - Execution finished successfully. Can't be stopped or started again unless restart command is given.
    * `failed` - Execution failed for some reason. Can be restarted with start command.
    * `stopped` - Stopped by default or someone stopped it. Can be started with start command.
* `status <job_key>` - Prints status of specific job
* `restart` - Terminates all current job processing and restarts from the scratch
* `exit` - Terminates all current job processing and gets out of the program
