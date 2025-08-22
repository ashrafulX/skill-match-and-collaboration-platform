$(document).ready(function () {
    $(".ajaxLoader").hide();

    // Job Filter Start
    $(".filter-checkbox").on("click", function () {
        var _filterObj = {};

        $(".filter-checkbox").each(function () {
            var _filterKey = $(this).data("filter");
            _filterObj[_filterKey] = Array.from(
                document.querySelectorAll("input[data-filter=" + _filterKey + "]:checked")
            ).map(function (el) {
                return el.value;
            });
        });

        // Run Ajax
        $.ajax({
            url: "/filter-jobs",
            data: _filterObj,
            dataType: "json",
            beforeSend: function () {
                $(".ajaxLoader").show();
            },
            success: function (res) {
                $("#filteredJobs").html(res.data);
                $(".ajaxLoader").hide();
            },
        });
    });
});
