# c1shell.py compiler 
import sys, time 

class Token:
   def __init__(self, line, column, category, lexeme):
      self.line = line
      self.column = column
      self.category = category
      self.lexeme = lexeme

# global variables 
outfile = None
source = ''
sourceindex = 0
line = 0
column = 0
tokenlist = []
tokenindex = -1
token = None
prevchar = '\n'
blankline = True
symbol = []
value = []
tempcount = 0

# constants
EOF           = 0
PRINT         = 1
UNSIGNEDINT   = 2
NAME          = 3
ASSIGNOP      = 4
LEFTPAREN     = 5
RIGHTPAREN    = 6
PLUS          = 7
MINUS         = 8
TIMES         = 9
NEWLINE       = 10
ERROR         = 11
POWER         = 12
DIV           = 13
IF            = 14
GT            = 15
LT            = 16
BEGINBLOCK    = 17
ENDBLOCK      = 18
STRING        = 19

catnames = ['EOF', 'PRINT', 'UNSIGNEDINT', 'NAME', 'ASSIGNOP',
            'LEFTPAREN', 'RIGHTPAREN', 'PLUS', 'MINUS',
            'TIMES', 'NEWLINE', 'ERROR',
            'POWER', 'DIV', 'IF', 'GT', 'LT', 'BEGINBLOCK', 'ENDBLOCK', 'STRING']

keywords = {'print': PRINT, 'if': IF}

smalltokens = {
   '=': ASSIGNOP,
   '(': LEFTPAREN,
   ')': RIGHTPAREN,
   '+': PLUS,
   '-': MINUS,
   '*': TIMES,
   '^': POWER,
   '/': DIV,
   '>': GT,
   '<': LT,
   '[': BEGINBLOCK,
   ']': ENDBLOCK,
   '\n': NEWLINE,
   '': EOF
}

def main():
   global source, outfile

   if len(sys.argv) == 3:
      try:
         infile = open(sys.argv[1], 'r')
         source = infile.read()
      except IOError:
         print('Cannot read input file ' + sys.argv[1])
         sys.exit(1)

      try:
         outfile = open(sys.argv[2], 'w')
      except IOError:
         print('Cannot write to output file ' + sys.argv[2])
         sys.exit(1)
   else:
      print('Wrong number of command line arguments')
      print('Format: python c1shell.py <infile> <outfile>')
      sys.exit(1)

   if source[-1] != '\n':
      source = source + '\n'

   outfile.write('@ ' + time.strftime('%c') + '%34s' % 'YOUR NAME HERE\n')
   outfile.write('@ ' + 'Compiler    = ' + sys.argv[0] + '\n')
   outfile.write('@ ' + 'Input file  = ' + sys.argv[1] + '\n')
   outfile.write('@ ' + 'Output file = ' + sys.argv[2] + '\n')

   try:
      tokenizer()
      outfile.write(
         '@------------------------------------------- Assembler code\n')
      parser()
      #escribirCodigo(segmentoCodigo, segmentoDatos )
   except RuntimeError as emsg:
      lexeme = token.lexeme.replace('\n', '\\n')
      print('\nError on '+ "'" + lexeme + "'" + ' line ' +
         str(token.line) + ' column ' + str(token.column))
      print(emsg)
      outfile.write('\nError on '+ "'" + lexeme + "'" + ' line ' +
         str(token.line) + ' column ' + str(token.column) + '\n')
      outfile.write(str(emsg) + '\n') 
   outfile.close()

def tokenizer():
   global token
   curchar = ' '

   while True:
      while curchar != '\n' and curchar.isspace():
         curchar = getchar()

      token = Token(line, column, None, '')

      if curchar.isdigit():
         token.category = UNSIGNEDINT
         while True:
            token.lexeme += curchar
            curchar = getchar()
            if not curchar.isdigit():
               break

      elif curchar.isalpha() or curchar == '_':
         while True:
            token.lexeme += curchar
            curchar = getchar()
            if not (curchar.isalnum() or curchar == '_'):
               break

         if token.lexeme in keywords:
            token.category = keywords[token.lexeme]
         else:
            token.category = NAME

      elif curchar == '"':  # STRING token
         token.category = STRING
         token.lexeme += curchar
         curchar = getchar()
         while curchar != '"' and curchar != '':
            token.lexeme += curchar
            curchar = getchar()
         if curchar == '"':
            token.lexeme += curchar
            curchar = getchar()
         else:
            token.category = ERROR
            raise RuntimeError('Unterminated string')

      elif curchar in smalltokens:
         token.category = smalltokens[curchar]
         token.lexeme = curchar
         curchar = getchar()

      else:
         token.category = ERROR
         token.lexeme = curchar
         raise RuntimeError('Invalid token')
      
      tokenlist.append(token)
      if token.category == EOF:
         break

def getchar():
   global sourceindex, column, line, prevchar, blankline

   if prevchar == '\n':
      line += 1
      column = 0
      blankline = True

   if sourceindex >= len(source):
      column = 1
      prevchar = ''
      return ''

   c = source[sourceindex]
   sourceindex += 1
   column += 1
   if not c.isspace():
      blankline = False
   prevchar = c

   if c == '\n' and blankline:
      return ' '
   else:
      return c

def enter(s, v):
   if s in symbol:
      return symbol.index(s)
   index = len(symbol)
   symbol.append(s)
   value.append(v)
   return index

def advance():
   global token, tokenindex 
   tokenindex += 1
   if tokenindex >= len(tokenlist):
      raise RuntimeError('Unexpected end of file')
   token = tokenlist[tokenindex]

def consume(expectedcat):
   if (token.category == expectedcat):
      advance()
   else:
     raise RuntimeError('Expecting ' + catnames[expectedcat])

def parser():
   advance()
   program()
   if token.category not in [EOF, NEWLINE]:
      raise RuntimeError('Expecting end of file')

def program():
   while token.category in [NAME, PRINT, IF]:
      stmt()

def stmt():
    simplestmt()
    if token.category == NEWLINE:
        consume(NEWLINE)
    elif token.category != EOF:
        raise RuntimeError('Expecting NEWLINE or EOF')


def simplestmt():
   if token.category == NAME:
      assignmentstmt()
   elif token.category == PRINT:
      printstmt()
   elif token.category == IF:
      ifstmt()
   else:
      raise RuntimeError('Expecting statement')

def ifstmt():
   consume(IF)
   condition()
   consume(BEGINBLOCK)
   consume(NEWLINE)
   simplestmt()
   consume(NEWLINE)
   consume(ENDBLOCK)
   # NEWLINE opcional
   if token.category == NEWLINE:
      consume(NEWLINE)


def condition():
   if token.category in [UNSIGNEDINT, NAME]:
      advance()
   else:
      raise RuntimeError('Expecting left operand in condition')

   comparator()

   if token.category in [UNSIGNEDINT, NAME]:
      advance()
   else:
      raise RuntimeError('Expecting right operand in condition')

def comparator():
   if token.category in [GT, LT]:
      advance()
   else:
      raise RuntimeError('Expecting comparison operator ( > or < )')





def assignmentstmt():
   left = token.lexeme       
   advance()
   consume(ASSIGNOP)
   expr()

def printstmt():
   advance()
   consume(LEFTPAREN)
   if token.category == STRING:
      advance()
   else:
      expr()
   consume(RIGHTPAREN)


def expr():
   term()
   while token.category == PLUS:
      advance()
      term()

def term():
   power()
   while token.category in [TIMES, DIV]:
      advance()
      power()

def power():
   factor()
   while token.category == POWER:
      advance()
      factor()

def factor():
   global sign
   if token.category == PLUS:
      advance()
      factor()
   elif token.category == MINUS:
      sign = -sign
      advance()
      factor()
   elif token.category == UNSIGNEDINT:
      advance()
   elif token.category == NAME:
      advance()
   elif token.category == LEFTPAREN:
      advance()
      expr()
      consume(RIGHTPAREN)
   elif token.category == STRING:
      advance()
   else:
      raise RuntimeError('Expecting factor')


# code generator (aún incompleto)
def cg_prolog(): pass
def cg_epilog(): pass
def cg_gettemp(): pass
def cg_assign(leftindex, rightindex): pass
def cg_print(index): pass
def cg_add(leftindex, rightindex): pass
def cg_mul(leftindex, rightindex): pass
def cg_neg(index): pass

# ejecutar programa
main()