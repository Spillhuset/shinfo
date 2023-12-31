const slideCache = new Map();
const backgroundCache = new Map();

let slideshowBackground, currentBackground;
let currentSlide, currentTimeout, useSecondDiv;

function onWsMessage(data) {
  switch (data.type) {
    case 'init':
    case 'update_slideshow': {
      slideshowBackground = data.slideshow.background;
      slideCache.clear();
      data.slideshow.slides.forEach(slide => slideCache.set(slide.id, slide));
      const slide = slideCache.get(currentSlide);
      displaySlide(slide)
      console.log("Updated slideshow with new info");
      break;
    }
  }
}

async function displaySlide(existingSlide) {
  clearTimeout(currentTimeout); // in case we manually skip
  const thisSlide = slideCache.get(currentSlide);
  const allSlides = Array.from(slideCache.values())
  const nextSlide = existingSlide || allSlides[(allSlides.indexOf(thisSlide) + 1) % allSlides.length ?? 0]

  const
    slide1 = document.getElementById('slide1'),
    slide2 = document.getElementById('slide2');

  if (!nextSlide) {
    if (!slide1.classList.contains("hidden")) slide1.classList.add("hidden");
    if (!slide2.classList.contains("hidden")) slide2.classList.add("hidden");
    displayBackground();
    return console.log("No slide is set up for this slideshow, waiting for next update through WS");
  }

  if (nextSlide.id !== currentSlide || existingSlide) {
    currentSlide = nextSlide?.id;
    const slide = useSecondDiv ? slide1 : slide2;
    slide.innerHTML = nextSlide.html;
    slide.classList.remove("hidden")
    useSecondDiv = !useSecondDiv;

    const slideToHide = useSecondDiv ? slide1 : slide2;
    slideToHide.classList.add("hidden");
    console.log("Switched to slide", nextSlide.id, "with duration", nextSlide.duration, "seconds");
  } else console.log("Waiting another", nextSlide.duration, "seconds since there's no other next slide");

  displayBackground(nextSlide);
  currentTimeout = setTimeout(displaySlide, nextSlide.duration * 1000);
}

async function displayBackground(nextSlide) {
  let backgroundName = nextSlide?.background || slideshowBackground || "empty";
  if (backgroundName === "null") backgroundName = "empty";
  if (currentBackground !== backgroundName) {
    currentBackground = backgroundName;
    let background = backgroundCache.get(backgroundName);
    if (!background) {
      backgroundCache.set(backgroundName, await fetch(`/viewer/backgrounds/${backgroundName}?raw=true`).then(response => response.text()));
      background = backgroundCache.get(backgroundName);
    }
    const backgroundDiv = document.getElementById("background");
    if (backgroundDiv.innerHTML !== background) backgroundDiv.innerHTML = background;
  }
}
