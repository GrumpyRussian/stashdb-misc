stashdb_apikey = 'put your key here'

import sys, re, requests

from_scene_id = sys.argv[1]
to_scene_id = sys.argv[2]

print('Submitting fingerprints from', from_scene_id, 'to', to_scene_id)

def stashdb_query(variables, query):
    req = {
        'variables': variables,
        'query': query
    }
    return requests.post('https://stashdb.org/graphql', headers={'APIKey': stashdb_apikey}, json=req).json()

variables = {'id': from_scene_id}
query = '''
  query($id: ID!) {
    findScene(id: $id) {
      fingerprints {
        hash
        algorithm
        duration
      }
    }
  }
'''
fingerprints = stashdb_query(variables, query)['data']['findScene']['fingerprints']

submit_fingerprint_gql = '''
  mutation(
    $scene_id: ID!
    $algorithm: FingerprintAlgorithm!
    $hash: String!
    $duration: Int!
  ) {
    submitFingerprint(
      input: {
        unmatch: false
        scene_id: $scene_id
        fingerprint: {
          hash: $hash
          algorithm: $algorithm
          duration: $duration
        }
      }
    )
  }
'''

for fingerprint in fingerprints:
    variables = {
        'scene_id': to_scene_id,
        'algorithm': fingerprint['algorithm'],
        'hash': fingerprint['hash'],
        'duration': fingerprint['duration']
    }
    print(stashdb_query(variables, submit_fingerprint_gql))
