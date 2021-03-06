from inbox.sqlalchemy_ext.util import generate_public_id
from tests.util.base import api_client

def test_namespace_id_validation(api_client, db):
    from inbox.models import Namespace
    actual_namespace_id, = db.session.query(Namespace.public_id).first()
    r = api_client.client.get('/n/{}'.format(actual_namespace_id))
    assert r.status_code == 200

    fake_namespace_id = generate_public_id()
    r = api_client.client.get('/n/{}'.format(fake_namespace_id))
    assert r.status_code == 404

    malformed_namespace_id = 'this string is definitely not base36-decodable'
    r = api_client.client.get('/n/{}'.format(malformed_namespace_id))
    assert r.status_code == 404

# TODO(emfree): Add more comprehensive parameter-validation tests.
