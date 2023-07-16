//[custom Javascript]

//Project:	Fab Admin - Responsive Admin Template
//Primary use:	Fab Admin - Responsive Admin Template

//should be included in all pages. It controls some layout



// Fullscreen
$(function () {
	'use strict'
	// Composite line charts, the second using values supplied via javascript
    		
		$("#linechart").sparkline([3,4,5,6,7,5,8,4,2,8,16], {
			type: 'line',
			width: '100',
			height: '38',
			lineColor: '#06d79c',
			fillColor: '#ffffff',
			lineWidth: 2,
			minSpotColor: '#0fc491',
			maxSpotColor: '#0fc491',
		});
		$("#linechart2").sparkline([3,4,5,6,7,5,8,4,2,8,16], {
			type: 'line',
			width: '100',
			height: '38',
			lineColor: '#1e88e5',
			fillColor: '#e3f3fc',
			lineWidth: 2,
			minSpotColor: '#1e88e5',
			maxSpotColor: '#1e88e5',
		});
	
		$("#barchart").sparkline([3,4,5,6,7,5,8,4,2,8,16], {
			type: 'bar',
			height: '38',
			barWidth: 6,
			barSpacing: 4,
			barColor: '#ffb22b',
		});
		$("#barchart2").sparkline([3,4,5,6,7,5,8,4,2,8,16], {
			type: 'bar',
			height: '38',
			barWidth: 6,
			barSpacing: 4,
			barColor: '#ffb22b',
		});
	
		$("#discretechart").sparkline([3,4,5,6,7,5,8,4,2,8,16], {
			type: 'discrete',
			width: '50',
			height: '38',
			lineColor: '#745af2',
		});
		$("#discretechart2").sparkline([3,4,5,6,7,5,8,4,2,8,16], {
			type: 'discrete',
			width: '50',
			height: '38',
			lineColor: '#745af2',
		});
		
		$("#linearea").sparkline([3,14,5,6,37,5,8,54,2,8,16.15,18,2], {
			type: 'line',
			width: '100%',
			height: '80',
			lineColor: '#06d79c',
			fillColor: '#06d79c',
			lineWidth: 2,
		});
		
		$("#baralc").sparkline([3,14,5,6,37,5,8,54,2,8,16.15,18,2,3,14,5,6,37,5,8,54,2,8,16.15,18,2,3,14,5,6,37,5,8,54,2,8,16.15,18,2], {
			type: 'bar',
			height: '80',
			barWidth: 6,
			barSpacing: 4,
			barColor: '#ffb22b',
		});
		
		$("#lineIncrease").sparkline([3,14,5,6,37,5,8,54,2,8,16.15,18,2], {
			type: 'line',
			width: '100%',
			height: '140',
			lineWidth: 2,
			lineColor: '#ffffff',
			fillColor: "#398bf7",
			spotColor: '#ffffff',
			minSpotColor: '#ffffff',
			maxSpotColor: '#ffffff',
			spotRadius: 3,
		});
		
		$("#lineToday").sparkline([3,14,5,6,37,5,8,54,2,8,16.15,18,2], {
			type: 'line',
			width: '100%',
			height: '70',
			lineColor: '#ffffff',
			fillColor: '#398bf7',
			lineWidth: 2,
			spotRadius: 3,
		});
		
		$("#baranl").sparkline([3,14,5,6,37,5,8,54,2,8,16.15,18,2,3,14,5,6,37,5,8,54,2,8,16.15,18,2], {
			type: 'bar',
			height: '70',
			barColor: '#fc4b6c',
			barWidth: 7,
    		barSpacing: 5,
		});
		
		$("#lineTo").sparkline([0,14,5,6,37,5,8,54,2,8,16.15,18,0], {
			type: 'line',
			width: '100%',
			height: '70',
			lineColor: '#ffffff',
			fillColor: '#398bf7',
			lineWidth: 3,
			spotColor: '#ffffff',
			highlightSpotColor: '#ffffff',
			highlightLineColor: '#ffffff',
			spotRadius: 3,
		});
		
		// donut chart
		$('.donut').peity('donut');
		
		// bar chart
		$(".bar").peity("bar");	
}); // End of use strict
		
// easypie chart
	$(function() {
		'use strict'
		$('.easypie').easyPieChart({
			easing: 'easeOutBounce',
			onStep: function(from, to, percent) {
				$(this.el).find('.percent').text(Math.round(percent));
			}
		});
		var chart = window.chart = $('.easypie').data('easyPieChart');
		$('.js_update').on('click', function() {
			chart.update(Math.random()*200-100);
		});
	});// End of use strict