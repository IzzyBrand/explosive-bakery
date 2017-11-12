$(document).ready(function(){
    $('ul.tabs').tabs();
    $('ul.tabs').tabs('select_tab', 'test');
});

alert(launchReady);
$('button').prop('disabled', true);