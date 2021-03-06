function resize() {
  $("#main").addClass("pull-right");

  if ($("#sidebar").width() < 200) {
    degree = 1;
    $("#side").removeClass("col-lg-3 col-md-3").addClass("col-lg-12 col-md-12");
    $("#main").addClass("col-lg-12 col-md-12").removeClass("pull-right col-lg-9 col-md-9");
    $("#sidebar").removeAttr("data-spy").removeClass("affix").removeClass("affix-top");
  } else {
    degree = 2;
    $("#side").addClass("col-lg-3 col-md-3").removeClass("col-lg-12 col-md-12");
    $("#main").removeClass("col-lg-12 col-md-12").addClass("pull-right col-lg-9 col-md-9");
    $("#sidebar").attr("data-spy","affix").affix( { offset: { top: $("#main").position().top } } );
  }
}

var degree = 0;

$(document).ready(function() {
  setTimeout(function() {
    if (side_toggle) { $("#nav_toggle").trigger("click"); }
    resize();
  }, 1000);
  
  $('body').scrollspy({
    'target': '.scroll_nav',
    'offset': 150
  });
  $('.scroll_nav').on('activate.bs.scrollspy', function() {
    $('.scroll_nav > ul > li:not(.active) > ul.panel-collapse').collapse('hide');
    $('.scroll_nav > ul > li.active > ul.panel-collapse').collapse('show');
  });

  $('[id^=tab_], #top').on('click', function(event) {
    event.preventDefault();
    $('html, body').stop().animate({scrollTop: $($(this).attr("href")).offset().top - 75}, 500);
  });
  
  $('ul.panel-collapse').on('show.bs.collapse', function() {
    $(this).parent().find("a>span.glyphicon.pull-right")
      .removeClass("glyphicon-triangle-bottom")
      .addClass("glyphicon-triangle-top");
      
  });
  $('ul.panel-collapse').on('hide.bs.collapse', function() {
    $(this).parent().find("a>span.glyphicon.pull-right")
      .removeClass("glyphicon-triangle-top")
      .addClass("glyphicon-triangle-bottom");
  });

});


$(window).on("scroll", throttle(function() {
  if ($(this).scrollTop() > $(window).height() / 2) {
    $('#top > div').animate({'right': '0%', 'opacity': 0.85}, 125);
  } else {
    $('#top > div').animate({'right': '-5%', 'opacity': 0}, 125);
  }
  if (degree == 1) {
    $("#sidebar").removeAttr("data-spy").removeClass("affix").removeClass("affix-top");
    // $('body').scrollspy('clear');
  }
  $("#sidebar").css("width", $("#side_con").css("width"));
}, 200, 500));

$(window).on("resize", throttle(resize, 200, 1000));

