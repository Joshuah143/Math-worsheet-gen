import reportlab
from reportlab.pdfgen.canvas import Canvas
import random


def arithmetic_arranger(list_of_question=None, return_or_not=False, pdfable=False, genquestions=False):
    if list_of_question is None:
        list_of_question = []
    for i in range(7):
        top = random.randint(1000, 9999)
        bottom = random.randint(1000, 9999)
        # minus is 0 plus is 1
        minus = random.randint(0, 1)
        while (not minus) and bottom >= top:
            bottom = random.randint(1, 9999)
        if minus:
            minus = '+'
        else:
            minus = '-'
        list_of_question.append(str(str(top) + ' ' + minus + ' ' + str(bottom)))
    print(list_of_question)

    one = ''
    two = ''
    three = ''
    four = ''
    for t in list_of_question:
        parts = t.split(sep=" ")
        if len(parts) > 3:
            raise Exception
        if (len(parts[0]) > 4) or (len(parts[2]) > 4):
            return 'Error: Numbers must only contain digits.'
        if (parts[1] != '-') and (parts[1] != '+'):
            return "Error: Operator must be '+' or '-'."
        if len(parts[0]) > len(parts[2]):
            maxlen = len(parts[0]) + 2
        else:
            maxlen = len(parts[2]) + 2
        tab = ' ' * 4
        if parts[1] == '+':
            awnser = str(int(parts[0]) + int(parts[2]))
        if parts[1] == '-':
            awnser = str(int(parts[0]) - int(parts[2]))
        one += parts[0].rjust(maxlen) + tab
        two += parts[1] + ' ' + parts[2].rjust(maxlen - 2) + tab
        three += '-' * maxlen + tab
        four += awnser.rjust(maxlen) + tab

    bre = '\n'
    returnable = one + bre + two + bre + three + bre + four
    if pdfable:
        yield one
        yield two
        yield three
        yield four
    if return_or_not:
        print(returnable, 'return')


# cs = list(arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49"], pdfable=True))
cs = list(arithmetic_arranger(pdfable=True, genquestions=True))
rows = 8
canvas = Canvas("hello.pdf")
canvas.setFont('Courier', 12)
x = 800
for i in range(rows):
    for i in range(4):
        canvas.drawString(50, x, cs[i])
        x -= 15
    cs = list(arithmetic_arranger(pdfable=True, genquestions=True))
    x -= 40


canvas.save()
