const productsSlider = document.getElementById("products-slider");
let imgElements = productsSlider.getElementsByTagName("img");
const intervalTime = 3000;
let indexValue = 0;

function slideImages() {
  for (let i = 0; i < imgElements.length; i++) {
    if (i > 2 && i <= 4) {
      let previousOne = i - 3;
      imgElements[previousOne].style.display = "none";
      imgElements[i - 1].style.display = "block";
    }
  }
}
function nextSlide(images, currentIndex) {
  images[currentIndex].style.display = "none";
  currentIndex = (currentIndex + 1) % images.length;
  images[currentIndex].style.display = "block";
  return currentIndex;
}

const phonesImgs = document.querySelectorAll(".phones-div img");
const giftImgs = document.querySelectorAll(".fashion-div img");
const fashionImgs = document.querySelectorAll(".gift-card-div img");

let currentIndex1 = 0;
let currentIndex2 = 0;
let currentIndex3 = 0;
const interval = 3000;

setInterval(function () {
  currentIndex1 = nextSlide(phonesImgs, currentIndex1);
  currentIndex2 = nextSlide(giftImgs, currentIndex2);
  currentIndex3 = nextSlide(fashionImgs, currentIndex3);
}, interval);
