@app.before_request
def add_user_to_g():


@app.route('/signup', methods=["GET", "POST"])
def signup():


@app.route('/login', methods=["GET", "POST"])
def login():


@app.route('/logout')
def logout():
    # todo

#################################################
# General user routes:

@app.route('/users')
def list_users():
    # shows all users if no search q, 
    # and searches for users
    # sorry no users found

@app.route('/users/<int:user_id>')
def users_show(user_id):    


@app.route('/users/<int:user_id>')
def users_show(user_id):
            """Show user profile. and all messages by the user"""

@app.route('/users/<int:user_id>/following')
def show_following(user_id):
    """Show list of people ANY USER is following."""

@app.route('/users/<int:user_id>/followers')
def users_followers(user_id):
    """Show list of followers of ANY USER."""

@app.route('/users/follow/<int:follow_id>', methods=['POST'])
def add_follow(follow_id):
    """Add a follow for the currently-logged-in user."""


@app.route('/users/stop-following/<int:follow_id>', methods=['POST'])
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user."""


@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""

    # todo

@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""
        # delete session and from db, using g.user

############################################
# Messages routes:        

@app.route('/messages/new', methods=["GET", "POST"])
def messages_add():
    """Add a message"""


@app.route('/messages/<int:message_id>', methods=["GET"])
def messages_show(message_id):
    """Show a message."""


@app.route('/messages/<int:message_id>/delete', methods=["POST"])
def messages_destroy(message_id):
    """Delete a message."""


#############################################
# Homepage and error pages
@app.route('/')
def homepage():
        """Show homepage:
    - anon users: no messages
    - logged in: 100 most recent messages of followees
    """


@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""
