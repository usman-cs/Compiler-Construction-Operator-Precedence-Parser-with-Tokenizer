import string
identifierNfa=[['-', 'A-Z,a-z,_'], ['-', '0-9,a-z,A-Z,_']]
numbersNfa=[['-', '$', '0-9'], ['-', '0-9', '.'], ['-', '-', '0-9']]
stringNfa=[['-', '"', '-', '-'], ['-', '-', '$', '-'], ['-', '-', 'all', '"'], ['-', '-', '-', '-']]
operator=['+' , '-', '*', '=', '==', '<=', '>=', '<', '>','/']
keywords=['False', 'await', 'else', 'import', 'pass', 'None', 'break', 'except', 'in', 'raise', 'True', 'class', 'finally', 'is', 'return', 'and', 'continue', 'for', 'lambda', 'try', 'as', 'def', 'from', 'nonlocal', 'while', 'assert', 'del', 'global', 'not', 'with', 'async', 'elif', 'if', 'or', 'yield']
saperators=[';', ')', '[', ']', ',', '(', '^', '}', '{']
operatorPrecedingTable=[['" "','id','+','*','$'],['id','-','>','>','>'],['+','<','>','<','>'],['*','<','>','>','>'],['$','<','<','<','" "']]

'''------------------------------------------------------Lexical Analyzer or Tokenization Part----------------------------------------'''

'''-------------------------------------------------Tested On Following Input--------------------------------------------'''
'''#include < iostream >
using namespace std ;

int main ( )
{
    int firstNumber , secondNumber , sumOfTwoNumbers ;
    cout << "Enter:" ;
    cin >> firstNumber >> secondNumber ;
    // sum of two numbers in stored in variable sumOfTwoNumbers
    sumOfTwoNumbers = firstNumber + secondNumber ;
    cout << firstNumber sum sab * secondNumber + sumOfTwoNumbers sub sum ;
    // Prints sum 
    cout << firstNumber << "+" << secondNumber << "=" << sumOfTwoNumbers ;     
    elif
    is
    return 0 ;
    1hello
}'''
try:
    src=[i.strip().split(' ') for i in open('src.txt','r').readlines() if i.strip()!=''] # Tokens Must be Saperated by Space
except:
    src=[['#include', '<', 'iostream', '>'], ['using', 'namespace', 'std', ';'], ['int', 'main', '(', ')'], ['{'], ['int', 'firstNumber', ',', 'secondNumber', ',', 'sumOfTwoNumbers', ';'], ['cout', '<<', '"Enter:"', ';'], ['cin', '>>', 'firstNumber', '>>', 'secondNumber', ';'], ['//', 'sum', 'of', 'two', 'numbers', 'in', 'stored', 'in', 'variable', 'sumOfTwoNumbers'], ['sumOfTwoNumbers', '=', 'firstNumber', '+', 'secondNumber', ';'], ['cout', '<<', 'firstNumber', 'sum', 'sab', '*', 'secondNumber', '+', 'sumOfTwoNumbers', 'sub', 'sum', ';'], ['//', 'Prints', 'sum'], ['cout', '<<', 'firstNumber', '<<', '"+"', '<<', 'secondNumber', '<<', '"="', '<<', 'sumOfTwoNumbers', ';'], ['elif'], ['is'], ['return', '0', ';'], ['1hello'], ['}']]
'''----------------------------------------------------------------------Nfa Code------------------------------------------------------------------------------------'''
def identifier(lexeme):
    global identifierNfa
    file=identifierNfa
    for pos,val in enumerate(file):
        for p,v in enumerate(val):
            if v=='0-9,a-z,A-Z,_':
                s=set()
                s.update(string.ascii_lowercase)
                s.update(string.ascii_uppercase)
                s.update({str(x) for x in range(0,10)})
                s.update('_')
                file[pos][p]=s
            elif v=='A-Z,a-z,_':
                s=set()
                s.update(string.ascii_lowercase)
                s.update(string.ascii_uppercase)
                s.update('_')
                file[pos][p]=s
    final_state=1
    state={0}
    for inp in lexeme:
        empty_set=set() 
        for ter in state:
            for pos,val in enumerate(file[ter]):
                if (val==inp or (type(val)==set and (inp in val))) and (val!='-'):
                    empty_set.add(pos)
            state=empty_set
                                
    if (final_state in state) and len(lexeme)<31 and (lexeme not in keywords):
        return 1
    else:
        return 0

def numbers(lexeme):
    global numbersNfa
    file=numbersNfa
    for pos,val in enumerate(file):
        for p,v in enumerate(val):
            if v=='0-9':
                s=set()
                s.update({str(x) for x in range(0,10)})
                file[pos][p]=s
    if lexeme[0]=='.':
        lexeme='0'+lexeme
    final_state=2
    state={0}
    for inp in lexeme:
        empty_set=set() 
        for ter in state:
            for pos,val in enumerate(file[ter]):
                if (val==inp or (type(val)==set and (inp in val)) or (val=="$")):
                    empty_set.add(pos)
            state=empty_set
                                
    if (final_state in state) :
        return 1
    else:
        return 0

def strings(input):
    global stringNfa
    file=stringNfa
    for pos,val in enumerate(file):
        for p,v in enumerate(val):
            if v=='all':
                s=set()
                s.update(string.ascii_letters+string.punctuation)
                s.update({str(x) for x in range(0,10)})
                file[pos][p]=s
    final_state=3
    state={0}
    for inp in input:
        empty_set=set() 
        for ter in state:
            for pos,val in enumerate(file[ter]):
                if val==inp or (type(val)==set and (inp in val) or (val=="$")):
                    empty_set.add(pos)
            state=empty_set
                                
    if (final_state in state):
        return 1
    else:
        return 0


print('\nToken Type\t\t','Value\n')
for k,i in enumerate(src):
    if i[0]=='//':
        print('Commet: \t\t',*i)
        continue
    for k1,j in enumerate(i):
        if j[0]=='#':
            print('Preprocessor Directive: ',j)
        elif identifier(j):
            src[k][k1]='id'
            print('Identifier: \t\t',j)
        elif numbers(j):
            print('Constant Or Float: \t',j)
        elif strings(j):
            print('Strings: \t\t',j)
        elif j in operator:
            print('Operator: \t\t',j)
        elif j in saperators:
            print('Saperator: \t\t',j)
        elif j in keywords:
            print('Keyword: \t\t',j)
        else:
            print('Invalid Token: \t\t',j)

'''--------------------------------Geting the Desired Data from Tokens and Give that to Operator Parse------------------------------'''

dataWithGivenOperator=[i for i in src if ('*' in i or '+' in i)]
cleanDataForBufferInput=[]
for i,j in enumerate(dataWithGivenOperator):
    temp=[]
    for k,v in enumerate(j):
        if v=='*' or v=='+' or v=='id':
            temp.append(v)
    cleanDataForBufferInput.append(temp)
dataForParser=[]
for i in cleanDataForBufferInput:
    temp=['']
    for j in i:
        if temp[-1]==j:
            pass
        else:
            temp.append(j)
    dataForParser.append(temp)
    temp=['']
for i in dataForParser:
    i.pop(0)

def parser(inputBuffer,stack,l):
    print('\n-----------------------ParsingInput',inputBuffer,' Using Operator Precedence parser------------------------')
    inputBuffer.append('$')
    while True:
        col=operatorPrecedingTable[0].index(inputBuffer[l])
        row=''
        for k,v in enumerate(operatorPrecedingTable):
            if stack[-1]==v[0]:
                row=k
        decision=operatorPrecedingTable[row][col]
        if decision=='" "':
            break
        elif decision=='>':
            print('------------------------------------------------------------------------------')
            print('\nStack: ',stack[::-1])
            print('InputBuffer:',inputBuffer[l])
            print('POP From Stack:',stack[-1])
            stack.pop()
        else:
            print('------------------------------------------------------------------------------')
            print('\nStack: ',stack[::-1])
            print('InputBuffer: ',inputBuffer[l])
            print('Push From Stack:',inputBuffer[l])
            stack.append(inputBuffer[l])
            l+=1
    return (stack[0]=='$' and inputBuffer[l])

for i in dataForParser:
    l=0
    stack=['$']
    result=parser(i,stack,l)
    if result:
        print('\nParsing Sucessfull')
    else:
        print('\n parsing Not Sucessfull')
    