#region generated meta
import typing
class Inputs(typing.TypedDict):
    prompt: str
    imageUrls: list[str]
    aspectRatio: typing.Literal["21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16"] | None
    outputFormat: typing.Literal["png", "jpeg", "webp", "jpg"] | None
    resolution: typing.Literal["1K", "2K", "4K"] | None
    numImages: float | None
class Outputs(typing.TypedDict):
    sessionID: typing.NotRequired[str]
    success: typing.NotRequired[bool]
#endregion

from oocana import Context
import requests

async def main(params: Inputs, context: Context) -> Outputs:
    """
    Edit images using the nano banana pro API.

    Submits a request to the fusion-api endpoint with image URLs and editing prompt,
    returns a session ID for tracking the image editing task.
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

    # Validate imageUrls array
    image_urls = params["imageUrls"]
    if not image_urls or len(image_urls) < 1 or len(image_urls) > 3:
        raise ValueError("imageUrls must contain between 1 and 3 image URLs")

    # Prepare request body with required parameters
    request_body = {
        "prompt": params["prompt"],
        "imageUrls": image_urls
    }

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
