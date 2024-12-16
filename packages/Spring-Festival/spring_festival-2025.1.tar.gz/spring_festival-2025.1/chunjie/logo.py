video_url = 'https://www.bilibili.com/video/BV12PqhYwEe3'
image_url = 'http://i0.hdslb.com/bfs/new_dyn/dd01c5c6c7571cd8ad98969db33ee947442128119.jpg'

simple_sologon = "巳巳如意，生生不息"

# 输出sologon
def print_simple_sologon():
  print(simple_sologon)

def _watch(watch_type: str):
  could_auto_open_browser = True
  try:
    import webbrowser
  except Exception:
    could_auto_open_browser = False
  if watch_type=="video":
    if not could_auto_open_browser:
      print(f"打开浏览器失败，可手动访问该地址：{video_url}")
    else:
      webbrowser.open(video_url)
  elif watch_type == "image":
    if not could_auto_open_browser:
      print(f"打开浏览器失败，可手动访问该地址：{image_url}")
    else:
      webbrowser.open(image_url)

# 跳转视频
def watch_video():
  _watch("video")

# 跳转高清图
def watch_image():
  _watch("image")

