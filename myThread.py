import time
from concurrent.futures import ProcessPoolExecutor
# from concurrent.futures import ThreadPoolExecutor
import asyncio
import time

async def download(url):
    print(f"开始下载{url}")
    await asyncio.sleep(1)
    print(f"完成{url}")

async def main():
    urls = ["url1", "url2", "url3", "url4", "url5"]
    tasks = [download(url) for url in urls]
    await asyncio.gather(*tasks)

start = time.time()
asyncio.run(main())
print(f"协程耗时：{time.time()-start:.2f}s")


# 多进程
# def download(url):
#     print(f"开始下载 {url}")
#     time.sleep(1)
#     print(f"完成 {url}")
#
#
# urls = ["url1", "url2", "url3", "url4", "url5"]
#
#
# if __name__ == '__main__':
#     start = time.time()
#     with ProcessPoolExecutor(max_workers=5) as executor:
#         executor.map(download, urls)
#     print(f"多进程耗时：{time.time()-start:.2f}s")


# 串行
# def download(url):
#     print(f"开始下载 {url}")
#     time.sleep(1)
#     print(f"完成 {url}")
#
#
# urls = ["url1", "url2", "url3", "url4", "url5"]
#
# start = time.time()
# for url in urls:
#     download(url)
# print(f"串行耗时：{time.time()-start:.2f}s")



# 多线程
# def download(url):
#     print(f"开始下载 {url}")
#     time.sleep(1)
#     print(f"完成 {url}")
#
#
# urls = ["url1", "url2", "url3", "url4", "url5"]
#
# start = time.time()
# with ThreadPoolExecutor(max_workers=5) as executor:
#     executor.map(download, urls)
# print(f"多线程耗时：{time.time()-start:.2f}s")



