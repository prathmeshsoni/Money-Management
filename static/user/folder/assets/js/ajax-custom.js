var substringMatcher = function(strs) {
  return function findMatches(q, cb) {
    var matches, substringRegex;
    matches = [];
    substrRegex = new RegExp(q, 'i');
    $.each(strs, function(i, str) {
      if (substrRegex.test(str)) {
        matches.push(str);
      }
    });
    cb(matches);
  };
};


var states = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        local: [
            {'name':'women fashion shoes', 'image': '../assets/images/mega-store/product/1.jpg', 'price':'$250'}, 
            {'name':'men analogue watch', 'image': '../assets/images/mega-store/product/2.jpg', 'price':'$150'},
            {'name':'wireless  headphones', 'image': '../assets/images/mega-store/product/3.jpg', 'price':'$130'},
            {'name':'redmi not 9 pro', 'image': '../assets/images/mega-store/product/4.jpg', 'price':'$80'},
            {'name':'Red Casual Backpack', 'image': '../assets/images/mega-store/product/5.jpg', 'price':'$145'},
            {'name':'sony xperia m5', 'image': '../assets/images/mega-store/hot-deal/1.jpg', 'price':'$130'},
            {'name':'Fogg Xtremo Scent', 'image': '../assets/images/mega-store/hot-deal/2.jpg', 'price':'$170'},
            {'name':'Realme Classic Watch ', 'image': '../assets/images/mega-store/hot-deal/3.jpg', 'price':'$180'},
            {'name':'Kofy Tomato Seed', 'image': '../assets/images/mega-store/media-product/6.jpg', 'price':'$320'},
            {'name':'lather bag', 'image': '../assets/images/mega-store/media-product/5.jpg', 'price':'$270'},
            ]
    });

    states.initialize();


$('.the-basics .typeahead').typeahead({
  hint: true,
  highlight: true,
  minLength: 1
},
{
  name: 'states',
  display: 'name',
  source: states.ttAdapter(),
  templates: {
    empty: [
      '<div class="empty-message">',
        'No Record Found !',
      '</div>'
    ].join('\n'),
    suggestion: function (data) {
        return '<a href="product-page(left-sidebar).html" class="man-section"><div class="image-section"><img src='+data.image+'></div><div class="description-section"><h4>'+data.name+'</h4><span>'+data.price+'</span></div></a>';
    }
  },
});