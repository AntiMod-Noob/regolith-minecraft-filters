import os
import sys
import json
import shutil

def main():
    # 1. Parse settings (Regolith passes these as a JSON string in argv[1])
    try:
        settings = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    except (json.JSONDecodeError, IndexError):
        settings = {}

    target_path = settings.get("target_path")
    if not target_path:
        print("Error: 'target_path' is not defined in filter settings.")
        sys.exit(1)
    
    if type(target_path) is not str:
        print("Error: 'target_path' must be a string in filter settings.")
        sys.exit(1)
        
    copy_packs = settings.get("copy_packs")
    if copy_packs is None:
        print("Error: 'copy_packs' is not defined in filter settings.")
        sys.exit(1)
    
    if type(copy_packs) is not bool:
        print("Error: 'copy_packs' must be a boolean in filter settings.")
        sys.exit(1)
    
    world_template_path = settings.get("world_template_path")
    if not world_template_path:
        print("Error: 'world_template_path' is not defined in filter settings.")
        sys.exit(1)
    
    if type(world_template_path) is not str:
        print("Error: 'world_template_path' must be a string in filter settings.")
        sys.exit(1)

    # 3. Define the Mapping: Source Folder -> Destination Subfolder
    # Minecraft World Templates expect packs inside specific subfolders
    mapping = {
        f"data/{world_template_path}": ""  # Contents of world_template go to root
    }
    if copy_packs:
        mapping["BP"]="behavior_packs/bp"
        mapping["RP"]="resource_packs/rp"

    # Optional: Clear the target folder first to ensure a clean export
    if os.path.exists(target_path):
        print(f"Cleaning target directory...")
        # Be careful: only use rmtree if you are sure target_path is the project folder
        shutil.rmtree(target_path) 
        os.makedirs(target_path, exist_ok=True)

    for source, destinationSubFolder in mapping.items():
        source_path = os.path.abspath(source)
        dest_path = os.path.join(target_path, destinationSubFolder)

        if os.path.exists(source_path):
            print(f"Copying {source} -> {dest_path}...")
            os.makedirs(dest_path, exist_ok=True)
            # Use dirs_exist_ok=True to merge rather than crash
            shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
        else:
            print(f"Skipping {source}: Folder does not exist.")

    print("Success: World template export finished.")

if __name__ == "__main__":
    main()