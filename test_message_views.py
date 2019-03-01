"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)


        db.session.commit()

        self.testuser_id = self.testuser.id

    
    def test_unauthorized_user(self):
        ''' Can unauthorize access /messages/new route'''
        # we can rewrite the same test for all routes to make sure unauthorized users
        # dont have access

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 5
       
            resp_get = c.get("/messages/new")
            resp_get_redirected = c.get("/messages/new", follow_redirects=True)
            
            # Make sure it redirects
            self.assertEqual(resp_get.status_code, 302)
            self.assertIn(b'Access unauthorized.', resp_get_redirected.data)
       
            resp_post = c.post("/messages/new")
            resp_post_redirected = c.post("/messages/new", follow_redirects=True)

            # Make sure it redirects
            self.assertEqual(resp_post.status_code, 302)
            self.assertIn(b'Access unauthorized.', resp_post_redirected.data)


#######################################################
        
        
    # GET/POST to endpoint return valid response
    def test_add_message(self):
        """Can user add a message?"""
        
        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # get
            resp_get = c.get("/messages/new")
            self.assertEqual(resp_get.status_code, 200)
            self.assertIn(b'new-message-form', resp_get.data)

            # post
            resp_post = c.post("/messages/new", data={"text": "Hello"})
            self.assertEqual(resp_post.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")


    #POST new messages and check for display and count
    def test_show_own_message(self):
        '''test to see if the messages posted are displayed'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp_post = c.post("/messages/new", data={"text": "Hello"})
            resp_post = c.post("/messages/new", data={"text": "Hi"})

            resp_get = c.get(f'/users/{self.testuser.id}')

            self.assertIn(b'<p>Hello</p>',resp_get.data)
            self.assertIn(b'<p>Hi</p>',resp_get.data)
            
            self.assertIn(b'id="message_count" value="2"',resp_get.data)


    #POST Delete messages and check for display and count
    def test_view_message(self):
        '''test to see if a message is clicked it shows separately'''
        
        # self.testuser_id = self.testuser.id

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp_post = c.post("/messages/new", data={"text": "Hello"})
            # import pdb; pdb.set_trace()
            u = User.query.get(self.testuser_id)
            msg_id = u.messages[0].id
            resp_get = c.get(f'/messages/{msg_id}')

            self.assertIn(b'class="single-message">Hello</p>',resp_get.data)
            self.assertIn(b'class="btn btn-outline-danger">Delete</button>',resp_get.data)
            
            # self.assertIn(b'id="message_count" value="2"',resp_get.data)        

            





    # #POST Delete messages and check for display and count
    # def test_delete_message(self):
    #     '''test to see if messages are deleted and count reflects the delete'''
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id

    #         resp_post = c.post("/messages/new", data={"text": "Hello"})
    #         resp_post = c.post("/messages/new", data={"text": "Hi"})

    #         resp_get = c.get(f'/users/{self.testuser.id}')

    #         self.assertIn(b'<p>Hello</p>',resp_get.data)
    #         self.assertIn(b'<p>Hi</p>',resp_get.data)
            
    #         self.assertIn(b'id="message_count" value="2"',resp_get.data)        

            

        