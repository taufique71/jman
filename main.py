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
            manager.stop_processing()
            print("Exiting program ...")
            break;
        elif command == "status":
            job_status = manager.get_job_status()
            print("------------------")
            print("Current Job Status")
            print("------------------")
            for key, val in job_status.items():
                print(key, "-", val)
            print("------------------")
        elif command == "start":
            manager.start_processing()
        elif command == "restart":
            manager.stop_processing()
            manager.initialize_job_threads()
            manager.start_processing()

if __name__ == "__main__":
    main()
