const slideCache = new Map();
const backgroundCache = new Map();

let screenBackground, slideshowBackground, currentBackground;
let currentSlide, currentTimeout, useSecondDiv, s3;

function onWsMessage(data) {
  switch (data.type) {
    case 'init': {
      ws.send(JSON.stringify({ type: "slideshow_done" }));
    }
    case 'update_screen': {
      screenBackground = data.screen.background;
      displayBackground();
      console.log("Updated screen with new info");
      break;
    }
    case 'run_slideshow': {
      s3 = data.s3;
      if (!data.slideshow) {
        slideshowBackground = null;
        displaySlide(false, false);
        displayBackground();
        return setTimeout(() => ws.send(JSON.stringify({ type: "slideshow_done", s3 })), 10000);
      }
    }
    case 'update_slideshow': {
      slideshowBackground = data.slideshow.background;
      slideCache.clear();
      data.slideshow.slides.forEach(slide => slideCache.set(slide.id, slide));
      const slide = slideCache.get(currentSlide);
      displaySlide(slide, true, data.type === "update_slideshow");
      console.log("Updated slideshow with new info");
      break;
    }
  }
}

async function displaySlide(existingSlide, sendIfDone = true, forceNewRender = false) {
  clearTimeout(currentTimeout); // in case we manually skip
  const thisSlide = slideCache.get(currentSlide);
  const allSlides = Array.from(slideCache.values())
  const nextSlide = existingSlide || allSlides[(allSlides.indexOf(thisSlide) + 1)]

  const
    slide1 = document.getElementById('slide1'),
    slide2 = document.getElementById('slide2');

  if (!nextSlide) {
    if (existingSlide === false) {
      slide1.classList.add("hidden");
      slide2.classList.add("hidden");
      currentSlide = null;
      displayBackground();
    }
    if (sendIfDone) ws.send(JSON.stringify({ type: "slideshow_done", s3 }));
    return;
  }

  if (nextSlide.id !== currentSlide || forceNewRender) {
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
  let backgroundName = nextSlide?.background || slideshowBackground || screenBackground;
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
