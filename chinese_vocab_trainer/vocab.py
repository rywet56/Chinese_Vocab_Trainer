class Vocab:
    class Word:
        def __init__(self, cha, pin, eng, score):
            self.character = cha
            self.pinyin = pin
            self.english = eng
            self.score = score
            self.updated = False

    def __init__(self, vocab_loc):
        self.vocab = self.read_vocab(vocab_loc)

    def get_vocab_list(self):
        return self.vocab

    def read_vocab(self, file_path):
        handler = open(file_path, 'r')
        content = handler.read().split("\n")

        vocabul = []
        temp = []
        # for c in content:
        #     if c != '-' and c != 'EOF':
        #         temp.append(c)
        #     elif c == '-':
        #         vocabul.append(temp)
        #         temp = []
        #     else:  # end of file
        #         vocabul.append(temp)

        for c in content:
            if c.split('_')[0] == 'box':
                temp = []
                vocabul.append(temp)
            elif c == 'EOF':
                pass
            else:
                temp.append(c)

        # [['发\tguo\tfsdf\t0', '风\tfads\tfads\t0', '公司股份\tasdf\tdsfads\t0'], ['嘎大幅\tsofas\tasdfs\t0', '发撒风\twffsd\tadsfd\t0'], ['发生的\tasdf\tdsfdsf\t0']]
        for level in range(len(vocabul)):
            for word in range(len(vocabul[level])):
                v = vocabul[level][word].split("\t")
                vocabul[level][word] = self.Word(v[0], v[1], v[2], int(v[3]))

        return vocabul

    def write_vocab(self, file_path="/Users/manuel/Desktop/chinese_new.txt"):
        handler = open(file_path, "w")
        boxes = len(self.vocab)
        box_no = 1
        for box in self.vocab:
            if box != None:
                handler.write("box_" + str(box_no) + "\n")
                for word in box:
                    handler.write(word.character + "\t" + word.pinyin + "\t" +
                                  word.english + "\t" + str(word.score) + "\n")
            box_no += 1
        handler.write("EOF")

    def get_word(self, box, index):
        return self.vocab[box][index]

    def get_words(self, box):
        """ returns [[vocab_object, original_position], ... ] in the same order as in the input file
        while also remembering the position within the input file."""
        number = len(self.vocab[box])
        indices = [i for i in range(0, number)]
        return [[self.vocab[box][i], i] for i in indices]

    def update_words(self, lower_limit, upper_limit):
        for box_no in range(len(self.vocab)):
            for word_no in range(len(self.vocab[box_no])):
                self.update_word(word_no, box_no, lower_limit, upper_limit)

        self.clean_vocab()

    def update_word(self, word_no, box_no, lower_limit, upper_limit):
        word = self.vocab[box_no][word_no]
        score = word.score
        if not self.is_already_updated(word):
            if score >= upper_limit and box_no+1 != len(self.vocab):
                self.vocab[box_no + 1].append(word)
                # word.score = 0
                self.vocab[box_no][word_no].updated = True
            elif score <= lower_limit and box_no+1 != 1:
                self.vocab[box_no - 1].append(word)
                # word.score = 0
                self.vocab[box_no][word_no].updated = True
            else:
                # smaller then upper_limit and bigger then lower_limit
                # word stays in box
                pass

    def is_already_updated(self, word):
        already_updated = False
        for box in self.vocab:
            if word in box and word.updated == True:
                already_updated = True

        return already_updated

    def clean_vocab(self):
        cleaned_vocab = [None] * len(self.vocab)
        for box_no in range(len(cleaned_vocab)):
            for word_no in range(len(self.vocab[box_no])):
                word = self.vocab[box_no][word_no]
                # word has not been moved up or down at all or
                # word has moved up and been marked as "not updated" in the else statement below
                if not word.updated:
                    # ADDING the word
                    if cleaned_vocab[box_no] is None:
                        cleaned_vocab[box_no] = [word]
                    else:
                        cleaned_vocab[box_no].append(word)
                    # ---------------
                else:
                    if word.score < 0:
                        word.score = 0
                        # ADDING the word
                        if cleaned_vocab[box_no] is None:
                            cleaned_vocab[box_no] = [word]
                        else:
                            cleaned_vocab[box_no].append(word)
                        # ---------------
                    else:
                        word.score = 0
                        word.updated = False

        # not elegant, only for temorary use!
        # if a box was empty, the clean method up until this point sets the box to None
        # the write function does not know how to handle None properly
        for box_no in range(len(cleaned_vocab)):
            if cleaned_vocab[box_no] is None:
                cleaned_vocab[box_no] = []

        self.vocab = cleaned_vocab
