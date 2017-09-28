import json
import os

tests = {}
folders = json.load(open('stats.json'))['dirs']
for folder in folders:
    if not os.path.exists(folder):
        print 'Folder not found (%s)' % folder
        continue

    subdirs = map(lambda x: '%s/%s' % (folder, x),
                  next(os.walk(folder))[1])
    for subdir in subdirs:
        fname = [f for f in os.listdir(subdir) if '.json' in f][0]
        json_path = '%s/%s' % (subdir, fname)
        cdict = json.load(open(json_path))
        tests[fname] = cdict

for test in tests:
    print tests[test]['comments']