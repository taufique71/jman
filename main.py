import json
import jobmanager

def main():
    config = json.loads( open("config.json").read() )
    out_file=open("./test_scripts/out.txt", "w")
    manager = jobmanager.Manager(config, stdin=None, stdout=out_file, stderr=None)
    while True:
        command = input("> ")
        command = command.lower()
        if command == "exit":
            print("Exiting program ...")
            manager.stop_processing()
            break;
        elif command == "status":
            # job_status = manager.get_job_status()
            print("########## Current Job Status ##########")
        elif command == "start":
            # manager.start_processing()
            print(command)
        elif command == "restart":
            # manager.stop_processing()
            # manager.start_processing()
            print(command)

if __name__ == "__main__":
    main()
