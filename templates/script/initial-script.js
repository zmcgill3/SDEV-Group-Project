var images = document.querySelectorAll('.carousel-slider img');
var dots = document.querySelectorAll('.dot');
var currentImg = 0; //index of first image
const interval = 3000; // speed of slides

function changeSlide(n) {
    // function to change the image using the dots
    for (var i=0; i < images.length; i++) {
        images[i].style.opacity = 0;
        dots[i].className = dots[i].className.replace('.active', '');
    }

    currentImg = (currentImg + 1) % images.length; // update the index number
    if (n != undefined) {
        clearInterval(timer);
        timer = setInterval(changeSlide, interval);
        currentImg = n;
    }
    images[currentImg].style.opacity = 1;
    dots[currentImg].className += '.active'; // set image as front image
}

// make slides change automatically
var timer = setInterval(changeSlide, interval)