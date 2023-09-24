import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog
from pathlib import Path


class App (ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title('FinDoc')
        self.geometry('700x700')
        self.state('zoomed')
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.bind('<Control-n>', self.new_file)
        self.bind('<Control-o>', self.open_file)
        self.bind('<Control-s>', self.save_file)

################################# Top Frame #################################

        self.topFrame = ctk.CTkFrame(self)
        self.topFrame.grid(row=0, column=0, sticky='nsew')
        self.topFrame.grid_rowconfigure(0, weight=1)
        self.topFrame.grid_columnconfigure(0, weight=1)

############################# Top Upper Frame #################################

        self.topUpperFrame = ctk.CTkFrame(self.topFrame)
        self.topUpperFrame.grid(row=0, column=0, sticky='nsew')
        self.topUpperFrame.grid_columnconfigure(1, weight=1)

###################################### Menu ################################################

        self.menu = tk.Frame(self.topUpperFrame)
        self.menu.grid(row=0, column=0)

        self.modeSelector = ctk.CTkSwitch(
            self.menu, text='テーマ', text_font=('游ゴシック', 12, 'bold'), width=50, command=self.toggle_darkmode)
        self.modeSelector.grid(row=0, column=0, sticky='nsew')

        self.targetLabel = tk.Label(
            self.menu, text='目標文字数', font=('游ゴシック', 14, 'bold'))
        self.targetLabel.grid(row=1, column=0)

        self.target = ctk.IntVar(self)
        self.targetInput = ctk.CTkEntry(
            self.menu, text_font=('游ゴシック', 14, 'bold'), textvariable=self.target, width=100)
        self.targetInput.grid(row=1, column=1)
        self.targetInput.bind('<FocusOut>', self.character_count)

        self.helpIcon = tk.PhotoImage(file='./image/help_icon.png')
        self.helpButton = tk.Button(
            self.menu, image=self.helpIcon, text='ヘルプ', font=('游ゴシック', 10), compound='top', command=self.help_dialog)
        self.helpButton.grid(row=1, column=3)

        self.newfileIcon = tk.PhotoImage(file='./image/newfile_icon.png')
        self.newfileButton = tk.Button(
            self.menu, image=self.newfileIcon, text='新規', font=('游ゴシック', 10), compound='top', command=self.new_file)
        self.newfileButton.grid(row=1, column=4)

        self.openfileIcon = tk.PhotoImage(file='./image/openfile_icon.png')
        self.openfileButton = tk.Button(
            self.menu, image=self.openfileIcon, text='開く', font=('游ゴシック', 10), compound='top', command=self.open_file)
        self.openfileButton.grid(row=1, column=5)

        self.saveIcon = tk.PhotoImage(file='./image/save_icon.png')
        self.saveButton = tk.Button(
            self.menu, image=self.saveIcon, text='保存', font=('游ゴシック', 10), compound='top', command=self.save_file)
        self.saveButton.grid(row=1, column=6, sticky='nsew')

        self.undoIcon = tk.PhotoImage(file='./image/undo_icon.png')
        self.undoButton = tk.Button(
            self.menu, image=self.undoIcon, text='元に戻す', font=('游ゴシック', 10), compound='top', command=lambda: self.text.edit_undo())
        self.undoButton.grid(row=1, column=7)

        self.redoIcon = tk.PhotoImage(file='./image/redo_icon.png')
        self.redoButton = tk.Button(
            self.menu, image=self.redoIcon, text='やり直す', font=('游ゴシック', 10), compound='top',  command=lambda: self.text.edit_redo())
        self.redoButton.grid(row=1, column=8)

        self.cutIcon = tk.PhotoImage(file='./image/cut_icon.png')
        self.cutButton = tk.Button(
            self.menu, image=self.cutIcon, text='切り取り', font=('游ゴシック', 10), compound='top',  command=lambda: self.focus_get().event_generate('<<Cut>>'))
        self.cutButton.grid(row=1, column=9)

        self.copyIcon = tk.PhotoImage(file='./image/copy_icon.png')
        self.copyButton = tk.Button(
            self.menu, image=self.copyIcon, text='コピー', font=('游ゴシック', 10), compound='top', command=lambda: self.focus_get().event_generate('<<Copy>>'))
        self.copyButton.grid(row=1, column=10)

        self.pasteIcon = tk.PhotoImage(file='./image/paste_icon.png')
        self.pasteButton = tk.Button(
            self.menu, image=self.pasteIcon, text='貼り付け', font=('游ゴシック', 10), compound='top', command=lambda: self.focus_get().event_generate('<<Paste>>'))
        self.pasteButton.grid(row=1, column=11, sticky='nsew')


################################### Additional Features #######################################

        self.additionalFeatures = tk.Frame(self.topUpperFrame)
        self.additionalFeatures.grid(row=0, column=2)

        self.countRawText = tk.Label(
            self.additionalFeatures, text='0文字（空白・改行を含む）', font=('游明朝', 10))
        self.countRawText.grid(row=0, column=0)

        self.count = tk.Label(self.additionalFeatures,
                              text='0/0文字達成', font=('游明朝', 14))
        self.count.grid(row=1, column=0)

#################################### Top Under Frame #############################################

        self.topUnderFrame = ctk.CTkFrame(self.topFrame)
        self.topUnderFrame.grid(row=1, column=0, sticky='nsew')
        self.topUnderFrame.grid_columnconfigure(0, weight=1)

        self.progressbar = ctk.CTkProgressBar(
            self.topUnderFrame, height=16)
        self.progressbar.grid(row=0, column=0, sticky='ew')
        self.progressbar.set(0)

################################### Bottom Frame ##########################################

        self.bottomFrame = ctk.CTkFrame(self)
        self.bottomFrame.grid(row=1, column=0, sticky='nsew')
        self.bottomFrame.grid_columnconfigure(0, weight=1)

        self.text = tk.Text(
            self.bottomFrame, font=('游明朝', 16), width=68, bd=2, relief='solid', undo=True, insertwidth=3.5, selectbackground='#8e8e8e')
        self.text.grid(row=0, column=0)
        self.text.bind('<KeyRelease>', self.character_count)

        self.textscroll = ctk.CTkScrollbar(
            self.bottomFrame, command=self.text.yview)
        self.textscroll.grid(row=0, column=1, sticky='ns')
        self.text['yscrollcommand'] = self.textscroll.set


################################### Right Click Pop-up Menu #####################################

        self.popupMenu = tk.Menu(self, tearoff=0, selectcolor='#8e8e8e')
        self.popupMenu.add_command(label='元に戻す', accelerator='Ctrl+Z',
                                   command=lambda: self.text.edit_undo())
        self.popupMenu.add_command(label='やり直す', accelerator='Ctrl+Y',
                                   command=lambda: self.text.edit_redo())
        self.popupMenu.add_command(label='切り取り', accelerator='Ctrl+X',
                                   command=lambda: self.focus_get().event_generate('<<Cut>>'))
        self.popupMenu.add_command(label='コピー', accelerator='Ctrl+C',
                                   command=lambda: self.focus_get().event_generate('<<Copy>>'))
        self.popupMenu.add_command(label='貼り付け', accelerator='Ctrl+V',
                                   command=lambda: self.focus_get().event_generate('<<Paste>>'))
        self.bind('<Button-3>',
                  lambda event: self.popupMenu.tk_popup(event.x_root, event.y_root))

########################################## Method ################################################

    def help_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title('ヘルプ')
        dialog.geometry('320x450')
        dialog.resizable(False, False)

        ctk.CTkLabel(dialog, text='ショートカットキー', text_font=(
            '游ゴシック', 14, 'bold')).grid(row=0, column=0, columnspan=2, sticky='nsew')

        ctk.CTkLabel(dialog, text='新規', text_font=(
            '游明朝', 10)).grid(row=1, column=0)
        ctk.CTkLabel(dialog, text='開く', text_font=(
            '游明朝', 10)).grid(row=2, column=0)
        ctk.CTkLabel(dialog, text='保存', text_font=(
            '游明朝', 10)).grid(row=3, column=0)
        ctk.CTkLabel(dialog, text='元に戻す', text_font=(
            '游明朝', 10)).grid(row=4, column=0)
        ctk.CTkLabel(dialog, text='やり直す', text_font=(
            '游明朝', 10)).grid(row=5, column=0)
        ctk.CTkLabel(dialog, text='切り取り', text_font=(
            '游明朝', 10)).grid(row=6, column=0)
        ctk.CTkLabel(dialog, text='コピー', text_font=(
            '游明朝', 10)).grid(row=7, column=0)
        ctk.CTkLabel(dialog, text='貼り付け', text_font=(
            '游明朝', 10)).grid(row=8, column=0)
        ctk.CTkLabel(dialog, text='全選択', text_font=(
            '游明朝', 10)).grid(row=9, column=0)
        ctk.CTkLabel(dialog, text='複数選択', text_font=(
            '游明朝', 10)).grid(row=10, column=0)
        ctk.CTkLabel(dialog, text='空白飛び', text_font=(
            '游明朝', 10)).grid(row=11, column=0)
        ctk.CTkLabel(dialog, text='空白飛び選択', text_font=(
            '游明朝', 10)).grid(row=12, column=0)

        ctk.CTkLabel(dialog, text='Ctrl+N', text_font=('游明朝', 10)
                     ).grid(row=1, column=1)
        ctk.CTkLabel(dialog, text='Ctrl+O', text_font=('游明朝', 10)
                     ).grid(row=2, column=1)
        ctk.CTkLabel(dialog, text='Ctrl+S', text_font=('游明朝', 10)
                     ).grid(row=3, column=1)
        ctk.CTkLabel(dialog, text='Ctrl+Z', text_font=('游明朝', 10)
                     ).grid(row=4, column=1)
        ctk.CTkLabel(dialog, text='Ctrl+Y', text_font=('游明朝', 10)
                     ).grid(row=5, column=1)
        ctk.CTkLabel(dialog, text='Ctrl+X', text_font=('游明朝', 10)
                     ).grid(row=6, column=1)
        ctk.CTkLabel(dialog, text='Ctrl+C', text_font=('游明朝', 10)
                     ).grid(row=7, column=1)
        ctk.CTkLabel(dialog, text='Ctrl+V', text_font=('游明朝', 10)
                     ).grid(row=8, column=1)
        ctk.CTkLabel(dialog, text='Ctrl+A', text_font=('游明朝', 10)
                     ).grid(row=9, column=1)
        ctk.CTkLabel(dialog, text='Shift+↑↓←→', text_font=('游明朝', 10)
                     ).grid(row=10, column=1)
        ctk.CTkLabel(dialog, text='Ctrl+↑↓←→', text_font=('游明朝', 10)
                     ).grid(row=11, column=1)
        ctk.CTkLabel(dialog, text='Ctrl+Shift+↑↓←→', text_font=('游明朝', 10)
                     ).grid(row=12, column=1)

        ctk.CTkLabel(dialog, text='').grid(row=13, column=0)

        ctk.CTkLabel(dialog, text='テーマの初期状態はパソコンのテーマに依存します。', text_font=('游明朝', 10)
                     ).grid(row=14, column=0, columnspan=2)


    def new_file(self, event=None):
        messagebox.askokcancel('確認', '保存されていない場合、現在のデータは失われますがよろしいですか？')
        self.text.delete('1.0', 'end')
        self.title('FinDoc')

    def open_file(self, event=None):
        directory = filedialog.askopenfilename(defaultextension='*.txt',
                                               filetypes=(('テキスト ファイル', '*.txt'), ('すべてのファイル', '*.*')))
        with open(directory, 'r', encoding='utf-8') as f:
            text = f.read()
        self.text.delete('1.0', 'end')
        self.text.insert('end', text)
        self.title(f'{Path(directory).stem}- FinDoc')

    def save_file(self, event=None):
        directory = filedialog.asksaveasfilename(defaultextension='*.txt',
                                                 filetypes=(('テキスト ファイル', '*.txt'), ('すべてのファイル', '*.*')))
        with open(directory, 'w', encoding='utf-8') as f:
            f.write(self.text.get('1.0', 'end'))
        self.title(f'{Path(directory).stem}- FinDoc')


    def character_count(self, args):
        rawText = len(self.text.get('1.0', 'end-1c'))
        currentCharacters = len(self.text.get(
            '1.0', 'end-1c').translate(str.maketrans({'\n': None, ' ': None, '　': None, '\t': None})))
        targetCharacters = self.target.get()
        self.countRawText.configure(text=f'{rawText}文字（空白・改行を含む）')
        self.count.configure(
            text=f'{currentCharacters}/{targetCharacters}文字達成')
        try:
            self.progressbar.set(currentCharacters/targetCharacters)
        except:
            self.progressbar.set(0)

    def darkmode(self):
        color1 = '#303030'
        color2 = '#383838'
        color3 = '#1e1e1e'
        textColor = '#ffffff'
        ctk.set_appearance_mode('dark')
        self.menu.configure(bg=color2)
        self.helpButton.configure(bg=color1, fg=textColor)
        self.newfileButton.configure(bg=color1, fg=textColor)
        self.openfileButton.configure(bg=color1, fg=textColor)
        self.saveButton.configure(bg=color1, fg=textColor)
        self.undoButton.configure(bg=color1, fg=textColor)
        self.redoButton.configure(bg=color1, fg=textColor)
        self.cutButton.configure(bg=color1, fg=textColor)
        self.copyButton.configure(bg=color1, fg=textColor)
        self.pasteButton.configure(bg=color1, fg=textColor)
        self.targetLabel.configure(bg=color2, fg=textColor)
        self.additionalFeatures.configure(bg=color2)
        self.count.configure(bg=color2, fg=textColor)
        self.countRawText.configure(bg=color2, fg=textColor)
        self.text.configure(bg=color3, foreground=textColor,
                            insertbackground=textColor, selectforeground=textColor)
        self.popupMenu.configure(bg=color1, fg=textColor)

    def lightmode(self):
        color1 = '#dfdfdf'
        color2 = '#d1d1d1'
        color3 = 'SystemButtonFace'
        textColor = '#000000'
        ctk.set_appearance_mode('light')
        self.menu.configure(bg=color2)
        self.helpButton.configure(bg=color1, fg=textColor)
        self.newfileButton.configure(bg=color1, fg=textColor)
        self.openfileButton.configure(bg=color1, fg=textColor)
        self.saveButton.configure(bg=color1, fg=textColor)
        self.undoButton.configure(bg=color1, fg=textColor)
        self.redoButton.configure(bg=color1, fg=textColor)
        self.cutButton.configure(bg=color1, fg=textColor)
        self.copyButton.configure(bg=color1, fg=textColor)
        self.pasteButton.configure(bg=color1, fg=textColor)
        self.targetLabel.configure(bg=color2, fg=textColor)
        self.additionalFeatures.configure(bg=color2)
        self.count.configure(bg=color2, fg=textColor)
        self.countRawText.configure(bg=color2, fg=textColor)
        self.text.configure(bg=color3, fg=textColor,
                            insertbackground=textColor, selectforeground=textColor)
        self.popupMenu.configure(bg=color1, fg=textColor)

    def toggle_darkmode(self):
        if self.modeSelector.get() == 1:
            self.darkmode()
        else:
            self.lightmode()

    def on_closing(self, event=None):
        close = messagebox.askyesno('終了', '本当に終了してよろしいですか？')
        if close:
            self.pause = True
            self.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode('system')
    ctk.set_default_color_theme('green')
    app = App()
    if ctk.get_appearance_mode() == 'Dark':
        app.modeSelector.toggle()
    else:
        app.lightmode()
    app.mainloop()
