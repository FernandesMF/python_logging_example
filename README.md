# python_logging_example
An example of how to use python logging lib. It uses the logger's tree, logging from a daemon thread, and catching errors.

## What you will find in this example

This is a prototype I made to see how I could use the standard python library for a big project I have been working.
There were three things that I needed and which were not obvious at first, which I believe this example can shed some light
if you are in the same situation:

__Logging classes__: the logging library uses three classes: Loggers, Handlers and Formatters; you can check out how to use them in this example (though this is pretty well explained in the official docs).

__Logger hierarchy__: when you have several classes/submodules, you might want to use a logger inside each of them; in order to avoid configuring each independently, or if you want to use "global" configuration (the configurations of the main logger in all other loggers), then the logger hierarchy is for you; you have to name the loggers according to their 'tree' convention, and subloggers will propagate the log upwards until the main logger.

__Logging fom another thread__: if you have another thread running a subprocess or a daemon, you have to take care or you might miss logs from that thread, especially in case of errors; but the logger hierarchy will be your best friend.

__Log traceback, in case of error__: there is a pretty nice function to log the traceback in case of exceptions; if you handle them correctly, you should not be missing any errors that might happen; i missed some at first, but hey, that's why we make prototypes xD

## How to run this script
You should run it as a python module. That means you should move to the directory above this module, and run it with
```
python -m python_logging_example
```
It should produce a log.txt file inside the module, which you can check out.

If you get errors with silly messages, don't worry: those were me checking if the script was catching errors.
Otherwise, something is wrong xD


Okay, that's pretty much it. I hope this can be helpful! :D
