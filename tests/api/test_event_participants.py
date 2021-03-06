import pytest
import json

from inbox.models import Account
from tests.util.base import (event_sync, events_provider,
                             api_client)

__all__ = ['events_provider', 'event_sync', 'api_client']


ACCOUNT_ID = 1


def test_api_create(events_provider, event_sync, db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{
            'name': 'alyssa p. hacker',
            'email': 'alyssa@example.com'
            }]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)

    assert len(e_resp_data['participants']) == 1
    participant = e_resp_data['participants'][0]
    assert participant['name'] == e_data['participants'][0]['name']
    assert participant['email'] == e_data['participants'][0]['email']
    assert participant['status'] == 'noreply'

    e_resp_data = api_client.get_data('/events/' + e_resp_data['id'], ns_id)

    assert len(e_resp_data['participants']) == 1
    participant = e_resp_data['participants'][0]
    assert participant['name'] == e_data['participants'][0]['name']
    assert participant['email'] == e_data['participants'][0]['email']
    assert participant['status'] == 'noreply'


def test_api_create_status_yes(events_provider, event_sync, db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{
            'email': 'alyssa@example.com',
            'status': 'yes'
            }]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)

    assert len(e_resp_data['participants']) == 1
    participant = e_resp_data['participants'][0]
    assert participant['name'] is None
    assert participant['email'] == e_data['participants'][0]['email']
    assert participant['status'] == 'yes'


def test_api_create_multiple(events_provider, event_sync, db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{
            'email': 'alyssa@example.com',
        }, {
            'email': 'ben.bitdiddle@example.com',
        }]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)

    assert len(e_resp_data['participants']) == 2
    participant0 = e_resp_data['participants'][0]
    participant1 = e_resp_data['participants'][1]
    assert participant0['name'] is None
    assert participant0['email'] == e_data['participants'][0]['email']
    assert participant0['status'] == 'noreply'
    assert participant1['name'] is None
    assert participant1['email'] == e_data['participants'][1]['email']
    assert participant1['status'] == 'noreply'


def test_api_create_status_no(events_provider, event_sync, db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{
            'email': 'alyssa@example.com',
            'status': 'no'
            }]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)

    assert len(e_resp_data['participants']) == 1
    participant = e_resp_data['participants'][0]
    assert participant['name'] is None
    assert participant['email'] == e_data['participants'][0]['email']
    assert participant['status'] == e_data['participants'][0]['status']


def test_api_create_status_maybe(events_provider, event_sync, db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{
            'email': 'alyssa@example.com',
            'status': 'maybe'
            }]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)

    assert len(e_resp_data['participants']) == 1
    participant = e_resp_data['participants'][0]
    assert participant['name'] is None
    assert participant['email'] == e_data['participants'][0]['email']
    assert participant['status'] == e_data['participants'][0]['status']


def test_api_create_status_noreply(events_provider, event_sync, db,
                                   api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{
            'email': 'alyssa@example.com',
            'status': 'noreply'
            }]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)

    assert len(e_resp_data['participants']) == 1
    participant = e_resp_data['participants'][0]
    assert participant['name'] is None
    assert participant['email'] == e_data['participants'][0]['email']
    assert participant['status'] == e_data['participants'][0]['status']


def test_api_create_no_name(events_provider, event_sync, db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{
            'email': 'alyssa@example.com'
            }]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)

    assert len(e_resp_data['participants']) == 1
    participant = e_resp_data['participants'][0]
    assert participant['name'] is None
    assert participant['email'] == e_data['participants'][0]['email']
    assert participant['status'] == 'noreply'


def test_api_create_no_email(events_provider, event_sync, db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{
            'name': 'alyssa p. hacker',
            }]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)

    assert e_resp_data["type"] == "invalid_request_error"


def test_api_create_bad_status(events_provider, event_sync, db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{
            'name': 'alyssa p. hacker',
            'email': 'alyssa@example.com',
            'status': 'bad'
            }]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)

    assert e_resp_data["type"] == "invalid_request_error"


def test_api_create_notes(events_provider, event_sync, db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{
            'email': 'alyssa@example.com',
            'notes': 'this is a note.'
            }]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)
    assert len(e_resp_data['participants']) == 1
    participant = e_resp_data['participants'][0]
    assert participant['name'] is None
    assert participant['email'] == e_data['participants'][0]['email']
    assert participant['notes'] == e_data['participants'][0]['notes']


def test_api_create_preserve_order(events_provider, event_sync,
                                   db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{'email': 'alyssa@example.com'},
                         {'email': 'ben.bitdiddle@example.com'},
                         {'email': 'pei.mihn@example.com'},
                         {'email': 'bill.ling@example.com'},
                         {'email': 'john.q@example.com'}]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)
    assert len(e_resp_data['participants']) == 5
    for i, p in enumerate(e_resp_data['participants']):
        assert p['email'] == e_data['participants'][i]['email']
        assert p['name'] is None


def test_api_add_participant(events_provider, event_sync,
                             db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{'email': 'alyssa@example.com'},
                         {'email': 'ben.bitdiddle@example.com'},
                         {'email': 'pei.mihn@example.com'},
                         {'email': 'bill.ling@example.com'},
                         {'email': 'john.q@example.com'}]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)
    assert len(e_resp_data['participants']) == 5
    for i, p in enumerate(e_resp_data['participants']):
        assert p['email'] == e_data['participants'][i]['email']
        assert p['name'] is None

    event_id = e_resp_data['id']
    e_data['participants'].append({'email': 'filet.minyon@example.com'})
    e_resp = api_client.put_data('/events/' + event_id, e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)

    assert len(e_resp_data['participants']) == 6
    for i, p in enumerate(e_resp_data['participants']):
        assert p['email'] == e_data['participants'][i]['email']
        assert p['name'] is None


def test_api_remove_participant(events_provider, event_sync,
                                db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{'email': 'alyssa@example.com'},
                         {'email': 'ben.bitdiddle@example.com'},
                         {'email': 'pei.mihn@example.com'},
                         {'email': 'bill.ling@example.com'},
                         {'email': 'john.q@example.com'}]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)
    assert len(e_resp_data['participants']) == 5
    for i, p in enumerate(e_resp_data['participants']):
        assert p['email'] == e_data['participants'][i]['email']
        assert p['name'] is None

    event_id = e_resp_data['id']
    e_data['participants'].pop()
    e_resp = api_client.put_data('/events/' + event_id, e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)
    assert len(e_resp_data['participants']) == 4
    for i, p in enumerate(e_resp_data['participants']):
        assert p['email'] == e_data['participants'][i]['email']
        assert p['name'] is None


def test_api_update_participant_status(events_provider, event_sync,
                                       db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{'email': 'alyssa@example.com'},
                         {'email': 'ben.bitdiddle@example.com'},
                         {'email': 'pei.mihn@example.com'},
                         {'email': 'bill.ling@example.com'},
                         {'email': 'john.q@example.com'}]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)
    assert len(e_resp_data['participants']) == 5
    for i, p in enumerate(e_resp_data['participants']):
        assert p['email'] == e_data['participants'][i]['email']
        assert p['name'] is None

    event_id = e_resp_data['id']

    update_data = {
        'participants': [{'email': 'alyssa@example.com',
                          'status': 'yes'},
                         {'email': 'ben.bitdiddle@example.com',
                          'status': 'no'},
                         {'email': 'pei.mihn@example.com',
                          'status': 'maybe'},
                         {'email': 'bill.ling@example.com'},
                         {'email': 'john.q@example.com'}]
    }

    e_resp = api_client.put_data('/events/' + event_id, update_data, ns_id)
    e_resp_data = json.loads(e_resp.data)

    # Make sure that nothing changed that we didn't specify
    assert e_resp_data['subject'] == 'Friday Office Party'
    assert e_resp_data['start'] == 1407542195
    assert e_resp_data['end'] == 1407543195
    assert e_resp_data['busy'] is False
    assert e_resp_data['all_day'] is False

    assert len(e_resp_data['participants']) == 5
    expected = ['yes', 'no', 'maybe', 'noreply', 'noreply']
    for i, p in enumerate(e_resp_data['participants']):
        assert p['email'] == e_data['participants'][i]['email']
        assert p['status'] == expected[i]
        assert p['name'] is None


@pytest.mark.parametrize('rsvp', ['yes', 'no', 'maybe'])
def test_api_participant_reply(events_provider, event_sync,
                               db, api_client, rsvp):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{'email': 'alyssa@example.com'},
                         {'email': 'ben.bitdiddle@example.com'},
                         {'email': 'pei.mihn@example.com'},
                         {'email': 'bill.ling@example.com'},
                         {'email': 'john.q@example.com'}]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)
    assert len(e_resp_data['participants']) == 5

    event_id = e_resp_data['id']
    participants = e_resp_data['participants']
    participant_id = participants[0]['id']

    url = '/events/{}?'.format(event_id)
    url += 'action=rsvp&participant_id={}&rsvp={}'.format(participant_id, rsvp)

    e_resp_data = api_client.get_data(url, ns_id)
    participants = e_resp_data['participants']
    assert len(participants) == 5
    assert participants[0]['status'] == rsvp

    e_resp_data = api_client.get_data('/events/' + e_resp_data['id'], ns_id)
    participants = e_resp_data['participants']
    assert len(participants) == 5
    assert participants[0]['status'] == rsvp


def test_api_participant_reply_invalid_rsvp(events_provider,
                                            event_sync,
                                            db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{'email': 'alyssa@example.com'},
                         {'email': 'ben.bitdiddle@example.com'},
                         {'email': 'pei.mihn@example.com'},
                         {'email': 'bill.ling@example.com'},
                         {'email': 'john.q@example.com'}]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)
    assert len(e_resp_data['participants']) == 5

    event_id = e_resp_data['id']
    participants = e_resp_data['participants']
    participant_id = participants[0]['id']

    url = '/events/{}?'.format(event_id)
    url += 'action=rsvp&participant_id={}&rsvp={}'.format(participant_id,
                                                          'bad')

    e_resp_data = api_client.get_data(url, ns_id)
    assert e_resp_data['type'] == 'api_error'


def test_api_participant_reply_invalid_participant(events_provider,
                                                   event_sync,
                                                   db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{'email': 'alyssa@example.com'},
                         {'email': 'ben.bitdiddle@example.com'},
                         {'email': 'pei.mihn@example.com'},
                         {'email': 'bill.ling@example.com'},
                         {'email': 'john.q@example.com'}]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)
    assert len(e_resp_data['participants']) == 5

    event_id = e_resp_data['id']

    url = '/events/{}?'.format(event_id)
    url += 'action=rsvp&participant_id={}&rsvp={}'.format('bad', 'yes')

    e_resp_data = api_client.get_data(url, ns_id)
    assert e_resp_data['type'] == 'invalid_request_error'


def test_api_participant_reply_invalid_event(events_provider,
                                             event_sync,
                                             db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{'email': 'alyssa@example.com'},
                         {'email': 'ben.bitdiddle@example.com'},
                         {'email': 'pei.mihn@example.com'},
                         {'email': 'bill.ling@example.com'},
                         {'email': 'john.q@example.com'}]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)
    assert len(e_resp_data['participants']) == 5

    participants = e_resp_data['participants']
    participant_id = participants[0]['id']

    url = '/events/{}?'.format(participant_id)
    url += 'action=rsvp&participant_id={}&rsvp={}'.format(participant_id,
                                                          'yes')

    e_resp_data = api_client.get_data(url, ns_id)
    assert e_resp_data['type'] == 'invalid_request_error'


def test_api_participant_reply_invalid_event2(events_provider,
                                              event_sync,
                                              db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{'email': 'alyssa@example.com'},
                         {'email': 'ben.bitdiddle@example.com'},
                         {'email': 'pei.mihn@example.com'},
                         {'email': 'bill.ling@example.com'},
                         {'email': 'john.q@example.com'}]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)
    assert len(e_resp_data['participants']) == 5

    participants = e_resp_data['participants']
    participant_id = participants[0]['id']

    url = '/events/{}?'.format('bad')
    url += 'action=rsvp&participant_id={}&rsvp={}'.format(participant_id,
                                                          'yes')

    e_resp_data = api_client.get_data(url, ns_id)
    assert e_resp_data['type'] == 'invalid_request_error'


def test_api_participant_reply_invalid_action(events_provider,
                                              event_sync,
                                              db, api_client):
    acct = db.session.query(Account).filter_by(id=ACCOUNT_ID).one()
    ns_id = acct.namespace.public_id

    e_data = {
        'subject': 'Friday Office Party',
        'start': 1407542195,
        'end': 1407543195,
        'busy': False,
        'all_day': False,
        'participants': [{'email': 'alyssa@example.com'},
                         {'email': 'ben.bitdiddle@example.com'},
                         {'email': 'pei.mihn@example.com'},
                         {'email': 'bill.ling@example.com'},
                         {'email': 'john.q@example.com'}]
    }

    e_resp = api_client.post_data('/events', e_data, ns_id)
    e_resp_data = json.loads(e_resp.data)
    assert len(e_resp_data['participants']) == 5

    event_id = e_resp_data['id']
    participants = e_resp_data['participants']
    participant_id = participants[0]['id']

    url = '/events/{}?'.format(event_id)
    url += 'action=bad&participant_id={}&rsvp={}'.format(participant_id,
                                                         'yes')

    e_resp_data = api_client.get_data(url, ns_id)
    assert e_resp_data['type'] == 'api_error'
