import json
import jobmanager

def main():
    config = json.loads( open("config.json").read() )
    out_file=open("./test_scripts/out.txt", "w")
    manager = jobmanager.Manager(config, stdin=None, stdout=out_file, stderr=None)
    while True:
        command = input("")
        command = command.lower()
        command = command.split(" ")
        if command[0] == "exit":
            manager.exit()
            print("Exiting program ...")
            break;
        elif command[0] == "status":
            status = manager.status()
            print("------------------")
            print("Current Job Status")
            print("------------------")
            if len(command) > 1:
                print(command[1], "-", status[command[1]])
            else:
                for key, val in status.items():
                    print(key, "-", val)
            print("------------------")
        elif command[0] == "start":
            if len(command) > 1:
                manager.start(command[1])
            else:
                manager.start()
        elif command[0] == "stop":
            if len(command) > 1:
                manager.stop(command[1])
            else:
                manager.stop()
        elif command[0] == "restart":
            manager.restart()
        else:
            print("[manager] > Invalid command")

if __name__ == "__main__":
    main()
