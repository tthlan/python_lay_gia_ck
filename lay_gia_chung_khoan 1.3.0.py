from re import A
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from datetime import datetime

# Tạo một trình duyệt Chrome
driver= webdriver.Chrome()

# Mở trang web
driver.get("https://iboard.ssi.com.vn/")
wait = WebDriverWait(driver, 1.5)  # Chờ tối đa

# Đợi một chút để trang tải hoàn chỉnh (có thể cần thay đổi thời gian chờ tùy vào tốc độ tải trang)
time.sleep(0.05)  # Đợi

board_values = []

# khai báo hàm nhận truyền vào 1 tham số - def tên_function(thamso, ...)
def lay_gia_chung_khoan(stock, board_values):
    # Nhập mã ck cần tìm vào ô id là selectSearchStock-input
    input_field = wait.until(EC.presence_of_element_located((By.ID, "selectSearchStock-input")))
    input_field.send_keys(stock)
    time.sleep(0.2)

    # Nhấn Enter để tìm kiếm
    input_field.send_keys(Keys.RETURN)
    time.sleep(0.2)

    div_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"//div[contains(@class, 'ag-row-selected') and @role='row']")))
    div = div_elements[1]

    matchedPrice = None; # khai báo biến sẽ gán object vào
    output = "" # khai báo biến để lưu giá trị là chuỗi

    if div and div.get_attribute("row-id") == stock and div.text != '':
        index = 0

        # lấy data chứng khoán giá khớp (matchedPrice)
        matchedPrice = div.find_element(By.CSS_SELECTOR, f"div[col-id='matchedPrice']")
        highest = div.find_element(By.CSS_SELECTOR, f"div[col-id='highest']")

        nowPrice = float(matchedPrice.text) if matchedPrice.text != '' else 0

        if matchedPrice:
            index = 0
            output = stock + ":" + matchedPrice.text # gán output là nối chuỗi stock và matchPrice

        if float(matchedPrice.text) == float(highest.text):
            output += " H " # nối chuỗi H vào biến output

        print(output) # In chuỗi biến output ra màn hình

        if stock in stocks:
            index = stocks.index(stock)

        if len(board_values) < len(stocks):
            board_values.append({stock: float(matchedPrice.text), 'counter': 1, 'trend': True}) # Ghi nhận giá vào board_values
        else:
            oldPrice = float(board_values[index].get(stock))

            oldCounter = board_values[index].get('counter')
            trendValue = board_values[index].get('trend')
            counter = int(board_values[index].get('counter'))

            if (oldPrice != nowPrice):
                # reset counter nếu chuyển xu hướng tăng
                if (nowPrice > oldPrice and trendValue == False):
                    trendValue = True # đổi từ false sang true cho xu hướng tăng
                    counter = 0
                elif (nowPrice < oldPrice  and trendValue == True):
                    trendValue = False # đổi từ true sang false cho xu hướng giảm
                    counter = 0
                else:
                    counter = oldCounter
                counter = counter + 1
                board_values[index] = {stock: float(matchedPrice.text), 'counter': counter, 'trend': trendValue} # cập nhật giá trị trên mảng board_values


# kết thúc code block của hàm def lay_gia_chung_khoan

time_end = "22:18:00" # nhấp giá trị giờ phút giây muốn ngừng chạy
time_end = datetime.strptime(time_end, "%H:%M:%S").time() # đổi ra giá trị sang kiểu time

stocks = ['STB', 'SSI'] # khai báo biến và gán giá trị

while datetime.now().time() < time_end: # vòng lặp (while) so sánh nếu thời-gian-hiện-tại nhỏ hơn giờ-kết-thúc thì code block
    for stock in stocks: # quét danh sách stocks
        lay_gia_chung_khoan(stock,board_values) # gọi hàm (function) lay_gia_chung_khoan truyền tham số stock - lấy giá từng stock

    print(board_values)
    time.sleep(5) # đợi sleep(5-giây) sau hãy chạy lại vòng lặp while
# hết code block của while

# Đóng trình duyệt
driver.quit()
# thoát chương trình
quit()