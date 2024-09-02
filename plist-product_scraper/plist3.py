from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time

# 创建一个目录来保存图片
if not os.path.exists('images'):
    os.makedirs('images')


def download_image(url, folder):
    try:
        # 设置重试策略
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }

        response = session.get(url, headers=headers, stream=True)
        if response.status_code == 200 and 'image/jpeg' in response.headers.get('content-type', ''):
            image_name = url.split("/")[-1]
            if image_name.lower().endswith('.jpg'):
                image_path = os.path.join(folder, image_name)

                with open(image_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Downloaded {url}")
            else:
                print(f"Skipped {url} (invalid image format)")
        else:
            print(f"Failed to download {url}, status code: {response.status_code}")
    except Exception as e:
        print(f"Could not download {url}. Reason: {e}")


# 启动WebDriver
chrome_driver_path = 'C:/Program Files/Google/Chrome/Application/chromedriver.exe'  # 修改为您的ChromeDriver路径
options = Options()
options.add_argument('--headless')  # 无头模式，不显示浏览器
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)


def scroll_to_load_all(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待页面加载
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def get_images_from_subpage(url):
    try:
        driver.get(url)
        print(f"Accessing sub page: {url}")

        # 等待页面加载完成
        driver.implicitly_wait(10)

        # 向下滚动页面以加载更多内容
        scroll_to_load_all(driver)

        # 创建一个目录来保存子页面的图片
        sub_folder = os.path.join('images', url.split("/")[-1].split('?')[0])
        if not os.path.exists(sub_folder):
            os.makedirs(sub_folder)

        # 获取子页面中的所有图片
        img_tags = driver.find_elements(By.TAG_NAME, 'img')
        print(f"Found {len(img_tags)} images on subpage")
        for img in img_tags:
            img_url = img.get_attribute('src')
            if img_url:
                if not img_url.startswith('http'):
                    img_url = 'http:' + img_url
                print(f"Image URL: {img_url}")
                download_image(img_url, sub_folder)

    except Exception as e:
        print(f"Error while processing {url}. Reason: {e}")


def get_subpage_links(url):
    try:
        driver.get(url)
        print(f"Accessing main page: {url}")

        # 应用Cookie
        cookies = [
            {'name': 'atpsida', 'value': '133fef617022166469cc94da_1721120783_1'},
            {'name': 'cna', 'value': 'DyYdH9oIpSwCAd9i6tsSO7Lg'},
            {'name': 'cookie2', 'value': '1844f715cd90d3abf7cf769ce47b2e3a'},
            {'name': 'isg', 'value': 'BHd3CPEC3dgs1VlUgVqG_7ZkBmvBPEueO4MGWMkkAMa3eJa60Q8B7sASWtAmkCMW'},
            {'name': 'mtop_partitioned_detect', 'value': '1'},
            {'name': 'sca', 'value': 'ae38b674'},
            {'name': 't', 'value': 'ecad988f42e2be137c4da0200331f99e'},
            {'name': 'tfstk',
             'value': 'fiJrhAtNjYHyXGRhuZ6F7lAT19BRFO31tp_CxHxhVabkdgMUYhTUd3N5VIWcbg4ht4BWLE-p8UO5ETNUTFtCd3_5RIreXE8F90QC-w8BxQijCAtJ29BH8VMsCAt3nKLzqJjnxsjOboYWpYxJ29EYcyc6i3FE_gP2E9YhnZjGj9VuEwmVnGSCK8f3EnbckMXh-ebloxj5fMVhr_qmes1h_-SdZc2QWgi-oS6fS3bkAH9mP_VJ4ZyULKRVbND5uJ2H3g-xApbLQX_M6a11_EDbU9-cYE56aVyy8Hx9tsJUr0TMoB8hDI3UTNRHVCdRg0DPkT7yBL98bX7A3Zp9hLq39FWy81vlgk2lntbA3iviA5QX3aTHUsm_Q66DC1XkGj35OTSw-LLzYJYMch9RMpuaowd5XtjepcVF86jynyIDm4JpayVFZiIV5mo0YFVeb8dlzpPL9_aA0NioqWFdZiIV5mo49WCS6i7sq0f..'},
            {'name': 'xlly_s', 'value': '1'}
        ]
        for cookie in cookies:
            driver.add_cookie(cookie)

        # 刷新页面以应用cookie
        driver.refresh()

        # 等待页面加载完成
        driver.implicitly_wait(10)

        # 向下滚动页面以加载更多内容
        scroll_to_load_all(driver)

        # 获取商品标题链接
        item_links = driver.find_elements(By.XPATH,
                                          "//div[@style='position: relative; box-sizing: border-box; display: flex; flex-direction: column; align-content: flex-start; flex-shrink: 0; padding: 10px 10px 0px; overflow: hidden; height: 54px;']/p[@title]")
        print(f"Found {len(item_links)} item links on the homepage")

        subpage_urls = []
        for index, link in enumerate(item_links):
            try:
                print(f"Processing item {index + 1}/{len(item_links)}")
                # 记录当前窗口句柄
                main_window = driver.current_window_handle

                # 模拟点击标题链接
                ActionChains(driver).move_to_element(link).click(link).perform()
                time.sleep(3)  # 等待页面加载

                # 切换到新窗口
                all_windows = driver.window_handles
                for window in all_windows:
                    if window != main_window:
                        driver.switch_to.window(window)
                        subpage_urls.append(driver.current_url)
                        print(f"Subpage URL: {driver.current_url}")
                        driver.close()  # 关闭子窗口
                        driver.switch_to.window(main_window)  # 切换回主窗口
                        break

            except Exception as e:
                print(f"Error clicking link. Reason: {e}")

        return subpage_urls

    except Exception as e:
        print(f"Error while processing {url}. Reason: {e}")


# 主函数
main_url = "https://huihuatiyu.1688.com/page/offerlist.htm?spm=a2615.2177701.wp_pc_common_topnav.0"
subpage_urls = get_subpage_links(main_url)

if subpage_urls:
    for subpage_url in subpage_urls:
        get_images_from_subpage(subpage_url)
else:
    print("No subpage URLs found.")

# 关闭WebDriver
driver.quit()
