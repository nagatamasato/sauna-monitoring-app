// 自動更新
setTimeout(function () {
    location.reload();
}, 1000);

// statusの値で表示するテキストを変える
// status == 1 Emergency
// status == 0 Normal

// stausの値に応じてテーブルの背景色を変更する
function setBgColor(value, color) {
    var table = document.getElementById('hosts');
    var rows = table.getElementsByTagName('tr');
    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        if (cells.length > 0 && cells[1].innerHTML == value) {
            rows[i].style.backgroundColor = color;
        }
    }
}
// statusが1なら背景色を黄色にする
setBgColor(1, 'yellow');

// statusの昇順にソート
