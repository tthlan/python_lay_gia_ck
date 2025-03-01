from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Tạo một trình duyệt Chrome
driver= webdriver.Chrome()

# Mở trang web
driver.get("https://iboard.ssi.com.vn/")
wait = WebDriverWait(driver, 1.5)  # Chờ tối đa

stock = 'YEG'

# Đợi một chút để trang tải hoàn chỉnh (có thể cần thay đổi thời gian chờ tùy vào tốc độ tải trang)
time.sleep(0.05)  # Đợi

# Nhập mã ck cần tìm vào ô id là selectSearchStock-input
input_field = wait.until(EC.presence_of_element_located((By.ID, "selectSearchStock-input")))
input_field.send_keys(stock)
time.sleep(0.2)

# Nhấn Enter để tìm kiếm
input_field.send_keys(Keys.RETURN)
time.sleep(0.2)

#############
div_elements = driver.find_elements(By.CSS_SELECTOR, f"div[role='row']")
matchedPrice = None;

for div in div_elements:
    if div.get_attribute("row-id") == stock and div.text != '':
        matchedPrice = div.find_elements(By.CSS_SELECTOR, f"div[col-id='matchedPrice']")

        if not matchedPrice:
            print('ma_ck: ' + div.text)
        else:
            for div_child in matchedPrice:
                print('gia_khop: ' + div_child.text)
                break
            break

# Đóng trình duyệt
driver.quit()