from datetime import datetime
import os
from queue import Queue
from typing import List, Optional

class BaseNotifier(object):
    """Representation of a polling object which waits for a completion or
    failure event.

    Args:
        source: Stream of data to check for triggers.
        delay: The time to wait between polls.
        triggers_failure: List of strings indicating failure to complete.
        triggers_success: List of strings indicating successful completion.
    """
    def __init__(self,
                 source: Queue,
                 delay: Optional[datetime.timedelta] = None,
                 triggers_failure: Optional[List[str]] = None,
                 triggers_success: Optional[List[str]] = None) -> None:
        pass


class FileNotifier(BaseNotifier):
    """Representation of a polling object which targets a file.

    Args:
        filepath: Path to the file to monitor.
        delay: The time to wait between polls.
        triggers_failure: List of strings indicating failure to complete.
        triggers_success: List of strings indicating successful completion.
    """
    def __init__(self,
                 filepath: str,
                 delay: Optional[datetime.timedelta] = None,
                 triggers_failure: Optional[List[str]] = None,
                 triggers_success: Optional[List[str]] = None) -> None:
        pass
