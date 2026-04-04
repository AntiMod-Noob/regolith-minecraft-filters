import os
import sys
import json
import shutil
import subprocess

def main():
    # 1. Parse settings (Regolith passes these as a JSON string in argv[1])
    try:
        settings = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    except (json.JSONDecodeError, IndexError):
        settings = {}

    prebuild_commands = settings.get("prebuild_commands")
    if prebuild_commands:
        if not isinstance(prebuild_commands,list):
            print("prebuild_commands must be an array of console command strings")
            return
        index = 0
        for cmd in prebuild_commands:
            if not isinstance(cmd,str):
                print(f"prebuild_commands[{index}] must be a console command string")
                return
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Success! Output: {result.stdout.strip()}")
            else:
                print(f"Error: {result.stderr}")
            index +=1

    
    outpath=os.path.abspath("./out")
    buildPath=os.path.abspath("../../build")
    if os.path.exists(outpath):
        shutil.rmtree(outpath)
    
    if os.path.exists(buildPath):
        shutil.rmtree(buildPath)
        
    os.makedirs(outpath,exist_ok=True)
    os.makedirs(buildPath,exist_ok=True)
    bppath=os.path.abspath("./BP")
    if os.path.exists(bppath):
        if len(os.listdir(bppath)) > 0:
            shutil.make_archive("bp","zip",root_dir=bppath)
            shutil.move("bp.zip",os.path.join(outpath,"bp.zip"))
    rppath=os.path.abspath("./RP")
    if os.path.exists(rppath):
        if len(os.listdir(rppath)) > 0:
            shutil.make_archive("rp","zip",root_dir=rppath)
            shutil.move("rp.zip",os.path.join(outpath,"rp.zip"))
    if len(os.listdir(outpath)) > 0:
        shutil.make_archive("build","zip",root_dir=outpath)
        shutil.move("build.zip",os.path.join(buildPath,"build.mcaddon"))
    else:
        print("Nothing to build")
    
            

if __name__ == "__main__":
    main()