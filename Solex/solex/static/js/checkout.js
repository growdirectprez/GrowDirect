// checkout.js — Square Web Payments SDK integration
"use strict";

async function initCheckout() {
  const form = document.getElementById("checkout-form");
  if (!form) return;

  const appId = form.dataset.appId;
  const locationId = form.dataset.locationId;
  const hasSubscription = form.dataset.hasSubscription === "true";
  const errDiv = document.getElementById("checkout-error");
  const storeCardSection = document.getElementById("store-card-section");

  if (!appId) {
    errDiv.textContent =
      "Square sandbox credentials not configured. Set SQUARE_SANDBOX_APPLICATION_ID in .env.";
    return;
  }

  if (typeof Square === "undefined") {
    errDiv.textContent = "Payment provider failed to load. Please refresh the page.";
    return;
  }

  let payments;
  try {
    payments = Square.payments(appId, locationId);
  } catch (e) {
    errDiv.textContent = "Could not initialise payment form: " + e.message;
    return;
  }

  // Payment card (always)
  let card;
  try {
    card = await payments.card();
    await card.attach("#card-container");
  } catch (e) {
    errDiv.textContent = "Could not load card input: " + e.message;
    return;
  }

  // Store card (subscription only)
  let storeCard = null;
  if (hasSubscription && storeCardSection) {
    storeCardSection.classList.remove("hidden");
    try {
      storeCard = await payments.card();
      await storeCard.attach("#store-card-container");
    } catch (e) {
      errDiv.textContent = "Could not load subscription card input: " + e.message;
      return;
    }
  }

  const payButton = document.getElementById("pay-button");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errDiv.textContent = "";
    payButton.disabled = true;
    payButton.textContent = "Processing\u2026";

    // Tokenize the payment card
    let tokenResult;
    try {
      tokenResult = await card.tokenize();
    } catch (e) {
      errDiv.textContent = "Card tokenization error: " + e.message;
      payButton.disabled = false;
      payButton.textContent = payButton.dataset.label || "Pay";
      return;
    }

    if (tokenResult.status !== "OK") {
      errDiv.textContent =
        tokenResult.errors?.[0]?.message || "Card tokenization failed.";
      payButton.disabled = false;
      payButton.textContent = payButton.dataset.label || "Pay";
      return;
    }

    // Tokenize the store card if present
    let storeTokenResult = null;
    if (storeCard) {
      try {
        storeTokenResult = await storeCard.tokenize();
      } catch (e) {
        errDiv.textContent = "Subscription card tokenization error: " + e.message;
        payButton.disabled = false;
        payButton.textContent = payButton.dataset.label || "Pay";
        return;
      }
      if (storeTokenResult.status !== "OK") {
        errDiv.textContent =
          storeTokenResult.errors?.[0]?.message || "Subscription card tokenization failed.";
        payButton.disabled = false;
        payButton.textContent = payButton.dataset.label || "Pay";
        return;
      }
    }

    const fd = new FormData(form);
    const fullName = (fd.get("name") || "").trim();
    const nameParts = fullName.split(/\s+/);
    const firstName = nameParts[0] || "";
    const lastName = nameParts.slice(1).join(" ") || "";

    const body = {
      email: fd.get("email"),
      name: fullName,
      payment_token: tokenResult.token,
      shipping_address: {
        first_name: firstName,
        last_name: lastName,
        line1: fd.get("line1"),
        city: fd.get("city"),
        region: fd.get("region"),
        postal_code: fd.get("postal_code"),
        country: "US",
      },
    };

    if (storeTokenResult) {
      body.store_payment_token = storeTokenResult.token;
    }

    let resp;
    try {
      resp = await fetch("/checkout/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        credentials: "same-origin",
      });
    } catch (e) {
      errDiv.textContent = "Network error. Please try again.";
      payButton.disabled = false;
      payButton.textContent = payButton.dataset.label || "Pay";
      return;
    }

    if (!resp.ok) {
      let j = {};
      try { j = await resp.json(); } catch (_) {}
      if (j.error === "login_required_for_subscription") {
        errDiv.textContent = "You must be signed in to subscribe. Sign in and try again.";
      } else if (j.error === "store_payment_token_required_for_subscription") {
        errDiv.textContent = "Please enter a card for subscription billing.";
      } else {
        errDiv.textContent = j.detail || j.error || "Checkout failed. Please try again.";
      }
      payButton.disabled = false;
      payButton.textContent = payButton.dataset.label || "Pay";
      return;
    }

    const data = await resp.json();
    const { order_token, subscription_next_charge } = data;
    let redirect = "/order/" + order_token;
    if (subscription_next_charge) {
      redirect += "?sub_next=" + encodeURIComponent(subscription_next_charge);
    }
    window.location.href = redirect;
  });
}

document.addEventListener("DOMContentLoaded", initCheckout);
