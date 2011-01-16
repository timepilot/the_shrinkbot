from twitter.api import Twitter, TwitterError
from twitter.oauth import OAuth, write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance

import os
import time
import sys


import eliza


CONSUMER_KEY='uS6hO2sV6tDKIOeVjhnFnQ'
CONSUMER_SECRET='MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk'

# The very first arg, if present, is the last id replied to.

if __name__ == '__main__':
    oauth_filename = os.environ.get('HOME', '') + os.sep + '.twitter_oauth'
    oauth_token, oauth_token_secret = read_token_file(oauth_filename)

    # We use two twitter clients, one to search, another to update. Just
    # easier that way...
    twitter = Twitter(domain='search.twitter.com')
    twitter.uriparts=()

    last_id_replied = ''

    print '###### args = ', sys.argv

    if len(sys.argv) > 1:
        last_id_replied = sys.argv[1]

    doctor = eliza.eliza()

    poster = Twitter(
        auth=OAuth(
            oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),
        secure=True,
        api_version='1',
        domain='api.twitter.com')

    while True:
        results = twitter.search(q="@the_shrinkbot", since_id=last_id_replied)['results']
    
        if not results:
            print 'No results this time...'

        for result in results:
            # Remove my name from the question.
            question = result['text'].replace('@the_shrinkbot', '')
            asker = result['from_user']
            id = str(result['id'])
            print " <<< " + asker + ": " + question
            doctor_response = doctor.respond(question.strip())

            # We append part of the ID to avoid duplicates.
            msg = '@%s %s (%s)' % (asker, doctor_response, id[-4:])
            print '====> Resp = %s' % msg
            last_id_replied = id
            poster.statuses.update(status=msg)
            print 'Last id replied = ', last_id_replied

        print 'Now sleeping... \n\n'
        time.sleep(30)
    



