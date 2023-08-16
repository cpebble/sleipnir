import docker
import logging
import multiprocessing as mp

logger = logging.getLogger("EventParser")
#logger.setLevel(logging.DEBUG)

class NotImplementedException(Exception):
    pass

def get_docker_client():
    client = docker.from_env()
    return client

class DockerEventParser():
    def __init__(self) -> None:
        # Flag to handle thread stopping
        self.should_parse = mp.Value('b', False)
        self.client = get_docker_client()
        self.subprocess = None

        logger.info("Got docker client access")

    def _event_loop_parser(self, callback) -> None:
        for event in self.events:
            # If the parser should stop, break the loop
            if self.should_parse.value == False:
                break
            # Handle events
            logger.debug(f"Recieved Event: {event}")
            try:
                callback(event)
            except Exception as ex:
                logger.warn("Callback function returned exception")
                logger.exception(ex)

    def start_parsing(self, callback=lambda n: None, should_subprocess=True):
        """Start a subprocess connecting and parsing the docker event stream"""
        if not should_subprocess:
            raise NotImplementedException

        if not self.subprocess is None:
            logger.error("Tried to spawn second subprocess")
            raise Exception("Process already running")
        self.should_parse.value = True
        self.events = self.client.events(decode=True)
        self.subprocess = mp.Process(target=self._event_loop_parser, args=(callback, ))
        self.subprocess.start()
        logger.debug(f"Started process with pid: {self.subprocess.pid}")

    def stop_parsing(self):
        assert self.subprocess is not None
        self.should_parse.value = False
        self.events.close()
        logger.info("Flipped flag, waiting for join")
        self.subprocess.join()
        logger.info("Docker subp joined")




