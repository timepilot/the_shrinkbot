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

    twitter = Twitter(
        auth=OAuth(
            oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),
        secure=True,
        api_version='1',
        domain='api.twitter.com')

    twitter.domain="search.twitter.com"
    twitter.uriparts=()
    # We need to bypass the TwitterCall parameter encoding, so we
    # don't encode the plus sign, so we have to encode it ourselves
    # query_string = "+".join(
    #     [quote(term.decode('UTF-8'))
    #      for term in options['extra_args']])

    last_id_replied = ''

    print '###### args = ', sys.argv

    if len(sys.argv) > 1:
        last_id_replied = sys.argv[1]

    while True:
        results = twitter.search(q="@the_shrinkbot", since_id=last_id_replied)['results']
        #print results

        if not results:
            print 'No results this time...'

        # Switch back to regular api domain.
        #twitter.domain="api.twitter.com"

        doctor = eliza.eliza()
    
        poster = Twitter(
            auth=OAuth(
                oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),
            secure=True,
            api_version='1',
            domain='api.twitter.com')
    
    
        for result in results:
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
    



