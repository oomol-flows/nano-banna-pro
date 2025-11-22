#region generated meta
import typing
class Inputs(typing.TypedDict):
    prompt: str
    aspectRatio: typing.Literal["21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16"] | None
    outputFormat: typing.Literal["png", "jpeg", "webp", "jpg"] | None
    resolution: typing.Literal["1K", "2K", "4K"] | None
class Outputs(typing.TypedDict):
    sessionID: typing.NotRequired[str]
    success: typing.NotRequired[bool]
#endregion

from oocana import Context
import requests

async def main(params: Inputs, context: Context) -> Outputs:
    """
    Generate images using the nano banana pro API.

    Submits a request to the fusion-api endpoint and returns a session ID
    for tracking the image generation.
    """

    # Get OOMOL token for authentication
    token = await context.oomol_token()

    # Prepare the API endpoint
    url = "https://fusion-api.oomol.com/v1/fal-nano-banana-pro/submit"

    # Prepare headers
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    # Prepare request body with required and optional parameters
    request_body = {
        "prompt": params["prompt"]
    }

    # Add optional parameters if provided
    if params.get("aspectRatio"):
        request_body["aspectRatio"] = params["aspectRatio"]

    if params.get("outputFormat"):
        request_body["outputFormat"] = params["outputFormat"]

    if params.get("resolution"):
        request_body["resolution"] = params["resolution"]

    # Make the API request
    response = requests.post(
        url,
        headers=headers,
        json=request_body,
        timeout=30.0
    )

    # Check if request was successful
    response.raise_for_status()

    # Parse the response
    result = response.json()

    return {
        "sessionID": result.get("sessionID", ""),
        "success": result.get("success", False)
    }
