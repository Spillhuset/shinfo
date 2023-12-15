document.addEventListener("DOMContentLoaded", resizeWindow);
window.addEventListener("resize", resizeWindow);

function resizeWindow() {
  document.body.style.zoom = window.innerWidth / 1920;
}
