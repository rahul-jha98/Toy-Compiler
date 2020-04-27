
'''
    This can be considered as the first phase of the compiler.
    In this we take the raw code and remove comments and extract
    functin definations replacing it with only prototype.
'''
class Preprocessor():
    def __init__(self, text):
        self.text = text
    
    def remove_comments(self):
        # Getting all the lines
        alllines = self.text.split('\n')
        nocommentlines = []


        for line in alllines:
            # In case we find the symbol ## we strip all the rest from
            # that line
            idx = line.find('##')
            newline = ""
            if idx == -1:
                newline = line
            else:
                newline = line[:idx]
            
            if newline.strip() != "":
                nocommentlines.append(newline)
        
        # Setting the text value with one with no comments
        self.text = '\n'.join(nocommentlines)



    '''
        Note: Although the below code works in most cases
        But the method is not ideal since we are taking the text as 
        raw input. It was done due to limited time constraints.
        A parser like tool can always be generated for this.
    '''
    def extract_functions(self):
        len = 0
        text = self.text
        ## Create a functions dictionary
        self.functions = {}

        while text.find('function') != -1:
            ## In case we find function in our code
            idx1 = text.find('function')
            text = text[idx1+8:]
            idx = text.find('(')
            name = text[:idx].strip()

            start_idx = text.find('{')
            end_idx = text.find('}')

            temp_start = start_idx
            temp_end = end_idx

            ## Consuming all the curly braces which are inside function
            ## Eg for loop and all            
            while text[temp_start + 1: temp_end].find('{') != -1:
                occur = text[temp_start + 1: temp_end].find('{')
                temp_start = temp_start + occur + 1
                temp_end = temp_end + text[temp_end+1:].find('}') + 1
                
            end_idx = temp_end

            if start_idx == -1 or end_idx == -1:
                return

            ## Taking the function body
            body = text[start_idx + 1 : end_idx]
            
            ## Since we have extracted the body we replace it with ; 
            ## This will convert the defination to its prototype
            self.text = self.text.replace(text[start_idx:end_idx+1], ';', 1)
            self.functions[name] = body


    ## Helper method which removes comments and extracts functions
    ## Returns processed text and functions defination dictionary
    def get_processed_input(self):
        self.remove_comments()
        self.extract_functions()
        return self.text, self.functions