import os, json, shutil,yaml
from kh2lib.kh2lib import kh2lib
lib = kh2lib()

# I think this will work nicely the only issue is you need to duplicate every instance of "566", not just the first one

TITLE = "Sora Climbers"


CHANGESPAWNS = True
spawndir = os.path.join(os.environ["USE_KH2_GITPATH"], "subfiles", "spawn", "ard")
if CHANGESPAWNS:
    if os.path.exists("spawns"):
        shutil.rmtree("spawns")

assets = []

changedards = {}

if CHANGESPAWNS:
    for root, dirs, files in os.walk(spawndir):
        path = root.split(os.sep)
        for f in files:
            fn = os.path.join(root, f)
            subfn = fn.replace(spawndir, '')
            if subfn.startswith(os.sep):
                subfn = subfn[1:]
            print(subfn)
            with open(fn) as f:
                spawn = yaml.load(f, Loader=yaml.FullLoader)
            changed = False
            for spi in range(len(spawn)):
                if len(spawn[spi]["Entities"]) == 0:
                    continue
                for e in range(len(spawn[spi]["Entities"])):
                    ent = spawn[spi]["Entities"][e]
                    if ent["ObjectId"] == 566 and e == 0:
                        spawn[spi]["Entities"].append(ent)
                        spawn[spi]["Entities"].append(ent)
                        changed = True
            if changed:
                outfn = os.path.join("spawns", subfn)
                if not os.path.exists(os.path.dirname(outfn)):
                    os.makedirs(os.path.dirname(outfn))
                with open(outfn, "w") as f:
                    yaml.dump(spawn, f)
                # subfn should always be of form ardname/spawnname
                spawnname = subfn.split(os.sep)[1]
                ardname = subfn.split(os.sep)[0]
                if not ardname in changedards:
                    changedards[ardname] = []
                changedards[ardname].append(spawnname)
else:
    for root, dirs, files in os.walk("spawns"):
        path = root.split(os.sep)
        for f in files:
            fn = os.path.join(root, f)
            spawnname = fn.split(os.sep)[2]
            ardname = fn.split(os.sep)[1]
            if not ardname in changedards:
                changedards[ardname] = []
            changedards[ardname].append(spawnname)

for ard in changedards:
    asset =  {
        "name": "ard/{}.ard".format(ard),
        "method": "binarc",
        "source": [
            {
                "name": changedards[ard][i].split(".")[0],
                "type": "AreaDataSpawn",
                "method": "spawnpoint",
                "source": [            
                    {
                        "name": "spawns/{}/{}".format(ard, changedards[ard][i])
                    }
                ]
            }
            for i in range(len(changedards[ard]))
        ]
    }
    assets.append(asset)

mod = {
    "originalAuthor": "Thundrio",
    "description": """READ THIS FIRST
Turn Sora into Ice Climbers! Have fun wobbling all the bosses!
v0.1
""",
    "title": TITLE,
    "assets": assets,
    "logo": "logo.png"
}
import yaml
yaml.dump(mod, open("mod.yml", "w"))