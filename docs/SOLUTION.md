### Technology Used
* Python 3.6
* MySQL

### Implemented Features
Following are the features included in the app.
For details on how to use it please refer to the [README](https://github.com/taufique71/widespace-job-manager/blob/master/README.md).

* Input via configuration file
* Can process multiple jobs at a time if dependency allows it
* All the jobs can be started or stopped anytime, at a time
* Individual jobs can be started or stopped any time
* All jobs can run automatically depending on the dependency defined in configuration file. No manual intervention is needed.
    * If a scheduled time is not mentioned, dependent jobs run automatically after the finish of the jobs on which they depend
    * Dependent jobs wait until all of their upstream jobs are not finished even if a schedule time is reached. 
    * If any job fails, further downstream job processing gets stopped and user is notified automatically.
* Application can monitor the status of a under processing job. It notifies the user when a job finishes successfully or fails during processing.
* User can start a failed job any time. When previously failed job finishes successfully all blocked downstream job processing are triggered automatically.
* Application monitors the amount of generated data and execution time of jobs. If any job takes more time than it should take or generates more data that it should generate, application notifies the user automatically.

### Unimplemented Features
* Couldn't manage time to provide interface for adding or removing jobs to the job queue
* Briefly looked for free smtp servers to send email. 
  Couldn't find any one with a simple look up. 
  So didn't implement email sending feature when interested parties are supposed to be notified.
  But application design will allow sending email as notification with very little refactor if any smtp servers are available.

### High Level Explanation of Solution Approach

Job dependency resembles a DAG(Directed Acyclic Graph). 
So a graph data structure is created from given dependency, where a job means a vertex and edge (job<sub>1</sub>, job<sub>2</sub>) means job<sub>1</sub> depends on job<sub>2</sub> for processing.
Vertices of the graph having zero outdegree means jobs corresponding to the vertices have no dependency.
When app starts processing, it takes the vertices with zero aoutdegree and starts processing each job in separate thread.
When a job finishes following changes occur in the order they appear - the thread ends, vertex corresponding to the job is removed from the graph, graph is rechecked for new zero outdegree vertices and if any then job corresponding to that vertex starts to run in another separate thread.

### Implementation Details

##### Module Overview
Four modules were developed - 
* `jobmanager` - Only module used my main function of the application. Manages all kind of job related operations; handles start, stop, restart and exit events.
    * Initiates job processing in threads when it's appropriate. Automates job execution one after another.
    * Initiates monitoring database log.
    * Synchronizes running threads when its time to stop.
    * Uses lock to avoid race conditions when two jobs finish at a time and tries to update the state of the manager
* `graph` - Includes graph data structure used by jobmanager module.
    * As graph data structure *edge list* is implemented.
* `joblogmonitor` - Includes thread which monitors database log. Used by jobmanager module.
    * `pymysql` is used to connect to MySQL database.
* `job` - Includes thread which handles job execution; monitors executing jobs; detects if job finished successfully or failed. Used by jobmanager module.
    * `subprocess` module is used to execute shell scripts.
    * `psutil` module is used to monitor child processes and kill them when needed. Processes were killed with SIGTERM signal.

##### Diagram corresponding to module usage 
```
                                 __main__
                                    ^
                                    |
                                    |
  joblogmonitor   --------->   jobmanager   <---------   graph
                                    ^
                                    |
                                    |
                                   job

```

##### Heuristic used to monitor job execution
This is not a full proof soulution but this is the heuristic that has been used to monitor if a job execution is successful or failed.
However, app was designed in such a way so that monitor logic can be changed easily if better heuristic is found.
* If process status is not zombie and not dead then job is considered `processing`
* If process status is not zombie but dead then job is considered `failed`
* If process status is zombie -
    * If any children of the process is left in the process table - 
        * If any children is dead then job is considered `failed`
        * If no children is dead then job is considered `processing`
    * If no children left in the process table - 
        * If parent process (app) could communicate with the process without err then job is considered `success`
        * If parent process (app) couldn't communicate with the process without err then job is considered `failed`

##### Assumption about log table structure
App assumes that table of the database where logs would be written by scripts would have following columns -
```sql
  `id` int(11) NOT NULL,
  `job_key` varchar(45) NOT NULL,
  `exec_time` int(11) NOT NULL,
  `amount_of_data` int(11) DEFAULT NULL,
  `timestamp` datetime,
  PRIMARY KEY (`id`)
```

