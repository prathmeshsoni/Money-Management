function getchart() {
    var data = $('#chart_form').serializeArray()[0]['value'];
    var type = $('input[name="type_date"]:checked').val();


    if (type == 'year'){
        if (data.split('-')[0])
            window.location.href = '/chart/' + data.split('-')[0] + '/';
    }
    else {
        if (data)
            window.location.href = '/chart/' + data + '/';
    }
}

function chart_shows(names, values) {
    let tem = []
    for (var i = 0; i < names.length; i++) {
        tem.push(names[i]);
    }
    var ctx6 = document.getElementById("chart_6").getContext("2d");
    if (window.chart6) {
        window.chart6.destroy();
    }
    var data6 = {
        labels: tem,
        datasets: [
            {
                data: values,
                backgroundColor: [
                    "#006400",
                    "#00008B",
                    "#FFD700",
                    "#8B0000",
                    "#000080",
                    "#808000",
                    "#2F4F4F",
                    "#800000",
                    "#008080"
                ],
                hoverBackgroundColor: [
                    "#006400",
                    "#00008B",
                    "#FFD700",
                    "#8B0000",
                    "#000080",
                    "#808000",
                    "#2F4F4F",
                    "#800000",
                    "#008080"
                ],
            },
        ],
    };

    var options = {
        animation: {
            duration: 3000,
        },
        responsive: true,
        legend: {
            labels: {
                fontFamily: "Poppins",
                fontColor: "#878787",
            },
        },
        plugins: {
            datalabels: {
                display: true,
                color: "#fff",
                anchor: "end",
                align: "start",
                offset: 8,
                formatter: (value, ctx) => {
                    let sum = 0;
                    let dataArr = ctx.dataset.data;
                    dataArr.map((data) => {
                        sum += data;
                    });
                    let percentage = ((value * 100) / sum).toFixed(2) + "%";
                    return percentage;
                },
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        const label = data6.labels[context.dataIndex];
                        const value = data6.datasets[0].data[context.dataIndex];
                        const dataset = data6.datasets[0];
                        const sum = dataset.data.reduce((acc, val) => acc + val, 0);
                        const percentage = ((value * 100) / sum).toFixed(2) + "%";
                        return `${label}: ₹ ${value} (${percentage})`;
                    },
                },
            },
        },
        elements: {
            arc: {
                borderWidth: 2,
            },
        },
        onClick: function (event, activeElements) {
            if (activeElements.length > 0) {
                var activeIndex = activeElements[0].index;

                // Retrieve data for the clicked segment
                var clickedLabel = data6.labels[activeIndex];
                // window.location.href = "/view/category/" + clickedLabel + "/";
                swal({
                    title: "Go To " + clickedLabel + " Page ? ",
                    text: '',
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "Yes, Redirect Pls",
                    cancelButtonText: "No",
                    closeOnConfirm: false,
                    closeOnCancel: true
                }, function (isConfirm) {
                    if (isConfirm) {

                        swal("Redirect In 2 Second");
                        $.toast({
                            heading: 'Redirect',
                            text: 'Redirecting......',
                            position: 'top-right',
                            loaderBg: '#fc4b6c !important',
                            icon: 'success',
                            hideAfter: 2000
                        });
                        setTimeout(() => {
                            window.location.href = "/view/category/" + clickedLabel + "/";
                        }, 2000);
                    }
                });
                // var clickedValue = data6.datasets[0].data[activeIndex];
                //
                // // Show the popup with the clicked segment information
                // var popup = document.getElementById("popup");
                // var popupTitle = document.getElementById("popup-title");
                // var popupLabel = document.getElementById("popup-label");
                // var popupValue = document.getElementById("popup-value");
                //
                // popupLabel.textContent = "Label: " + clickedLabel;
                // popupValue.textContent = "Value: " + clickedValue;
                //
                // popup.style.display = "block";
                // popup.style.left = event.pageX + "px";
                // popup.style.top = event.pageY + "px";
            }
        }
// cutoutPercentage: 10,
    };

    var pieChart = new Chart(ctx6, {
        type: "pie",
        data: data6,
        options: options,
    });
}

function chart_shows_1(names, values) {
    var ctx6 = document.getElementById("chart_7").getContext("2d");
    let tem = []
    for (var i = 0; i < names.length; i++) {
        tem.push(names[i]);
    }

    var data6 = {
        labels: tem,
        datasets: [
            {
                data: values,
                backgroundColor: colors = [
                    "#8B0000",
                    "#006400",
                    "#00008B",
                    "#FFD700",
                    "#000080",
                    "#808000",
                    "#2F4F4F",
                    "#800000",
                    "#008080"
                ],
                hoverBackgroundColor: [
                    "#8B0000",
                    "#006400",
                    "#00008B",
                    "#FFD700",
                    "#000080",
                    "#808000",
                    "#2F4F4F",
                    "#800000",
                    "#008080"
                ],
            },
        ],
    };

    var options = {
        animation: {
            duration: 3000,
        },
        responsive: true,
        legend: {
            labels: {
                fontFamily: "Poppins",
                fontColor: "#878787",
            },
        },
        plugins: {
            datalabels: {
                display: true,
                color: "#fff",
                anchor: "end",
                align: "start",
                offset: 8,
                formatter: (value, ctx) => {
                    let sum = 0;
                    let dataArr = ctx.dataset.data;
                    dataArr.map((data) => {
                        sum += data;
                    });
                    let percentage = ((value * 100) / sum).toFixed(2) + "%";
                    return percentage;
                },
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        const label = data6.labels[context.dataIndex];
                        const value = data6.datasets[0].data[context.dataIndex];
                        const dataset = data6.datasets[0];
                        const sum = dataset.data.reduce((acc, val) => acc + val, 0);
                        const percentage = ((value * 100) / sum).toFixed(2) + "%";
                        return `${label}: ₹ ${value} (${percentage})`;
                    },
                },
            },
        },
        elements: {
            arc: {
                borderWidth: 2,
            },
        },
        onClick: function (event, activeElements) {
            if (activeElements.length > 0) {
                var activeIndex = activeElements[0].index;

                // Retrieve data for the clicked segment
                var clickedLabel = data6.labels[activeIndex];
                // window.location.href = "/view/category/" + clickedLabel + "/";
                swal({
                    title: "Go To " + clickedLabel + " Page ? ",
                    text: '',
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "Yes, Redirect Pls",
                    cancelButtonText: "No",
                    closeOnConfirm: false,
                    closeOnCancel: true
                }, function (isConfirm) {
                    if (isConfirm) {

                        swal("Redirect In 2 Second");
                        $.toast({
                            heading: 'Redirect',
                            text: 'Redirecting......',
                            position: 'top-right',
                            loaderBg: '#fc4b6c !important',
                            icon: 'success',
                            hideAfter: 2000
                        });
                        setTimeout(() => {
                            window.location.href = "/view/category/" + clickedLabel + "/";
                        }, 2000);
                    }
                });
                // var clickedValue = data6.datasets[0].data[activeIndex];
                //
                // // Show the popup with the clicked segment information
                // var popup = document.getElementById("popup");
                // var popupTitle = document.getElementById("popup-title");
                // var popupLabel = document.getElementById("popup-label");
                // var popupValue = document.getElementById("popup-value");
                //
                // popupLabel.textContent = "Label: " + clickedLabel;
                // popupValue.textContent = "Value: " + clickedValue;
                //
                // popup.style.display = "block";
                // popup.style.left = event.pageX + "px";
                // popup.style.top = event.pageY + "px";
            }
        }
    };

    var pieChart = new Chart(ctx6, {
        type: "pie",
        data: data6,
        options: options,
    });

}