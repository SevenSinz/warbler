"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from models import db, User, Message, FollowersFollowee, Like

bcrypt = Bcrypt()

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()



class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        FollowersFollowee.query.delete()
        # add Like table
        Like.query.delete()

        self.client = app.test_client()

        hashed_pwd = bcrypt.generate_password_hash("HASHED_PASSWORD").decode('UTF-8')

        self._user1 = User(
            id=1000,
            email="test1@test.com",
            username="testuser1",
            password=hashed_pwd
        )
        
        self._user2 = User(
            id=2000,
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        
        db.session.add(self._user1)
        db.session.add(self._user2)
        db.session.commit()


    def test_user_model(self):
        """Does basic model work?"""
        
        # User should have no messages, no followers, followees or likes
        self.assertEqual(self._user1.id, 1000)
        self.assertEqual(len(self._user1.messages), 0)
        self.assertEqual(len(self._user1.followers), 0)
        self.assertEqual(len(self._user1.following), 0)
        self.assertEqual(len(self._user1.liked_messages), 0)

    def test_repr_method(self):
        """Does the repr method work as expected?"""    

        self.assertEqual(repr(self._user1), f'<User #{self._user1.id}: testuser1, test1@test.com>')

    def test_is_following(self):
        """Does is_following work?"""    

        # successfully detect when user1 is NOT following user2
        self.assertFalse(self._user1.is_following(self._user2))

        # successfully detect when user1 IS following user2
        stalker = FollowersFollowee(
            followee_id = 1000,
            follower_id = 2000
        )
        db.session.add(stalker)
        db.session.commit()

        self.assertTrue(self._user1.is_following(self._user2))


    def test_is_followed_by(self):
        """Does is_followed_by work?"""    

        # successfully detect when user1 IS NOT followed by user2
        self.assertFalse(self._user1.is_followed_by(self._user2))

        # successfully detect when user1 IS  followed by user2
        stalker = FollowersFollowee(
            followee_id = 2000,
            follower_id = 1000
        )
        db.session.add(stalker)
        db.session.commit()

        self.assertTrue(self._user1.is_followed_by(self._user2))


    def test_user_signup(self):
        """Does User.signup successfully create a new user given valid credentials?"""    

        user = User.signup(username='uname', email='email@email.com', password='123456', image_url='/static/images/image.png')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user.username=='uname')
        self.assertTrue(user.email=='email@email.com')
        self.assertTrue(user.authenticate('uname', '123456'))
        self.assertTrue(user.image_url=='/static/images/image.png')

    def test_default_image(self):
        """Does User.signup successfully create a new user with default image, given no image?"""   

        user_with_image = User.signup(username='uname2', email='email2@email.com', password='123456', image_url='')
        db.session.add(user_with_image)
        db.session.commit()

        self.assertTrue(user_with_image.image_url=='/static/images/default-pic.png')

# check with form error message
    def test_user_signup_uniqueness(self):
        """Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?"""    

        # trying to create a new user with the same username/email
        user = User.signup(username='uname', email='email@email.com', password='123456', image_url='/static/images/image.png')
        user_not_unique = User.signup(username='uname', email='emaillll@email.com', password='123456', image_url='/static/images/image.png')
        db.session.add(user)
        db.session.add(user_not_unique)

        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        
    def test_user_signup_uniqueness(self):
        """Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?"""    

        # trying to create a new user with missing email
        user_missing_email = User(username='uname', password='123456', image_url='/static/images/image.png')
        db.session.add(user_missing_email)

        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        
    def test_user_authenticate_correct(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""

        self.assertTrue(self._user1.authenticate(self._user1.username, "HASHED_PASSWORD"))


    def test_user_authenticate_fail(self):
        """ Does User.authenticate fail to return a user when the username is invalid?"""

        self.assertFalse(self._user1.authenticate("wrong_username", "HASHED_PASSWORD"))

    def test_user_authenticate_fail(self):
        """ Does User.authenticate fail to return a user when the password is invalid?"""

        self.assertFalse(self._user1.authenticate(self._user1.username, "WRONG_PASSWORD"))
