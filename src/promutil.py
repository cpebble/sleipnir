from pathlib import Path
import logging
import multiprocessing
import os
import tempfile


logger = logging.getLogger()
logger.setLevel(os.getenv("LOGLEVEL", "INFO"))
WORKDIR = Path(tempfile.mkdtemp("promconf"))
logger.debug(f"Using tmpfile {WORKDIR}")


class PromtailHandler:
    def __init__(self) -> None:
        self.watched_files = set()
        self.subprocess = None
        pass

    def _update_promtail_config(self):
        pass

    def watch_new_file(self, filename: Path) -> None :
        filepath = Path(filename)
        if filepath in self.watched_files:
            logger.info("Tried to watch watched file")
            return
        self.watched_files.add(filepath)
        self._update_promtail_config()

    def stop_watching_file(self, filename: Path) -> None:
        filepath = Path(filename)
        if not filepath in self.watched_files:
            logger.warn(f"Tried to remove unknown file: {str(filepath)}")
            return
        self.watched_files.remove(filepath)
        self._update_promtail_config()
        return

