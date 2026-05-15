# Deployment Status 2026-05-15

## Cloudflare Pages

Project:

```text
affiliate-video-skill-pack
```

Live Pages URL:

```text
https://affiliate-video-skill-pack.pages.dev
```

Latest deployment preview observed:

```text
https://ad987e57.affiliate-video-skill-pack.pages.dev
```

Verified routes:

- `/`
- `/checkout`
- `/success`
- `/cancel`
- `/api/nowpayments/offers`
- `/api/nowpayments/create-invoice`
- `/api/nowpayments/ipn`
- `/terms`
- `/refund`
- `/styles.css`
- `/checkout.js`
- `/sitemap.xml`

## Custom Domain

Requested domain:

```text
affiliate-video.getgeofix.xyz
```

Cloudflare Pages custom-domain API result:

```text
created/already exists, status pending or initializing
```

DNS status during verification:

```text
affiliate-video.getgeofix.xyz CNAME affiliate-video-skill-pack.pages.dev
```

Required DNS record if the zone is managed outside the active Cloudflare account:

```text
Type: CNAME
Host: affiliate-video
Value: affiliate-video-skill-pack.pages.dev
```

## Checkout

Direct payment is connected through Cloudflare Pages Functions and NOWPayments hosted invoices.

Live smoke checks:

- `GET https://affiliate-video.getgeofix.xyz/api/nowpayments/offers` returned the three USD-priced offers.
- `POST https://affiliate-video.getgeofix.xyz/api/nowpayments/create-invoice` for `pro-pack` returned a NOWPayments hosted invoice URL.
- `POST https://affiliate-video.getgeofix.xyz/api/nowpayments/ipn` with a signed smoke-test payload returned `{"ok":true}`.

The API key and IPN secret are stored as Cloudflare Pages production secrets, not committed to the repo.
