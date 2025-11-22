import os
from urllib.parse import urlparse

#region generated meta
import typing
class Inputs(typing.TypedDict):
    image_url: str
    save_dir: str | None
class Outputs(typing.TypedDict):
    saved_path: typing.NotRequired[str]
#endregion

from oocana import Context

async def main(params: Inputs, context: Context) -> Outputs:
    save_dir = params["save_dir"]
    image_url = params["image_url"]
    filename = params.get("filename")
    
    # 如果 save_dir 为 None，直接返回 null
    if save_dir is None:
        return {"saved_path": None}
    
    # 确保保存目录存在
    os.makedirs(save_dir, exist_ok=True)
    
    # 如果没有提供文件名，从URL中提取
    if not filename:
        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "image.jpg"  # 默认文件名
    
    # 构建完整的保存路径
    saved_path = os.path.join(save_dir, filename)
    return {"saved_path": saved_path}