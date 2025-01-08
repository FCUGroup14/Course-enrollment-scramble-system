import tkinter as tk
from tkinter import messagebox

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
        
        # 上移按鈕
        self.move_up_button = tk.Button(root, text="上移", command=self.move_up)
        self.move_up_button.pack(side=tk.LEFT, padx=5)
        
        # 下移按鈕
        self.move_down_button = tk.Button(root, text="下移", command=self.move_down)
        self.move_down_button.pack(side=tk.LEFT, padx=5)
        
        # 提交按鈕
        self.submit_button = tk.Button(root, text="提交設定", command=self.submit_courses)
        self.submit_button.pack(pady=10)
    
    def add_course(self):
        # 獲取用戶輸入的課程代碼
        course_code = self.course_entry.get().strip()
        
        # 檢查課程代碼的格式
        if len(course_code) == 4 and course_code.isdigit():
            # 將課程代碼添加到列表中
            self.course_data.append(course_code)
            self.update_course_listbox()
            self.course_entry.delete(0, tk.END)
        else:
            messagebox.showerror("錯誤", "請輸入有效的四位數課程代碼")
    
    def update_course_listbox(self):
        # 更新顯示的課程列表
        self.course_listbox.delete(0, tk.END)
        for course in self.course_data:
            self.course_listbox.insert(tk.END, course)
    
    def move_up(self):
        # 獲取選中的課程
        selected_index = self.course_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            if index > 0:  # 確保選中的項目不會移動到列表的最前面
                # 交換選中課程和上一個課程
                self.course_data[index], self.course_data[index - 1] = self.course_data[index - 1], self.course_data[index]
                self.update_course_listbox()
                self.course_listbox.selection_set(index - 1)  # 保持選中的項目不變
            else:
                messagebox.showwarning("警告", "此課程已經是最高優先順序")
    
    def move_down(self):
        # 獲取選中的課程
        selected_index = self.course_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            if index < len(self.course_data) - 1:  # 確保選中的項目不會移動到列表的最後面
                # 交換選中課程和下一個課程
                self.course_data[index], self.course_data[index + 1] = self.course_data[index + 1], self.course_data[index]
                self.update_course_listbox()
                self.course_listbox.selection_set(index + 1)  # 保持選中的項目不變
            else:
                messagebox.showwarning("警告", "此課程已經是最低優先順序")
    
    def submit_courses(self):
        # 顯示提交成功的訊息
        if not self.course_data:
            messagebox.showwarning("警告", "請至少添加一門課程")
        else:
            print("設定的課程代碼:", self.course_data)
            messagebox.showinfo("設定成功", "課程優先順序設定完成，開始搶課！")
            
            # 開始搶課
            self.start_enrollment(self.course_data)

    def start_enrollment(self, course_data):
        # 開始搶課邏輯
        print("開始搶課，課程順序：", course_data)
        for course in course_data:
            print(f"正在搶課：{course}")
            # 模擬搶課過程
            # 實際的搶課邏輯，比如檢查課程是否有名額等
            # 在這裡您可以使用實際的自動化腳本來進行搶課
            print(f"課程 {course} 加選成功！")
        messagebox.showinfo("搶課成功", "所有課程搶選完成！")

# 創建Tkinter窗口並運行應用
root = tk.Tk()
app = CoursePriorityApp(root)
root.mainloop()
