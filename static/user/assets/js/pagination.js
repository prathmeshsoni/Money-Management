 $('#pagination-here').bootpag({
            total: 10,
            page: 1,
            maxVisible: 4,
            leaps: true,
            href: "#result-page-{{number}}",
        })
        $('#pagination-here').on("page", function(event, num) {

            $("#content").html("Page " + num);
        });