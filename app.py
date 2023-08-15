from flask import Flask, render_template, request, json
app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def hello_world():
    return render_template('index.html')

@app.route('/setGame', methods=['GET', 'POST'])
def setGame():
    args = request.form.to_dict()
    print(args)
    global _num, _times
    result = '游戏已重新开始'
    try:
        _num, _times = int(args['num']), int(args['times'])
        if not 1 <= _num <= 10:
            result = '数字个数必须为1-10的整数'
        if not _times > 0:
            result = '猜测个数必须为大于0的整数'
    except:
        result = '输入有误，请检查后重新输入'
    return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True)