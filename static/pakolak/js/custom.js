// JavaScript Document

$(function() {
 "use strict";

  function responsive_dropdown () {

    /* ---- For Mobile Menu Dropdown JS Start ---- */
    $("#menu-main span.opener").on("click", function(){
      var menuopener = $(this);
      if (menuopener.hasClass("plus")) {
         
        if (menuopener.parents('.sub-menu-level1').length) {
          menuopener.parent().find('.second-sub-menu').slideDown(700);
        }else{
          menuopener.parent().find('.mobile-sub-menu').slideDown(700);
        }
        menuopener.removeClass('plus');
        menuopener.addClass('minus');
      }
      else
      {
        menuopener.parent().find('.mobile-sub-menu, .second-sub-menu').slideUp();
        menuopener.removeClass('minus');
        menuopener.addClass('plus');
      }
      return false;
    });

    jQuery( ".mobilemenu" ).on("click", function() {
      jQuery( ".mobilemenu-content" ).slideToggle();
      if ($(this).hasClass("openmenu")) {
        $(this).removeClass('openmenu');
        $(this).addClass('closemenu');
      }
      else
      {
        $(this).removeClass('closemenu');
        $(this).addClass('openmenu');
      }
      return false;
    });
    /* ---- For Mobile Menu Dropdown JS End ---- */

    /* ---- For Sidebar JS Start ---- */
    $('.sidebar-box span.opener').on("click", function(){
    
      if ($(this).hasClass("plus")) {
        $(this).parent().find('.sidebar-contant').slideDown();
        $(this).removeClass('plus');
        $(this).addClass('minus');
      }
      else
      {
        $(this).parent().find('.sidebar-contant').slideUp();
        $(this).removeClass('minus');
        $(this).addClass('plus');
      }
      return false;
    });
    /* ---- For Sidebar JS End ---- */

    /* ---- For Footer JS Start ---- */
    $('.footer-static-block span.opener').on("click", function(){
    
      if ($(this).hasClass("plus")) {
        $(this).parent().find('.footer-block-contant').slideDown();
        $(this).removeClass('plus');
        $(this).addClass('minus');
      }
      else
      {
        $(this).parent().find('.footer-block-contant').slideUp();
        $(this).removeClass('minus');
        $(this).addClass('plus');
      }
      return false;
    });
    /* ---- For Footer JS End ---- */

     /* ---- For Navbar JS Start ---- */
    $('.navbar-toggle').on("click", function(){
      var menu_id = $('#menu');
      var nav_icon = $('.navbar-toggle i');
      if(menu_id.hasClass('menu-open')){
        menu_id.removeClass('menu-open');
        nav_icon.removeClass('fa-times');
        nav_icon.addClass('fa-bars');
      }else{
        menu_id.addClass('menu-open');
        nav_icon.addClass('fa-times');
        nav_icon.removeClass('fa-bars');
      }
      return false;
    });
    /* ---- For Navbar JS End ---- */

    /* ---- For Category Dropdown JS Start ---- */
    $('.btn-sidebar-menu-dropdown').on("click", function() {
      var sb_block = $('.sidebar-block');
      $('.cat-dropdown').slideToggle();

      if(sb_block.hasClass("open1")){
        sb_block.addClass("close1").removeClass("open1");
      }else{
        sb_block.addClass("open1").removeClass("close1");
      }
      return false;
    });
    /* ---- For Category Dropdown JS End ---- */

    /* ---- For Content Dropdown JS Start ---- */
    $('.content-link').on("click", function() {
      $('.content-dropdown').toggle();
    });
    /* ---- For Content Dropdown JS End ---- */
  }


  function owlcarousel_slider () {
    /* ------------ OWL Slider Start  ------------- */

    /* ---- main-banner Start ---- */
      $(".main-banner").owlCarousel({
     
        //navigation : true,  Show next and prev buttons
        items: 1,
        slideSpeed : 300,
        paginationSpeed : 400,
        loop:true,
        smartSpeed: 1000,
        autoPlay: true,
        singleItem:true,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
            },
            768:{
              dots: false,
              nav: true,
            }
        }
      });
      /* ----- main-banner End  ------ */

      /* -----  categorie slider Start  ------ */
      $('.categorie-part').owlCarousel({
        items: 4,
        nav: true,
        dots: false,
        loop:true,
        slideSpeed : 300,
        paginationSpeed : 400,
        smartSpeed: 1000,
        autoplay:false,
        autoplayTimeout:3000,
        autoplayHoverPause:true,
        responsiveClass:true,
        responsive:{
            0:{
              items:1,
              nav: false,
            },
            446:{
              items:2,
              nav: false,
            },
            576:{
              items:2,
            },
            768:{
                items:2,
            },
            992:{
                items:3,
            },
            1200:{
                items:4,
            }
        }
      });
      /* ----- categorie slider End  ------ */

      /* -----  packages slider Start  ------ */
      $('.packages-part').owlCarousel({
        items: 4,
        nav: true,
        dots: false,
        loop:true,
        slideSpeed : 300,
        paginationSpeed : 400,
        smartSpeed: 1000,
        autoplay:true,
        autoplayTimeout:3000,
        autoplayHoverPause:true,
        responsiveClass:true,
        responsive:{
            0:{
              items:1,
              nav: false,
            },
            576:{
              items:1,
            },
            768:{
                items:2,
            },
            992:{
                items:2,
            },
            1200:{
                items:3,
            }
        }
      });
      /* ----- packages slider End  ------ */

      /* -----  packages slider Start  ------ */
      $('.room-part').owlCarousel({
        items: 4,
        nav: true,
        dots: false,
        loop:true,
        slideSpeed : 300,
        paginationSpeed : 400,
        smartSpeed: 1000,
        autoplay:false,
        autoplayTimeout:3000,
        autoplayHoverPause:true,
        responsiveClass:true,
        responsive:{
            0:{
              items:1,
              nav: false,
            },
            576:{
              items:1,
            },
            768:{
                items:2,
            },
            992:{
                items:2,
            },
            1200:{
                items:3,
            }
        }
      });
      /* ----- packages slider End  ------ */

      /* -----  hotel-restaurent slider Start  ------ */
      $('.hotel-restaurent').owlCarousel({
        items: 4,
        nav: true,
        dots: false,
        loop:true,
        slideSpeed : 300,
        paginationSpeed : 400,
        smartSpeed: 1000,
        autoplay:false,
        autoplayTimeout:3000,
        autoplayHoverPause:true,
        responsiveClass:true,
        responsive:{
            0:{
              items:1,
              nav: false,
            },
            576:{
              items:1,
            },
            768:{
                items:2,
            },
            992:{
                items:2,
            },
            1200:{
                items:3,
            }
        }
      });
      /* ----- hotel-restaurent slider End  ------ */

      /* -----  hotel-restaurent slider Start  ------ */
      $('.hotel-restaurent2').owlCarousel({
        items: 2,
        nav: false,
        dots: false,
        loop:true,
        slideSpeed : 300,
        paginationSpeed : 400,
        smartSpeed: 1000,
        autoplay:true,
        autoplayTimeout:3000,
        autoplayHoverPause:true,
        responsiveClass:true,
        responsive:{
            0:{
              items:1,
              nav: false,
            },
            576:{
              items:1,
            },
            768:{
                items:2,
            },
            992:{
                items:2,
            },
            1200:{
                items:2,
            }
        }
      });
      /* ----- hotel-restaurent slider End  ------ */

      /* -----  tranportation slider Start  ------ */
      $('.tranportation-part').owlCarousel({
        items: 4,
        nav: true,
        dots: false,
        loop:true,
        slideSpeed : 300,
        paginationSpeed : 400,
        smartSpeed: 1000,
        autoplay:false,
        autoplayTimeout:3000,
        autoplayHoverPause:true,
        responsiveClass:true,
        responsive:{
            0:{
              items:1,
              nav: false,
            },
            576:{
              items:1,
            },
            768:{
                items:2,
            },
            992:{
                items:2,
            },
            1200:{
                items:3,
            }
        }
      });
      /* ----- tranportation slider End  ------ */

      /* ---- testimonial Start ---- */
      $(".client-slider").owlCarousel({
     
        //navigation : true,  Show next and prev buttons
        items: 1,
        slideSpeed : 300,
        paginationSpeed : 400,
        loop:true,
        smartSpeed: 1000,
        autoPlay: true,
        singleItem:true,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
            },
            768:{
              dots: false,
              nav: true,
            }
        }
      });
      /* ----- testimonial End  ------ */
    
    /* -----  our-team slider Start  ------ */
      $('.our-team').owlCarousel({
        items: 4,
        nav: true,
        dots: false,
        loop:true,
        smartSpeed: 1000,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
            },
            420:{
                items:2,
            },
            768:{
                items:2,
            },
            992:{
                items:3,
            },
            1200:{
                items:4,
            }
        }
      });
      /* ----- our-team slider End  ------ */

    /* ----- blog Start  ------ */
      $('#blog').owlCarousel({
        items: 3,
        nav: true,
        dots: false,
        loop:true,
        smartSpeed: 1000,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
              nav: false,
            },
            576:{
                items:1,
            },
            768:{
                items:2,
            },
            1200:{
                items:3,
            }
        }
      });
      /* ----- blog End  ------ */
      /* -----  service-part slider Start  ------ */
      $('#service-part').owlCarousel({
        items: 3,
        nav: true,
        dots: false,
        loop:true,
        slideSpeed : 300,
        paginationSpeed : 400,
        smartSpeed: 1000,
        autoplay:true,
        autoplayTimeout:3000,
        autoplayHoverPause:true,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
                nav: false,
            },
            501:{
                items:2,
            },
            768:{
                items:2,
            },
            992:{
                items:3,
            },
            1200:{
                items:3,
            }
        }
      });
    /* ----- service-part slider End  ------ */
      
    return false;
    /* ------------ OWL Slider End  ------------- */
  }

  function scrolltop_arrow () {
   /* ---- Page Scrollup JS Start ---- */
   //When distance from top = 250px fade button in/out
    var scrollup = $('.scrollup');
    var headertag = $('header');
    var mainfix = $('.main');
    $(window).scroll(function(){
      if ($(this).scrollTop() > 0) {
          scrollup.fadeIn(300);
      } else {
          scrollup.fadeOut(300);
      }

      /* header-fixed JS Start */
      if ($(this).scrollTop() > 40){
         headertag.addClass("header-fixed");
      }
      else{ 
         headertag.removeClass("header-fixed");
      }

      /* main-fixed JS Start */
      if ($(this).scrollTop() > 0){
         mainfix.addClass("main-fixed");
      }
      else{ 
         mainfix.removeClass("main-fixed");
      }
      /* ---- Page Scrollup JS End ---- */
    });
    
    //On click scroll to top of page t = 1000ms
    scrollup.on("click", function(){
      $("html, body").animate({ scrollTop: 0 }, 1000);
      return false;
    });
  }
     
  /*countdown-clock Js Start*/
  function countdown_clock() {
    $('.countdown-clock').downCount({
      date: '03/04/2024 11:39:00',
          offset: +10
      }, 
      function () {
        //alert('done!'); Finish Time limit
      return false;
    });
  }
  /*countdown-clock Js End*/

  /* faq_tab Js Start */
  function  faq_tab (){
    $("#tabs li a").on("click", function(e){
      var title = $(e.currentTarget).attr("title");
      $("#tabs li a , .tab_content li div").removeClass("selected");
      $(".tab-"+title +", .items-"+title).addClass("selected");
      $("#items").attr("class","tab-"+title);

      return false;
    });
  }
  /* faq_tab Js End */

  /*datepicker Js Start*/
  function datepicker () {
    $( ".datepicker" ).datepicker();
    return false;
  }
  /*datepicker Js Ends*/

  /*select2 Js Start*/
  function select2 () {
    if($('.select').length > 0){
      $('.select').select2();
    }
  }
  /*select2 Js End*/

  //Dropdown
   function dropdown () {
      $('.drop-option').on( "click", function() {

        if($(this).find('.drop-list').hasClass('active')) {
          $(this).parent().removeClass("dropdown-active");
          $(this).find('.drop-list').removeClass('active');
          $(this).find('.select-option').slideUp(300);
        }
        else {
          $(this).parent().addClass("dropdown-active");
          $('.drop-option .select-option').slideUp(300);
          $('.drop-option .active').removeClass('active');
          $(this).find('.drop-list').addClass('active');
          $(this).find('.select-option').slideDown(300);
        }
        return false;
      });
      $('.drop-option .select-option a').on( "click", function() {
        $(this).parent().parent().find('span').text($(this).text());
        $('.drop-option').find('.select-option').slideUp(300);
      });
  }

  /*Load-More Js Start*/
  function load_more () {
    $(".the-world").slice(0, 6).show();
    $("#loadMore-best").on('click', function (e) {
        e.preventDefault();
        $(".the-world:hidden").slice(0, 6).slideDown();
        if ($(".the-world:hidden").length == 0) {
            $("#load").fadeOut('slow');
        }
    });
  }

  /*Load-More Js Ends*/

  /* Price-range Js Start */
  function price_range () {
      $( "#slider-range" ).slider({
        range: true,
        min: 0,
        max: 800,
        values: [ 75, 500 ],
        slide: function( event, ui ) {
          $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
        }
      });
      $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) + " - $" + $( "#slider-range" ).slider( "values", 1 ) );
  }
  /* Price-range Js End */

  /* Sticky sidebar adjust JS Start */
  function sticky_sidebar_adjust () {
    $('.shorting .view').on('click', '.list-types', function() {
      if($(this).hasClass("list")){
        $(this).addClass("active");
        $(".shorting .view .list-types.grid").removeClass("active");
        $(".product-listing").removeClass("grid-type").addClass("list-type");
      }
      if($(this).hasClass("grid")){
        $(this).addClass("active");
        $(".shorting .view .list-types.list").removeClass("active");
        $(".product-listing").removeClass("list-type").addClass("grid-type");
      }

      return false;
    }); 


    $(".product-detail-tab .nav-tabs li a").length > 0 && $(".product-detail-tab .nav-tabs li a").on("click", function() {
         window.dispatchEvent(new Event("resize"))
    }); 

    $(".shorting .list-types .list-types-icon").length > 0 && $(".shorting .list-types .list-types-icon").on("click", function() {
      setTimeout(
        function() {
          window.dispatchEvent(new Event("resize"))
        },500);
    });
  }
  /* Sticky sidebar adjust JS End */

  /* ---- slidebar JS Start ---- */
  function slidebar_open(){
    $('.slidebar-open').on("click", function(){
      var menu_id = $('.shop-list');
      var nav_icon = $('.slidebar-open');
      if(menu_id.hasClass('menu-open')){
        menu_id.removeClass('menu-open');
        nav_icon.removeClass('fa-closed');
        nav_icon.addClass('fa-bar');
      }else{
        menu_id.addClass('menu-open');
        nav_icon.addClass('fa-closed');
        nav_icon.removeClass('fa-bar');
      }
      return false;
    });
  }
  /* ---- slidebar JS End ---- */

/*---------- Payment Card validation Js Start-----------*/
  function card_wrapper () {
    if($('form.card-form').length > 0){
      var card = new Card({
        form: 'form.card-form',
        container: '.card-wrapper',

        formSelectors: {
            nameInput: 'input[name="first-name"], input[name="last-name"]'
        }
      });
    }
  }
  /*---------- Payment Card validation Js End-----------*/

   /*Video_Popup Js Start*/
  function video_popup() {
    if($('.popup-youtube').length > 0){
    $('.popup-youtube').magnificPopup({          
        disableOn: 700,          
        type: 'iframe',          
        mainClass: 'mfp-fade',          
        removalDelay: 160,          
        preloader: false,          
        fixedContentPos: false      
      });    
    }  
  }
  /*Video_Popup Js Ends*/

  /*counter Js Start*/
  function counter () {
    if($('.counter').length > 0){
      $('.counter').countUp({
        delay: 10,
        time: 1000
      });
    }
  }
  /*counter Js End*/

  function daterangepicker() {
    if($('input[name="daterange"]').length > 0) {
      $('input[name="daterange"]').daterangepicker({
        opens: 'center'
      }, function(start, end, label) {
        console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
      });
    }
  }

  $(document).ready(function() {
    scrolltop_arrow ();
    owlcarousel_slider();  
    responsive_dropdown();
    countdown_clock ();
    faq_tab (); 
    datepicker ();
    dropdown ();
    select2 ();
    load_more ();
    price_range ();
    sticky_sidebar_adjust ();
    slidebar_open ();
    card_wrapper ();
    video_popup ();
    counter ();
    daterangepicker();
  });

});

/* Start isotope Portfolio Js */
function portfolio_isotope(){
  if($('.isotope').length > 0){
    // init Isotope
    var $container = $('.isotope').isotope({
      itemSelector: '.grid-item',
      getSortData: {
      }
    });
  }

  // bind filter click
  $('.portfolio-filter').on('click', 'li a', function() {
    var filterValue = $(this).attr('data-filter');
    // use filterFn if matches value
    $(".portfolio-filter li a ").removeClass('active');
    $( this ).addClass('active');
    $container.isotope({
      filter: filterValue
    });
  });
  return false;
}
/* End isotope Portfolio Js */

$( window ).on( "load", function() {
  // Animate loader off screen 
  $(".se-pre-con").fadeOut("slow");
  portfolio_isotope ();

  //stickySidebar
    if($('#sidebar').length > 0){
      $('#sidebar').stickySidebar({
        topSpacing: 20,
        bottomSpacing: 20
      });
    }


  // Animation WOW Start
  var wow = new WOW(
    {
      boxClass:     'wow',      // animated element css class (default is wow)
      animateClass: 'animate__animated', // animation css class (default is animated)
      offset:       100,          // distance to the element when triggering the animation (default is 0)
      mobile:       true,       // trigger animations on mobile devices (default is true)
      live:         true,       // act on asynchronously loaded content (default is true)
      callback:     function(box) {
        // the callback is fired every time an animation is started
        // the argument that is passed in is the DOM node being animated
      },
      scrollContainer: null // optional scroll container selector, otherwise use window
    }
  );
  wow.init();
  // Animation WOW End
  
});

  
  