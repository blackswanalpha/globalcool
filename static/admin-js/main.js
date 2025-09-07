(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Enhanced Sidebar Toggler
    $('.sidebar-toggler').click(function () {
        $('.sidebar, .content').toggleClass("open");
        $('.sidebar-overlay').toggleClass("active");

        // Prevent body scroll when sidebar is open on mobile
        if ($(window).width() < 992) {
            $('body').toggleClass('overflow-hidden');
        }
        return false;
    });

    // Desktop sidebar collapse toggle
    $('#sidebarToggle').click(function() {
        $('.sidebar').toggleClass('collapsed');
        $('.content').toggleClass('expanded');

        // Save state to localStorage
        localStorage.setItem('sidebarCollapsed', $('.sidebar').hasClass('collapsed'));
        return false;
    });

    // Close sidebar when clicking overlay
    $('.sidebar-overlay').click(function() {
        $('.sidebar, .content').removeClass("open");
        $('.sidebar-overlay').removeClass("active");
        $('body').removeClass('overflow-hidden');
    });

    // Restore sidebar state from localStorage
    if (localStorage.getItem('sidebarCollapsed') === 'true' && $(window).width() >= 992) {
        $('.sidebar').addClass('collapsed');
        $('.content').addClass('expanded');
    }

    // Handle window resize
    $(window).resize(function() {
        if ($(window).width() >= 992) {
            $('.sidebar, .content').removeClass("open");
            $('.sidebar-overlay').removeClass("active");
            $('body').removeClass('overflow-hidden');
        }
    });

    // Enhanced search functionality
    $('#globalSearch').on('input', function() {
        const query = $(this).val();
        if (query.length > 2) {
            // Implement search functionality here
            console.log('Searching for:', query);
            // You can add AJAX call here to search backend
        }
    });

    // Notification badge update
    function updateNotificationBadge() {
        // This would typically fetch from an API
        const notificationCount = $('.dropdown-menu .dropdown-item').length - 1; // Subtract header
        const badge = $('#notificationBadge');

        if (notificationCount > 0) {
            badge.show();
        } else {
            badge.hide();
        }
    }

    // Initialize notification badge
    updateNotificationBadge();

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if( target.length ) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 70 // Account for fixed header
            }, 1000);
        }
    });

    // Auto-hide alerts after 5 seconds
    $('.alert').delay(5000).fadeOut('slow');

    // Tooltip initialization
    $('[data-bs-toggle="tooltip"]').tooltip();

    // Popover initialization
    $('[data-bs-toggle="popover"]').popover();

    // Form validation enhancement
    $('form').on('submit', function() {
        $(this).find('button[type="submit"]').prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-2"></i>Processing...');
    });

    // Auto-save form data to localStorage (for longer forms)
    $('form[data-autosave]').each(function() {
        const formId = $(this).attr('id') || 'autosave-form';
        const savedData = localStorage.getItem(formId);

        if (savedData) {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(key => {
                $(`[name="${key}"]`).val(data[key]);
            });
        }

        $(this).on('input change', function() {
            const formData = {};
            $(this).serializeArray().forEach(item => {
                formData[item.name] = item.value;
            });
            localStorage.setItem(formId, JSON.stringify(formData));
        });

        $(this).on('submit', function() {
            localStorage.removeItem(formId);
        });
    });

    // Enhanced dropdown behavior
    $('.dropdown-toggle').on('click', function(e) {
        // Close other dropdowns when opening a new one
        $('.dropdown-menu.show').not($(this).next()).removeClass('show');
    });

    // Keyboard navigation for dropdowns
    $(document).on('keydown', '.dropdown-menu', function(e) {
        const items = $(this).find('.dropdown-item:visible');
        const current = items.filter(':focus');
        let next;

        switch(e.keyCode) {
            case 38: // Up arrow
                e.preventDefault();
                next = current.length ? items.eq(items.index(current) - 1) : items.last();
                break;
            case 40: // Down arrow
                e.preventDefault();
                next = current.length ? items.eq(items.index(current) + 1) : items.first();
                break;
            case 27: // Escape
                $(this).prev('.dropdown-toggle').focus();
                $(this).removeClass('show');
                break;
        }

        if (next && next.length) {
            next.focus();
        }
    });

    // Loading states for AJAX requests
    $(document).ajaxStart(function() {
        $('#spinner').addClass('show');
    }).ajaxStop(function() {
        $('#spinner').removeClass('show');
    });

    // Confirmation dialogs for destructive actions
    $('[data-confirm]').on('click', function(e) {
        const message = $(this).data('confirm') || 'Are you sure you want to perform this action?';
        if (!confirm(message)) {
            e.preventDefault();
            return false;
        }
    });

    // Auto-refresh notifications every 30 seconds
    setInterval(function() {
        // This would typically make an AJAX call to fetch new notifications
        updateNotificationBadge();
    }, 30000);


    // Progress Bar
    $('.pg-bar').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, {offset: '80%'});


    // Calender
    $('#calender').datetimepicker({
        inline: true,
        format: 'L'
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        items: 1,
        dots: true,
        loop: true,
        nav : false
    });


    // Worldwide Sales Chart
    var ctx1 = $("#worldwide-sales").get(0).getContext("2d");
    var myChart1 = new Chart(ctx1, {
        type: "bar",
        data: {
            labels: ["2016", "2017", "2018", "2019", "2020", "2021", "2022"],
            datasets: [{
                    label: "USA",
                    data: [15, 30, 55, 65, 60, 80, 95],
                    backgroundColor: "rgba(0, 156, 255, .7)"
                },
                {
                    label: "UK",
                    data: [8, 35, 40, 60, 70, 55, 75],
                    backgroundColor: "rgba(0, 156, 255, .5)"
                },
                {
                    label: "AU",
                    data: [12, 25, 45, 55, 65, 70, 60],
                    backgroundColor: "rgba(0, 156, 255, .3)"
                }
            ]
            },
        options: {
            responsive: true
        }
    });


    // Salse & Revenue Chart
    var ctx2 = $("#salse-revenue").get(0).getContext("2d");
    var myChart2 = new Chart(ctx2, {
        type: "line",
        data: {
            labels: ["2016", "2017", "2018", "2019", "2020", "2021", "2022"],
            datasets: [{
                    label: "Salse",
                    data: [15, 30, 55, 45, 70, 65, 85],
                    backgroundColor: "rgba(0, 156, 255, .5)",
                    fill: true
                },
                {
                    label: "Revenue",
                    data: [99, 135, 170, 130, 190, 180, 270],
                    backgroundColor: "rgba(0, 156, 255, .3)",
                    fill: true
                }
            ]
            },
        options: {
            responsive: true
        }
    });
    


    // Single Line Chart
    var ctx3 = $("#line-chart").get(0).getContext("2d");
    var myChart3 = new Chart(ctx3, {
        type: "line",
        data: {
            labels: [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150],
            datasets: [{
                label: "Salse",
                fill: false,
                backgroundColor: "rgba(0, 156, 255, .3)",
                data: [7, 8, 8, 9, 9, 9, 10, 11, 14, 14, 15]
            }]
        },
        options: {
            responsive: true
        }
    });


    // Single Bar Chart
    var ctx4 = $("#bar-chart").get(0).getContext("2d");
    var myChart4 = new Chart(ctx4, {
        type: "bar",
        data: {
            labels: ["Italy", "France", "Spain", "USA", "Argentina"],
            datasets: [{
                backgroundColor: [
                    "rgba(0, 156, 255, .7)",
                    "rgba(0, 156, 255, .6)",
                    "rgba(0, 156, 255, .5)",
                    "rgba(0, 156, 255, .4)",
                    "rgba(0, 156, 255, .3)"
                ],
                data: [55, 49, 44, 24, 15]
            }]
        },
        options: {
            responsive: true
        }
    });


    // Pie Chart
    var ctx5 = $("#pie-chart").get(0).getContext("2d");
    var myChart5 = new Chart(ctx5, {
        type: "pie",
        data: {
            labels: ["Italy", "France", "Spain", "USA", "Argentina"],
            datasets: [{
                backgroundColor: [
                    "rgba(0, 156, 255, .7)",
                    "rgba(0, 156, 255, .6)",
                    "rgba(0, 156, 255, .5)",
                    "rgba(0, 156, 255, .4)",
                    "rgba(0, 156, 255, .3)"
                ],
                data: [55, 49, 44, 24, 15]
            }]
        },
        options: {
            responsive: true
        }
    });


    // Doughnut Chart
    var ctx6 = $("#doughnut-chart").get(0).getContext("2d");
    var myChart6 = new Chart(ctx6, {
        type: "doughnut",
        data: {
            labels: ["Italy", "France", "Spain", "USA", "Argentina"],
            datasets: [{
                backgroundColor: [
                    "rgba(0, 156, 255, .7)",
                    "rgba(0, 156, 255, .6)",
                    "rgba(0, 156, 255, .5)",
                    "rgba(0, 156, 255, .4)",
                    "rgba(0, 156, 255, .3)"
                ],
                data: [55, 49, 44, 24, 15]
            }]
        },
        options: {
            responsive: true
        }
    });

    
})(jQuery);

