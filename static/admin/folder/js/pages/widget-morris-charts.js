//[widget morris charts Javascript]

//Project:	Fab Admin - Responsive Admin Template
//Primary use:   Used only for the morris charts


$(function () {
    "use strict";

    // AREA CHART
    var area = new Morris.Area({
      element: 'revenue-chart',
      resize: true,
      data: [
        { y: '2017-01', a: 5,  b: 4 },
		{ y: '2017-02', a: 2,  b: 3 },
		{ y: '2017-03', a: 8,  b: 7 },
		{ y: '2017-04', a: 1,  b: 5 },
		{ y: '2017-05', a: 5,  b: 2 },
		{ y: '2017-06', a: 1,  b: 3 },
		{ y: '2017-07', a: 5,  b: 2 }
      ],
		xkey: 'y',
		ykeys: ['a', 'b'],
		labels: ['Individual Score', 'Team Score'],
		fillOpacity: 0.5,
		lineWidth:1,
		lineColors: ['#7460ee', '#ffb22b'],
		hideHover: 'auto'
    });

    // LINE CHART
    var line = new Morris.Line({
      element: 'line-chart',
      resize: true,
      data: [
        {y: '2007', item1: 9870},
        {y: '2008', item1: 1234},
        {y: '2009', item1: 6548},
        {y: '2010', item1: 8459},
        {y: '2011', item1: 9518},
        {y: '2012', item1: 2154},
        {y: '2013', item1: 1254},
        {y: '2014', item1: 1254},
        {y: '2015', item1: 6258},
        {y: '2016', item1: 9521}
      ],
		xkey: 'y',
		ykeys: ['item1'],
		labels: ['Analatics'],
		lineWidth:2,
		pointFillColors: ['rgba(30,136,229,1)'],
		lineColors: ['rgba(30,136,229,1)'],
		hideHover: 'auto',
    });

    //DONUT CHART
    var donut = new Morris.Donut({
      element: 'sales-chart',
      resize: true,
      colors: ["#745af2", "#fc4b6c", "#06d79c"],
      data: [
        {label: "Download Sales", value: 50},
        {label: "In-Store Sales", value: 35},
        {label: "Mail-Order Sales", value: 15}
      ],
      hideHover: 'auto'
    });
    //BAR CHART
    var bar = new Morris.Bar({
      element: 'bar-chart',
      resize: true,
      data: [
        {y: 'Mon', a: 4, b: 5, c: 6},
        {y: 'Tue', a: 1, b: 2, c: 3},
        {y: 'Wed', a: 7, b: 5, c: 3},
        {y: 'Thu', a: 1, b: 2, c: 5},
        {y: 'Fri', a: 9, b: 5, c: 9},
        {y: 'Sat', a: 10, b: 5, c: 6},
		{y: 'Sun', a: 5, b: 3, c: 7}
      ],
		barColors: ['#745af2', '#fc4b6c', '#06d79c'],
		barSizeRatio: 0.5,
		barGap:5,
		xkey: 'y',
		ykeys: ['a', 'b', 'c'],
		labels: ['Morning', 'Evening', 'Night'],
		hideHover: 'auto'
    });
  });