function searchInputHandler(inputId, resultsId) {
    $('#' + inputId).on('keyup', function() {
      var query = $(this).val();
      $.ajax({
        type: 'GET',
        url: '/get_candidate_values',
        data: {'column': 'column_name', 'query': query},
        success: function(response) {
          var results = response.data;
          var list = $('#' + resultsId + ' ul');
          list.empty(); // Clear any previous results
  
          // Loop through the results and create a new <li> element for each one
          for (var i = 0; i < results.length; i++) {
            var item = $('<li>').text(results[i]);
  
            // Add a click event listener to each <li> element
            item.on('click', function() {
              $('#' + inputId).val($(this).text());
              $('#' + resultsId).hide();
            });
  
            list.append(item);
          }
  
          // Show the search results
          $('#' + resultsId).show();
        },
        error: function(error) {
          console.log(error);
        }
      });
    });
}

function addToTag() {
    var list = $('#search-box-tags ul');

    var item = $('<li class="badge_tag">').text($('#search-tag-filter-input').val());

    var removeButton = $('<span class="remove-button">').text('x');

    // Add a click event listener to the remove button
    removeButton.on('click', function() {
      $(this).parent().remove();
    });

    // Add the remove button to the item
    item.append(removeButton);

    list.append(item);
}

function getCheckedOptions() {
  var checkedValues = [];
  $('input[type="checkbox"]:checked').each(function() {
    checkedValues.push($(this).val());
  });
  return checkedValues;
}

function getAddedTags() {
  var tags = [];
    $('#search-box-tags li').each(function() {
      tags.push($(this).text().trim().replace(/x$/, ''));
    });
  return tags;
}

// function isLoggedIn(callback) {
//   $.ajax({
//     type: 'GET',
//     url: '/logged_in', 
//     success: function(response) {
//       console.log("response");
//       if (response.logged_in) {
//         callback(true);
//       } else {
//         callback(false);
//       }
//     },
//     error: function(error) {
//       console.log(error);
//       callback(false);
//     }
//   });
// }

// var loginStatus = false;

// // setInterval(updateLoggedIn, 1000);

// function updateLoggedIn(){
//     isLoggedIn(setLoginStatus);
// }

// function setLoginStatus(data) {
//     loginStatus = data;
// }