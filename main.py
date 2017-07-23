import json
import jobmanager

def main():
    config = json.loads( open("config.json").read() )
    out_file=open("./test_scripts/out.txt", "w")
    manager = jobmanager.Manager(config, stdin=None, stdout=out_file, stderr=None)
    while True:
        command = input("")
        command = command.lower()
        if command == "exit":
            print("Stopping running jobs ...")
            manager.stop_processing()
            print("Exiting program ...")
            break;
        elif command == "status":
            job_status = manager.get_job_status()
            print("########## Current Job Status ##########")
            for key, val in job_status.items():
                print(key, "-", val)
        elif command == "start":
            manager.start_processing()
            print(command)
        elif command == "restart":
            manager.stop_processing()
            manager.re_initialize_job_thread()
            manager.start_processing()
            print(command)

if __name__ == "__main__":
    main()
