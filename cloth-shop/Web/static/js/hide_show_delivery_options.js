  $(document).ready(function() {

    $('#deliver-to-house').hide();
    $('#deliver-to-parcel-locker').hide();

    $('input[name="delivery"]').change(function() {
      var selectedOption = $(this).val();

      if (selectedOption === 'house') {
        $('#deliver-to-house').show();
        $('#deliver-to-parcel-locker').hide();
      } else if (selectedOption === 'locker') {
        $('#deliver-to-parcel-locker').show();
        $('#deliver-to-house').hide();
      }
    });
  });

