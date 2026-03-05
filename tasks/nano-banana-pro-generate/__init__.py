#region generated meta
import typing
class Inputs(typing.TypedDict):
    prompt: str
    imageUrls: list[str] | None
    aspectRatio: typing.Literal["21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16"] | None
    outputFormat: typing.Literal["png", "jpeg", "webp", "jpg"] | None
    resolution: typing.Literal["1K", "2K", "4K"] | None
    numImages: int | None
class Outputs(typing.TypedDict):
    sessionID: typing.NotRequired[str]
    success: typing.NotRequired[bool]
#endregion

from oocana import Context
import requests

async def main(params: Inputs, context: Context) -> Outputs:
    """
    Generate or edit images using the nano banana pro API.

    If imageUrls is provided, performs image editing.
    Otherwise, performs image generation.
    Submits a request to the fusion-api endpoint and returns a session ID
    for tracking the task.
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

    # Prepare request body with required parameters
    request_body = {
        "prompt": params["prompt"]
    }

    # Add imageUrls if provided (for editing mode)
    image_urls = params.get("imageUrls")
    if image_urls:
        # Validate imageUrls array
        if len(image_urls) < 1 or len(image_urls) > 3:
            raise ValueError("imageUrls must contain between 1 and 3 image URLs")
        request_body["imageUrls"] = image_urls

    # Add optional parameters if provided
    if params.get("aspectRatio"):
        request_body["aspectRatio"] = params["aspectRatio"]

    if params.get("outputFormat"):
        request_body["outputFormat"] = params["outputFormat"]

    if params.get("resolution"):
        request_body["resolution"] = params["resolution"]

    # Add numImages parameter
    num_images = params.get("numImages")
    if num_images is not None:
        # Validate range
        if num_images < 1 or num_images > 8:
            raise ValueError("numImages must be between 1 and 8")
        request_body["numImages"] = int(num_images)

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
