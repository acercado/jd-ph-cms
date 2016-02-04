$(function () {

  var is_type;
  var acct_name;
  var acct_id;
  var table1 = $('#DataTables_Table_0').DataTable();
  var rowToDelete;
  $('#DataTables_Table_0 tbody').on( 'click', 'a#btn_del', function () {
      rowToDelete = table1.row( $(this).parents('tr') );
      var rowNode = rowToDelete.node();
      console.log(rowNode);
  } );

  $('.data-tables').on('click','a#btn_del', function() {
    acct_name = $(this).data('acct-name');
    acct_id = $(this).data('acct-id');
    if ($('a.btn-featured').length > 0) {
      // the button exists, exclusive to 'featured items' page
      is_type = $(this).data('is-type').toLowerCase();
    }
  {% if request.path|slice:":13" == '/cms/featured' %}
    $('#modal_del div.modal-body p').first().text('Remove from featured list?');
    // $('#modal_del div.modal-body').append('<p>'+acct_name+'</p>');

    $('#filter-duration').on('apply.daterangepicker', function(ev, picker) {
      console.log('Startdate: ' + picker.startDate.format('YYYY-MM-DD'));
      console.log('Enddate: ' + picker.endDate.format('YYYY-MM-DD'));
      $('#datetime-start').val(picker.startDate.format('YYYY-MM-DD H:M'))
    });
    is_type = $(this).data('is-type').toLowerCase();
  {% endif %}
    $(".modal_delete_text").text(acct_name);
    $("#modal_delete_val").val(acct_id);
    console.log('ID: ' + acct_id);
  });

  // clicked OK button on delete modal
  $('div#modal_del button.btn-primary').on('click',function() {
    {% if request.path|slice:":22" == '/cms/location/accounts' %}
      $.post('/cms/accounts/delete/' + $("#modal_delete_val").val())
        .done(function() {
          rowToDelete.remove();
          table1.draw();
          $('#modal_deleted').modal('show');
        });
    {% elif request.path|slice:":19" == '/cms/whiskey-family' %}
      $.post('/cms/whiskey-family/delete/' + $("#modal_delete_val").val())
        .done(function() {
          rowToDelete.remove();
          table1.draw();
          $('#modal_deleted').modal('show');
        });
    {% elif request.path|slice:":18" == '/cms/rewards/setup' %}
      $.post('/cms/rewards/setup/delete/' + $("#modal_delete_val").val())
        .done(function() {
          rowToDelete.remove();
          table1.draw();
          $('#modal_deleted').modal('show');
        });
    {% elif request.path|slice:":25" == '/cms/rewards/loyaltycodes' %}
      $.post('/cms/rewards/loyaltycodes/delete/' + $("#modal_delete_val").val())
        .done(function() {
          rowToDelete.remove();
          table1.draw();
          $('#modal_deleted').modal('show');
        });
    {% elif request.path|slice:":19" == '/cms/contests/setup' %}
      $.post('/cms/contests/setup/delete/' + $("#modal_delete_val").val())
        .done(function() {
          rowToDelete.remove();
          table1.draw();
          $('#modal_deleted').modal('show');
        });
    {% elif request.path|slice:":19" == '/cms/accounts/edit/' %}
      var prod_offer_to_delete = $("#modal_delete_val").val();
      $.post('/cms/accounts/product_offers/delete/' + $("#modal_delete_val").val())
        .done(function() {
          $('.form-group.prod-offers.'+prod_offer_to_delete).fadeOut();
          $('#modal_deleted').modal('show');
        });
    {% elif request.path|slice:":9" == '/cms/news' %}
      $.post('/cms/news/delete/' + $("#modal_delete_val").val())
        .done(function() {
          rowToDelete.remove();
          table1.draw();
          $('#modal_deleted').modal('show');
        });
    {% elif request.path|slice:":10" == '/cms/users' %}
      $.post('/cms/users/delete/' + $("#modal_delete_val").val())
        .done(function() {
          rowToDelete.remove();
          table1.draw();
          $('#modal_deleted').modal('show');
        });
    {% elif request.path|slice:":13" == '/cms/featured' %}
      if(is_type=='') is_type = 'account';
      $.post('/cms/featured/remove/' + $("#modal_delete_val").val() + '/' + is_type)
        .done(function() {
          rowToDelete.remove();
          table1.draw();
          $('#modal_deleted').modal('show');
        });
    {% endif %}
  });

  {% if mode == 'saved' %}
      $('#modal-success div.modal-body').text('Saved.');
      $('#modal-success').modal('show');
  {% elif mode == 'edited' %}
    $('#modal-success div.modal-body').text('Record updated.');
      $('#modal-success').modal('show');
  {% endif %}

  {% if request.path|slice:":23" == '/cms/rewards/setup/edit' %}
      if($('#id_reward_type').val()=='prize') {
        $('#id_value').val(0);
      }
  {% endif %}

  {% if errors != '' and request.path|slice:":30" == '/cms/perksnprizes/loyaltycodes' %}
    $('#modal-success h4.modal-title').text("Error(s)");
    $('#modal-success div.modal-body').text('{{errors}}');
    $('#modal-success').modal('show');
  {% endif %}
});