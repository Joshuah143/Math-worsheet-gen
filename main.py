import reportlab
from reportlab.pdfgen.canvas import Canvas
import random
import os
import math
import time
import shutil


def arithmetic_arranger(list_of_question=None, return_or_not=False, pdfable=False, genquestions=False):
    if list_of_question is None:
        list_of_question = []
    if genquestions:
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
    comidify = 7
    factorranger = 10
    factorincrease = 15
    if modifyco:
        a = random.randint(1, comidify)
        c = random.randint(1, comidify)
    else:
        a, c = 1, 1
    if largefactors:
        factorranger += factorincrease
    b, d = random.randint(1, factorranger), random.randint(1, factorranger)
    e = int((a * c))
    f = int((b * c) + (a * d))
    g = int((b * d))
    string = f'{e}x + {f}x + {g}'
    solution = [a, b, c, d]
    while (checkforfactors(solution) not in solution) and (checkforfactors(solution) != None):
        factor = checkforfactors(solution)
        solution.append(factor)
        e = e / factor
        f = f / factor
        g = g / factor
    solutions = f'({a}x+{b})({c}x+{d})'
    for o in range(len(solution) - 4):
        ting = o + 4
        solutions += f'({solution[ting]})'
    return [(string, solutions), e, f, g]


def checkforfactors(lists):
    for i in range(2, max(lists) + 1):
        t = 0
        for v in lists:
            if v % i == 0:
                t += 1
        if t == len(lists):
            return i
    return None


def listfactors(num):
    facts = lambda num: [i for i in range(2, num) if num % i == 0]
    return facts(num)


def printadditionsubtraction():
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


def printfactor(problems=15,
                probsgetharder=False,
                studentfilename='Student-factor.pdf',
                teacherfilename='Teacher-factor.pdf',
                destintaionpath=None):
    canvas = Canvas(studentfilename)
    canvas2 = Canvas(teacherfilename)
    watermarktop = 'Math worksheet'
    watermarkbttom = 'By Joshua Himmens, joshua.himmens@gmail.com'
    instructions = 'Factor completly:'
    canvas2.setFont('Courier', 20)
    canvas.setFont('Courier', 20)
    canvas.drawString(220, 770, watermarktop)
    canvas2.drawString(220, 770, watermarktop)
    canvas2.setFont('Courier', 12)
    canvas.setFont('Courier', 12)
    canvas.drawString(150, 750, watermarkbttom)
    canvas2.drawString(150, 750, watermarkbttom)
    canvas.drawString(228, 700, instructions)
    canvas2.drawString(228, 700, instructions)
    canvas2.setFont('Courier', 12)
    canvas.setFont('Courier', 12)
    top = 650
    oldtop = top
    leftjustify = 50
    probspace = 40
    qnum = 0
    intervals = [10, 20]
    for i in range(problems):
        if qnum < intervals[0] and probsgetharder:
            prob = quadratic_aranger()
        if intervals[0] < qnum < intervals[1] and probsgetharder:
            prob = quadratic_aranger(largefactors=True)
        if qnum > intervals[1] and probsgetharder:
            prob = quadratic_aranger(modifyco=True, largefactors=True)
        canvas.drawString(leftjustify, top, prob[0][0] + ':')
        canvas2.drawString(leftjustify, top, prob[0][0] + ':')
        canvas2.setFont('Courier', 5)
        canvas.setFont('Courier', 5)
        if prob[1] < 10:
            canvas.drawString(leftjustify+15, top+5, '2')
            canvas2.drawString(leftjustify+15, top+5, '2')
        else:
            canvas.drawString(leftjustify + 22, top + 5, '2')
            canvas2.drawString(leftjustify + 22, top + 5, '2')
        canvas2.setFont('Courier', 12)
        canvas.setFont('Courier', 12)
        canvas2.drawString(leftjustify + 120, top, prob[0][1])
        top -= probspace
        qnum += 1
    leftjustify = 300
    top = oldtop
    for i in range(problems):
        if qnum < intervals[0] and probsgetharder:
            prob = quadratic_aranger()
        if intervals[0] < qnum < intervals[1] and probsgetharder:
            prob = quadratic_aranger(largefactors=True)
        if qnum > intervals[1] and probsgetharder:
            prob = quadratic_aranger(modifyco=True, largefactors=True)
        canvas.drawString(leftjustify, top, prob[0][0] + ':')
        canvas2.drawString(leftjustify, top, prob[0][0] + ':')
        canvas2.setFont('Courier', 5)
        canvas.setFont('Courier', 5)
        if prob[1] < 10:
            canvas.drawString(leftjustify + 15, top + 5, '2')
            canvas2.drawString(leftjustify + 15, top + 5, '2')
        else:
            canvas.drawString(leftjustify + 22, top + 5, '2')
            canvas2.drawString(leftjustify + 22, top + 5, '2')
        canvas2.setFont('Courier', 12)
        canvas.setFont('Courier', 12)
        canvas2.drawString(leftjustify + 120, top, prob[0][1])
        top -= probspace
        qnum += 1
    canvas.save()
    canvas2.save()
    if destintaionpath is not None:
        teacherpath = destintaionpath + '/Key'
        studentpath = destintaionpath + '/Worksheet'
        if not os.path.isdir(studentpath + '/'):
            os.mkdir(studentpath)
        if not os.path.isdir(teacherpath + '/'):
            os.mkdir(teacherpath)
        shutil.move(studentfilename, studentpath)
        shutil.move(teacherfilename, teacherpath)




printfactor(probsgetharder=True)
printadditionsubtraction()
for i in range(50):
    printfactor(probsgetharder=True,
                studentfilename=f'factor_{i + 1}.pdf',
                teacherfilename=f'factor_{i + 1}_TEACHER.pdf',
                destintaionpath='/Users/joshuahimmens/Desktop/Testfolder')