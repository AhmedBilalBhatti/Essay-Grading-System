/*=== Javascript function indexing hear===========

1.counterUp ----------(Its use for counting number)
2.stickyHeader -------(header class sticky)
3.wowActive ----------( Waw js plugins activation)
4.swiperJs -----------(All swiper in this website hear)
5.salActive ----------(Sal animation for card and all text)
6.textChanger --------(Text flip for banner section)
7.timeLine -----------(History Time line)
8.datePicker ---------(On click date calender)
9.timePicker ---------(On click time picker)
10.timeLineStory -----(History page time line)
11.vedioActivation----(Vedio activation)
12.searchOption ------(search open)
13.cartBarshow -------(Cart sode bar)
14.sideMenu ----------(Open side menu for desktop)
15.Back to top -------(back to top)
16.filterPrice -------(Price filtering)

==================================================*/

(function ($) {
    'use strict';
  
    var rtsJs = {
        m: function (e) {
            rtsJs.d();
            rtsJs.methods();
        },
        d: function (e) {
            this._window = $(window),
            this._document = $(document),
            this._body = $('body'),
            this._html = $('html')
        },
        methods: function (e) {
            rtsJs.sideCollups();
            rtsJs.niceSelect();
            rtsJs.newTab();
            rtsJs.darkLightSwitcher();
            rtsJs.stickySearch();
        },
        
        sideCollups: function () {
            // Toggle classes on button click
            $('#collups-left').on('click', function (e) {
              $('#collups-left').toggleClass('collapsed');
              $('.left-side-bar').toggleClass('collapsed');
              $('.main-center-content-m-left').toggleClass('collapsed');
            });
            // Popup Toggle
            $(".single_action__haeader svg, .avatar").click(function(e) {
                e.preventDefault();
                var $popup = $(this).siblings('.slide-down__click');
            
                $popup.slideToggle();
                $(".slide-down__click").not($popup).slideUp(0);
            });
            // Popup Toggle
            $(".single_action__haeader").click(function(e) {
                $(this).toggleClass('active');
            });

            $(".right-side-open-clouse").click(function(e) {
                $(this).parent().toggleClass('close-right');
                $('.main-center-content-m-left').toggleClass('close-right-sidebar');
            });



        },

        niceSelect: function(){
            $('.nice-select').each(function() {
  
                var select = $(this),
                    name = select.attr('name');
                
                select.hide();
                
                select.wrap('<div class="nice-select-wrap"></div>');
                
                var parent = select.parent('.nice-select-wrap');
                
                parent.append('<ul id=' + name + ' style="display:none"></ul>');
                
                select.find('option').each(function() {
              
                  var option = $(this),
                      value = option.attr('value'),
                      label = option.text();
                  
                  if (option.is(":first-child")) {
                    
                    $('<a href="#" class="drop">' + label + '</a>').insertBefore(parent.find('ul'));
                    
                  } else {
                    
                    parent.find('ul').append('<li><a href="#" id="' + value + '">' + label + '</a></li>');
                    
                  }
                  
                });
                
                parent.find('a').on('click', function(e) {
                  
                  parent.toggleClass('down').find('ul').slideToggle(300);
                  
                  e.preventDefault();
                
                });
                
                parent.find('ul a').on('click', function(e) {
                  
                  var niceOption = $(this),
                          value = niceOption.attr('id'),
                      text = niceOption.text();
                  
                  select.val(value);
                  
                  parent.find('.drop').text(text);
                  
                  e.preventDefault();
                
                });
                
            });
        },

        newTab: function(){
            $(document).ready(function(){
                $('.new-chat-option').on('click', function(){
                    $('.question_answer__wrapper__chatbot').hide(5);
                });
                $('.chat-history-area-start .single-history').on('click', function(){
                    $('.question_answer__wrapper__chatbot').hide(5).show(5);
                });
            });
        },

        darkLightSwitcher: function(e){
            $(document).ready(function() {

                // THEME MODE SWITCHER JS
                  var rts_light = $('.rts-dark-light');
                  if(rts_light.length){
                  var toggle = document.getElementById("rts-data-toggle");
                  var storedTheme = localStorage.getItem('intellact-theme') || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
                  if (storedTheme)
                      document.documentElement.setAttribute('data-theme', storedTheme)
                      toggle.onclick = function() {
                      var currentTheme = document.documentElement.getAttribute("data-theme");
                      var targetTheme = "light";
              
                      if (currentTheme === "light") {
                          targetTheme = "dark";
                      }
                      document.documentElement.setAttribute('data-theme', targetTheme)
                      localStorage.setItem('intellact-theme', targetTheme);
                  };
                  }
              });
        },

        stickySearch: function (e) {
            $(document).ready(function(){
                $(window).scroll(function(){
                    // Calculate the distance between the bottom of the page and the bottom of the viewport
                    var distanceFromBottom = $(document).height() - $(window).height() - $(window).scrollTop();
        
                    // Define a threshold for when to add the 'active' class
                    var threshold = 200; // You can adjust this value according to your requirement
        
                    // If the distance from the bottom is less than the threshold, add the 'active' class
                    if(distanceFromBottom < threshold) {
                        $('.chatbot .search-form').addClass('active');
                    } else {
                        $('.chatbot .search-form').removeClass('active');
                    }
                });
            });
 
        },

        
    }

    rtsJs.m();
  })(jQuery, window) 







