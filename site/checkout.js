(async function () {
  const fallbackLinks = {
    pro_pack_checkout_url:
      "https://github.com/zack-dev-cm/affiliate-video-skill-pack/issues/new?title=Pro%20Pack%20checkout%20setup",
    setup_review_checkout_url:
      "https://github.com/zack-dev-cm/affiliate-video-skill-pack/issues/new?title=Setup%20review%20request",
    managed_launch_checkout_url:
      "https://github.com/zack-dev-cm/affiliate-video-skill-pack/issues/new?title=Managed%20launch%20request",
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
    return usableUrl(url);
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
    setCheckout("pro-pack-checkout", config.pro_pack_checkout_url, fallbackLinks.pro_pack_checkout_url),
    setCheckout("setup-review-checkout", config.setup_review_checkout_url, fallbackLinks.setup_review_checkout_url),
    setCheckout("managed-launch-checkout", config.managed_launch_checkout_url, fallbackLinks.managed_launch_checkout_url),
  ].some(Boolean);

  const status = document.getElementById("checkout-status");
  if (status) {
    status.textContent = configured
      ? "Checkout links are configured through checkout-config.json."
      : "Checkout is in request mode. Add checkout-config.json with hosted payment URLs to enable direct payment.";
  }
})();
