import json
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Dict, Optional


class ComfyUIClient:
    """Lightweight REST client for queuing and polling headless ComfyUI workflows."""

    def __init__(self, server_address: str = "127.0.0.1:8188") -> None:
        self.server_address = server_address.rstrip("/")
        self.base_url = f"http://{self.server_address}"
        self.client_id = str(uuid.uuid4())

    def is_alive(self, timeout: float = 2.0) -> bool:
        """Check if the ComfyUI server is reachable."""
        try:
            with urllib.request.urlopen(f"{self.base_url}/system_stats", timeout=timeout) as resp:
                return resp.status == 200
        except urllib.error.URLError:
            return False

    def queue_prompt(self, workflow: Dict[str, Any]) -> str:
        """Submit an API-format workflow dictionary and return the prompt_id."""
        payload = json.dumps({"prompt": workflow, "client_id": self.client_id}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/prompt",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        return result["prompt_id"]

    def get_history(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve execution history for a completed prompt_id."""
        with urllib.request.urlopen(f"{self.base_url}/history/{prompt_id}") as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get(prompt_id)

    def wait_for_completion(self, prompt_id: str, poll_interval: float = 0.5, timeout: float = 300.0) -> Dict[str, Any]:
        """Poll the server until the queued prompt finishes and return its outputs."""
        start = time.time()
        while time.time() - start < timeout:
            history = self.get_history(prompt_id)
            if history is not None:
                return history.get("outputs", {})
            time.sleep(poll_interval)
        raise TimeoutError(f"ComfyUI job {prompt_id} timed out after {timeout}s.")

    def download_output(self, filename: str, subfolder: str = "", folder_type: str = "output", dest_dir: str = ".") -> Path:
        """Download a generated output file from ComfyUI to disk."""
        query = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": folder_type})
        dest_path = Path(dest_dir) / filename
        urllib.request.urlretrieve(f"{self.base_url}/view?{query}", dest_path)
        return dest_path
