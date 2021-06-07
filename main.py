import reportlab
from reportlab.pdfgen.canvas import Canvas
import random
import os

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


def quadratic_aranger(modifyco=False, largefactors=False):
    # (a+b)(c+d)=e+f+g
    # e = ac
    # f = bc + ad
    # g = bd
    if modifyco:
        a, b = random.randint(1, 7), random.randint(1, 7)
    else:
        a, b = 1
    print(a, b)
    pass


if False:
    canvas = Canvas("Teacher-addition.pdf")
    canvas2 = Canvas("Student-subtraction.pdf")
    cs = list(arithmetic_arranger(pdfable=True, genquestions=True))
    rows = 8
    watermarktop = 'Math worksheet'
    watermarkbttom = 'By Joshua Himmens, joshua.himmens@gmail.com'
    canvas2.setFont('Courier', 20)
    canvas.setFont('Courier', 20)
    canvas.drawString(220, 770, watermarktop)
    canvas2.drawString(220, 770, watermarktop)
    canvas2.setFont('Courier', 12)
    canvas.setFont('Courier', 12)
    canvas.drawString(150, 750, watermarkbttom)
    canvas2.drawString(150, 750, watermarkbttom)
    canvas2.setFont('Courier', 12)
    canvas.setFont('Courier', 12)
    x = 700
    leftjustify = 60
    for i in range(rows):
        for i in range(4):
            canvas.drawString(leftjustify, x, cs[i])
            if i != 3:
                canvas2.drawString(leftjustify, x, cs[i])
            x -= 12
        cs = list(arithmetic_arranger(pdfable=True, genquestions=True))
        x -= 36
    canvas.save()
    canvas2.save()



