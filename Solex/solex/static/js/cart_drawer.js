function cartDrawer() {
  return {
    lines: [],
    subtotal_cents: 0,
    async refresh() {
      const r = await fetch("/cart.json", { credentials: "same-origin" });
      const d = await r.json();
      this.lines = d.lines;
      this.subtotal_cents = d.subtotal_cents;
      document.querySelectorAll("#cart-count").forEach(
        el => el.textContent = d.lines.reduce((n,l)=>n+l.qty,0)
      );
    },
  };
}
window.cartDrawer = cartDrawer;

document.addEventListener("submit", async (e) => {
  const form = e.target;
  if (!form.matches("form.js-cart-form")) return;
  e.preventDefault();
  const r = await fetch(form.action, {
    method: "POST",
    body: new FormData(form),
    credentials: "same-origin",
  });
  if (r.ok) {
    window.dispatchEvent(new CustomEvent("cart-updated"));
    window.dispatchEvent(new CustomEvent("open-cart"));
  }
});
