# masarmaps.com — GitHub Pages connection

Planned account and repository: `alsaadii98/masar-website`.

Read the current provider zone before applying these targets.

## Website targets

| Type | Name | Target |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | alsaadii98.github.io |

Optional IPv6 targets, if IPv6 is configured:

| Type | Name | Target |
|---|---|---|
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |

Use the provider's supported TTL, preferably 300 seconds for the initial change. Website A, AAAA, or ALIAS records pointing to a previous web host must be reconciled with these targets. Keep the existing nameservers and DNS provider.

## Preserve Hostinger email

1. Read and retain the entire current DNS zone and the available rollback snapshot before applying changes.
2. Identify the active MX, SPF, DKIM, DMARC, autodiscover, autoconfig, mail, and other email-service records from that zone.
3. Preserve those records exactly, including values, priorities, and TTLs. Preserve unrelated verification and service records as well.
4. Change only the website records for `@` and `www`. An apex CNAME is unsuitable where the domain has MX and TXT records; use the A records above.
5. Inspect existing CAA records. If certificate issuance is restricted, verify that GitHub's certificate issuer is permitted while retaining the existing authorizations.
6. After applying the website changes, compare the full zone against the saved state and confirm that the email records still match. Check the resulting public MX and TXT records as well.

Do not reset the DNS zone or change nameservers to connect this website. The GitHub Actions workflow deploys static files and does not modify Hostinger email or DNS.

## Initial deployment order

1. Create the repository and upload the prepared source.
2. Enable Pages with GitHub Actions as its publishing source.
3. Set `masarmaps.com` as the Pages custom domain.
4. Apply the website DNS records at the current authoritative DNS provider.
5. Confirm the Actions run succeeds, the domain's DNS check passes, and HTTPS becomes available.
6. Enable HTTPS enforcement and check both `https://masarmaps.com` and `https://www.masarmaps.com`.
7. Verify the email DNS against the saved zone.

## References

- GitHub custom domains: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- GitHub Pages workflows: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
