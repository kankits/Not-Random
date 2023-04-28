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

function createStarRating(rating, numRatings) {
  let stars = '<p>';
  const fullStars = Math.floor(rating);
  const halfStar = rating % 1 !== 0;
  const emptyStars = 5 - fullStars - halfStar;
  for (let i = 0; i < fullStars; i++) {
    stars += '<i class="fas fa-star rating-star"></i>';
  }
  if (halfStar) {
    stars += '<i class="fas fa-star-half-alt rating-star"></i>';
  }
  for (let i = 0; i < emptyStars; i++) {
    stars += '<i class="far fa-star rating-star"></i>';
  }
  stars += `</p><br><p style="color: blue; font-size: small;">${numRatings} ratings</p>`;
  return stars;
}

function createRatingDropdown(loggedIn) {
  let dropdown = '<div class="dropdown">';
  if (loggedIn) {
    dropdown += '<button class="btn btn-primary dropdown-toggle" type="button" id="rating-dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">';
  }
  else{
    dropdown += '<button class="btn btn-primary dropdown-toggle disabled" type="button" id="rating-dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">';
  }
  dropdown += '<i class="fas fa-thumbs-up fa-2x" style="color: goldenrod;"></i>';
  dropdown += '</button>';
  dropdown += '<div class="dropdown-menu" aria-labelledby="rating-dropdown">';
  dropdown += '<div class="rating-stars">';
  for (let i = 1; i <= 5; i++) {
    dropdown += `<i class="fas fa-star fa-1x rating-star-rate" data-value="${i}"></i>`;
  }
  dropdown += '</div>';
  dropdown += '</div>';
  dropdown += '</div>';

  return dropdown;
}

// jQuery event handler for hovering over a star
$(document).on('mouseenter', '.rating-star-rate', function() {
  $(this).addClass('fas').removeClass('far');
  $(this).prevAll('.rating-star-rate').addClass('fas').removeClass('far');
  $(this).nextAll('.rating-star-rate').addClass('far').removeClass('fas');
});

// jQuery event handler for clicking on a star
$(document).on('click', '.rating-star-rate', function() {
  const rating = $(this).data('value');
  console.log('Selected rating:', rating);
  // TODO: Add code to submit rating to server or update UI
});

function createFavoriteButton(inFavorite, loggedIn) {
  if (loggedIn) {
    if (inFavorite) {
      return '<button type="button" class="btn btn-primary"><i class="fas fa-heart fa-2x", style="padding-right: 10px;"></i>Add to Favorites</button>';
    }
    return '<button type="button" class="btn btn-primary"><i class="far fa-heart fa-2x", style="padding-right: 10px;"></i>Add to Favorites</button>';
  }
  else{
    return '<button type="button" class="btn btn-primary disabled"><i class="fas fa-heart fa-2x", style="padding-right: 10px;"></i>Add to Favorites</button>';
  }
}

// This is just some dummy data for demonstration purposes
var allResults = [
  { title: 'Book 1', category: 'Books', option: "option1", name: "abc", tag: "abc", place: "place1", city: "city1", state: "state1", rating: 4.5, num_ratings: 100, in_favorite: true, given_rating: 5},
  { title: 'Book 2', category: 'Books', option: "option2", name: "def", tag: "def", place: "place2", city: "city2", state: "state2", rating: 4.5, num_ratings: 100, in_favorite: true, given_rating: 4},
  { title: 'Electronics 1', category: 'Electronics', option: "option3", name: "ghi", tag: "ghi", place: "place3", city: "city3", state: "state3", rating: 4.5, num_ratings: 100, in_favorite: true, given_rating: 3},
  { title: 'Electronics 2', category: 'Electronics', option: "option1", name: "abc", tag: "abc", place: "place4", city: "city4", state: "state4", rating: 4.5, num_ratings: 100, in_favorite: false, given_rating: 2},
  { title: 'Clothing 1', category: 'Clothing', option: "option2", name: "def", tag: "def", place: "place5", city: "city5", state: "state5", rating: 4.5, num_ratings: 100, in_favorite: false, given_rating: 1},
  { title: 'Clothing 2', category: 'Clothing', option: "option3", name: "ghi", tag: "ghi", place: "place6", city: "city6", state: "state6", rating: 4.5, num_ratings: 100, in_favorite: false, given_rating: 0}
];