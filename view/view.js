// 自動更新
setTimeout(function () {
    location.reload();
}, 1000);

// statusの値で表示するテキストを変える
// status == 1 Emergency
// status == 0 Normal

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
// statusが1なら背景色を黄色にする
setBgColor(1, 'red');

// stausの値に応じてテーブルの背景色を変更・点滅
// function blinkRow(rowId) {
//     var row = document.getElementById(rowId);
//     var originalColor = row.style.backgroundColor;
//     var blinkInterval = setInterval(function() {
//       row.style.backgroundColor = (row.style.backgroundColor == 'yellow') ? originalColor : 'yellow';
//     }, 500);
//     setTimeout(function() {
//       clearInterval(blinkInterval);
//       row.style.backgroundColor = originalColor;
//     }, 5000);
//   }
//   blinkRow('row2');

// statusの昇順にソート
// function sortTable() {
//     var table, rows, switching, i, x, y, shouldSwitch;
//     table = document.getElementById("hosts");
//     switching = true;
//     while (switching) {
//       switching = false;
//       rows = table.getElementsByTagName("tr");
//       for (i = 1; i < (rows.length - 1); i++) {
//         shouldSwitch = false;
//         x = rows[i].getElementsByTagName("td")[3];
//         y = rows[i + 1].getElementsByTagName("td")[3];
//         if (Number(x.innerHTML) > Number(y.innerHTML)) {
//           shouldSwitch = true;
//           break;
//         }
//       }
//       if (shouldSwitch) {
//         rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
//         switching = true;
//       }
//     }
// }

// sortTable();
