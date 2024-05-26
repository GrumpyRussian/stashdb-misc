# Scenes with both the 'Big Tits' and 'Small Tits' tags

import os, time, re, json
import libarchive

file_7z = 'stashdb.7z'
print('Based on', file_7z, '(' + time.asctime(time.gmtime(os.path.getmtime(file_7z))) + ')')
print()

def process(what, func):
    n = 0
    with libarchive.file_reader('stashdb.7z') as archive:
        for entry in archive:
            if re.match(fr'{what}/.', entry.pathname):
                n += 1
                func(json.loads(b''.join(entry.get_blocks())))
    print('processed', n, what, ' ')

tag1_id = None
tag2_id = None
def tag_id_by_name(e):
    global tag1_id, tag2_id
    if e['name'] == 'Big Tits':
        tag1_id = e['id']
    elif e['name'] == 'Small Tits':
        tag2_id = e['id']
process('tags', tag_id_by_name)
print('"Big Tits" tag:', tag1_id, ' ')
print('"Small Tits" tag:', tag2_id, ' ')
print()

all_females = set()
all_males = set()
names = {}
def process_performer(e):
    if e['gender'] == 'MALE':
        all_males.add(e['id'])
    elif e['gender'] == 'FEMALE':
        all_females.add(e['id'])
        names[e['id']] = e['name']
process('performers', process_performer)
print('all males:', len(all_males), ' ')
print('all females:', len(all_females), ' ')
print()

results = []
def process_scene(e):
    tag_ids = [x['id'] for x in e['tags']]
    # both the 'Big Tits' and 'Small Tits' tags
    if tag1_id in tag_ids and tag2_id in tag_ids:
        scene_performers = set([x['performer']['id'] for x in e['performers']])
        scene_females = all_females & scene_performers
        # only one female performer
        if len(scene_females) == 1:
            female_id = list(scene_females)[0]
            # all other performers are males
            if scene_performers - scene_females <= all_males:
                results.append({'scene_id': e['id'], 'female_id': female_id})
process('scenes', process_scene)
print()

print('scene|female performer')
print('-----|----------------')

for e in sorted(results, key=lambda e: names[e['female_id']]):
    scene_id = e['scene_id']
    female_id = e['female_id']
    print('|'.join([
        f'[scene](https://stashdb.org/scenes/{scene_id})',
        f'[{names[female_id]}](https://stashdb.org/performers/{female_id})']))
