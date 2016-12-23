import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import Entry

ENTRIES = [

    {
        "id": 0,
        "title": "Introduction to Pyramid",
        "body": "Today's lecture was difficult for me to follow due to the breakneck speed. I enjoyed working on the deque today, it was a breeze and I'm really seeing the value of class composition. Once I got to working on the pyramid assignment I was pretty lost and I'm still trying to work through it. I have no doubt that pyramid is awesome, and while I can follow along with the class notes, I'm not really at a point yet where I understand what's going on. I'm hoping that will change soon.",
        "date": "Dec. 19, 2016"
    },

    {
        "id": 1,
        "title": "Jinja Ninja",
        "body": "After reading some of posts by other people, I feel like the only person in the whole class who's having a harder time with the frameworks than with the echo server assignment.  The fact that I did not take the 301 class is really showing which is unfortunate but I think I can catch up in due time.",
        "date": "Dec. 20, 2016"
    },

    {
        "id": 2,
        "title": "Literally NoSQL",
        "body": "Today I came to the realization of how learning in this class will work for me, and likely most of the class. When Pyramid was introduced I did not understand what was going on. One day after the introduction, the first assignment sounds like a breeze. It seems things start to soak in the next day instead of during lecture. The human brain acts in funny ways. I've also come to accept the fact that this class will take over my life until it is over. it's a significant sacrifice that people more knowledgeable than myself think I must take to get to where I know I want to go.",
        "date": "Dec. 21, 2016"
    },

]

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        for entry in ENTRIES:
            model = Entry(id=entry['id'],
                          title=entry['title'],
                          body=entry['body'],
                          creation_date=['creation date'])
            dbsession.add(model)
