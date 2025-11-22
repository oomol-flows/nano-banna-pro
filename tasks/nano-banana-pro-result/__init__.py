#region generated meta
import typing
class Inputs(typing.TypedDict):
    sessionID: str
    pollingInterval: float | None
    timeout: float | None
class Outputs(typing.TypedDict):
    images: typing.NotRequired[list[str]]
#endregion

from oocana import Context
import requests
import asyncio
import time

async def main(params: Inputs, context: Context) -> Outputs:
    """
    Continuously polls the image generation status until completion, failure, or timeout.

    Polls the fusion-api endpoint at regular intervals to check the status of the image
    generation. Returns when the state is "completed", "failed", or when timeout is reached.
    """

    # Get OOMOL token for authentication
    token = await context.oomol_token()

    # Get polling parameters
    session_id = params["sessionID"]
    polling_interval = params.get("pollingInterval") or 2  # Default: 2 seconds
    timeout = params.get("timeout") or 300  # Default: 300 seconds (5 minutes)

    # Prepare the API endpoint
    url = f"https://fusion-api.oomol.com/v1/fal-nano-banana-pro/result/{session_id}"

    # Prepare headers
    headers = {
        "Authorization": token
    }

    # Initialize variables
    start_time = time.time()
    state = "unknown"
    images: list[str] = []
    poll_count = 0

    # Polling loop
    while True:
        poll_count += 1
        elapsed_time = time.time() - start_time

        # Check if timeout exceeded
        if elapsed_time >= timeout:
            raise TimeoutError(f"Polling timed out after {timeout} seconds")

        # Report progress (0-100%)
        progress = min(int((elapsed_time / timeout) * 100), 99)
        context.report_progress(progress)

        try:
            # Make the API request
            response = requests.get(
                url,
                headers=headers,
                timeout=30.0
            )

            # Check if request was successful
            response.raise_for_status()

            # Parse the response
            result = response.json()

            # Extract data from response
            state = result.get("state", "unknown")

            # Get images array from data field if available
            if "data" in result and isinstance(result["data"], dict):
                data = result["data"]
                # Extract URLs from images array if it exists
                if "images" in data and isinstance(data["images"], list):
                    images = [img["url"] for img in data["images"] if isinstance(img, dict) and "url" in img]

            # Check if completed or failed
            state_lower = state.lower()
            if state_lower == "completed":
                context.report_progress(100)
                break
            elif state_lower == "failed" or state_lower == "error":
                raise RuntimeError(f"Image generation failed with state: {state}")
            # If state is "processing" or any other state, continue polling

            # Wait before next poll
            await asyncio.sleep(polling_interval)

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request error: {str(e)}")
        except TimeoutError:
            raise
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {str(e)}")

    return {
        "images": images
    }
