$(document).ready(function(){
    $('ul.tabs').tabs();
    $('ul.tabs').tabs('select_tab', 'test');
    form = $('#new-test-form');
    date = new Date().toISOString().substring(0, 10)
    form.find('#new-test-date').val(date);
    form.find('#new-test-name').val('testing');
    form.find('#new-test-length').val(6);
    form.find('#new-test-diameter').val(1);
    $('form#new-test-form').submit(function(e){
        e.preventDefault();
        $.ajax({
            url:'/maketest',
            type:'post',
            data:$('form#new-test-form').serialize(),
            success: newTestDone
        });
    });
});

function newTest(x) {
    button = $(x);
    button.prop('disabled', true);
    form = $('#new-test-form');
    req = form.find('.input-field.required input');
    complete = true;
    for (i = 0; i < req.length; i++) {
        inp = req.eq(i);
        if (inp.val() == '') {
            complete = false;
            inp.addClass('invalid');
        }
        else {
            inp.removeClass('invalid');
        }
    }
    if (!complete) {
        return;
    }
    $('form#new-test-form').submit();
}

function newTestDone(resp) {
    resp = JSON.parse(resp);
    if (!resp['worked']) {
        Materialize.Toast('Error...', 300);
        return;
    }
    console.log(resp);
    id = resp['id']
    $('div.buttons button').data('id', id);

    button = $('#start-test-button');
    button.removeClass('hidden');
    $('#new-test-button').prop('disabled', true);
    $('form#new-test-form').find('input').prop('disabled', true);
    $('button#cancel-test-button').removeClass('hidden');
}

function startTest(x) {
    id = $(x).data('id');
    $.ajax({url: '/starttest/' + id,
            success: startSuccess,
            error: startError});
}

function startSuccess(resp) {
    console.log('uh');
    button = $('#start-test-button');
    button.prop('disabled', true);
    cancelButton = $('button#cancel-test-button')
    cancelButton.prop('disabled', true);
    stopButton = $('button#stop-test-button');
    stopButton.removeClass('hidden');
}

function startError(resp) {
    Materialize.toast('Error in starting test...');
}

function stopTest(x) {
    button = $(x);
    id = button.data('id');
    $.ajax({url: '/stoptest/' + id,
            success: testDone,
            error: testFail});
}

function testDone(resp) {
    Materialize.toast('Test complete', 2000);
    buttons = $('.buttons button:not("#new-test-button")')
    buttons.prop('disabled', false);
    buttons.addClass('hidden');
    $('#new-test-button').prop('disabled', false);
    $('.buttons button').removeData('id')
}

function testFail(resp) {
    Materialize.toast('Test failed');
}

function cancelTest(x) {
    button = $(x);
    $.ajax({url: '/cancel/' + button.data('id'),
            success: cancelComplete,
            error: cancelFailure})
}

function cancelComplete(resp) {
    Materialize.toast('Test cancelled', 1500);
    $('#new-test-button').prop('disabled', false);
    $('#start-test-button').addClass('hidden');
    $('#cancel-test-button').addClass('hidden');
    $('#new-test-form input').prop('disabled', false);
    $('.buttons button').removeData('id');
}

function cancelFailure(resp) {
    Materialize.toast('Error in cancelling test');
}

