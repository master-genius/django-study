function top_block_show(nid, html, classname) {
    var domn = document.getElementById(nid);
    if (domn) {
        domn.innerHTML = html;
        domn.className = classname;
    }
}

function top_block_reset(nid, html='', classname='') {
    var domn = document.getElementById(nid);
    if (domn) {
        domn.innerHTML = html;
        domn.className = classname;
    }
}