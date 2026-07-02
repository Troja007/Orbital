# Orbital Target, Node, And Selector Cross-Reference

Source URL: https://developer.cisco.com/docs/orbital/queries/#specifying-nodes

Source title: Orbital API - Cisco DevNet / Query API / Specifying Nodes

Reviewed: 2026-06-02

Import type: Structured terminology and selector cross-reference from the Cisco DevNet Orbital Query API documentation. This file is not a verbatim copy of the page.

## Purpose

Orbital uses several terms for the same practical concept: selecting which endpoints a query or script should run against.

Customer-facing wording often uses terms such as targets, devices, endpoints, or hosts. The API documentation uses the heading `Specifying Nodes` and the request field `nodes`.

For project work, treat these as related but not identical:

| Term | Where it appears | Meaning in project work |
| --- | --- | --- |
| target / search target | User-facing and operational wording | The endpoint population intended for a query or script. |
| device / endpoint | Product/help wording | A managed endpoint with Orbital capability. |
| node | API and some help wording | The Orbital endpoint service/agent object used by API targeting. |
| `nodes` | API request field | Array of selector strings that define target endpoints. |
| selector prefix | API syntax | The prefix before `:` in a `nodes` entry, such as `host`, `ip`, or `orb`. |

Project rule: when explaining this to customers, use `target` first, then map it to API `nodes`. Example: "The API calls search targets `nodes`; each entry in the `nodes` array is a selector such as `host:NAME` or `ip:10.0.0.1`."

## API Field Relationship

The Query API common request fields include:

| API field | Meaning |
| --- | --- |
| `nodes` | Node selector array. Examples include host, Orbital ID, operating system, and network range selectors. |
| `os` | Adds all hosts with the listed operating systems to the target set. |
| `allowOS` | Filters returned results to listed operating systems after target selection. It does not define the target set itself. |

Important distinction:

- `os` changes target selection.
- `allowOS` filters returned results after target selection.
- `allowOS:<value>` can also appear as a selector prefix in the documented `nodes` selector list, but the documentation describes it as a result filter after target selection.

## Selector Prefixes

The API documentation lists these prefixes for the `nodes` array.

| Prefix | Example | Meaning |
| --- | --- | --- |
| `allowOS` | `allowOS:darwin` | Result filter applied after target selection. |
| `amp` | `amp:348301bf-2082-4d83-b340-e6ab2e58579c` | Secure Endpoint computer GUID. |
| `ampuuid` | `ampuuid:348301bf-2082-4d83-b340-e6ab2e58579c` | Secure Endpoint computer GUID. |
| `cm` | `cm:528601bf-2082-4d83-b340-e6ab2e58579c` | Secure Client computer GUID. |
| `cmid` | `cmid:528601bf-2082-4d83-b340-e6ab2e58579c` | Secure Client computer GUID. |
| `anyconnectudid` | `anyconnectudid:163F665789D42AA0EB883A023D67D8CE391DF362` | AnyConnect UDID. |
| `host` | `host:DESKTOP-XYZ` | Host name. |
| `hostname` | `hostname:WOPR` | Host name. |
| `hwaddr` | `hwaddr:02:42:c8:1f:7d:fa` | MAC address. |
| `orb` | `orb:oLPkT67m4nj-QpdGDPNCmQ` | Orbital ID. |
| `orbital` | `orbital:oLPkT67m4nj-QpdGDPNCmQ` | Orbital ID. |
| `ip` | `ip:10.0.0.1` | IPv4 or IPv6 address. |
| `ip4` | `ip4:10.0.0.1` | IPv4 address. |
| `ipv4` | `ipv4:10.0.0.1` | IPv4 address. |
| `ip6` | `ip6:fe80::3926:f1ac:d0cf:d1d7` | IPv6 address. |
| `ipv6` | `ipv6:fe80::3926:f1ac:d0cf:d1d7` | IPv6 address. |
| `mac` | `mac:02:42:c8:1f:7d:fa` | MAC address. |
| `machine` | `machine:48469d02bacd44eba481a1a3f0020ea1` | Unique machine identifier. |
| `os` | `os:windows` | All nodes with the given operating system. |
| `nodeversion` | `nodeversion:1.12.6` | Orbital node version. |
| `osqueryversion` | `osqueryversion:4.4.0` | osquery version. |
| `netmask` | `netmask:192.168.1.168/24` | IPv4 network range in CIDR notation. |
| `random` | `random:5` | Random endpoints. |
| `queryId` | `queryId:zfmCLhXjFO6aIvV3frhg_w` | Reuse an existing query definition. |

## Wildcards

The API documentation confirms wildcard matching for some prefixes.

Confirmed example:

```text
ipv4:127.0.0.%
```

Project handling:

- Treat `%` as a wildcard selector only where Orbital supports it.
- `host:%onik%` and `ip:192.168.1.%` match the documented wildcard concept, but verify the exact prefix behavior before using them in a customer-facing example.
- Prefer `ipv4:192.168.1.%` over `ip:192.168.1.%` when the intention is clearly IPv4-only.
- Use `netmask:192.168.1.168/24` when CIDR range targeting is intended.
- Do not assume IPv6 wildcard or IPv6 subnet targeting; existing project context says advanced IPv6 wildcard/subnet operations are not supported.

## Query Examples From API Pattern

Scheduled query with one hostname target:

```json
{
  "nodes": ["host:FRONT-DESK-123"]
}
```

Live query with one hostname target:

```json
{
  "nodes": ["host:FRONT-DESK-123"]
}
```

Scheduled stock query with multiple selectors:

```json
{
  "nodes": ["host:FRONT-DESK-123", "ip:1.2.3.4"],
  "os": ["windows"]
}
```

## Static, Dynamic, And Special Relationship

Use this file together with `Orbital_Queries.md`.

The help-page context describes:

- `all` as a special prefix for all devices.
- Direct known-device selectors as static targeting.
- Wildcard-based selectors using `%` as dynamic targeting.
- Dynamic selectors can include matching devices that reconnect while the query is active.
- Static selectors that do not resolve at query start can be dropped.

The API page gives the concrete `nodes` selector syntax. The help page gives the behavior model.

## Common Customer Confusion

Do not use these terms as if they are always interchangeable:

- Catalog `ID` is a query/script catalog identifier.
- Orbital ID is an endpoint/node selector value used with `orb:` or `orbital:`.
- Secure Endpoint computer GUID is used with `amp:` or `ampuuid:`.
- Secure Client computer GUID is used with `cm:` or `cmid:`.
- AnyConnect UDID is used with `anyconnectudid:`.
- `queryId:` reuses an existing query definition; it is not an endpoint ID.

Recommended wording:

> In the Orbital API, endpoint targets are specified in the `nodes` array. Each entry is a selector string. For example, `host:DESKTOP-XYZ` targets by hostname, `ipv4:10.0.0.1` targets by IPv4 address, and `netmask:192.168.1.168/24` targets an IPv4 CIDR range.

## Project Rules

- Always record whether a target selector is exact, wildcard-based, random, OS-based, network-based, or query-derived.
- For destructive or response-action scripts, avoid `random`, broad OS selectors, broad wildcards, and large network ranges unless the user explicitly approves the impact.
- For customer examples, say "targets" or "target endpoints" first, then show the API `nodes` syntax.
- For API request bodies, use the field name `nodes`.
- Verify selector behavior on the current API documentation before finalizing automation that depends on wildcard matching, GUID type, or operating system filtering.
