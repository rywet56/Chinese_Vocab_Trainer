import sys, os
sys.path.append('/Users/manuel/OneDrive/Chinese_Vocab_Trainer')
from tkinter import *
from random import shuffle
from chinese_vocab_trainer.vocab import Vocab
# from PIL import ImageTk, Image


class Application:
    def __init__(self):
        self.vocab = None
        self.direction = "ec"
        self.box = 0
        # stack created after pressing start button
        self.word_list = None
        # list of words generated from word_list but
        self.rand_word_list = None
        # word currently being asked to translate
        self.current_word = None
        # accessors to labels in window that display vocabulary
        self.chin = None
        self.pin = None
        self.eng = None
        # number of words that have already been tested
        self.words_tested = None
        # number of words that should be tested
        self.num_words = None
        # upper and lower limiting threshold for deciding whether vocab is move or not
        self.low_limit = None
        self.up_limit = None

        self.buttons = {"start": None, "finish": None, "next": None, "reveal": None, "correct": None, "wrong": None}
        self.activity = {"start": False, "finish": False, "next": False, "reveal": False, "correct": True,
                         "wrong": True}
        self.but_active = {"start": "black", "finish": "black", "next": "black", "reveal": "black",
                               "correct": "green", "wrong": "#F36B60"}
        self.but_inactive = {"start": "grey", "finish": "grey", "next": "grey", "reveal": "grey",
                                 "correct": "grey", "wrong": "grey"}

    def start_gui(self):
        root = Tk()
        root.title("Chinese Vocabulary Trainer")
        root.resizable(0, 0)

        # it works!!!!!!
        img = PhotoImage(file='chin.png')
        root.tk.call('wm', 'iconphoto', root._w, img)
        # -------------------------


        # my_img = ImageTk.PhotoImage(Image.open("chin.png"))

        # root.iconbitmap('/Users/manuel/OneDrive/Chinese_Vocab_Trainer/chinese_vocab_trainer/chin.icns')

        # img = Image("photo", file="chin.png®")
        # root.iconphoto(True, img) # you may also want to try this.
        # root.tk.call('wm', 'iconphoto', root._w, img)

        mainframe = LabelFrame(root, text='', padx=0, pady=0, borderwidth=0)
        mainframe.pack(padx=20, pady=0)

        loadframe = LabelFrame(mainframe, text='', padx=10, pady=0, borderwidth=0)
        loadframe.grid(row=0, column=0, padx=0, pady=0)

        trainingframe = LabelFrame(mainframe, text='', padx=0, pady=20, borderwidth=0)
        trainingframe.grid(row=1, column=0, padx=0, pady=0)

        # ----------
        # LOAD FRAME

        # Entry frame
        entryframe = LabelFrame(loadframe, text='', padx=0, pady=0, borderwidth=0)
        entryframe.grid(row=0, column=0, padx=0, pady=0, rowspan=2)

        no_words = Label(entryframe, text="number of words")
        no_words.grid(row=0, column=0)

        number_words_entry = Entry(entryframe, width=5, borderwidth=5)
        number_words_entry.grid(row=0, column=1, columnspan=1, padx=5, pady=5)
        number_words_entry.insert(0, "0")

        low_limit = Label(entryframe, text="lower limit")
        low_limit.grid(row=1, column=0)

        low_limit_entry = Entry(entryframe, width=5, borderwidth=5)
        low_limit_entry.grid(row=1, column=1, columnspan=1, padx=5, pady=5)
        low_limit_entry.insert(0, "-2")

        up_limit = Label(entryframe, text="upper limit")
        up_limit.grid(row=2, column=0)

        up_limit_entry = Entry(entryframe, width=5, borderwidth=5)
        up_limit_entry.grid(row=2, column=1, columnspan=1, padx=5, pady=5)
        up_limit_entry.insert(0, "+5")

        # Drop Frame
        dropframe = LabelFrame(loadframe, text='', padx=0, pady=0, borderwidth=0)
        dropframe.grid(row=0, column=1, padx=0, pady=0)

        chapter = StringVar()
        chapter.set("Box 1")
        chap = OptionMenu(dropframe, chapter, "Box 1", "Box 2", "Box 3", "Box 4", "Box 5")
        chap.grid(row=0, column=0)

        direction = StringVar()
        direction.set("English -> Chinese")
        dir_drop = OptionMenu(dropframe, direction, "English -> Chinese", "Chinese -> English")
        dir_drop.grid(row=0, column=1)

        filepath_entry = Entry(dropframe, width=30, borderwidth=5)
        filepath_entry.grid(row=0, column=2, columnspan=1, padx=10, pady=10)
        filepath_entry.insert(0, "/Users/manuel/Desktop/chinese.txt")

        # button frame
        buttonframe = LabelFrame(loadframe, text='', padx=0, pady=0, borderwidth=0)
        buttonframe.grid(row=1, column=1, padx=0, pady=0)

        self.buttons["start"] = Button(buttonframe, text="Start", fg="black", padx=40, pady=20, font=("Helvetica", 15),
                                       width=5, command=lambda: self.start_learning(filepath_entry.get(), chapter.get(),
                                        direction.get(), number_words_entry.get(), low_limit_entry.get(), up_limit_entry.get()))
        self.buttons["start"].grid(row=0, column=0)

        self.buttons["finish"] = Button(buttonframe, text="Finish", fg="grey", padx=40, pady=20, font=("Helvetica", 15),
                        width=5, command=lambda: self.finish(filepath_entry.get()))
        self.buttons["finish"].grid(row=0, column=1, padx=20)

        # ----------
        # TRAINING FRAME

        # VOCAB FRame
        vocabframe = LabelFrame(trainingframe, text='', padx=0, pady=0, borderwidth=0)
        vocabframe.grid(row=0, column=1, padx=0, pady=20)

        self.chin = StringVar()
        chin_label = Label(vocabframe, textvariable=self.chin, bg="lightgrey", width=20, font=("Helvetica", 30))
        chin_label.grid(row=0, column=0, padx=5)

        self.pin = StringVar()
        pin_label = Label(vocabframe, textvariable=self.pin, bg="lightgrey", width=20, font=("Helvetica", 30))
        pin_label.grid(row=0, column=1, padx=5)

        self.eng = StringVar()
        eng_label = Label(vocabframe, textvariable=self.eng, bg="lightgrey", width=20, font=("Helvetica", 30))
        eng_label.grid(row=0, column=2, padx=5)

        # ACTION FRAME
        actionframe = LabelFrame(trainingframe, text='', padx=0, pady=20, borderwidth=0)
        actionframe.grid(row=1, column=1, padx=0, pady=0)

        self.buttons["next"] = Button(actionframe, text="Next", fg="grey", padx=40, pady=20, font=("Helvetica", 15),
                      width=5, command=lambda: self.next())
        self.buttons["next"].grid(row=3, column=0, padx=20)

        self.buttons["reveal"] = Button(actionframe, text="Reveal", fg="grey", padx=40, pady=20, font=("Helvetica", 15),
                        width=5, command=lambda: self.reveal())
        self.buttons["reveal"].grid(row=3, column=1, padx=20)

        self.buttons["correct"] = Button(actionframe, text="correct", fg="grey", padx=40, pady=20, font=("Helvetica", 15),
                         width=5, command=lambda: self.correct(chapter.get()))
        self.buttons["correct"].grid(row=3, column=2, padx=20)

        self.buttons["wrong"] = Button(actionframe, text="wrong", fg="grey", padx=40, pady=20, font=("Helvetica", 15),
                       width=5, command=lambda: self.wrong(chapter.get()))
        self.buttons["wrong"].grid(row=3, column=3, padx=20)

        root.mainloop()

    def start_app(self):
        self.start_gui()

    def correct(self, chapter):
        if self.activity["reveal"]:
            print("correct")
            if self.current_word != None:
                self.current_word[0].score += 1

            self.buttons["correct"].config(fg=self.but_inactive['correct'])
            self.buttons["wrong"].config(fg=self.but_inactive['wrong'])
            self.activity["correct"] = True
            self.activity["wrong"] = True
            self.activity["reveal"] = False
            self.buttons["next"].config(fg=self.but_active['next'])

    def wrong(self, chapter):
        if self.activity["reveal"]:
            print("wrong")
            if self.current_word != None:
                self.current_word[0].score -= 1

            self.buttons["correct"].config(fg=self.but_inactive['correct'])
            self.buttons["wrong"].config(fg=self.but_inactive['wrong'])
            self.activity["correct"] = True
            self.activity["wrong"] = True
            self.activity["reveal"] = False
            self.buttons["next"].config(fg=self.but_active['next'])

    def next(self):
        if (self.activity["correct"] or self.activity["wrong"]) and self.activity["start"]:
            print("Next")
            # changes self.current_word to a new word
            self.get_next_word()
            if self.current_word != None:
                if self.direction == "ec":
                    self.eng.set(self.current_word[0].english)
                    self.chin.set("")
                    self.pin.set("")
                else:
                    self.chin.set(self.current_word[0].character)
                    self.eng.set("")
                    self.pin.set("")

                self.buttons["next"].config(fg=self.but_inactive['next'])
                self.activity["next"] = True
                self.buttons["reveal"].config(fg=self.but_active['reveal'])
                self.activity["correct"] = False
                self.activity["wrong"] = False

            else:
                print("This box is empty, Choose another box")
                self.buttons["next"].config(fg=self.but_inactive['next'])
                self.activity["correct"] = False
                self.activity["wrong"] = False
        else:
            self.buttons["next"].config(fg=self.but_inactive['next'])
            print("This box is empty, Choose another box")

    def reveal(self):
        if self.activity["next"]:
            print("Reveal")
            if self.current_word != None:
                if self.direction == "ec":
                    self.chin.set(self.current_word[0].character)
                    self.pin.set(self.current_word[0].pinyin)
                else:
                    self.eng.set(self.current_word[0].english)
                    self.pin.set(self.current_word[0].pinyin)

            self.buttons["reveal"].config(fg=self.but_inactive['reveal'])
            self.activity["reveal"] = True
            self.activity["next"] = False
            self.buttons["correct"].config(fg=self.but_active['correct'])
            self.buttons["wrong"].config(fg=self.but_active['wrong'])

    def get_next_word(self):
        if self.words_tested >= self.num_words:
            self.words_tested = 0
        if self.rand_word_list != []:
            self.current_word = self.rand_word_list[self.words_tested]
            self.words_tested += 1
        ###############################
        else:
            self.current_word = None

    def shuffle_words(self, number):
        # determine number of words to be asked
        if number == 0 or number > len(self.word_list):
            number = len(self.word_list)
            self.num_words = number

        shuffle(self.word_list)
        self.rand_word_list = self.word_list[0:number]

    def start_learning(self, file_path, box, direction, number, low_limit, up_limit):
        print("Start")
        """ This should initiate the underlying program """
        # number_words_entry.get()
        self.vocab = Vocab(file_path)
        self.direction = self.get_direction(direction)
        self.box = int(box.split(" ")[1])
        self.num_words = int(number)
        self.words_tested = 0
        self.word_list = self.vocab.get_words(box=self.box - 1)
        self.shuffle_words(self.num_words)

        self.chin.set("")
        self.pin.set("")
        self.eng.set("")

        self.low_limit = int(low_limit)
        self.up_limit = int(up_limit)

        # change coloring of buttons
        self.activity["start"] = True
        self.buttons["finish"].config(fg=self.but_active['finish'])
        self.buttons["next"].config(fg=self.but_active['next'])

        self.activity["correct"] = True
        self.activity["wrong"] = True

    def finish(self, filepath):
        # Ensure that you can only finish the session and save it if the Start button has been pressed at least once
        if self.activity["start"]:
            print("Finish")
            # 1) put the learned and classified words from a session back into
            # the original Vocab object.
            old_vocab = self.vocab.get_vocab_list()
            box = self.box - 1
            for word in self.word_list:
                orig_pos = word[1]
                old_vocab[box][orig_pos] = word[0]

            # 2) update the box that a word belongs to based on its score
            self.vocab.update_words(self.low_limit, self.up_limit)

            # 3) write update vocab object to file
            self.vocab.write_vocab(file_path=filepath)

            self.activity["correct"] = False
            self.activity["wrong"] = False
            self.activity["next"] = False
            self.activity["reveal"] = False
            self.activity["start"] = False
            self.buttons["next"].config(fg=self.but_inactive['next'])
            self.buttons["reveal"].config(fg=self.but_inactive['next'])
            self.buttons["correct"].config(fg=self.but_inactive['next'])
            self.buttons["wrong"].config(fg=self.but_inactive['next'])
            self.buttons["finish"].config(fg=self.but_inactive['finish'])

            self.chin.set("")
            self.pin.set("")
            self.eng.set("")

    def get_direction(self, direction):
        if direction == "English -> Chinese":
            return "ec"
        elif direction == "Chinese -> English":
            return "ce"


if __name__ == "__main__":
    app = Application()
    app.start_app()


