import aiohttp
import asyncio


async def download_image(session, url, img_path):
    async with session.get(url) as response:
        with open(img_path, "wb") as img_file:
            img_file.write(await response.read())


async def download_images(url, n_im):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(download_image(session, url, f"artifacts/easy/img_{i}.jpeg")) for i in range(n_im)]
        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(download_images(url="https://picsum.photos/500/500", n_im=50))
