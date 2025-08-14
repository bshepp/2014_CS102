# DNS and SSL Cutover Checklist (gengine.darkforestlabs.com)

Date: 2025-08-13/14 (PST)

## Frontend: Amplify Custom Domain (LIVE)

- App: geometry-engine-web (`appId: d2vt3koij47dy3`)
- Custom domain: `gengine.darkforestlabs.com`
- Status: LIVE (Amplify-managed cert validated)

Required DNS (Route 53 zone `darkforestlabs.com`):
- A/ALIAS
  - Name: `gengine.darkforestlabs.com`
  - Target: `d3b2k3c25nn81q.cloudfront.net` (Amplify CloudFront)
  - HostedZoneId: `Z2FDTNDATAQYW2`
- CNAME (SSL validation)
  - Name: `_161437339038eca8d8cc4ddd24c9be2f.gengine.darkforestlabs.com`
  - Value: `_e327a56b667d15c84e7894282c7ffee6.xlfgrmvvlj.acm-validations.aws`

Verification steps:
- Amplify Console → Domain management → `gengine.darkforestlabs.com` → Status becomes Connected
- curl `https://gengine.darkforestlabs.com` returns 200 (after propagation)

Notes:
- Do not create a conflicting CNAME at the root host (`gengine.darkforestlabs.com`) if using A/ALIAS. One record set per name.

## MCP API: mcp.gengine.darkforestlabs.com (API Gateway + Lambda)

- ACM cert (us-east-1): `arn:aws:acm:us-east-1:290318879194:certificate/c4fbbc0f-69ba-4064-b6e0-e255aa9883dd`
- Status: Pending validation
- Validation CNAME:
  - Name: `_592c77b7f53c08bd548552b3f3f2c1bd.mcp.gengine.darkforestlabs.com`
  - Value: `_763fcca04bf795e71fa37f82e9a0e2a3.xlfgrmvvlj.acm-validations.aws`

Next after ISSUED:
- Create API Gateway custom domain (REST v1, EDGE), base path map to `geometry-oracle-mcp-api` (id `s6ngc23inj`, stage `prod`)
- Create Route 53 A/ALIAS to the API Gateway distribution domain/zone

## REST API: api.gengine.darkforestlabs.com (Planned)

- Not deployed yet (FastAPI via Lambda/API Gateway)
- When ready:
  - Request ACM cert (us-east-1) for `api.gengine.darkforestlabs.com`
  - Add Route 53 validation CNAME
  - Create API Gateway custom domain + A/ALIAS

## Registrar NS Check

Ensure `darkforestlabs.com` registrar uses these Route 53 nameservers:
- ns-1255.awsdns-28.org
- ns-221.awsdns-27.com
- ns-556.awsdns-05.net
- ns-1987.awsdns-56.co.uk

## Quick CLI references

- Check Amplify domain status:
  - `aws amplify list-domain-associations --app-id d2vt3koij47dy3`
- Check ACM cert status:
  - `aws acm describe-certificate --region us-east-1 --certificate-arn arn:aws:acm:us-east-1:290318879194:certificate/c4fbbc0f-69ba-4064-b6e0-e255aa9883dd --query 'Certificate.Status'`
