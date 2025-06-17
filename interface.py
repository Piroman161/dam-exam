import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Имитация базы данных
materials = [
    {
        "material_id": 1,
        "name": "Сталь",
        "type": "Металл",
        "quantity_in_stock": 1000,
        "unit": "кг",
        "package_quantity": 50,
        "min_quantity": 10,
        "unit_price": 150.00
    },
    {
        "material_id": 2,
        "name": "Пластик",
        "type": "Полимер",
        "quantity_in_stock": 500,
        "unit": "л",
        "package_quantity": 20,
        "min_quantity": 5,
        "unit_price": 80.00
    }
]

next_id = 3

class MaterialForm(tk.Toplevel):
    def __init__(self, master, material=None):
        super().__init__(master)
        self.title("Добавление материала" if material is None else "Редактирование материала")
        self.geometry("400x400")
        self.resizable(False, False)
        
        self.material = material
        self.result = None

        # Поля формы
        labels = [
            ("Наименование:", 'name'),
            ("Тип материала:", 'type'),
            ("Количество на складе:", 'quantity_in_stock'),
            ("Единица измерения:", 'unit'),
            ("Количество в упаковке:", 'package_quantity'),
            ("Минимальное количество:", 'min_quantity'),
            ("Цена за единицу:", 'unit_price')
        ]

        self.entries = {}

        for idx, (label_text, key) in enumerate(labels):
            lbl = tk.Label(self, text=label_text)
            lbl.grid(row=idx, column=0, padx=10, pady=5, sticky='w')
            if key == 'type':
                combo = ttk.Combobox(self, values=["Металл", "Полимер", "Керамика", "Дерево", "Другие"])
                combo.grid(row=idx, column=1, padx=10, pady=5)
                self.entries[key] = combo
            else:
                entry = tk.Entry(self)
                entry.grid(row=idx, column=1, padx=10, pady=5)
                self.entries[key] = entry

        # Если редактирование - заполняем поля текущими данными
        if material:
            self.entries['name'].insert(0, material['name'])
            self.entries['type'].set(material['type'])
            self.entries['quantity_in_stock'].insert(0, str(material['quantity_in_stock']))
            self.entries['unit'].insert(0, material['unit'])
            self.entries['package_quantity'].insert(0, str(material['package_quantity']))
            self.entries['min_quantity'].insert(0, str(material['min_quantity']))
            self.entries['unit_price'].insert(0, str(material['unit_price']))

        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=15)

        btn_save = tk.Button(btn_frame, text="Сохранить", command=self.save)
        btn_save.pack(side='left', padx=10)

        btn_cancel = tk.Button(btn_frame, text="Отмена", command=self.cancel)
        btn_cancel.pack(side='left', padx=10)

    def save(self):
        try:
            name = self.entries['name'].get().strip()
            type_ = self.entries['type'].get().strip()
            quantity_in_stock = float(self.entries['quantity_in_stock'].get())
            unit = self.entries['unit'].get().strip()
            package_quantity = float(self.entries['package_quantity'].get())
            min_quantity = float(self.entries['min_quantity'].get())
            unit_price = float(self.entries['unit_price'].get())

            if not name:
                messagebox.showerror("Ошибка", "Введите название материала.")
                return

            data = {
                'name': name,
                'type': type_,
                'quantity_in_stock': quantity_in_stock,
                'unit': unit,
                'package_quantity': package_quantity,
                'min_quantity': min_quantity,
                'unit_price': unit_price
            }

            if self.material:
                # Обновление существующего
                self.result = data
                self.result['material_id'] = self.material['material_id']
            else:
                # Новое добавление
                global next_id
                data['material_id'] = next_id
                next_id += 1
                self.result = data

            self.destroy()
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте правильность введённых чисел.")

    def cancel(self):
        self.destroy()

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Управление материалами")
        self.geometry("800x600")
        
        # Логотип (можно добавить изображение при необходимости)
        lbl_logo = tk.Label(self, text="Логотип", font=("Comic Sans MS", 14))
        lbl_logo.pack(pady=10)

        # Таблица материалов
        columns = ("material_id", "name", "type", "quantity_in_stock", 
                   "unit", "package_quantity", "min_quantity", "unit_price")
        
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        
        for col in columns:
            if col == 'material_id':
                continue  # скрываем ID в отображении
            self.tree.heading(col, text=col.replace('_', ' ').title())
        
        # Скрываем колонку ID
        self.tree.column('material_id', width=0, stretch=False)
        
        self.tree.pack(fill='both', expand=True, padx=10)

        # Кнопки управления
        btn_frame = tk.Frame(self)
        
        btn_add = tk.Button(btn_frame, text="Добавить материал", bg="#546F94", fg="white",
                            font=("Comic Sans MS", 10), command=self.add_material)
        
        btn_edit = tk.Button(btn_frame, text="Редактировать выбранный материал", bg="#546F94", fg="white",
                             font=("Comic Sans MS", 10), command=self.edit_material)
        
        btn_add.pack(side='left', padx=10)
        btn_edit.pack(side='left', padx=10)

        btn_frame.pack(pady=10)
         
    def load_materials(self):
       for item in self.tree.get_children():
           self.tree.delete(item)
       for mat in materials:
           values = (
               mat["material_id"],
               mat["name"],
               mat["type"],
               mat["quantity_in_stock"],
               mat["unit"],
               mat["package_quantity"],
               mat["min_quantity"],
               mat["unit_price"]
           )
           # вставляем без ID в отображение (ID скрыт колонкой)
           item_id=self.tree.insert('', 'end', values=values[1:], iid=str(mat["material_id"]))
    
    def add_material(self):
       form = MaterialForm(self)
       self.wait_window(form)
       if form.result:
           materials.append(form.result)
           self.load_materials()

    def edit_material(self):
       selected_item = self.tree.selection()
       if not selected_item:
           messagebox.showwarning("Предупреждение", "Пожалуйста выберите материал для редактирования.")
           return
       item_id=int(selected_item[0])
       material = next((m for m in materials if m["material_id"]==item_id), None)
       if not material:
           messagebox.showerror("Ошибка", "Материал не найден.")
           return
       form = MaterialForm(self, material)
       self.wait_window(form)
       if form.result:
           # Обновляем данные в списке
           index = materials.index(material)
           materials[index] = form.result
           self.load_materials()

if __name__ == "__main__":
    app = MainApp()
    app.load_materials()
    app.mainloop()