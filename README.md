# widespace-job-manager

This app was developed as a test project for Widespace Bangladesh



### Prerequisites
* Python 3 (obigatory)
* Virtualenv (suggested)



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
When the app starts command can be given from the console. 
The app takes four commands - `start`, `status`, `restart`, `exit`.
* `start` - Starts processing jobs depending on the job configuration
* `status` - Prints status of all jobs in console
* `restart` - Terminates all current job processing and restarts from the scratch
* `exit` - Terminates all current job processing and gets out of the program
