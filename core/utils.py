
from django.contrib.auth.models import User
from redis import Redis, ConnectionPool

from core.models import Drawing


redis = Redis(connection_pool=ConnectionPool())


class Actions(object):
    """
    Callable object created with each socketio handler and handles
    each drawing action.
    """

    def __init__(self, socket):
        self.socket = socket
        self.handlers = ("join", "leave", "save")

    def __call__(self, message):
        """
        Main entry point for handling an action. Determine the action
        and relevant redis keys from the message, and call the
        appropriate action handler. Each handler returns a bool used
        by the socketio view to determine whether to broadcast the
        message received.
        """
        self.drawing_key, action = message[:2]
        self.drawing_data_key = "drawing-%s" % self.drawing_key
        self.user_data_key = "users-%s" % self.drawing_key
        if action in self.handlers:
            handler = getattr(self, action)
        else:
            handler = self.default
        return handler(message)

    def join(self, message):
        """
        User is joining - add them to the user set and send them all
        drawing actions and users as join actions.
        """
        redis.sadd(self.user_data_key, ",".join(message[2:]))
        user_actions = [s for m in redis.smembers(self.user_data_key)
                        for s in [self.drawing_key, "join"] + m.split(",")]
        drawing_actions = [s for m in redis.lrange(self.drawing_data_key, 0, -1)
                           for s in m.split(",")]
        self.socket.send(user_actions + drawing_actions)
        return True

    def leave(self, message):
        """
        User is leaving - remove them from the user set and remove
        the drawing action list if there are no more users.
        """
        redis.srem(self.user_data_key, ",".join(message[2:]))
        if len(redis.smembers(self.user_data_key)) == 0:
            redis.delete(self.drawing_data_key)
        return True

    def save(self, message):
        """
        Create a drawing object given the title and image data.
        """
        drawing = Drawing.objects.create(title=message[2],
                                         data=message[3].replace(" ", "+"))
        for user in redis.smembers(self.user_data_key):
            drawing.users.add(User.objects.get(id=user.split(",")[1]))
        return False

    def default(self, message):
        """
        Default action that handles any drawing events such as mouse
        movement and presses. Simply add the actions to the list for
        this drawing.
        """
        redis.rpush(self.drawing_data_key, ",".join(message))
        return True
