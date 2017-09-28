

function goboom() {
    console.log($.ajax('/boom'));
}

function getdata() {
    $.ajax('/getdata', {complete: doit});
    
}

function doit(resp) {
    $('p').text(resp.responseText);
}

setInterval(getdata, 100);