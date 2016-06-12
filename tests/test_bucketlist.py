from flask import url_for
import json
from test_config import BaseTestCase
from manage import db, app
from app.models import BucketList, User, BucketListItem

class BucketListTest(BaseTestCase):
    """This class contains all bucketlist tests"""

    def get_login_token(self):
        """method to use to represent Authorization means for the tests"""
        user = User(username='Margie', password='1234')
        db.session.add(user)
        db.session.commit()
        response = self.request('POST', url_for(
            'login'), data=json.dumps(
            {'username': 'Margie', 'password': '1234'}),
                                content_type='application/json')
        token = response.data
        print('token')
        print(token)
        return token

    def test_necessary_response_is_authorized(self):
        """Test token in the header is valid."""
        response = self.app.post('/api/v1.0/bucketlists/',
                                 headers=self.get_login_token())
        self.assert400(response)

    def test_succesfull_bucketlist_creation_with_correct_info(self):
        user = User(username="Test", password="1234")
        db.session.add(user)
        db.session.commit()
        data = {"list_name": "Bucketlist 1"}
        response = self.request('POST', url_for('bucketlists'),
                                auth =('Margie', '1234'),
                               data=json.dumps({"list_name": "Bucketlist 1"}),
                               headers=self.get_login_token(),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(data['list_name'], response.data)

    def test_bucket_list_creation_fails_when_no_info_is_provided(self):
        """tests that creation of a bucket-list fails when wrong info is sent"""
        user = User(username='Margie', password='1234')
        db.session.add(user)
        db.session.commit()
        response = self.request(
            'POST', url_for('bucketlists'), auth=('Margie', '1234'),
            data=json.dumps(
                {'list_name': ''}),
            headers=self.get_login_token(),
            content_type='application/json')
        self.assertEqual(response.status_code, 203)
        self.assertIn("Enter a bucketlist name", response.data)

    def test_bucket_list_creation_fails_when_same_bucket_list_is_provided(self):
        """tests that creation of a bucket-list fails when same info is sent"""
        user = User(username='Margie', password='1234')
        db.session.add(user)
        db.session.commit()
        bucketlist = BucketList(name="Bucketlist 1", created_by=user.id)
        db.session.add(bucketlist)
        db.session.commit()
        response = self.request(
            'POST', url_for('bucketlist'), auth=('Margie', '1234'),
            data=json.dumps(
                {'bucket_list_name': 'Bucket List 1'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 203)
        self.assertIn(
            "bucket list : Bucket List 1 already exists", response.data)
