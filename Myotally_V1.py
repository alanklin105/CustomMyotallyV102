import tkinter
from tkinter import messagebox, filedialog, ttk
import os
import winsound
import sort  # Imports your sort.py logic
try:
    import call_Myotally as MT
except ImportError:
    MT = None

class this_GUI:
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.main_window.title('Myotally V102')

        # --- SECTION 1: PRE-PROCESSING (SORTING) ---
        label_sort_title = tkinter.Label(self.main_window, text="STEP 1: ORGANIZE RAW IMAGES", font=('Helvetica', 10, 'bold'))
        label_sort_title.pack(pady=(15, 0))

        frame_sort = tkinter.Frame(self.main_window, bd=1, relief="sunken", padx=10, pady=10)
        frame_sort.pack(pady=5, padx=15, fill='x')

        tkinter.Label(frame_sort, text='Folder containing unsorted .tif files:').grid(row=0, column=0, sticky='w')
        self.entry_sort = tkinter.Entry(frame_sort, width=40)
        self.entry_sort.grid(row=1, column=0, padx=5, pady=5)

        btn_browse_sort = tkinter.Button(frame_sort, text="Browse", command=self.browse_sort_folder)
        btn_browse_sort.grid(row=1, column=1, padx=2)

        btn_execute_sort = tkinter.Button(frame_sort, text="Sort Folder", command=self.execute_sort, bg="#bbdefb")
        btn_execute_sort.grid(row=2, column=0, columnspan=2, pady=5, sticky='ew')

        # Visual Separator
        ttk.Separator(self.main_window, orient='horizontal').pack(fill='x', padx=20, pady=20)

        # --- SECTION 2: ANALYSIS PARAMETERS ---
        label_analysis_title = tkinter.Label(self.main_window, text="STEP 2: RUN MYOTALLY ANALYSIS", font=('Helvetica', 10, 'bold'))
        label_analysis_title.pack()

        # Analysis Parent Folder
        frame_main = tkinter.Frame(self.main_window, padx=15)
        frame_main.pack(fill='x', pady=5)
        tkinter.Label(frame_main, text='Analysis Parent Folder:').pack(anchor='w')
        self.entry1 = tkinter.Entry(frame_main, width=45)
        self.entry1.pack(side='left', padx=5)
        tkinter.Button(frame_main, text="Browse", command=self.browse_main_folder).pack(side='left')

        # Individual File Selection (Restored Browse Buttons)
        frame_files = tkinter.Frame(self.main_window, pady=10)
        frame_files.pack()

        # DAPI
        tkinter.Label(frame_files, text='DAPI image name:').grid(row=0, column=0, sticky='e')
        self.entry2 = tkinter.Entry(frame_files, width=25)
        self.entry2.grid(row=0, column=1, padx=5)
        tkinter.Button(frame_files, text="Browse", command=lambda: self.browse_file(self.entry2)).grid(row=0, column=2)

        # Laminin
        tkinter.Label(frame_files, text='Laminin image name:').grid(row=1, column=0, sticky='e', pady=5)
        self.entry3 = tkinter.Entry(frame_files, width=25)
        self.entry3.grid(row=1, column=1, padx=5)
        tkinter.Button(frame_files, text="Browse", command=lambda: self.browse_file(self.entry3)).grid(row=1, column=2)

        # MFI
        tkinter.Label(frame_files, text='MFI image name(s):').grid(row=2, column=0, sticky='e')
        self.entry4 = tkinter.Entry(frame_files, width=25)
        self.entry4.grid(row=2, column=1, padx=5)

        # Settings
        frame_settings = tkinter.Frame(self.main_window, pady=10)
        frame_settings.pack()
        tkinter.Label(frame_settings, text='Quality:').pack(side='left')
        self.image_quality_var = tkinter.IntVar(value=2)
        tkinter.Radiobutton(frame_settings, text='Low', variable=self.image_quality_var, value=1).pack(side='left')
        tkinter.Radiobutton(frame_settings, text='High', variable=self.image_quality_var, value=2).pack(side='left')

        # Size
        frame_size = tkinter.Frame(self.main_window)
        frame_size.pack()
        tkinter.Label(frame_size, text='Fiber Size Range: Min').pack(side='left')
        self.entry6_2 = tkinter.Entry(frame_size, width=8); self.entry6_2.pack(side='left', padx=2)
        tkinter.Label(frame_size, text='to Max').pack(side='left')
        self.entry6_3 = tkinter.Entry(frame_size, width=8); self.entry6_3.pack(side='left', padx=2)

        self.cbvar7 = tkinter.IntVar(value=0)
        tkinter.Checkbutton(self.main_window, text='Use Default Size (200-3000)', variable=self.cbvar7).pack(pady=5)

        # Ratio
        frame_ratio = tkinter.Frame(self.main_window, pady=5)
        frame_ratio.pack()
        tkinter.Label(frame_ratio, text='pixel : µm² ratio:').pack(side='left')
        self.entry8_1 = tkinter.Entry(frame_ratio, width=10)
        self.entry8_1.insert(0, '1')
        self.entry8_1.pack(side='left')

        # Execution Buttons
        frame_btns = tkinter.Frame(self.main_window, pady=20)
        frame_btns.pack()
        tkinter.Button(frame_btns, text='RUN MYOTALLY', command=self.run, bg="#c8e6c9", width=20, height=2).pack(side='left', padx=10)
        tkinter.Button(frame_btns, text='Quit', command=self.main_window.destroy, width=10).pack(side='left')

        self.main_window.mainloop()

    # --- Methods ---
    def browse_sort_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.entry_sort.delete(0, tkinter.END)
            self.entry_sort.insert(0, path)

    def browse_main_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.entry1.delete(0, tkinter.END)
            self.entry1.insert(0, path)

    def browse_file(self, entry_widget):
        """Returns only the filename, not the full path."""
        full_path = filedialog.askopenfilename()
        if full_path:
            filename = os.path.basename(full_path)
            entry_widget.delete(0, tkinter.END)
            entry_widget.insert(0, filename)

    def execute_sort(self):
        folder = self.entry_sort.get()
        if not folder:
            messagebox.showwarning("Input Error", "Please select a folder to sort.")
            return
        result_msg, is_success = sort.sort_images_by_suffix(folder)
        if is_success:
            messagebox.showinfo("Success", result_msg)
        else:
            messagebox.showerror("Error", result_msg)

    def run(self):
        if not MT:
            messagebox.showerror("Error", "call_Myotally.py not found.")
            return
        try:
            path = self.entry1.get()
            dapi = self.entry2.get()
            laminin = self.entry3.get()
            if not path or not dapi or not laminin:
                raise ValueError("Folder path, DAPI, and Laminin names are all required.")

            if self.cbvar7.get() == 0:
                MT.main(path, dapi, laminin, self.entry4.get(),
                        self.image_quality_var.get(), float(self.entry6_2.get()),
                        float(self.entry6_3.get()), float(self.entry8_1.get()))
            else:
                MT.main(path, dapi, laminin, self.entry4.get(),
                        self.image_quality_var.get(), 200, 3000, float(self.entry8_1.get()))

            
            messagebox.showinfo('Success', 'Processing Complete!')
        except Exception as e:
            winsound.MessageBeep(winsound.MB_ICONHAND)
            messagebox.showerror('Error', f'An error occurred: {e}')

if __name__ == "__main__":
    this_GUI()
