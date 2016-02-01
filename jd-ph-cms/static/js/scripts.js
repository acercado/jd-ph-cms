$(function () {
  
  /* Initialize DataTables */
  var oTable = $('.data-tables').DataTable({
    "paging": true,
    "lengthChange": false,
    "searching": true,
    "ordering": true,
    "info": true,
    "autoWidth": true,
    "aaSorting": [],
    // "order": [[ 1, "asc" ]],
    // "columnDefs": [
    //   {
    //       "targets": [ 0 ],
    //       "visible": false,
    //       "searchable": false,
    //   },
    // ],
    "dom": '<"top">rt<"bottom"lip><"clear">',
    // "dom": '<"top">rt<"bottom"lip><"clear">',
    "responsive": true,
    // buttons: true,
    "buttons": [
      'csv',
      {
          extend: 'excel',
          text: 'xls'
      },
    ]
  });

  // var oTable = $('.data-tables').DataTable( {
  //   // dom: '<"top">rt<"bottom"lip><"clear">',
  //   buttons: [
  //       'copy', 'excel', 'pdf'
  //   ]
  // });

  // new $.fn.dataTable.Buttons( oTable, {
  //     buttons: [
  //         'csv', 'excel', 'pdf'
  //     ]
  // } );

  // oTable.buttons().container()
  //     .appendTo( $('div.button-container', oTable.table().container() ) );

  // oTable.buttons( 0, null ).containers().appendTo( 'body' );

  $('#search_table').keyup(function(){
      console.log('Search table triggered.');
      oTable.search($(this).val()).draw() ;
  });

  oTable.buttons().container()
      .appendTo( $('.button-container') );
  



  $('.autocomplete').autocomplete({
    source: "/cms/rewards/loyaltycodes/search",
    minLength: 3,
    select: function( event, ui ) {
      console.log( ui.item ?
        "Selected: " + ui.item.label + " aka " + ui.item.value :
        "Nothing selected, input was " + this.value );
    }
  });

  $('input[type="checkbox"],input[type="radio"]').iCheck({
    checkboxClass: 'icheckbox_flat',
    radioClass: 'iradio_flat'
  });
  
  //Date range picker with time picker
  $('#publishtime, #filter-duration').daterangepicker({timePicker: true, timePickerIncrement: 30, format: 'YYYY-MM-DD h:mm A'});
  
  //Single Date picker
  $('.duration-dates').daterangepicker({
        singleDatePicker: true,
        showDropdowns: true,
              format: 'YYYY-MM-DD'

  });

  //WYSIWYG HTML5
  // $(".textarea").wysihtml5();
  
  //Timepicker
  $(".timepicker").timepicker({
    showInputs: false,
    minuteStep: 1
  });
  

});

  
/* Vertically-center Modals */
function reposition() {
  var modal = $(this),
    dialog = modal.find('.modal-dialog');
  modal.css('display', 'block');
  
  // Dividing by two centers the modal exactly, but dividing by three 
  // or four works better for larger screens.
  dialog.css("margin-top", Math.max(0, ($(window).height() - dialog.height()) / 2));
}
// Reposition when a modal is shown
$('.modal').on('show.bs.modal', reposition);
// Reposition when the window is resized
$(window).on('resize', function() {
  $('.modal:visible').each(reposition);
});
