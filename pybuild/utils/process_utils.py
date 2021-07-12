import logging
import os
import subprocess

from threading import Thread


class _AsyncLoggingThread(Thread):
    """Async Logging Thread class"""

    def __init__(self, process, file_descriptor, logger=None, callback=None):
        """Initialization function.

        Args:
            process: Process object returned from Popen.
            file_descriptor: Process stdout or stderr.
            logger: Logging function for either info or error, should be dependent on file_descriptor passed.
            callback: Function that takes a single argument, string.
        """
        assert callable(file_descriptor.readline)
        if callback is not None:
            assert callable(callback)
        self._process = process
        self._file_descriptor = file_descriptor
        self._logger = logger
        self._callback = callback

        Thread.__init__(self)

        self._close = False


    def run(self):
        """Thread runner function to collect logging information.
        """
        while self._process.poll() is None and not self._close:
            output = self._file_descriptor.readline()
            if output:
                if self._logger is not None:
                    self._logger(str(output.rstrip(), encoding='utf-8'))
                if self._callback is not None:
                    self._callback(str(output.rstrip(), encoding='utf-8'))


    def close(self):
        self._close = True


def create_process(executable : str, command : str, wait : bool = True, log_output : bool = True, callback_func : callable = None) -> subprocess.Popen:
    """Create processes for the system to run using subprocess.

    This function will create processes that are maintained by subprocess, the subprocess will yield a return code if function blocks (waits).

    Args:
        executable: String to executable binary.
        command: Command to execute with the binary.
        wait: Wait until program has terminated.
        log_output: Log processes output to terminal, some functions may want this turned off.
        callback_func: Callback function for process to call on the event of output.

    Returns:
        On wait = True, the function will yield the return code associated with the process.
    """
    # Set Python output if calling interpreter to Unbuffered, allowing
    # print and other statements to flow through to logger
    os.environ['PYTHONUNBUFFERED'] = '1'

    async_threads = []
    # processed_command = shlex.join([executable, command])
    processed_command = ' '.join([executable, command])
    process = subprocess.Popen(processed_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ, shell=True)

    for stream, log_type in [(process.stdout, logging.info if log_output else None), (process.stderr, logging.error if log_output else None)]:
        async_threads.append(_AsyncLoggingThread(process, stream, logger=log_type, callback=callback_func))
        async_threads[-1].start()

    if wait:
        process.wait()
        [x.join() for x in async_threads]
        return process.poll()
    return process