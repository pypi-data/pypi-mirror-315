import asyncio
from inspect import iscoroutinefunction
import json
from typing import Optional

from .mqtt_message import MQTTMessage
from .callback_request import CallbackRequest
from .payload_formats import PayloadFormat

from logging import getLogger


logger = getLogger(__name__)


class CallbackRunner(object):
    """
    This class provides functionality for processing callback requests in an
    asynchronous event-driven architecture. It maintains a queue of requests
    and a processing loop to handle callbacks either as coroutines or regular
    methods.

    The class is primarily designed to integrate with asynchronous I/O
    operations and supports interaction with external messaging or event
    systems. It ensures callbacks are properly queued and executed in a
    thread-safe manner.

    :ivar __ready: Indicates if the processing loop is ready to handle
        callbacks.
    :type __ready: bool
    :ivar __loop: Event loop instance used for processing callbacks and
        queue operations.
    :type __loop: asyncio.AbstractEventLoop
    """
    __queue = asyncio.Queue()

    def __init__(self):
        self.__loop: Optional[asyncio.AbstractEventLoop] = None
        self.__ready: bool = False

    @property
    def loop(self):
        """
        Provides access to the 'loop' property that is asyncio loop, which returns the private attribute '__loop'.
        This property is read-only and does not allow modification.

        :return: The value of the private '__loop' attribute.
        :rtype: Same type as the '__loop' attribute.
        """
        return self.__loop

    @loop.setter
    def loop(self, loop):
        self.__loop = loop

    def convert_payload(self, request: CallbackRequest, payload: str):
        if request.payload_format == PayloadFormat.JSON:
            try:
                ret_val = json.loads(payload)
            except (json.JSONDecodeError, AttributeError, TypeError) as e:
                logger.error(e)
                ret_val = payload
        elif request.payload_format == PayloadFormat.RAW:
            ret_val = payload
        else:
            raise NotImplementedError(f"Custom payload formats ({request.payload_format}) are not yet supported!")
        return ret_val

    async def process_callbacks(self):
        """
        Handles invocation of callback methods for queued request objects asynchronously.

        This method continuously processes requests from an internal queue. Each request
        object contains a callback method, a topic, a message, and any additional parameters.
        If the callback method specified in the request object is a coroutine function, it
        is awaited; otherwise, it is executed synchronously. The method guarantees queued
        callback methods are invoked in the order they were added to the queue.

        Method exits only after the queue has been shut down by using stop() method of the class.

        :return: None
        """
        self.__ready = True
        while True:
            try:
                request, msg = await self.__queue.get()
            except asyncio.QueueShutDown:
                break

            try:
                final_msg = MQTTMessage(topic=request.topic,
                                        message=self.convert_payload(request, msg.message))
            except Exception as e:
                logger.error(e)
                raise
            if iscoroutinefunction(request.cb_method):
                await request.cb_method(request.topic, final_msg, request.parameters)
            else:
                request.cb_method(request.topic, final_msg, request.parameters)

    def stop(self):
        """
        Stops the processing by shutting down the internal queue.

        This method ensures that all resources associated with the queue are properly
        released, and no more items can be enqueued or processed. It should be
        invoked when processing is complete or the queue needs to be terminated
        gracefully.
        """
        self.__queue.shutdown()

    def run_callback(self, cb_request: CallbackRequest, msg: MQTTMessage):
        """
        Handles the execution of a callback by queuing the provided callback request and
        message for processing. Ensures that the processor is ready before queuing, and
        allows asynchronous processing if the loop is active.

        :param cb_request: The callback request object to be processed.
        :type cb_request: CallbackRequest
        :param msg: The MQTT message associated with the callback request.
        :type msg: MQTTMessage
        :return: None
        """
        while not self.__ready:
            print("Processor not ready yet.")
            return
        if self.__loop is not None:
            asyncio.run_coroutine_threadsafe(self.__queue.put((cb_request, msg)), self.__loop)