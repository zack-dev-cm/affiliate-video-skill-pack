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

## Direct Checkout

Direct checkout is enabled by creating `site/checkout-config.json` during deployment:

```json
{
  "pro_pack_checkout_url": "https://provider.example/checkout/pro-pack",
  "setup_review_checkout_url": "https://provider.example/checkout/setup-review",
  "managed_launch_checkout_url": "https://provider.example/checkout/managed-launch",
  "provider": "stripe_or_gumroad_or_lemonsqueezy_or_polar"
}
```

Do not commit secrets. Use hosted checkout URLs only.

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
- `dist/affiliate-video-pro-pack.zip`
