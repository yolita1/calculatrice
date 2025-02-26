import tkinter as tk

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculatrice")
        self.expression = ""
        self.text_input = tk.StringVar()
        self.entry = tk.Entry(master, textvariable=self.text_input, font=('arial', 20, 'bold'), bd=30, insertwidth=4, width=14, borderwidth=4, justify='right')
        self.entry.grid(row=0, column=0, columnspan=4)
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        row = 1
        col = 0
        for button in buttons:
            if button == "=":
                tk.Button(master, text=button, padx=20, pady=20, font=('arial', 20, 'bold'), command=self.evaluate).grid(row=row, column=col, sticky="nsew")
            else:
                tk.Button(master, text=button, padx=20, pady=20, font=('arial', 20, 'bold'), command=lambda b=button: self.button_click(b)).grid(row=row, column=col, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1
        tk.Button(master, text="C", padx=20, pady=20, font=('arial', 20, 'bold'), command=self.clear).grid(row=row, column=0, columnspan=4, sticky="nsew")
        for i in range(5):
            master.grid_rowconfigure(i, weight=1)
        for i in range(4):
            master.grid_columnconfigure(i, weight=1)

    def button_click(self, char):
        self.expression += str(char)
        self.text_input.set(self.expression)

    def evaluate(self):
        try:
            result = str(eval(self.expression))
            self.text_input.set(result)
            self.expression = result
        except Exception:
            self.text_input.set("Erreur")
            self.expression = ""

    def clear(self):
        self.expression = ""
        self.text_input.set("")

root = tk.Tk()
calc = Calculator(root)
root.mainloop()
