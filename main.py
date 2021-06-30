from reportlab.pdfgen.canvas import Canvas
import random
import os
import math
import time
import shutil
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import sys


version = f'version = 0.8.3              time generated: {datetime.datetime.now()}'


def arithmetic_arranger(list_of_question=[], return_or_not=False, pdfable=False, genquestions=False):
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


def quadratic_aranger(modifyco=False, largefactors=False, positivenegitive=1, allowzero=False):
    # posneg is o for all neg 1 for mix, 2 for all positive
    # (a+b)(c+d)=e+f+g
    # e = ac
    # f = bc + ad
    # g = bd
    comidify = 7
    factorranger = 10
    factorincrease = 15
    co = 1
    posneg = 1
    b, d = 0, 0
    if positivenegitive == 1:
        posneg = factorranger * -1
    elif positivenegitive == 2:
        posneg = 1
    elif positivenegitive == 0:
        co = -1
        posneg = 0
    if modifyco:
        a = random.randint(1, comidify)
        c = random.randint(1, comidify)
    else:
        a, c = 1, 1
    if largefactors:
        factorranger += factorincrease
    while (b == 0) or (d == 0):
        b, d = random.randint(posneg, co * factorranger), random.randint(posneg, co * factorranger)
    e = int((a * c))
    f = int((b * c) + (a * d))
    g = int((b * d))
    string = ''
    if e != 1:
        string += f'{int(e)}x '
    else:
        string += f'x '
    if f > 0:
        string += f'+ {int(f)}x '
    elif f == 0:
        pass
    else:
        string += f'- {int(abs(f))}x '
    if g > 0:
        string += f'+ {int(g)}'
    elif g == 0:
        pass
    else:
        string += f'- {int(abs(g))}'
    # string = f'{e}x + {f}x + {g}'
    solution = [a, b, c, d]
    y = checkforfactors([a, b])
    z = checkforfactors([c, d])
    while checkforfactors([a, b]) is not None:
        solution.append(y)
        a = a // y
        b = b // y
        y = checkforfactors([a, b])
    while checkforfactors([c, d]) is not None:
        solution.append(z)
        c = c // z
        d = d // z
        z = checkforfactors([c, d])
    solutions = ''
    if a != 1:
        solutions += f'({int(a)}x'
    else:
        solutions += '(x'
    if b >= 0:
        solutions += f'+{int(b)})'
    else:
        solutions += f'{int(b)})'
    if c != 1:
        solutions += f'({int(c)}x'
    else:
        solutions += '(x'
    if d >= 0:
        solutions += f'+{int(d)})'
    else:
        solutions += f'{int(d)})'
    # solutions = f'({a}x{bst})({c}x{dst})'
    text = 1
    for i in range(4, len(solution)):
        text = text * solution[i]
    if (text != 0) and (text != 1):
        solutions += f'({text})'
    # list: (tuple: (str, str), int, int, int
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
                destintaionpath=None,
                removeold=False) -> None:
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
            prob = quadratic_aranger(positivenegitive=2)
        elif intervals[0] <= qnum <= intervals[1] and probsgetharder:
            prob = quadratic_aranger(largefactors=True, positivenegitive=1)
        elif qnum > intervals[1] and probsgetharder:
            prob = quadratic_aranger(modifyco=True, largefactors=True)
        elif not probsgetharder:
            prob = quadratic_aranger()
        canvas.drawString(leftjustify, top, prob[0][0] + ':')
        canvas2.drawString(leftjustify, top, prob[0][0] + ':')
        canvas2.setFont('Courier', 5)
        canvas.setFont('Courier', 5)
        if prob[1] == 1:
            canvas.drawString(leftjustify + 7, top + 5, '2')
            canvas2.drawString(leftjustify + 7, top + 5, '2')
        elif prob[1] < 10:
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
        elif intervals[0] < qnum < intervals[1] and probsgetharder:
            prob = quadratic_aranger(largefactors=True, positivenegitive=1)
        elif qnum > intervals[1] and probsgetharder:
            prob = quadratic_aranger(modifyco=True, largefactors=True)
        elif not probsgetharder:
            prob = quadratic_aranger()
        canvas.drawString(leftjustify, top, prob[0][0] + ':')
        canvas2.drawString(leftjustify, top, prob[0][0] + ':')
        canvas2.setFont('Courier', 5)
        canvas.setFont('Courier', 5)
        if prob[1] == 1:
            canvas.drawString(leftjustify + 7, top + 5, '2')
            canvas2.drawString(leftjustify + 7, top + 5, '2')
        elif prob[1] < 10:
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
    canvas2.setFont('Courier', 5)
    canvas.setFont('Courier', 5)
    canvas.drawString(0, 0, f'{version}')
    canvas2.drawString(0, 0, f'{version}')
    canvas2.setFont('Courier', 12)
    canvas.setFont('Courier', 12)
    canvas.setAuthor('Joshua Himmens')
    canvas2.setAuthor('Joshua Himmens')
    canvas.setTitle('Math Worksheet')
    canvas2.setTitle('Math Worksheet')
    canvas.save()
    canvas2.save()
    if destintaionpath is not None:
        teacherpath = destintaionpath + '/Key'
        studentpath = destintaionpath + '/Worksheet'
        if not os.path.isdir(studentpath + '/'):
            os.mkdir(studentpath)
        if os.path.isfile(studentpath + '/' + studentfilename):
            if removeold:
                os.remove(studentpath + '/' + studentfilename)
                print('removing old file')
            else:
                print("FILE EXSISTS, change filename of path")
                return
        if os.path.isfile(teacherpath + '/' + teacherfilename):
            if removeold:
                os.remove(teacherpath + '/' + teacherfilename)
                print('removing old file')
            else:
                print("FILE EXSISTS, change filename of path")
                return
        if not os.path.isdir(teacherpath + '/'):
            os.mkdir(teacherpath)
        shutil.move(studentfilename, studentpath)
        shutil.move(teacherfilename, teacherpath)


def sendmail_ssl(message, email, name=None, filepaths=None, title='Math worksheet'):
    default_smtp_server = "smtp.gmail.com"
    gmail_user = 'joshuahimmens@gmail.com'
    gmail_password = ''  # todo: add app password
    default_name = 'Joshua Himmens'
    emailintro = "Hi"
    if name is not None:
        emailintro += ' ' + str(name)
    emailintro += ','
    emailextro = f"Regards,\n{default_name}\n\n\n This email was automatically sent with python," \
                 f" if there is any errors please email me back at '{gmail_user}'"
    message = f"""
{emailintro}\n\n{message}\n\n{emailextro}
sent at: {datetime.datetime.now()}"""
    try:
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = email
        msg['Subject'] = title
        msg.attach(MIMEText(message, 'plain'))
        if filepaths is not None:
            if type(filepaths) == list:
                for fn in filepaths:
                    with open(fn, "rb") as f:
                        attach = MIMEApplication(f.read(), _subtype="pdf")
                    if '/' in filepaths:
                        attach.add_header('Content-Disposition', 'attachment',
                                          filename=str(fn.split(sep='/')[-1]))
                    else:
                        attach.add_header('Content-Disposition', 'attachment',
                                          filename=str(fn))
                    msg.attach(attach)
            else:
                with open(filepaths, "rb") as f:
                    attach = MIMEApplication(f.read(), _subtype="pdf")
                if '/' in filepaths:
                    attach.add_header('Content-Disposition', 'attachment',
                                      filename=str(filepaths.split(sep='/')[-1]))
                else:
                    attach.add_header('Content-Disposition', 'attachment',
                                      filename=str(filepaths))
                msg.attach(attach)
        mailer = smtplib.SMTP_SSL(default_smtp_server, 465)
        mailer.login(gmail_user, gmail_password)
        mailer.sendmail(gmail_user, email, msg.as_string())
        mailer.close()
        print("email sent", email)
    except TypeError as e:
        print("email failed" + str(e))
        return False


def sendfactors(destemail, name=None):
    printfactor(problems=15,
                probsgetharder=True,
                studentfilename='Student-factor.pdf',
                teacherfilename='Teacher-factor.pdf',
                destintaionpath=None,
                removeold=False)
    sendmail_ssl('Attached is your math worksheet, thanks '
                 'for using my script. I would really appreciate feedback, so feel free to respond.'
                 '\n\nThis worksheet was generated just for you, feel free to use it as much as you would like.'
                 '\n\nI am also more then happy to create whatever you need, just lmk.',
                 destemail, name=name, filepaths=['Teacher-factor.pdf', 'Student-factor.pdf'])


printadditionsubtraction()
printfactor(problems=15,
            probsgetharder=True,
            studentfilename='Student-factor.pdf',
            teacherfilename='Teacher-factor.pdf',
            removeold=False,
            destintaionpath=None)

if __name__ == '__main__':
    args = sys.argv
    print(args)
    if 'sf' in args:
        ind = args.index('sf')
        try:
            emailgiven = args[ind + 1]
            try:
                namegiven = args[ind + 2]
            except IndexError:
                namegiven = None
            try:
                sendfactors(emailgiven, namegiven)
            except Exception as e:
                print(e)
        except IndexError:
            print('Error try changing what you entered')
