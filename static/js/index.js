function startGame(_num, _times) {
    if ($('#mainDIV').length !== 0) $('#mainDIV').remove()

    let div0 = document.createElement('div')
    div0.id = 'mainDIV'

    let div1 = document.createElement('div')
    let label = document.createElement('label')
    label.id = 'label'
    label.innerText = '您还剩' + _times + '次机会，请输入你的数字：';
    div1.append(label)
    let input = document.createElement('input')
    input.id = 'guass';
    div1.append(input)
    let button = document.createElement('button')
    button.innerText = '确定';
    button.onclick = function () {
        sendGuass();
    }
    div1.append(button)
    div0.append(div1)

    let div2 = document.createElement('div')
    let table = document.createElement('table');
    table.id = 'show'
    div2.append(table)

    div0.append(div2)

    document.body.append(div0)
}

function sendGuass() {
    let tb = $('#show')
    tb.empty()

    let value = {number: $('#guass').val()}
    $.ajax({
        url: '/getCurrentStatus',
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        data: value,
        success: function (response) {
            console.log(response)

            let data = response['data'];
            for (let i in data) {
                tb.append('<tr>\n<td>\n' + data[i][0] + '</td>\n<td>' + data[i][1] + '</td>\n</tr>\n')
            }
            if (response['status'] == 1) {
                setTimeout(() => alert('输入数字有误，请检查后重新输入'), 10);
            } else if (response['status'] == 2) {
                $('#label').parent().empty().prepend('<label>很可惜，您没能猜出来，正确答案是' + response['answer'] + '</label>')
            } else if (response['status'] == 3) {
                $('#label').parent().empty().prepend('<label>恭喜你猜对了！正确答案就是' + response['answer'] + '</label>')
            }
            else {
                $('#label').text('您还剩' + response['_times'] + '次机会，请输入你的数字：')
            }
        },
        error: function () {
            alert('网页出现错误，请重新开始游戏')
        }
    });
}