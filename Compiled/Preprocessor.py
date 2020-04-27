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

    def extract_functions(self):
        len = 0
        text = self.text
        self.functions = {}
        while text.find('function') != -1:
            idx1 = text.find('function')
            text = text[idx1+8:]
            idx = text.find('(')
            name = text[:idx].strip()

            start_idx = text.find('{')
            end_idx = text.find('}')

            body = text[start_idx + 1 : end_idx]
            
            self.text = self.text.replace(text[start_idx:end_idx+1], ';', 1)
            self.functions[name] = body


    def get_processed_input(self):
        self.remove_comments()
        self.extract_functions()
        return self.text, self.functions
