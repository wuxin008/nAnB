from flask import Flask, render_template, request, json
import random

app = Flask(__name__)
_num, _times = 0, 0

ans = ''
ans_dict = {}
data = []

def check(number):
    if len(number) != _num:
        return 1
    if len({i: 1 for i in number}) != _num:
        return 1
    return 0

@app.route('/')
@app.route('/index.html')
def hello_world():
    return render_template('index.html')

@app.route('/setGame', methods=['GET', 'POST'])
def setGame():
    args = request.form.to_dict()
    print('setGame:args', args)
    global _num, _times, ans, ans_dict, data
    status, message = 0, '游戏已重新开始'
    ans = ''
    ans_dict = {}
    data = []
    try:
        _num, _times = int(args['num']), int(args['times'])
        if not 1 <= _num <= 10:
            status = 1
            message = '数字个数必须为1-10的整数'
        if not _times > 0:
            status = 2
            message = '猜测个数必须为大于0的整数'
    except:
        status = 3
        message = '输入有误，请检查后重新输入'

    if not status:
        origin = list(range(10))
        random.shuffle(origin)
        for i in range(_num):
            ans += str(origin[i])
        ans_dict = {i: j for i, j in zip(ans, range(1, _num + 1))}
        print(ans, ans_dict)
    return json.dumps({
        'status': status,
        '_num': _num,
        '_times': _times,
        'message': message
    })

@app.route('/getCurrentStatus', methods=['GET', 'POST'])
def getCurrectStatus():
    global _num, _times

    args = request.form.to_dict()
    print('getCurrentStatus:args:', args)

    number = args['number']

    status = check(number)
    print('number:', number, 'status', status)

    answer = 0
    if not status:
        if _times > 1 and number != ans:
            _times -= 1
            nA = 0
            nB = 0
            for i in range(_num):
                t = ans_dict.get(number[i], 0)
                if t == i + 1:
                    nA += 1
                if t != 0:
                    nB += 1
            # print(str(nA) + 'A' + str(nB - nA) + 'B')
            data.append([number, str(nA) + 'A' + str(nB - nA) + 'B'])
        elif number == ans:
            status = 3
            answer = ans
        else:
            status = 2
            answer = ans


    return json.dumps({
        'status': status,
        'data': data,
        '_num': _num,
        '_times': _times,
        'answer': answer
    })

if __name__ == '__main__':
    app.run(debug=True)
