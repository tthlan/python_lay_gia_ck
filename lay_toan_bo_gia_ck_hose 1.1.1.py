from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


driver= webdriver.Chrome()

# Mở trang web
driver.get("https://iboard.ssi.com.vn/")
wait = WebDriverWait(driver, 0.15)  # Chờ


########### 1.0.1 - Thêm code để tắt popups trước khi băt đầu lấy mã
screen_width = driver.execute_script("return window.innerWidth")
screen_height = driver.execute_script("return window.innerHeight")

# Tính toán giữa màn hình
center_x = screen_width / 2
center_y = screen_height / 2

# Sử dụng ActionChains để di chuyển chuột về giữa
actions = ActionChains(driver)
actions.move_by_offset(center_x, center_y).perform()

try:
    # <div class="banner-carousel z-46">
    # Di chuyển tới nút icon-close để click để tắt popup banner-carousel z-46
    element = driver.find_element(By.CSS_SELECTOR, f"div[class='banner-carousel z-46']")
    if (element):
        subelement = element.find_element(By.CLASS_NAME, "icon-close")
        subelement.click()

    # <button class="btn btn-close" type="button">Tắt quảng cáo</button>
    # Di chuyển tới nút btn btn-close để click để tắt popup tiếp theo
    button = driver.find_element(By.CSS_SELECTOR, f"button[class='btn btn-close']")
    if (button):
        button.click()

except Exception as e:
    print(f"Không có tìm thấy element popups")
########### 1.0.1 - End

# Chọn sàn HOSE
link = driver.find_element(By.CSS_SELECTOR, f"div[data-menu-id='priceboardMenu-hose']")
link.click()
driver.implicitly_wait(0.20)

link = driver.find_element(By.CSS_SELECTOR, f"li[data-menu-id='priceboardMenu-hoseHose']")
link.find_element(By.CSS_SELECTOR, 'a').click()
driver.implicitly_wait(0.20)

#############
# Dùng mảng để chứa dữ liệu
board_values = [];

########### 1.1.0
# bắt đầu hàm scrapStock nhận vào 4 tham số trong đó có tham số (biến)
# board_value sẽ được cập nhật dữ liêu
def scrapStock(board_values, price_low, price_high, total_traded):

    container = driver.find_elements(By.CLASS_NAME, "ag-center-cols-clipper")
    div_elements = container[1].find_elements(By.XPATH, f".//div[string-length(@row-id) = 3 and @role='row']")


    matchedPrice = None

    flag = True
    stock_scrap = []

    while flag:

        stock = ""

        for div in div_elements:

            if div.text != '':

                stock = div.get_attribute("row-id")
                if stock in stock_scrap: continue
                stock_scrap.append(stock)

                matchedPrice = div.find_element(By.CSS_SELECTOR, f"div[col-id='matchedPrice']")
                nmTotalTradedQty = div.find_element(By.CSS_SELECTOR, f"div[col-id='nmTotalTradedQty']")


                if matchedPrice and matchedPrice.text != "":
                    if (float(matchedPrice.text) >= price_low) and (float(matchedPrice.text) <= price_high) and int((nmTotalTradedQty.text).replace(",", "")) > total_traded:
                        data = {
                            stock:
                            {
                                'Giá': "{:.2f}".format(float(matchedPrice.text)),
                                'KLGD': "{:,}".format(int((nmTotalTradedQty.text).replace(",", ""))),
                            }
                        }
                        # Thêm dữ liệu vào mảng
                        board_values.append(data)

                    if stock == 'YEG': # or stock == 'VRE':
                        flag = False
                        break
        # kết thúc for div

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
# Kết thúc hàm scrapStock

# gọi hàm scrapStock
scrapStock(board_values, 10, 15, 1000000)

# Kết nối mảng và in ra command line
result = "\n".join(map(str, board_values))
print(result)
print("Số mã trên sàn HOSE đã lấy được: " + str(len(board_values)))

# Đóng trình duyệt
driver.quit()
quit()