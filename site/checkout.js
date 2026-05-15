(async function () {
  const fallbackLinks = {
    setup_review_checkout_url:
      "https://github.com/zack-dev-cm/affiliate-video-skill-pack/issues/new?title=Setup%20review%20request",
    managed_launch_checkout_url:
      "https://github.com/zack-dev-cm/affiliate-video-skill-pack/issues/new?title=Managed%20launch%20request",
  };

  const buttonOffers = {
    "setup-review-checkout": "setup-review",
    "managed-launch-checkout": "managed-launch",
  };

  function usableUrl(value) {
    return typeof value === "string" && /^https:\/\/.+/.test(value) && !value.includes("REPLACE_WITH");
  }

  function setCheckout(id, url, fallback) {
    const node = document.getElementById(id);
    if (!node) return false;
    const target = usableUrl(url) ? url : fallback;
    node.setAttribute("href", target);
    node.dataset.configured = usableUrl(url) ? "true" : "false";
    node.dataset.offer = buttonOffers[id] || "";
    return usableUrl(url);
  }

  function setStatus(message, tone) {
    const status = document.getElementById("checkout-status");
    if (!status) return;
    status.textContent = message;
    status.dataset.tone = tone || "neutral";
  }

  async function createInvoice(offer) {
    const response = await fetch("/api/nowpayments/create-invoice", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ offer }),
    });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok || !usableUrl(payload.invoice_url)) {
      const detail = typeof payload.message === "string" ? ` ${payload.message}` : "";
      throw new Error(`Could not create NOWPayments invoice.${detail}`);
    }
    return payload.invoice_url;
  }

  function attachInvoiceCheckout(configured) {
    Object.keys(buttonOffers).forEach((id) => {
      const node = document.getElementById(id);
      if (!node || node.dataset.configured === "true") return;
      node.addEventListener("click", async (event) => {
        event.preventDefault();
        if (node.dataset.loading === "true") return;
        node.dataset.loading = "true";
        node.setAttribute("aria-busy", "true");
        const previousText = node.textContent;
        node.textContent = "Creating invoice...";
        setStatus("Creating a secure NOWPayments invoice. Prices are set in USD.", "neutral");
        try {
          const invoiceUrl = await createInvoice(buttonOffers[id]);
          window.location.assign(invoiceUrl);
        } catch (error) {
          setStatus(`${error.message} Use the support link if retrying does not work.`, "error");
          node.dataset.loading = "false";
          node.setAttribute("aria-busy", "false");
          node.textContent = previousText;
        }
      });
    });

    setStatus(
      configured
        ? "Checkout uses configured hosted links from checkout-config.json."
        : "NOWPayments invoice checkout is enabled for setup services. Prices are set in USD; buyers choose supported crypto or fiat rails on the hosted invoice.",
      "success",
    );
  }

  let config = {};
  try {
    const response = await fetch("/checkout-config.json", { cache: "no-store" });
    if (response.ok) {
      config = await response.json();
    }
  } catch (error) {
    config = {};
  }

  const configured = [
    setCheckout("setup-review-checkout", config.setup_review_checkout_url, fallbackLinks.setup_review_checkout_url),
    setCheckout("managed-launch-checkout", config.managed_launch_checkout_url, fallbackLinks.managed_launch_checkout_url),
  ].some(Boolean);

  attachInvoiceCheckout(configured);
})();
