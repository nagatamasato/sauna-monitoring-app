// 自動更新
setTimeout(function () {
    location.reload();
}, 1000);

// stausの値に応じてテーブルの背景色を変更する
function setBgColor(status, color) {
    var table = document.getElementById('hosts');
    var rows = table.getElementsByTagName('tr');
    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        if (cells.length > 0 && cells[1].innerHTML == status) {
            rows[i].style.backgroundColor = color;
        }
    }
}
// statusが1なら背景色を赤色にする
setBgColor("Emergency", 'red');
setBgColor("Failure to get status", 'yellow');
