import json
import jobmanager

def main():
    config = json.loads( open("config.json").read() )
    out_file=open("./test_scripts/out.txt", "w")
    manager = jobmanager.Manager(config, stdin=None, stdout=out_file, stderr=None)
    manager.start_jobs()

if __name__ == "__main__":
    main()
