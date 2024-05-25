# Analyzes the use of the "Short Woman" tag

# Takes scenes that:
# - has the tag set
# - has only one female performer with known height
# - all other performers are males
# Then checks the height of the female performer

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

def is_short(h):
    return 155 <= h <= 165

tag_name = 'Short Woman'
tag_id = None
def tag_id_by_name(e):
    global tag_id
    if e['name'] == tag_name:
        tag_id = e['id']
process('tags', tag_id_by_name)
print('id for the "Short Woman" tag:', tag_id)
print()

all_females = set()
all_males = set()
heights = {}
names = {}
def process_performer(e):
    if e['gender'] == 'MALE':
        all_males.add(e['id'])
    elif e['gender'] == 'FEMALE':
        all_females.add(e['id'])
        if not e['height'] is None:
            heights[e['id']] = e['height']
            names[e['id']] = e['name']
process('performers', process_performer)
print('all males:', len(all_males), ' ')
print('all females:', len(all_females), ' ')
print('females with known height:', len(heights), ' ')
print('short females:', len([x for x in heights if is_short(heights[x])]), ' ')
print()

results = []
def process_scene(e):
    global all, right
    # the "Short Woman" tag
    if tag_id in [x['id'] for x in e['tags']]:
        scene_performers = set([x['performer']['id'] for x in e['performers']])
        scene_females = all_females & scene_performers
        # only one female performer
        if len(scene_females) == 1:
            female_id = list(scene_females)[0]
            # all other performers are males
            if scene_performers - scene_females <= all_males:
                # height of the female is known 
                if female_id in heights:
                    results.append({'scene_id': e['id'], 'female_id': female_id})
process('scenes', process_scene)
a = len(results)
r = len([e for e in results if is_short(heights[e['female_id']])])
print('all:', a, ' ')
print('right:', r, ' ')
print('ratio:', r / a, ' ')
print('wrong:', a - r, ' ')
print()


print('scene|right?|height|female performer')
print('-----|------|------|----------------')

# order first by height, then by name
def key(e):
    return heights[e['female_id']], names[e['female_id']]

for e in sorted(results, key=key, reverse=1):
    scene_id = e['scene_id']
    female_id = e['female_id']
    print('|'.join([
        f'[scene](https://stashdb.org/scenes/{scene_id})',
        ('yes' if is_short(heights[female_id]) else 'no'),
        f'{heights[female_id]}',
        f'[{names[female_id]}](https://stashdb.org/performers/{female_id})']))
