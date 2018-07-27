# ledger
`This project is a work-in-progress.`

General ledger for managing money between a group of people.

## Motivation
When money floats between people often, it doesn't make sense to pay people back immediately given the overhead of counting cash and electronic transfers. Instead, it makes more sense to keep a record of transactions then reconcile the accumulated amount periodically.

## Implementation
### Technologies
- Flask, Bootstrap, HTML5, CSS3
- WSGI intended for local use

### Design Considerations
- Server dependent, form based, template based
- Limited security consideration, no anti-botting (captchas), no sanitation, no sanity checks
  - not for use in production
