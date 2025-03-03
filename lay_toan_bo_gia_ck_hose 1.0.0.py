from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


driver= webdriver.Chrome()

# Mở trang web
driver.get("https://iboard.ssi.com.vn/")
wait = WebDriverWait(driver, 0.15)  # Chờ

screen_width = driver.execute_script("return window.innerWidth")
screen_height = driver.execute_script("return window.innerHeight")

# Tạm tính và click vào chính dữ trang tính để có thể cuộn màn hình xuống sau được
center_x = screen_width / 2
center_y = screen_height / 2
actions = ActionChains(driver)
actions.move_by_offset(center_x, center_y).perform()

# Chọn sàn HOSE
link = driver.find_element(By.CSS_SELECTOR, f"li[data-menu-id='priceboardMenu-hose']") # hose
link.find_element(By.CSS_SELECTOR, 'a').click()
driver.implicitly_wait(0.15)

#############
container = driver.find_elements(By.CLASS_NAME, "ag-center-cols-clipper")
div_elements = container[1].find_elements(By.XPATH, f".//div[string-length(@row-id) = 3 and @role='row']")

matchedPrice = None

flag = True
stock_scrap = []
board_values = [];

while flag:

    stock = ""

    for div in div_elements:

        if div.text != '':

            stock = div.get_attribute("row-id")
            if stock in stock_scrap: continue
            stock_scrap.append(stock)

            matchedPrice = div.find_element(By.CSS_SELECTOR, f"div[col-id='matchedPrice']")

            if matchedPrice and matchedPrice.text != "":
                data = {
                    stock:
                    {
                        'Giá': "{:.2f}".format(float(matchedPrice.text)),
                    }
                }
                # Dùng mảng để chứa dữ liệu
                board_values.append(data)

                if stock == 'YEG': # or stock == 'VRE':
                    flag = False
                    break

    if flag == True:
        if stock == 'VJC': # mã đọc được gần cuối để ctrl + down rồi mới được tiếp được
            actions.key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).perform() # tới cuối trang crtl page_down rồi page up và down để đọc nhưng gia cuối
            actions.click().send_keys(Keys.PAGE_UP).perform()
            actions.click().send_keys(Keys.PAGE_DOWN).perform()
        else:
            actions.click().send_keys(Keys.PAGE_DOWN).perform() # page_down đọc tiếp từng trang

        container = driver.find_elements(By.CLASS_NAME, "ag-center-cols-clipper")
        div_elements = container[1].find_elements(By.XPATH, f".//div[string-length(@row-id) = 3 and @role='row']")
    else:
        break

# Kết nối mảng và in ra command line
result = "\n".join(map(str, board_values))
print(result)
print("Số mã trên sàn HOSE đã lấy được: " + str(len(board_values)))

# Đóng trình duyệt
driver.quit()
quit()