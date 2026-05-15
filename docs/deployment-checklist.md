# Deployment Checklist

## Static Page

Local smoke test:

```bash
python3 -m http.server 8787 --directory site
```

Deploy to Cloudflare Pages:

```bash
python3 scripts/deploy_cloudflare_pages.py \
  --project-name affiliate-video-skill-pack \
  --custom-domain affiliate-video.getgeofix.xyz
```

The script uses `npx -y wrangler` and `CLOUDFLARE_API_TOKEN`. If more than one Cloudflare account is available, set `CLOUDFLARE_ACCOUNT_ID`.

## NOWPayments Checkout

Checkout is enabled through Cloudflare Pages Functions and NOWPayments hosted invoices:

```bash
npx -y wrangler pages secret put NOWPAYMENTS_API_KEY \
  --project-name affiliate-video-skill-pack

npx -y wrangler pages secret put NOWPAYMENTS_IPN_SECRET \
  --project-name affiliate-video-skill-pack
```

Do not commit API keys or IPN secrets. The invoice function sends `price_currency=usd` and omits
`pay_currency`, so the buyer chooses from the payment rails available in the NOWPayments hosted invoice.

Expected routes after deployment:

- `/api/nowpayments/offers`
- `/api/nowpayments/create-invoice`
- `/api/nowpayments/ipn`
- `/checkout.html`
- `/examples.html`
- `/success.html`
- `/cancel.html`

Fiat card or bank options are controlled by NOWPayments account settings, buyer location, provider support,
invoice amount, and KYB/KYC requirements. If fiat is not visible inside the hosted invoice, finish the
NOWPayments fiat-on-ramp provider activation in the dashboard.

## Hosted URL Override

The checkout page still supports an optional `site/checkout-config.json` override during deployment:

```json
{
  "setup_review_checkout_url": "https://provider.example/checkout/setup-review",
  "managed_launch_checkout_url": "https://provider.example/checkout/managed-launch",
  "provider": "stripe_or_gumroad_or_lemonsqueezy_or_polar"
}
```

Do not commit secrets. Use hosted checkout URLs only. When an override URL is present, it takes priority over
the local NOWPayments invoice function for that offer.

## Domain

Preferred custom domain:

```text
affiliate-video.getgeofix.xyz
```

Avoid taking over the root `getgeofix.xyz` because other product pages already use subdomains on that zone.

If Cloudflare reports the custom domain as created but the host does not resolve, add this DNS record in the DNS provider that controls `getgeofix.xyz`:

```text
Type: CNAME
Host: affiliate-video
Value: affiliate-video-skill-pack.pages.dev
Proxy: enabled if the DNS provider is Cloudflare, otherwise provider default
```

The current Cloudflare account token can create the Pages custom-domain entry, but the `getgeofix.xyz` zone may be managed outside that account.

## Release

Before release:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_monetization_pack.py --out dist/affiliate-video-pro-pack.zip
```

Upload both release assets:

- `dist/affiliate-video-campaign-operator-claude.zip`
- `dist/affiliate-video-pro-pack.zip` (free launch pack)
