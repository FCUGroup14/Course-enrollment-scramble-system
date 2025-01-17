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
        
        # 調整順序按鈕
        self.move_up_button = tk.Button(root, text="向上移動", command=self.move_up)
        self.move_up_button.pack(side=tk.LEFT, padx=5)
        
        self.move_down_button = tk.Button(root, text="向下移動", command=self.move_down)
        self.move_down_button.pack(side=tk.LEFT, padx=5)
        
        # 儲存課程按鈕
        self.save_button = tk.Button(root, text="儲存課程順序", command=self.save_courses)
        self.save_button.pack(pady=10)
    
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

# 主程式
if __name__ == "__main__":
    root = tk.Tk()
    app = CoursePriorityApp(root)
    root.mainloop()
