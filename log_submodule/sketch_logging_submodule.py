"""
This is a submodule to be used by 'sketch_logging'. Let's get down to work.
"""


import logging
import threading
import time


DTHREAD_WAIT_SECS: float = 0.5
WAIT_SECS = 2


def not_main() -> None:
    """Not the entry point of my sketch application"""

    # this time, when i instantiate a logger using the module name, it should become a
    # child to the main logger (as the name of this submodule, when executed via the main
    # module, should be '__main__.sketch_logging_submodule'); if that works, i should be
    # able to log via propagation
    not_main_logger = logging.getLogger(name=__name__)

    not_main_logger.info("Submodule logging worked just fine.")
    not_main_logger.info("Now let's get that other thread running.")

    stop_event: threading.Event = threading.Event()
    secondary_thread: threading.Thread = threading.Thread(
        target=logging_loop, args=[stop_event], daemon=True
    )
    secondary_thread.start()
    time.sleep(WAIT_SECS)
    stop_event.set()
    secondary_thread.join()

    not_main_logger.info("Now let's try that other loop... hope it is not broken!")
    second_stop_event: threading.Event = threading.Event()
    second_secondary_thread: threading.Thread = threading.Thread(
        target=faulty_loop, args=[second_stop_event], daemon=True
    )
    second_secondary_thread.start()
    time.sleep(WAIT_SECS)
    second_stop_event.set()
    second_secondary_thread.join()

    not_main_logger.info("The subthreads should be over. Let's head back to main.")


def logging_loop(stop_event: threading.Event) -> None:
    """Keeps logging and waiting, until the stop event is set."""

    logger: logging.Logger = logging.getLogger(name=__name__ + ".logging_loop")

    while not stop_event.is_set():
        logger.info("This log should be coming from another thread!")
        time.sleep(DTHREAD_WAIT_SECS)

    logger.info("Loop is done. Let's wrap this thread up.")


def faulty_loop(stop_event: threading.Event) -> None:
    """Calls a function that will raise an error inside a loop. It is just to test
    logging exceptions that happen in another thread."""

    logger: logging.Logger = logging.getLogger(name=__name__ + ".faulty_loop")

    while not stop_event.is_set():
        logger.info("Let's call that function over there.")
        try:
            faulty_function()
            time.sleep(DTHREAD_WAIT_SECS)
        except Exception as e:
            logger.exception(e)
            time.sleep(DTHREAD_WAIT_SECS)

    logger.info("Loop is done, let's wrap it up.")


def faulty_function() -> None:
    """Raises an error."""

    raise RuntimeError("Oh no! This function is actually broken!")
