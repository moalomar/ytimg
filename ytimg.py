import aiohttp, asyncio, os


links = [

    "https://i.ytimg.com/vi_webp/{}/maxresdefault.webp",    # 0
    "https://i.ytimg.com/vi/{}/maxresdefault.jpg",          # 1

    "https://i.ytimg.com/vi_webp/{}/sddefault.webp",        # 2
    "https://i.ytimg.com/vi/{}/sddefault.jpg",              # 3

    "https://i.ytimg.com/vi_webp/{}/hqdefault.webp",        # 4
    "https://i.ytimg.com/vi/{}/hqdefault.jpg",              # 5

    "https://i.ytimg.com/vi_webp/{}/0.webp",                # 6
    "https://i.ytimg.com/vi/{}/0.jpg",                      # 7

    "https://i.ytimg.com/vi_webp/{}/mqdefault.webp",        # 8
    "https://i.ytimg.com/vi/{}/mqdefault.jpg",              # 9

    "https://i.ytimg.com/vi_webp/{}/1.webp",                # 10
    "https://i.ytimg.com/vi/{}/1.jpg",                      # 11

    "https://i.ytimg.com/vi_webp/{}/2.webp",                # 12
    "https://i.ytimg.com/vi/{}/2.jpg",                      # 13

    "https://i.ytimg.com/vi_webp/{}/3.webp",                # 14
    "https://i.ytimg.com/vi/{}/3.jpg",                      # 15

]


async def fetch(video_id, dirname, session, images):
    filepath = '404 NOT FOUND'
    for i in images:
        async with session.get(links[i].format(video_id)) as response:
            if response.status == 200:
                filename = video_id + '.' + links[i].split('/')[-1]
                filepath = os.path.join(dirname, filename)
                with open(filepath, 'wb') as file:
                    file.write(await response.read())
                break
    global count, digits
    padding = ' ' * (digits - len(str(count)))
    print(f'{count}{padding}    {filepath}')
    count -= 1
    return filepath


async def create_tasks(videos_ids, dirname, images):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for video_id in videos_ids:
            task = asyncio.create_task(fetch(video_id, dirname, session, images))
            tasks.append(task)
        return await asyncio.gather(*tasks)


count = digits = 0
def download(videos_ids, dirname, images=range(len(links))):
    global count, digits
    count = len(videos_ids)
    digits = len(str(count))
    os.makedirs(dirname, exist_ok=True)
    return asyncio.run(create_tasks(videos_ids, dirname, images))
