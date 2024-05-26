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


print('heights stats')
print('=============')

heights = {}
def process_performer(e):
    if e['height'] not in heights:
        heights[e['height']] = 1
    else:
        heights[e['height']] += 1
process('performers', process_performer)

print('height|number of performers')
print('------|--------------------')

print('|'.join(['None', str(heights[None])]))
del heights[None]
for h in sorted(heights):
    print('|'.join([str(h), str(heights[h])]))
print()


print('strange heights')
print('===============')

results = []
def process_performer(e):
    if e['height'] is not None and e['height'] < 140:
        results.append(e)
process('performers', process_performer)

print('height|performer')
print('------|---------')
for e in sorted(results, key=lambda e: e['height']):
    print('|'.join([
        str(e['height']),
        f"[{e['name']}](https://stashdb.org/performers/{e['id']})"]))
