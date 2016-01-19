"""
    Initialization for MBE tests.
"""
import os
import queue
import time

from bson.objectid import ObjectId
import cherrypy
from multiprocessing import Queue
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from mbe.node import Node
from administration import Administration
from optimalbpm.broker.lib.messaging.handler import BrokerWebSocketHandler
from optimalbpm.common.messaging.constants import GOING_AWAY
from optimalbpm.common.queue.monitor import Monitor
import optimalbpm.common.messaging.websocket
from optimalbpm.common.testing.init_env import init_env
from optimalbpm.broker.lib.messaging.websocket import MockupWebSocket
from optimalbpm.schemas.constants import zero_object_id

__author__ = 'nibo'

# Test users uuids
object_id_user_root = "000000010000010001e64c30"
object_id_user_test = "000000010000010001e64c31"
object_id_user_testagent = "000000010000010001e64c32"

object_id_right_admin_nodes = "000000010000010001e64d01"


def before_all(context):
    init_env(context)


def init_low_level(context, feature):

    # Fake session registration
    _peers = {
        "sender":
            {
                "address": "source_peer",
                "user": context.user,
                "queue": Queue()
            },
        "receiver":
            {
                "address": "destination_peer",
                "user": context.user,
                "queue": Queue()
            }
    }

    context.monitor = Monitor(
        _handler=BrokerWebSocketHandler(_process_id=context.agent_process_id, _peers=_peers,
                                        _schema_tools=context.db_access.schema_tools, _address="broker",
                                        _database_access=context.db_access), _logging_function=cherrypy.log.error)

    optimalbpm.common.messaging.websocket.monitor = context.monitor

    # Register mockup WebSockets
    context.sender = MockupWebSocket(session_id="sender", context=context)
    context.receiver = MockupWebSocket(session_id="receiver", context=context)

    def _stop_broker():
        pass
    if feature.name in ["Process Management", "Process definition management API"]:
        context.node = Node(_database_access=context.db_access, _rights=[object_id_right_admin_nodes])
        context.administration = Administration(context.db_access, context.node,
                                                _send_queue=context.monitor.queue,
                                                _stop_broker=None,
                                                _address="",
                                                _process_id=zero_object_id)



def before_feature(context, feature):
    """
    Initialisation for all features.

    :param context:
    :param feature:
    :return:

    """
    if feature.name in ["Process Management", "Process definition management API", "Message broker"]:
        init_low_level(context, feature)



def after_feature(context, feature):
    print("After feature " + feature.name + ", stopping broker.")
    context.sender.close(code=GOING_AWAY, reason="Close sender")
    context.receiver.close(code=GOING_AWAY, reason="Close receiver")
    if feature.name in ["Process Management", "Process definition management API", "Message broker"]:
        context.monitor.stop()
        time.sleep(.1)