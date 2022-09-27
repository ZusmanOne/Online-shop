var domain = 'http://localhost:8000/ '

window.onload = function() {
    var list = document.getElementById('list');
    var rubricListLoader = new XМLHttpRequest()
    rubricListLoader.onreadystatechange = function() {
        if (rubricListLoader.readyState == 4) {
            if (rubricListLoader.status == 200) {
                var data = JSON.parse(rubricListLoader.responseText);
                var s = '<ul>';
                for (i=0; i < data.length; i++) {
                    s += '<li>' + data[i].name + '</li>';
                }
                s += '</ul>'
                list.innerHTML = s;
            }
        }
    }
    function rubricListLoad() {
        rubricListLoader.open('GET', domain + 'api/product/', true);
        rubricListLoader.send();
    }
    rubricListLoad();
}