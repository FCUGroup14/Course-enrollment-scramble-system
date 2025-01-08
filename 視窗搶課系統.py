import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CoursePriorityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("搶課優先順序設定")
        
        # 初始化課程代碼列表
        self.course_data = []
        
        # 設置標題
        self.title_label = tk.Label(root, text="請輸入欲加選的課程代碼", font=("Arial", 14))
        self.title_label.pack(pady=10)
        
        # 設置課程代碼輸入框
        self.course_entry_label = tk.Label(root, text="請輸入課程代碼：")
        self.course_entry_label.pack(pady=5)
        
        self.course_entry = tk.Entry(root, width=30)
        self.course_entry.pack(pady=5)
        
        # 添加課程按鈕
        self.add_button = tk.Button(root, text="添加課程", command=self.add_course)
        self.add_button.pack(pady=10)
        
        # 顯示課程列表
        self.course_listbox_label = tk.Label(root, text="課程列表（可手動調整順序）：")
        self.course_listbox_label.pack(pady=5)
        
        self.course_listbox = tk.Listbox(root, width=40, height=10, selectmode=tk.SINGLE)
        self.course_listbox.pack(pady=10)
        
        # 調整順序按鈕
        self.move_up_button = tk.Button(root, text="向上移動", command=self.move_up)
        self.move_up_button.pack(side=tk.LEFT, padx=5)
        
        self.move_down_button = tk.Button(root, text="向下移動", command=self.move_down)
        self.move_down_button.pack(side=tk.LEFT, padx=5)
        
        # 儲存課程按鈕
        self.save_button = tk.Button(root, text="儲存課程順序", command=self.save_courses)
        self.save_button.pack(pady=10)
        
        # 完成選課按鈕
        self.complete_button = tk.Button(root, text="選課完成，開始搶課", command=self.show_login_window)
        self.complete_button.pack(pady=10)
    
    def add_course(self):
        course_code = self.course_entry.get()
        if course_code:
            if course_code in self.course_data:  # 檢查課程代碼是否已存在
                messagebox.showwarning("錯誤", f"課程代碼 {course_code} 已經存在，請輸入不同的課程代碼。")
            else:
                self.course_data.append(course_code)
                self.course_listbox.insert(tk.END, course_code)
            self.course_entry.delete(0, tk.END)
    
    def move_up(self):
        selected_index = self.course_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            if selected_index > 0:
                # 移動選中的課程
                course_code = self.course_data[selected_index]
                self.course_data[selected_index] = self.course_data[selected_index - 1]
                self.course_data[selected_index - 1] = course_code
                
                # 更新顯示順序
                self.course_listbox.delete(selected_index)
                self.course_listbox.insert(selected_index - 1, course_code)
                self.course_listbox.select_set(selected_index - 1)
    
    def move_down(self):
        selected_index = self.course_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            if selected_index < len(self.course_data) - 1:
                # 移動選中的課程
                course_code = self.course_data[selected_index]
                self.course_data[selected_index] = self.course_data[selected_index + 1]
                self.course_data[selected_index + 1] = course_code
                
                # 更新顯示順序
                self.course_listbox.delete(selected_index)
                self.course_listbox.insert(selected_index + 1, course_code)
                self.course_listbox.select_set(selected_index + 1)
    
    def save_courses(self):
        if not self.course_data:
            messagebox.showwarning("錯誤", "課程列表為空，請添加課程後再儲存。")
            return
        with open("course_priority.txt", "w") as f:
            for course in self.course_data:
                f.write(course + "\n")
        messagebox.showinfo("儲存成功", "課程順序已儲存!")
    
    def show_login_window(self):
        # 彈出視窗讓使用者輸入帳號和密碼
        login_window = tk.Toplevel(self.root)
        login_window.title("登入選課系統")

        tk.Label(login_window, text="帳號：").pack(pady=5)
        account_entry = tk.Entry(login_window, width=30)
        account_entry.pack(pady=5)
        
        tk.Label(login_window, text="密碼：").pack(pady=5)
        password_entry = tk.Entry(login_window, width=30, show="*")
        password_entry.pack(pady=5)

        login_button = tk.Button(login_window, text="登入並搶課", command=lambda: self.start_enrollment(account_entry, password_entry, login_window))
        login_button.pack(pady=10)
    
    def start_enrollment(self, account_entry, password_entry, login_window):
        user_account = account_entry.get()
        user_password = password_entry.get()

        if not user_account or not user_password:
            messagebox.showwarning("錯誤", "帳號或密碼不可為空！")
            return

        # 讀取課程優先順序
        try:
            with open("course_priority.txt", "r") as file:
                course_ids = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            messagebox.showerror("錯誤", "課程順序檔案不存在，請先設定課程順序！")
            return
        
        # 使用 Selenium 開啟瀏覽器並操作 Flask 選課系統
        driver = webdriver.Chrome()

        # 打開選課系統頁面（此為 Flask 本地伺服器的 URL）
        driver.get('http://localhost:5000/login')  # 這裡用 Flask 本地伺服器的 URL

        # 登入選課系統
        username_field = driver.find_element(By.NAME, 'username')  # 替換為選課系統中帳號輸入框的 name 屬性
        password_field = driver.find_element(By.NAME, 'password')  # 替換為選課系統中密碼輸入框的 name 屬性

        username_field.send_keys(user_account)
        password_field.send_keys(user_password)

        login_button = driver.find_element(By.XPATH, '//*[@id="login_button"]')  # 替換為選課系統中登入按鈕的 XPATH
        login_button.click()

        # 等待頁面載入完成
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'course_selection_page')))  # 替換為課程選擇頁面的元素 ID

        # 開始搶課
        successfully_enrolled_courses = []  # 追蹤成功加選的課程
        for course_id in course_ids:
            try:
                # 找到並選擇課程
                course_button = driver.find_element(By.XPATH, f'//button[@data-course-id="{course_id}"]')  # 替換為課程選擇按鈕的 XPATH
                course_button.click()
                successfully_enrolled_courses.append(course_id)
                print(f"已成功選擇課程: {course_id}")
                
                # 等待確認
                time.sleep(2)
            except Exception as e:
                print(f"無法選擇課程: {course_id}")

        # 最後關閉瀏覽器
        driver.quit()

        print(f"成功選擇的課程: {successfully_enrolled_courses}")
        login_window.destroy()

# 主程式
if __name__ == "__main__":
    root = tk.Tk()
    app = CoursePriorityApp(root)
    root.mainloop()
