---
type: spec
domain: infra
status: active
created: 2026-03-14
updated: 2026-03-19
---
# Canary Lab — Network Topology

> Last updated: 2026-03-07
> Machine: Mac Mini M4 (192.168.10.102)

---

## ISP

| Detail | Value |
|--------|-------|
| Provider | Frontier Communications |
| Type | Fiber |
| External IP | 47.154.122.225 |
| Location | Rancho Palos Verdes, CA |
| Static IP | Not required (Cloudflare Tunnel is outbound-only) |

---

## Network Architecture

```
Frontier Fiber Modem/Router (4 ports)
  └── Port 1 → D-Link DSR-250 (192.168.10.1)
  └── Ports 2-4 — available

DSR-250 Business Router (192.168.10.0/24)
  ├── .100  Google Nest WiFi (WAN side → bridges to 192.168.86.x)
  ├── .101  SmartThings Hub (ethernet adapter)
  ├── .102  Mac Mini M4 16GB — Canary Dev Server
  ├── .103  (reserved) Mac Studio — Ollama inference (future)
  └── .117  iMac — QA Server

Google Nest WiFi (192.168.86.0/24)
  └── 22 household devices (phones, tablets, IoT, smart home)
```

---

## Wired Lab Segment (192.168.10.x)

| IP | MAC Prefix | Device | Role |
|----|-----------|--------|------|
| .1 | 60:63:4c (D-Link) | DSR-250 | Business router / firewall / gateway |
| .100 | 58:cb:52 (Google) | Nest WiFi | Bridge to household WiFi (192.168.86.x) |
| .101 | d0:52:a8 (Physical Graph / SmartThings) | SmartThings Hub | Smart home controller |
| .102 | d0:11:e5 (Apple) | Mac Mini M4 16GB | **Canary Dev Server** |
| .103 | — | (reserved) | **Future: Mac Studio — Ollama inference** |
| .117 | — (Apple) | iMac | **Canary QA Server** |

---

## Mac Mini M4 — Dev Server (192.168.10.102)

### Hardware
- Model: Mac mini (Mac16,10) — MU9D3LL/A
- Chip: Apple M4
- Memory: 16 GB
- Disk: 228 GB (47 GB free)
- Hostname: Geoffs-Mac-mini.local

### Network Interfaces
| Interface | Type | IP | Subnet |
|-----------|------|-----|--------|
| en0 | Ethernet (primary) | 192.168.10.102 | 192.168.10.0/24 |
| en1 | Wi-Fi | 192.168.86.38 | 192.168.86.0/24 |

Note: Dual-homed on both wired and WiFi networks.

### Docker Containers
| Container | Ports | Status |
|-----------|-------|--------|
| canary_localhost_flask | :5001 | Healthy |
| canary_localhost_pg | :5432 | Healthy |
| canary_localhost_valkey | :6379 | Healthy |
| canary_localhost_nginx | :80, :443 | Up |
| canary_localhost_tsp_sub1 | internal | Up |
| canary_localhost_tsp_sub2 | internal | Up |
| canary_localhost_tsp_sub3 | internal | Up |
| canary_localhost_tsp_sub4 | internal | Up |

### Services
| Service | Port | Binding |
|---------|------|---------|
| Flask (Docker) | 5001 | 0.0.0.0 |
| PostgreSQL (Docker) | 5432 | 0.0.0.0 |
| Valkey (Docker) | 6379 | 0.0.0.0 |
| Nginx (Docker) | 80, 443 | 0.0.0.0 |
| Ollama | 11434 | 127.0.0.1 |
| Cloudflare Tunnel | outbound | 127.0.0.1:20241 |
| AirPlay | 5000, 7000 | * |

### Docker Disk Usage
| Resource | Size | Reclaimable |
|----------|------|-------------|
| Images | 24.5 GB | 18.6 GB (75%) |
| Containers | 3.7 MB | 1.0 MB |
| Volumes | 1.6 GB | 110 MB |
| Build Cache | 27.6 GB | 20.6 GB |
| **Total reclaimable** | — | **~39 GB** |

### Ollama
| Detail | Value |
|--------|-------|
| Model | qwen3:14b (Q4_K_M quantization) |
| Size | 9.3 GB |
| Port | 11434 (localhost only) |
| Docker access | host.docker.internal:11434 |

---

## Cloudflare Tunnels

**Tunnel:** `canary-qa` (ID: 831b63d5) — shared tunnel, two connectors, always-on.

Each machine runs its own `cloudflared` process. Hostname-based routing directs traffic to the correct machine.

| Hostname | Machine | IP | Port |
|----------|---------|----|------|
| dev.growdirect.app | Mac Mini | 192.168.10.102 | :5001 |
| qa.growdirect.app | iMac | 192.168.10.117 | :5001 |

| Detail | Value |
|--------|-------|
| TLS | Handled by Cloudflare (automatic) |
| Domain | growdirect.app (nameservers on Cloudflare) |
| Mac Mini config | `~/.cloudflared/config.yml` (local file) |
| iMac config | Token-based (Cloudflare Zero Trust dashboard) |
| Connectors | 2 active — darwin_arm64 (Mac Mini) + linux_amd64 (iMac Docker) |

Both tunnels are outbound-only — no inbound ports open on the DSR-250 or Frontier router. After a container rebuild on either machine, the tunnel automatically picks up the new container. No tunnel restart needed.

---

## WiFi Network (192.168.86.x) — Household

22 devices on Google Nest WiFi mesh. These are behind the Nest's NAT and cannot directly reach the wired lab segment (192.168.10.x). This provides natural network isolation between household devices and Canary infrastructure.

Nest WiFi points identified by MAC prefix 58:cb:52 at .25 and .51.

---

## Security Notes

1. **No inbound ports open** — Cloudflare Tunnel handles all external access
2. **DSR-250 firewall** — business-class router with stateful firewall, VPN, VLAN support
3. **Natural segmentation** — lab on wired 10.x, household on WiFi 86.x behind Nest NAT
4. **Ollama bound to localhost** — not exposed to network (Docker accesses via host.docker.internal)
5. **PostgreSQL/Valkey bound to 0.0.0.0** — accessible from LAN; consider restricting to localhost + Docker bridge if security tightening needed

---

## Future: Mac Studio Inference Server

When added to the lab:
- Plug into DSR-250, reserve IP at .103
- Install Ollama, run qwen3:14b (or larger models with 192GB unified memory)
- Update `OWL_URL=http://192.168.10.103:11434` in `.env`
- Run as launchd service for auto-restart on crash/reboot
- Add health check so Flask falls back to deterministic mode if unreachable
- Cost: ~$4,000 one-time vs ~$550/mo for AWS GPU instance

---

## Future: VLAN Hardening

The DSR-250 supports VLANs. Recommended segmentation:

| VLAN | Subnet | Purpose |
|------|--------|---------|
| VLAN 10 | 192.168.10.0/24 | Canary Lab (Mini, iMac, Studio) |
| VLAN 20 | 192.168.20.0/24 | IoT / SmartThings (isolated) |
| VLAN 86 | 192.168.86.0/24 | Household WiFi (Nest-managed) |

This would fully isolate the SmartThings hub from the lab segment.
