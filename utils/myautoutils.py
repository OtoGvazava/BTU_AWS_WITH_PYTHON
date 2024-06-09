import aiohttp

async def get_my_auto_image_urls():
    image_urls = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.3"
    }

    auto_page_n = lambda nth_page: f"https://api2.myauto.ge/ka/products?TypeID=0&ForRent=&Mans=&CurrencyID=3&MileageType=1&Page={nth_page}"

    async with aiohttp.ClientSession(headers=headers) as session:
        for page_n in range(1):
            response = await session.get(auto_page_n(page_n))
            response.raise_for_status()

            data = await response.json()

            for item in data['data']['items']:
                car_id = item['car_id']
                photo = item['photo']
                picn = item['pic_number']
                print(f"Car ID: {car_id}")
                print("Image URLs:")
                for id in range(1, picn + 1):
                    image_url = f"https://static.my.ge/myauto/photos/{photo}/large/{car_id}_{id}.jpg"
                    image_urls.append(image_url)
                    print(image_url)
                print()

    return image_urls
