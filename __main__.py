"""
This sketch is about the standard logging library. I want to accomplish the following
things:
- instantiate a logger, two handlers (one for a file, the other for the terminal) and
  a formatter
- attach the handlers and formatters to the logger, make it log in the format i want
- make logging from imported modules, in the same file as the main module (use global
  variable to store the file name? or perhaps, use propagation)
- make logging from another thread in the same file as the main thread
- log a traceback in case of error; check both errors in the main thread and in
  secondary threads

Yep, that's pretty much it. Let's get down to it!
"""


import logging
import time

import sketch.log_submodule.sketch_logging_submodule


LOG_FILE: str = "log.txt"
MAIN_LOGGER: str = "python_logging_example"
MAIN_WAIT_SECS: float = 2


def setup_main_logging_instances() -> dict:
    """Instances the main logger, its handlers and its formatter, and returns them in a
    JSON-like dictionary"""

    formatter: logging.Formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    main_term_handler: logging.Handler = logging.StreamHandler()
    main_term_handler.setFormatter(formatter)

    main_file_handler: logging.Handler = logging.FileHandler(LOG_FILE, mode="w")
    main_file_handler.setFormatter(formatter)

    # loggers should be instantiated like this, else we might reinstantiate and shadow
    main_logger: logging.Logger = logging.getLogger(name=MAIN_LOGGER)
    main_logger.setLevel(logging.INFO)
    main_logger.addHandler(main_term_handler)
    main_logger.addHandler(main_file_handler)

    return {
        "logger": [main_logger],
        "handlers": [main_term_handler, main_file_handler],
        "formatter": [formatter]
    }


def log_sketch_main() -> None:
    """Entry point of my sketch application"""

    main_logger: logging.Logger = logging.getLogger(name=MAIN_LOGGER)

    main_logger.info("Alright, let's get this started.")
    sketch.log_submodule.sketch_logging_submodule.not_main()
    time.sleep(MAIN_WAIT_SECS)
    main_logger.info("Cool. Glad it is done.")
    main_logger.info("Now let's try to raise an error.")
    raise RuntimeError("Error: something weird happened.")


if __name__ == "__main__":

    # it is important to get the main logging instance or else we can't log exceptions
    # caught at this level.
    main_logging_instances: dict = setup_main_logging_instances()
    main_logger_instance: logging.Logger = main_logging_instances["logger"][0]

    try:
        log_sketch_main()
    except Exception as e:
        main_logger_instance.exception(e)
