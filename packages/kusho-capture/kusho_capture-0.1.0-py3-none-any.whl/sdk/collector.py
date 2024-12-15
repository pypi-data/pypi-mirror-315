import threading
import queue
import time
import requests
import logging
import random
import json
from typing import Dict, Any

class EventCollector:
    def __init__(
        self,
        collector_url: str,
        batch_size: int = 100,
        flush_interval: int = 60,
        max_queue_size: int = 10000,
        sample_rate: float = 0.1
    ):
        self.collector_url = collector_url.rstrip('/')
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.sample_rate = sample_rate
        self.queue = queue.Queue(maxsize=max_queue_size)
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Add console handler if none exists
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        self._start_worker()

    def _should_sample(self) -> bool:
        return random.random() < self.sample_rate

    def _start_worker(self):
        def worker():
            while True:
                batch = []
                try:
                    timeout = time.time() + self.flush_interval
                    while len(batch) < self.batch_size and time.time() < timeout:
                        try:
                            item = self.queue.get(timeout=0.1)
                            batch.append(item)
                        except queue.Empty:
                            continue

                    if batch:
                        self._send_batch(batch)

                except Exception as e:
                    self.logger.error(f"Worker error: {str(e)}")
                    time.sleep(1)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def _send_batch(self, batch: list):
        try:
            url = f"{self.collector_url}/api/v1/events"
            payload = {"events": batch}
            
            self.logger.debug(f"Sending request to: {url}")
            self.logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                url,
                json=payload,
                timeout=5
            )
            
            self.logger.debug(f"Response status code: {response.status_code}")
            self.logger.debug(f"Response body: {response.text}")
            
            response.raise_for_status()
            self.logger.info(f"Successfully sent batch of {len(batch)} events")
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            if hasattr(e.response, 'text'):
                self.logger.error(f"Response text: {e.response.text}")
        except Exception as e:
            self.logger.error(f"Failed to send batch: {str(e)}", exc_info=True)

    def capture(self, event: Dict[str, Any]):
        if not self._should_sample():
            return
            
        try:
            self.logger.debug(f"Capturing event: {json.dumps(event, indent=2)}")
            self.queue.put(event, block=False)
            self.logger.debug("Event added to queue successfully")
        except queue.Full:
            self.logger.warning("Queue full - dropping event")