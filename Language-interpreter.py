#Group_3  Avinash and Brandon
#Project Phase 3.1 
import re
import sys

id_regex = r"^[a-zA-Z$][a-zA-Z\d$]*"
num_regex = r"[0-9]+"
symbol_regex = r"\+|\-|\*|/|\(|\)|:=|;"
keyword_regex = r"if|then|else|endif|while|do|endwhile|skip"
real_tokens = []

class Node:
    def __init__(self, token_t, token_v, left, middle, right):
        self.token_type = token_t
        self.token_value = token_v 
        self.left = left 
        self.right = right 
        self.middle = middle 

def scanner(line):
    global real_tokens
    real_tokens = []
    character_blocks = line.split() 

    for block in character_blocks:
        real_tokens.append(recur_breakup2(block))
        
    real_tokens = [i for i in real_tokens if i]
    return real_tokens

def recur_breakup2(chunk):
    
    if (re.fullmatch(keyword_regex, chunk)):
            return ("KEYWORD", chunk)
    if (re.fullmatch(id_regex, chunk)):
            return ("IDENTIFIER", chunk)
    if (re.fullmatch( num_regex, chunk)):
            return ("NUMBER", chunk)
    if (re.fullmatch( symbol_regex,chunk)):
            return ("SYMBOL", chunk)

    if ( re.match( num_regex, chunk ) ):
        holder1 = re.match(num_regex, chunk)
        holder = re.split( r'\d+', chunk, 1)
        real_tokens.append(("NUMBER", holder1.group(0)))
        return recur_breakup2( holder[1] )

    if ( re.match( keyword_regex, chunk ) ):
         holder1 = re.match(keyword_regex, chunk)
         holder = re.split( keyword_regex, chunk, 1)
         real_tokens.append(("KEYWORD", holder1.group(0)))
         return recur_breakup2( holder[1] )

    if ( re.match( id_regex, chunk ) ):
        holder1 = re.match(id_regex, chunk)
        holder = re.split( id_regex, chunk, 1)
        real_tokens.append(("IDENTIFIER", holder1.group(0)))
        return recur_breakup2( holder[1] )

    if ( re.match( symbol_regex, chunk ) ):
        holder1 = re.match(symbol_regex, chunk)
        holder = re.split( symbol_regex, chunk, 1)
        real_tokens.append(("SYMBOL", holder1.group(0)))
        return recur_breakup2( holder[1] )

    else:
        return ("ERROR READING", chunk)

def recur_helper(hldr):
    for spl in hldr:
        if(spl != ''):
            recur_breakup2(str(spl))
tokens = [] 
file_holder = None 
indent = 8
p_flag = False

class Node:
    def __init__(self, token_t, token_v, left, middle, right):
        self.token_type = token_t 
        self.token_value = token_v 
        self.left = left 
        self.right = right 
        self.middle = middle 
        

    def print_tree(self, depth):
        global indent
        global p_flag
        if depth == 0:
            file_holder.write("AST: \n\n")
            if p_flag:
                print("AST: \n")
        if self.token_type is None or self.token_value is None:
            return
        if p_flag:
            print((" "*(indent * depth)) + self.token_value+ " : " + self.token_type)
        file_holder.write(str((" "*(indent * depth)) + self.token_value+ " : " + self.token_type + "\n"))
        if self.left:
            self.left.print_tree(depth + 1)
        if self.middle:
            self.middle.print_tree(depth + 1)
        if self.right:
            self.right.print_tree(depth + 1)
    

def parse_expression(): 
    global tokens
    t = parse_term()
    while (len(tokens) > 0) and tokens[0][1] == '+':
        tokens.pop(0)
        t = Node('SYMBOL','+', t, None, parse_term())
    return t
    
def parse_term(): 
    global tokens
    t = parse_factor()
    while (len(tokens) > 0) and tokens[0][1] == '-':
        tokens.pop(0)
        t = Node('SYMBOL','-', t, None, parse_factor())
    return t  

def parse_factor(): 
    global tokens
    t = parse_piece()
    while (len(tokens) > 0) and (tokens[0][1] == '/'):
        tokens.pop(0)
        t = Node('SYMBOL','/', t, None, parse_piece())
    return t

def parse_piece(): 
    global tokens
    t = parse_element()
    while (len(tokens) > 0) and tokens[0][1] == '*':
        tokens.pop(0)
        t = Node('SYMBOL','*', t, None, parse_element())
    return t 

def parse_element(): 
    global tokens
    if len(tokens) <= 0:
        return None
    if tokens[0][1] == '(':
        tokens.pop(0)
        t = parse_expression()
        if tokens[0][1] == ')':
            tokens.pop(0)
            return t
        else:
            raise Exception("There is no closing parenthesis") 
    else:
        if (tokens[0][0] == 'NUMBER') or (tokens[0][0] == 'IDENTIFIER'):
            tt,tv = tokens[0][0],tokens[0][1] 
            tokens.pop(0)
            return Node(tt,tv, None, None, None)    

def parse_statement(): 
    global tokens
    t = parse_basestatement()
    if (len(tokens) > 0):
        if (tokens[0][1] == ';'):
            while (len(tokens) > 0) and tokens[0][1] == ';':
                tokens.pop(0)
                t = Node('SYMBOL',';', t, None, parse_basestatement())
        elif (tokens[0][0] != 'KEYWORD'): 
            t = parse_expression()
    return t

def parse_basestatement(): 
    global tokens
    t = None
    if (len(tokens) > 0):
        if (tokens[0][0] == 'IDENTIFIER'):
            t = parse_assignment()
        elif (tokens[0][1] == ':='):
            tokens.pop(0)
            print("test to see if it reaches here")
            t = parse_assignment()
        elif (tokens[0][1] == 'if'):
            t = parse_ifstatement()
        elif (tokens[0][1] == 'while'):
            t = parse_whilestatement()
        elif (tokens[0][1] == 'skip'):
            tokens.pop(0)
            t = Node('KEYWORD', 'skip', None, None, None)
            return t
    return t

def parse_assignment():
    global tokens
    t = None
    current_identifier = str(tokens[0][1])
    tokens.pop(0)
    if (tokens[0][1] == ':='):
        tokens.pop(0)
        tLeft = Node('IDENTIFIER', current_identifier, None, None, None)
        t = Node('SYMBOL', ':=', tLeft, None, parse_expression())
    return t


def parse_ifstatement(): 
    global tokens
    t = None
    tRight = None 
    if (tokens[0][1] == 'if'):
        tokens.pop(0)
        tLeft = parse_expression()
    if (tokens[0][1] == 'then'):
        tokens.pop(0)
        tMiddle = parse_statement()
    if (tokens[0][1] == 'else'):
        tokens.pop(0)
        tRight = parse_statement()
    if (tokens[0][1] == 'endif'):
        tokens.pop(0)
        t = Node('IF-STATEMENT', 'if', tLeft, tMiddle, tRight)
    return t
        

def parse_whilestatement(): 
    global tokens
    t = None
    tRight = None 
    if (tokens[0][1] == 'while'):
        tokens.pop(0)
        tLeft = parse_expression()
    if (tokens[0][1] == 'do'):
        tokens.pop(0)
        tRight = parse_statement()
    if (tokens[0][1] == 'endwhile'):
        tokens.pop(0)
        t = Node('WHILE-LOOP', 'while', tLeft, None, tRight)
    return t

root = None

stack = []

def preorder_push(root, counter):
    global stack
    x = get_top()

    if x and (x[2].token_type == 'NUMBER') and (x[1].token_type == 'NUMBER') and is_std_op(x[0]):
        stack.pop()
        stack.pop()
        stack.pop()
        if x[0].token_value == '+':
            stack.append( Node('NUMBER', str( int(x[1].token_value) + int(x[2].token_value)), None, None, None) )   
        elif x[0].token_value == '-':
            stack.append( Node('NUMBER', str( int(x[1].token_value) - int(x[2].token_value)), None, None, None) ) 
        elif x[0].token_value == '*':
            stack.append( Node('NUMBER', str( int(x[1].token_value) * int(x[2].token_value)), None, None, None) )
        elif x[0].token_value == '/':
            if int(x[2].token_value) == 0:
                print('Error: Division by 0')
                exit()
            stack.append( Node('NUMBER', str( int((int(x[1].token_value) / int(x[2].token_value)))), None, None, None) )
        

    if root: 
        stack.append(root)
        preorder_push(root.left, counter-1)
        preorder_push(root.right, counter-1)
    if counter >= 0:
        preorder_push(None, counter - 1)

def get_top():
    global stack
    l = len(stack)
    if l >= 3:
        return (stack[l-3], stack[l-2], stack[l-1] )
    else:
        return False

def is_std_op(ex):
    return ex.token_value == '+' or ex.token_value == '-' or ex.token_value == '*' or ex.token_value == '/'
#_______________________main function_______________
outFile = open(sys.argv[2], "w")
_tokens = []
realTK = []
p_console = False

if (len(sys.argv) > 3) and (str(sys.argv[3]) == '-p'):
        p_console=True

def nonblack_lines(f): 
    for l in f:
        line = l.rstrip()
        if line:
            yield line

outFile.write("Tokens: \n\n")

token_lists = []
with open(sys.argv[1]) as file_in:
    if p_console:
        print("Tokens: \n")
    for line in nonblack_lines(file_in):
        outFile.write("Line: "+line + "\n")
        if p_console: 
            print(("Line: "+line))
          
        _tokens=scanner(line)
        for item in _tokens:
            outFile.write(item[0] + ": " + item[1] + "\n")
            realTK.append(item)
            if p_console:
                print(item[0] + ": " + item[1])

        outFile.write("\n")
        if p_console: 
            print()
        token_lists.append(realTK)

for list in token_lists:
    if (len(list) == 0):
        continue
    tokens = list 
    file_holder = outFile 
    if p_console: 
        p_flag = True
    root = parse_statement() 
    root.print_tree(0) 
    preorder_push(root, 10)
    result = stack[0]
    outFile.write('\nOutput: ' + str(result.token_value) + '\n\n')
    stack = []
outFile.close()
