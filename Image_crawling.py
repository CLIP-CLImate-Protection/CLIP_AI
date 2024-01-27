from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
import os


KEYWORD = '춘식이'
SAVE_PATH = "/Users/kdy1021/Desktop/도연/Solution_Challenge/dataset/"

if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
driver.get(f'https://www.google.com/imghp')
search_bar = driver.find_element(By.NAME, "q")
search_bar.send_keys(KEYWORD)
search_bar.submit()

PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")
new_height = 0



if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)

while True:
    driver.execute_script("window.scrollBy(0,5000)")
    time.sleep(PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height - last_height > 0:
        last_height = new_height
        continue
    else:
        break

img_elements = driver.find_elements(By.CSS_SELECTOR, ".rg_i")
imgs = []

for idx, img in enumerate(img_elements):
    print(f"{KEYWORD} : {idx + 1}/{len(img_elements)} proceed...")
    try:
        img.click()
        time.sleep(PAUSE_TIME)
        # 이부분에서 에러나면, 직접 개발자 도구 활용해서 XPATH 추출한 뒤에 변경
        img_element = driver.find_element(By.XPATH,
                                          '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]')
        img_src = img_element.get_attribute('src')
        img_alt = img_element.get_attribute('alt')
        imgs.append({
            'alt': img_alt,
            'src': img_src
        })

        urllib.request.urlretrieve(img_src, f"{SAVE_PATH}/{KEYWORD}_{idx}.png")
        print(f"{KEYWORD}_{idx}.png is saved.")

    except:
        print(f'error in {idx}')
        idx = idx - 1
        pass

driver.close()

print('done')

# Reference: https://with-ahn-ssu.tistory.com/51