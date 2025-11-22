# Nano Banana Pro

**Generate high-quality images using the Nano Banana Pro API with customizable resolution, aspect ratio, and format options for creative workflows.**

[中文文档](./README_zh-CN.md)

## Overview

Nano Banana Pro is an OOMOL package that provides an easy-to-use interface for generating AI images using the Nano Banana Pro API. This package offers both URL-based and file-based workflows, allowing you to seamlessly integrate AI image generation into your creative projects.

## Features

- **Text-to-Image Generation**: Create images from text prompts using advanced AI models
- **Flexible Output Options**:
  - Multiple aspect ratios (21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16)
  - Various formats (PNG, JPEG, WebP, JPG)
  - Resolution options (1K, 2K, 4K)
- **Two Workflow Types**:
  - **URL Output**: Get direct download URLs for generated images
  - **File Output**: Automatically save generated images to your local directory
- **Automatic Polling**: Built-in status checking that waits for image generation to complete
- **Batch Processing**: Generate and save multiple images efficiently

## Available Blocks

### 1. Nano Banana Pro Image Generator (Private Task)

Submits an image generation request to the Nano Banana Pro API.

**Inputs:**
- `prompt` (required): Text description of the image to generate
- `aspectRatio` (optional): Aspect ratio of the output image (default: 1:1)
- `outputFormat` (optional): Image format (default: png)
- `resolution` (optional): Image resolution (default: 1K)

**Outputs:**
- `sessionID`: Unique session identifier for tracking the generation process
- `success`: Boolean indicating whether the submission was successful

### 2. Nano Banana Pro Result Checker (Private Task)

Continuously polls the API to check image generation status until completion.

**Inputs:**
- `sessionID` (required): Session ID from the image generator
- `pollingInterval` (optional): Time between status checks in seconds (default: 2)
- `timeout` (optional): Maximum wait time in seconds (default: 300)

**Outputs:**
- `images`: Array of generated image URLs

### 3. Save Image (Private Task)

Downloads an image from a URL and saves it to a specified directory.

**Inputs:**
- `image_url` (required): URL of the image to download
- `save_dir` (optional): Directory path where the image will be saved

**Outputs:**
- `saved_path`: Full path where the image was saved

### 4. Nano Banana Pro URL (Subflow)

Complete workflow that generates images and returns download URLs.

**Inputs:**
- `prompt` (required): Text description of the image to generate
- `aspectRatio` (optional): Aspect ratio (default: 16:9)
- `outputFormat` (optional): Image format (default: webp)
- `resolution` (optional): Image resolution (default: 1K)

**Outputs:**
- `images`: Array of generated image URLs

### 5. Nano Banana Pro File (Subflow)

Complete workflow that generates images and saves them as local files.

**Inputs:**
- `prompt` (required): Text description of the image to generate
- `save_dir` (optional): Directory where images will be saved
- `aspectRatio` (optional): Aspect ratio (default: 16:9)
- `outputFormat` (optional): Image format (default: webp)
- `resolution` (optional): Image resolution (default: 1K)

**Outputs:**
- `array`: Array of file paths where generated images were saved

## Usage Examples

### Using the URL Workflow

The URL workflow is ideal when you want to work with image URLs directly or process images in memory:

1. Add the "Nano Banana Pro URL" subflow to your workflow
2. Connect a text prompt (e.g., "A small tiger cub looking up at the camera")
3. Optionally configure aspect ratio, format, and resolution
4. The workflow will return an array of image URLs you can use in subsequent blocks

### Using the File Workflow

The File workflow is perfect when you need local copies of generated images:

1. Add the "Nano Banana Pro File" subflow to your workflow
2. Provide a text prompt describing your desired image
3. Specify a directory where images should be saved
4. Optionally configure aspect ratio, format, and resolution
5. The workflow will return an array of local file paths

### Custom Workflows

You can also build custom workflows using the individual task blocks:

1. Use "Nano Banana Pro Image Generator" to submit requests
2. Pass the `sessionID` to "Nano Banana Pro Result Checker" to poll for results
3. Optionally use "Save Image" to download images from the returned URLs

## Configuration Options

### Aspect Ratios

Choose from various aspect ratios to match your creative needs:
- Cinematic: 21:9
- Widescreen: 16:9
- Photography: 3:2, 4:3
- Square: 1:1
- Portrait: 4:5, 3:4, 2:3
- Mobile: 9:16

### Output Formats

- **PNG**: Lossless compression, supports transparency
- **JPEG/JPG**: Smaller file sizes, good for photos
- **WebP**: Modern format with excellent compression

### Resolution

- **1K**: Fast generation, suitable for previews and web use
- **2K**: Balanced quality and generation time
- **4K**: Highest quality, longer generation time

## Technical Details

### Architecture

The package consists of:
- **3 Private Task Blocks**: Core functionality for API interaction and file operations
- **2 Subflows**: Pre-configured workflows for common use cases
- **Python Executor**: All tasks run using Python with async support

### Dependencies

The package automatically installs all required dependencies through the bootstrap script:
- Python packages managed via Poetry
- Node.js packages managed via npm

### API Integration

- Connects to the Nano Banana Pro image generation service
- Uses OOMOL token authentication via `context.oomol_token()`
- Implements automatic retry and timeout handling
- Provides progress reporting during long operations

## Best Practices

1. **Start with lower resolutions** (1K) for testing and previews
2. **Use descriptive prompts** for better image quality
3. **Choose appropriate aspect ratios** based on your final use case
4. **Monitor timeout settings** for high-resolution images (they may take longer)
5. **Organize saved files** by using specific directory structures

## Troubleshooting

**Images not generating:**
- Check your OOMOL token is valid
- Verify the prompt is descriptive enough
- Ensure network connectivity

**Timeout errors:**
- Increase the timeout value for high-resolution images
- Check if the API service is available

**File save errors:**
- Verify the save directory exists and has write permissions
- Ensure sufficient disk space is available

## Repository

[https://github.com/oomol-flows/nano-banna-pro](https://github.com/oomol-flows/nano-banna-pro)

## Version

0.0.1

## License

See repository for license information.
