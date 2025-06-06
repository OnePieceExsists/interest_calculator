from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Toplevel, Radiobutton, IntVar
from tkinter import ttk
from logic.calculator import InterestCalculator
from utils.helpers import validate_input, format_result

class AppGUI:
    def __init__(self, master):
        self.master = master
        master.title("Interest Calculator")
        # Set main 1&2 windows to 30% of screen size & center
        screen_w = master.winfo_screenwidth()
        screen_h = master.winfo_screenheight()
        w = int(screen_w * 0.3)
        h = int(screen_h * 0.3)
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        master.geometry(f"{w}x{h}+{x}+{y}")
        self.credit_type = IntVar(value=0)
        self.show_credit_type_window()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def show_credit_type_window(self):
        self.clear_window()
        Label(self.master, text="Choose Credit Type:", anchor="center").grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

        Radiobutton(self.master, text="Maturity loan", variable=self.credit_type, value=1, anchor="w").grid(row=1, column=0, sticky="nsew")
        Radiobutton(self.master, text="Amortizing loan", variable=self.credit_type, value=2, anchor="w").grid(row=2, column=0, sticky="nsew")
        Radiobutton(self.master, text="Annuity loan", variable=self.credit_type, value=3, anchor="w").grid(row=3, column=0, sticky="nsew")

        Button(self.master, text="Next", command=self.open_main_form).grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

    def open_main_form(self):
        if self.credit_type.get() == 0:
            messagebox.showwarning("Warning", "Please select a credit type.")
            return
        self.build_main_form()

    def build_main_form(self):
        self.clear_window()
        Label(self.master, text="Amount of the Credit:", anchor="center").grid(row=0, column=0, sticky="nsew")
        self.principal = StringVar()
        Entry(self.master, textvariable=self.principal, justify="center").grid(row=0, column=1, sticky="nsew")

        Label(self.master, text="Interest Rate (%):", anchor="center").grid(row=1, column=0, sticky="nsew")
        self.rate = StringVar()
        Entry(self.master, textvariable=self.rate, justify="center").grid(row=1, column=1, sticky="nsew")

        Label(self.master, text="Years to Pay Off:", anchor="center").grid(row=2, column=0, sticky="nsew")
        self.time = StringVar()
        Entry(self.master, textvariable=self.time, justify="center").grid(row=2, column=1, sticky="nsew")

        Button(self.master, text="Calculate", command=self.calculate).grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")
        self.result_label = Label(self.master, text="", anchor="center")
        self.result_label.grid(row=4, column=0, columnspan=2, sticky="nsew")

        # Make columns expand equally
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

    def calculate(self):
        if validate_input(self.principal.get(), self.rate.get(), self.time.get()):
            principal = float(self.principal.get())
            rate = float(self.rate.get())
            time = int(float(self.time.get()))
            credit_type = self.credit_type.get()

            # Generate table data based on credit type
            if credit_type == 1:
                table_data = self.generate_maturity_loan_table(principal, rate, time)
            elif credit_type == 2:
                table_data = self.generate_amortizing_loan_table(principal, rate, time)
            elif credit_type == 3:
                table_data = self.generate_annuity_loan_table(principal, rate, time)
            else:
                messagebox.showerror("Error", "Unknown credit type selected.")
                return

            self.show_results_table(table_data)

    def show_results_table(self, table_data):
        result_window = Toplevel(self.master)
        result_window.title("Credit Repayment Table")
        # Set result window to 80% of screen size and center it
        screen_w = result_window.winfo_screenwidth()
        screen_h = result_window.winfo_screenheight()
        w = int(screen_w * 0.8)
        h = int(screen_h * 0.8)
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        result_window.geometry(f"{w}x{h}+{x}+{y}")

        columns = ("Year", "Debt Start", "Interest", "Amortization", "Payment", "Debt End")
        tree = ttk.Treeview(result_window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)
        tree.grid(row=0, column=0, sticky="nsew")

        for row in table_data:
            tree.insert("", "end", values=row)

        result_window.grid_rowconfigure(0, weight=1)
        result_window.grid_columnconfigure(0, weight=1)

    # Add these methods to generate the table data for each loan type
    def generate_maturity_loan_table(self, principal, rate, time):
        # Example logic for maturity loan (interest only, principal repaid at end)
        table = []
        total_interest = 0
        for year in range(1, time + 1):
            interest = principal * rate / 100
            amortization = 0 if year < time else principal
            payment = interest + amortization
            debt_end = principal if year < time else 0
            table.append([
                year,
                f"{principal:.2f}",
                f"{interest:.2f}",
                f"{amortization:.2f}",
                f"{payment:.2f}",
                f"{debt_end:.2f}"
            ])
            total_interest += interest
        # Totals row
        table.append([
            "Total", "", f"{total_interest:.2f}", f"{principal:.2f}", f"{total_interest + principal:.2f}", ""
        ])
        return table

    def generate_amortizing_loan_table(self, principal, rate, time):
        # Example logic for amortizing loan (equal principal payments)
        table = []
        remaining = principal
        total_interest = 0
        total_amortization = 0
        total_payment = 0
        amortization = principal / time
        for year in range(1, time + 1):
            interest = remaining * rate / 100
            payment = interest + amortization
            debt_end = remaining - amortization
            table.append([
                year,
                f"{remaining:.2f}",
                f"{interest:.2f}",
                f"{amortization:.2f}",
                f"{payment:.2f}",
                f"{debt_end:.2f}"
            ])
            total_interest += interest
            total_amortization += amortization
            total_payment += payment
            remaining = debt_end
        table.append([
            "Total", "", f"{total_interest:.2f}", f"{total_amortization:.2f}", f"{total_payment:.2f}", ""
        ])
        return table

    def generate_annuity_loan_table(self, principal, rate, time):
        # Example logic for annuity loan (equal total payments)
        table = []
        r = rate / 100
        n = time
        if r == 0:
            annuity = principal / n
        else:
            annuity = principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
        remaining = principal
        total_interest = 0
        total_amortization = 0
        total_payment = 0
        for year in range(1, n + 1):
            interest = remaining * r
            amortization = annuity - interest
            debt_end = remaining - amortization
            table.append([
                year,
                f"{remaining:.2f}",
                f"{interest:.2f}",
                f"{amortization:.2f}",
                f"{annuity:.2f}",
                f"{debt_end:.2f}"
            ])
            total_interest += interest
            total_amortization += amortization
            total_payment += annuity
            remaining = debt_end
        table.append([
            "Total", "", f"{total_interest:.2f}", f"{total_amortization:.2f}", f"{total_payment:.2f}", ""
        ])
        return table


def main():
    root = Tk()
    app = AppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()