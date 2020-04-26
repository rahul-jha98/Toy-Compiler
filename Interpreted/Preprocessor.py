class Preprocessor():
    def __init__(self, text):
        self.text = text
    
    def remove_comments(self):
        alllines = self.text.split('\n')
        nocommentlines = []
        for line in alllines:
            idx = line.find('##')
            newline = ""
            if idx == -1:
                newline = line
            else:
                newline = line[:idx]
            
            if newline.strip() != "":
                nocommentlines.append(newline)
        
        self.text = '\n'.join(nocommentlines)

    def get_processed_input(self):
        self.remove_comments()
        return self.text
