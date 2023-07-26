window.onload = function(){
    let themeslider   = document.querySelector('.home-slide'),
        elemOne   = document.querySelector('#img-1'),
        elemTwo   = document.querySelector('#img-2'),
        elemThree   = document.querySelector('#img-3'),
        elemFour   = document.querySelector('#img-4'),
        elemFive   = document.querySelector('#img-5'),
        elemSix   = document.querySelector('#img-6');
        elemSeven   = document.querySelector('#img-7'),
        elemEight   = document.querySelector('#img-8'),
        elemNine   = document.querySelector('#img-9');

    themeslider.addEventListener('mousemove',function(e){
        var pageX = e.clientX - window.innerWidth/1,
            pageY = e.clientY - window.innerHeight/1;
        elemOne.style.transform = 'translateX(' + (7 + pageX/150) + '%) translateY(' + (1 + pageY/150) + '%)';
        elemTwo.style.transform = 'translateX(' + (7 + pageX/150) + '%) translateY(' + (1 + pageY/150) +  '%)';
        elemThree.style.transform = 'translateX(' + (7 + pageX/150) + '%) translateY(' + (1 + pageY/150) +  '%)';
        elemFour.style.transform = 'translateX(' + (7 + pageX/150) + '%) translateY(' + (1 + pageY/150) +  '%)';
        elemFive.style.transform = 'translateX(' + (7 + pageX/150) + '%) translateY(' + (1 + pageY/150) +  '%)';
        elemSix.style.transform = 'translateX(' + (7 + pageX/150) + '%) translateY(' + (1 + pageY/150) +  '%)'
        elemSeven.style.transform = 'translateX(' + (7 + pageX/150) + '%) translateY(' + (1 + pageY/150) +  '%)';
        elemEight.style.transform = 'translateX(' + (7 + pageX/150) + '%) translateY(' + (1 + pageY/150) +  '%)';
        elemNine.style.transform = 'translateX(' + (7 + pageX/150) + '%) translateY(' + (1 + pageY/150) +  '%)';
    });
};