document.addEventListener("DOMContentLoaded", function () {
  new Sortable(document.getElementById("sortable"), {
    animation: 150,
    handle: ".sortable-handle",
    onUpdate: event => {
      const parent = event.srcElement;
      const children = parent.children;
      const ids = Array.from(children).map(child => child.dataset.orderId);

      const form = document.getElementById("form-order");
      const input = document.getElementById("form-order-input");
      input.value = ids.join(",");
      form.submit();
    },
  });
})
