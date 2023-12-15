document.addEventListener("DOMContentLoaded", async function () {
  const main = document.getElementById("background-goes-in-here");
  const url = new URL(window.location.href);
  url.searchParams.delete("preview");
  const background = await fetch(url.toString(), { headers: { "X-Preview": "true" } }).then(response => response.text());
  main.innerHTML = background;
});
