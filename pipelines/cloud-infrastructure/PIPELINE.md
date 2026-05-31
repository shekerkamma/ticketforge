# Cloud & Infrastructure Category — Pipeline Tests

End-to-end pipeline combining **project-level** diagram skills (`cloud`, `network`, `security`, `iot`) with **global-level** operational skills (`cso`, `canary`, `land-and-deploy`, `investigate`) for infrastructure documentation and DevSecOps workflows.

## Skills in this pipeline

### Project-level (installed in `.agents/skills/`)
| Skill | Role | Output | Stencil Family |
|---|---|---|---|
| `cloud` | Cloud provider architecture diagrams | PlantUML (` ```plantuml `) | `mxgraph.aws4.*`, `mxgraph.azure.*`, `mxgraph.gcp2.*`, `mxgraph.alibaba_cloud.*`, `mxgraph.kubernetes.*` |
| `network` | Network topology (LAN/WAN/DC) | PlantUML (` ```plantuml `) | `mxgraph.networks.*`, `mxgraph.cisco.*`, `mxgraph.cisco19.*`, `mxgraph.cisco_safe.*` |
| `security` | Security architecture (IAM, encryption, threats) | PlantUML (` ```plantuml `) | `mxgraph.aws4.*` (security subset: `cognito`, `guardduty`, `kms`, etc.) |
| `iot` | IoT architecture (devices → edge → cloud) | PlantUML (` ```plantuml `) | `mxgraph.aws4.*` (IoT subset: `iot_core`, `greengrass`, `sensor`, etc.) |
| `diagram-export` | Rasterize PlantUML → PNG/SVG/PDF | Image files | N/A |
| `architecture` | Layered HTML/CSS (for final summary view) | Embedded HTML | N/A |
| `infocard` | Component summary cards | Embedded HTML | N/A |
| `marp` / `slide-narrative` | Presentation layer | Markdown slides / prose | N/A |

### Global-level (in `~/.claude/skills/`)
| Skill | Role | Output |
|---|---|---|
| `cso` | Chief Security Officer — 14-phase security audit | Findings report with severity ratings |
| `canary` | Post-deploy canary monitoring | Health report with screenshots & error logs |
| `land-and-deploy` | Merge PR → deploy → verify health | Deploy report |
| `investigate` | Root cause debugging (Iron Law: no fix without RCA) | Investigation report with hypothesis chain |

### How They Connect

```
cloud ──────┐
network ────┤
security ───┤──→ Full infrastructure diagram set
iot ────────┘         │
                      ├──→ diagram-export (PNG/SVG for decks)
                      ├──→ architecture (HTML summary view)
                      ├──→ infocard (component cards)
                      └──→ marp (presentation)

cso ──→ security (diagram the findings)
canary ──→ investigate (debug what canary caught)
land-and-deploy ──→ canary (verify the deploy)
investigate ──→ cloud/network/security (diagram the fix)
```

---

## Pipeline 1: Full Infrastructure Diagram Stack

**Goal:** Document a single system's infrastructure across all four diagram types — cloud topology, network layout, security posture, and IoT edge layer.

**System under test:** Smart factory with cloud backend — sensors on the factory floor push telemetry through edge gateways to AWS, with a corporate network connecting the operations center, and security controls across all layers.

### Step 1 — Cloud architecture
**Skill:** `cloud`

> Use the cloud skill to draw an AWS architecture for a smart factory cloud backend. Components: IoT Core (MQTT broker), Kinesis Data Streams (telemetry ingestion), Lambda (event processing), DynamoDB (device state), S3 (telemetry archive), SageMaker (anomaly detection model), SNS (alerts), CloudWatch (monitoring). Group IoT Core and Kinesis in a "Data Ingestion" VPC zone. Group Lambda, DynamoDB, S3 in a "Processing" zone. SageMaker and SNS in an "Intelligence" zone. Show the data flow left-to-right from ingestion to alerting.

**Grade:**
- [ ] `@startuml` / `@enduml` present
- [ ] `left to right direction` used
- [ ] ` ```plantuml ` fence (not ` ```text `)
- [ ] `mxgraph.aws4.*` stencils for all services (e.g., `mxgraph.aws4.iot_core`, `mxgraph.aws4.kinesis_data_streams`, `mxgraph.aws4.lambda_function`)
- [ ] Three `rectangle` zones: Data Ingestion, Processing, Intelligence
- [ ] Sync flows (`-->`) for API calls, async flows (`..>`) for event-driven paths
- [ ] Labeled connections describing the data (e.g., `"MQTT telemetry"`, `"anomaly score"`)
- [ ] No manual `fillColor` or `strokeColor` specified

### Step 2 — Network topology
**Skill:** `network`

> Use the network skill to draw the corporate network connecting the factory operations center to the AWS cloud backend from Step 1. Show: Internet (cloud shape) → corporate firewall (Cisco NGFW) → core router → two switches: one for the Operations Center LAN (operator workstations, SCADA servers, historian database) and one for the Factory Floor network (PLCs, HMIs, edge gateways). Add a VPN tunnel (dashed line) from the corporate firewall to the AWS VPC. Add a DMZ zone between the firewall and the factory floor with a data diode for one-way telemetry export. Use Cisco stencils.

**Grade:**
- [ ] `@startuml` / `@enduml` present
- [ ] ` ```plantuml ` fence
- [ ] `mxgraph.cisco.*` or `mxgraph.cisco_safe.*` stencils for network devices
- [ ] `cloud "Internet"` for the Internet boundary
- [ ] `rectangle` zones: Operations Center LAN, Factory Floor, DMZ
- [ ] Physical links `--` for Ethernet, dashed `..` for VPN tunnel
- [ ] Data diode shown as one-way connection (`-->` only, not bidirectional)
- [ ] Labeled connections (e.g., `"1 Gbps"`, `"IPsec VPN"`, `"OPC-UA"`)

### Step 3 — Security architecture
**Skill:** `security`

> Use the security skill to draw the security architecture for the smart factory system. Show:
> - **Identity zone:** Cognito (operator auth), IAM roles (service-to-service), STS (temporary creds for edge devices)
> - **Perimeter zone:** WAF on the API, Network Firewall on VPC, Shield for DDoS
> - **Data protection zone:** KMS (encrypt telemetry at rest), Secrets Manager (DB creds, API keys), Certificate Manager (mTLS for IoT devices)
> - **Detection zone:** GuardDuty (threat detection), Security Hub (posture dashboard), CloudTrail (audit log), Macie (PII scan on archived telemetry)
>
> Flow: Operator/Device → Cognito/STS → IAM → WAF/Firewall → Protected Resources. Audit trail from all zones flows to CloudTrail → Security Lake.

**Grade:**
- [ ] `@startuml` / `@enduml` present
- [ ] `left to right direction` for access flow
- [ ] ` ```plantuml ` fence
- [ ] `mxgraph.aws4.*` security stencils (e.g., `mxgraph.aws4.cognito`, `mxgraph.aws4.guardduty`, `mxgraph.aws4.key_management_service`)
- [ ] Four `rectangle "Trust Boundary"` zones: Identity, Perimeter, Data Protection, Detection
- [ ] Access flows `-->` from user to resources
- [ ] Audit flows `..>` (dashed) from all zones to CloudTrail/Security Lake
- [ ] Labeled connections describing credentials/protocols

### Step 4 — IoT edge architecture
**Skill:** `iot`

> Use the iot skill to draw the factory floor IoT architecture. Show:
> - **Factory Floor zone:** Temperature sensors, vibration sensors, PLCs, industrial PCs
> - **Edge zone:** Two Greengrass edge gateways (redundant), running local ML inference (anomaly detection) and data aggregation
> - **Cloud zone:** IoT Core (MQTT broker), IoT Device Management (fleet provisioning), IoT Device Defender (security monitoring), IoT Analytics (pipeline → dataset → data store)
> - **Digital Twin zone:** IoT TwinMaker (3D visualization of factory), IoT SiteWise (asset models)
>
> Data flow: Sensors → PLC → Edge Gateway → IoT Core → branches to Analytics and Digital Twin. Device management and defender monitor the edge gateways.

**Grade:**
- [ ] `@startuml` / `@enduml` present
- [ ] `left to right direction` (Device → Edge → Cloud)
- [ ] ` ```plantuml ` fence
- [ ] `mxgraph.aws4.*` IoT stencils (e.g., `mxgraph.aws4.sensor`, `mxgraph.aws4.iot_thing_plc`, `mxgraph.aws4.greengrass`, `mxgraph.aws4.iot_core`, `mxgraph.aws4.iot_twinmaker`)
- [ ] Four zones: Factory Floor, Edge, Cloud, Digital Twin
- [ ] Sync flows `-->` for commands, async `..>` for telemetry/MQTT
- [ ] Labeled connections with protocols (`"MQTT"`, `"OPC-UA"`, `"HTTPS"`)
- [ ] Redundant edge gateways both shown

### Step 5 — Unified summary diagram
**Skill:** `architecture`

> Take all four diagrams from Steps 1-4 and produce a single layered HTML architecture diagram that shows the full smart factory system. Use `three-column` layout with `steel-blue` style.
> - **User layer:** Operator workstations, SCADA HMI, mobile app
> - **Application layer:** MQTT broker, event processor, anomaly detector, alert manager
> - **AI/Logic layer:** SageMaker anomaly model, edge ML inference, digital twin engine
> - **Data layer:** DynamoDB, S3, IoT Analytics data store, historian DB
> - **Infrastructure layer:** EKS, Greengrass edge, Kinesis, Lambda, IoT Core
> - **External layer:** Sensor network, PLCs, third-party SCADA
> - **Left sidebar:** Security (IAM, KMS, mTLS, WAF, GuardDuty)
> - **Right sidebar:** Network (VPN, firewall, DMZ, data diode)

**Grade:**
- [ ] Direct HTML embedding (no ` ```html ` fence)
- [ ] No empty lines in HTML block
- [ ] `steel-blue` style, `three-column` layout
- [ ] All 6 layers populated with components from Steps 1-4
- [ ] Both sidebars with concrete items (not generic)
- [ ] Components are consistent with the PlantUML diagrams (same names, same groupings)

### Step 6 — Export all diagrams
**Skill:** `diagram-export`

> Export all four PlantUML diagrams from Steps 1-4 to:
> 1. SVG (for embedding in docs)
> 2. PNG at 2x (for slide decks)
>
> Also export the HTML architecture summary from Step 5 as a PNG screenshot.

**Grade:**
- [ ] PlantUML export command: `java -jar plantuml.jar -tsvg` and `-tpng -scale 2`
- [ ] Notes about mxgraph stencils requiring the docu.md PlantUML fork
- [ ] HTML screenshot via headless browser (`puppeteer`, `playwright`, or `/browse` skill)
- [ ] Concrete commands, not vague instructions

---

## Pipeline 2: Security Audit → Diagram → Fix → Deploy → Verify

**Goal:** Run the full DevSecOps lifecycle — audit the system, diagram the findings, fix the issues, deploy, and verify.

### Step 1 — Security audit
**Skill:** `cso` (global)

> Run `/cso` on the smart factory codebase. Focus on:
> - Secrets in config files
> - IAM policy over-permissions
> - Unencrypted data stores
> - Missing network segmentation
> - IoT device authentication gaps

**Grade:**
- [ ] 14-phase audit structure followed
- [ ] Findings have severity ratings (Critical/High/Medium/Low)
- [ ] Each finding has evidence (file path, line number, or config reference)
- [ ] Confidence gate applied (8/10 for daily mode)
- [ ] Actionable remediation per finding

### Step 2 — Diagram the current (vulnerable) state
**Skill:** `security`

> Using the CSO audit findings from Step 1, draw a security architecture diagram showing the CURRENT state with the vulnerabilities highlighted. Use labeled connections to annotate the gaps:
> - "IAM: overly permissive *" on broad policies
> - "MISSING: encryption at rest" on unencrypted stores
> - "MISSING: mTLS" on device connections without mutual auth
> - "OPEN: no WAF" on unprotected endpoints

**Grade:**
- [ ] Valid PlantUML with security stencils
- [ ] Vulnerabilities visible in the diagram (labeled connections or note annotations)
- [ ] Trust boundaries show where segmentation is missing
- [ ] Not a "fixed" diagram — shows the current broken state

### Step 3 — Diagram the target (fixed) state
**Skill:** `security`

> Now draw the TARGET security architecture after all CSO findings are remediated:
> - KMS encryption on all data stores
> - Least-privilege IAM with role-per-service
> - mTLS on all IoT device connections via Certificate Manager
> - WAF on all public endpoints
> - GuardDuty + Security Hub for continuous monitoring
> - Network segmentation with firewall rules between zones

**Grade:**
- [ ] Valid PlantUML with security stencils
- [ ] All vulnerabilities from Step 2 are now addressed
- [ ] New components visible (KMS, WAF, Certificate Manager, GuardDuty)
- [ ] Clear visual difference from the "before" diagram

### Step 4 — Investigate a production incident
**Skill:** `investigate` (global)

> A canary alert fired: IoT telemetry latency spiked from 200ms to 5s after the last deploy. The anomaly detection pipeline is timing out. Use the investigate skill to find the root cause.

**Grade:**
- [ ] Iron Law followed: no fix proposed before root cause identified
- [ ] Phase 1: Root cause investigation (check CloudWatch, IoT Core metrics, Kinesis throughput)
- [ ] Phase 2: Pattern analysis (is this a known pattern — throttling, cold start, config regression?)
- [ ] Phase 3: Hypothesis testing with 3-strike rule
- [ ] Freeze boundary set to affected module
- [ ] Root cause identified with evidence before any fix suggested

### Step 5 — Diagram the fix
**Skills:** `cloud` + `network`

> The root cause was: Kinesis shard count was reduced in the last deploy (from 4 to 1), causing throughput bottleneck. Draw an updated cloud diagram showing:
> 1. Kinesis with 4 shards (restored)
> 2. Auto-scaling policy on Kinesis
> 3. CloudWatch alarm on `IncomingRecords` threshold
>
> Also update the network diagram to show a new CloudWatch → PagerDuty alerting path.

**Grade:**
- [ ] Cloud diagram updated with Kinesis shard annotation
- [ ] Auto-scaling and alarm components added
- [ ] Network diagram updated with alerting path
- [ ] Changes are minimal and targeted (not a full redraw)

### Step 6 — Deploy the fix
**Skill:** `land-and-deploy` (global)

> The Kinesis shard fix is in PR #42. Use land-and-deploy to:
> 1. Run pre-flight checks
> 2. Merge the PR
> 3. Wait for CI/CD
> 4. Verify the deploy

**Grade:**
- [ ] Pre-flight checks run (CI status, conflicts, approvals)
- [ ] PR merged via `gh pr merge`
- [ ] Deploy platform auto-detected
- [ ] Wait for deploy with status polling
- [ ] Canary verification triggered after deploy

### Step 7 — Post-deploy canary verification
**Skill:** `canary` (global)

> Run `/canary` on the IoT telemetry dashboard after the Kinesis fix deploy. Monitor for 5 minutes. Check:
> - Telemetry latency back to <500ms
> - No console errors on the dashboard
> - Anomaly detection pipeline responding

**Grade:**
- [ ] Baseline captured before monitoring loop
- [ ] Pages discovered (dashboard URL + key pages)
- [ ] Continuous monitoring loop runs for specified duration
- [ ] Health report generated with latency metrics
- [ ] Console error detection active
- [ ] Pass/fail verdict with evidence

---

## Pipeline 3: Multi-Cloud Comparison

**Goal:** Use the `cloud` skill across different providers to compare architectures for the same workload.

### Step 1 — AWS version
**Skill:** `cloud`

> Use the cloud skill to draw an AWS serverless event-processing pipeline: API Gateway → Lambda → SQS → Lambda (processor) → DynamoDB + S3. Add CloudWatch for monitoring and X-Ray for tracing.

**Grade:**
- [ ] `mxgraph.aws4.*` stencils throughout
- [ ] VPC zone not required (serverless)
- [ ] Async flow `..>` between SQS and consumer Lambda
- [ ] Monitoring/tracing shown as separate concern

### Step 2 — Azure version
**Skill:** `cloud`

> Draw the equivalent on Azure: API Management → Azure Functions → Service Bus → Azure Functions (processor) → Cosmos DB + Blob Storage. Add Application Insights for monitoring.

**Grade:**
- [ ] `mxgraph.azure.*` stencils throughout
- [ ] Same logical architecture, different service names
- [ ] Equivalent connection patterns (sync `-->`, async `..>`)

### Step 3 — GCP version
**Skill:** `cloud`

> Draw the equivalent on GCP: Cloud Endpoints → Cloud Functions → Pub/Sub → Cloud Functions (processor) → Firestore + Cloud Storage. Add Cloud Monitoring and Cloud Trace.

**Grade:**
- [ ] `mxgraph.gcp2.*` stencils throughout
- [ ] Same logical architecture, different service names

### Step 4 — Kubernetes-native version
**Skill:** `cloud`

> Draw the Kubernetes-native version: Ingress → API pod → NATS (message queue) → Worker pods → PostgreSQL (StatefulSet) + MinIO (PVC). Add Prometheus + Grafana for monitoring.

**Grade:**
- [ ] `mxgraph.kubernetes.*` stencils (e.g., `mxgraph.kubernetes.ing`, `mxgraph.kubernetes.pod`, `mxgraph.kubernetes.svc`, `mxgraph.kubernetes.sts`, `mxgraph.kubernetes.pvc`)
- [ ] Correct K8s primitives (not cloud services)

### Step 5 — Comparison info cards
**Skill:** `infocard`

> Create a comparison infocard for the four cloud implementations:
>
> | | AWS | Azure | GCP | K8s |
> |---|---|---|---|---|
> | Compute | Lambda | Functions | Cloud Functions | Pods |
> | Queue | SQS | Service Bus | Pub/Sub | NATS |
> | DB | DynamoDB | Cosmos DB | Firestore | PostgreSQL |
> | Storage | S3 | Blob | Cloud Storage | MinIO |
> | Cold start | ~200ms | ~500ms | ~300ms | N/A |
> | Vendor lock-in | High | High | High | Low |
>
> Use `comparison` or `matrix-table` layout. Technical tone.

**Grade:**
- [ ] All four providers compared with correct service mappings
- [ ] Metrics (cold start, lock-in) prominently displayed
- [ ] Direct HTML, no code fence
- [ ] Layout suits comparison (not hero-card or timeline)

---

## Pipeline 4: IoT End-to-End (Device to Dashboard)

**Goal:** Trace an IoT data packet from physical sensor to executive dashboard, diagramming every layer.

### Step 1 — Physical sensor network
**Skill:** `iot`

> Draw the sensor layer of a cold-chain logistics system. Show: temperature sensors in 3 refrigerated trucks, GPS trackers, door open/close sensors. Each truck has a Greengrass edge gateway aggregating sensor data. Use LoRaWAN protocol between sensors and gateways.

**Grade:**
- [ ] `mxgraph.aws4.sensor` / `mxgraph.aws4.iot_thing_temperature_sensor` for sensors
- [ ] `mxgraph.aws4.greengrass` for edge gateways
- [ ] `mxgraph.aws4.iot_lorawan_protocol` for LoRaWAN
- [ ] Three truck zones, each with sensors + gateway
- [ ] Labeled with `"LoRaWAN"` and `"MQTT"` protocols

### Step 2 — Edge processing
**Skill:** `iot`

> Zoom into one truck's Greengrass edge gateway. Show the edge components: Greengrass Nucleus, Stream Manager (buffers telemetry when offline), local ML component (predicts if temperature will breach threshold in next 30 min), OTA update agent. The gateway connects to IoT Core via cellular (4G fallback to satellite).

**Grade:**
- [ ] `mxgraph.aws4.iot_greengrass_nucleus`, `mxgraph.aws4.iot_greengrass_stream_manager`, `mxgraph.aws4.iot_greengrass_component`
- [ ] `mxgraph.aws4.iot_over_the_air_update` for OTA
- [ ] Internal edge components grouped in one zone
- [ ] Connection to IoT Core labeled `"4G / Satellite fallback"`

### Step 3 — Cloud ingestion and processing
**Skill:** `cloud`

> Draw the cloud backend for the cold-chain system. IoT Core receives MQTT telemetry → IoT Rules Engine fans out to: (a) Kinesis for real-time stream processing, (b) S3 for archive, (c) IoT Events for threshold breach detection. Kinesis feeds Lambda for enrichment → DynamoDB (current state) + Timestream (time-series). IoT Events triggers SNS → SMS alerts when temperature breaches.

**Grade:**
- [ ] `mxgraph.aws4.*` stencils for all services
- [ ] Fan-out from IoT Rules Engine shown as multiple `-->` arrows
- [ ] Real-time path vs. archive path visually distinct
- [ ] Alert path through IoT Events → SNS → SMS

### Step 4 — Network connectivity
**Skill:** `network`

> Draw the network layer connecting the trucks to the cloud. Show: Cellular modem (4G LTE) in each truck → carrier network → Internet → AWS VPC with Private Link. Add a backup path: satellite modem → satellite provider → Internet. Show the operations center connected via corporate VPN. Use the appropriate stencils for wireless/cellular links.

**Grade:**
- [ ] Wireless/cellular links shown as dashed `..>` lines
- [ ] Primary (4G) and backup (satellite) paths both shown
- [ ] VPN tunnel to operations center via `..` dashed line
- [ ] `cloud "Internet"` and `cloud "Carrier Network"` shapes
- [ ] AWS Private Link endpoint shown

### Step 5 — Security overlay
**Skill:** `security`

> Draw the security architecture for the cold-chain system:
> - **Device identity:** X.509 certificates per truck gateway, stored in IoT Core registry
> - **Transport:** mTLS from gateway to IoT Core, Certificate Manager for cert lifecycle
> - **Data protection:** KMS encryption on S3, DynamoDB, Timestream. Secrets Manager for API keys.
> - **Access control:** IAM roles per Lambda function (least privilege), Cognito for dashboard operators
> - **Monitoring:** GuardDuty for anomaly detection, CloudTrail for audit, IoT Device Defender for device-side monitoring

**Grade:**
- [ ] Device identity with X.509 certificates shown (not just IAM users)
- [ ] mTLS labeled on device-to-cloud connections
- [ ] IoT Device Defender connected to edge gateways (not just cloud resources)
- [ ] Audit trail flows to CloudTrail
- [ ] Trust boundaries separate device, edge, cloud, and operator zones

### Step 6 — Executive dashboard infocard
**Skill:** `infocard`

> Create an executive infocard for the cold-chain monitoring system:
> - **Fleet:** 200 trucks, 600 sensors, 99.7% uptime
> - **Alerts:** 12 temperature breaches this month (down 40% from last month)
> - **Latency:** sensor-to-dashboard p99: 3.2 seconds
> - **Cost:** $0.14/truck/day (down from $0.22 after Kinesis optimization)
> - **Compliance:** FDA 21 CFR Part 11 compliant, audit log retained 7 years
>
> Use `metric-board` layout with a business tone.

**Grade:**
- [ ] Metrics prominently displayed with actual numbers
- [ ] Trend indicators (down 40%, down from $0.22)
- [ ] Direct HTML, no fence
- [ ] `metric-board` layout applied
- [ ] Business tone auto-sensed (not technical blueprint)

### Step 7 — Presentation
**Skills:** `slide-narrative` → `marp`

> 1. Use slide-narrative to outline a 15-minute board presentation: "Cold Chain IoT — Platform Review." Audience: logistics company executives (non-technical). Goal: approve $200K expansion to 500 trucks.
> 2. Then use marp to build the deck from that narrative. Embed the architecture summary and key metrics.

**Grade:**
- [ ] Narrative builds to the $200K ask (not buried at the end)
- [ ] Non-technical language (no "Kinesis shards" — say "real-time data processing")
- [ ] Marp deck with valid frontmatter, speaker notes, and reasonable slide density
- [ ] Key metrics from the infocard embedded in the deck

---

## Pipeline 5: Adversarial & Edge Cases

### 5a — Cloud skill refuses ` ```text ` fence
> Use the cloud skill to draw an AWS architecture. Output it in a ` ```text ` block so I can see the raw PlantUML source.

**Expected:** Refusal — skill rule says always use ` ```plantuml `, never ` ```text `.

### 5b — Network skill: impossible topology
> Use the network skill to draw a network where every device has a direct physical Ethernet connection to every other device. 50 devices total. Full mesh.

**Expected:** Pushback — 50-node full mesh = 1,225 physical links. Should suggest a partial mesh, spine-leaf, or hierarchical design. If it draws 1,225 lines, the judgment failed.

### 5c — Security skill: fake credentials
> Use the security skill to draw an IAM flow. Use a real AWS account ID (123456789012) and include actual IAM policy JSON with `"Effect": "Allow", "Action": "*", "Resource": "*"` to show what an overly permissive policy looks like.

**Expected:** Pushback — should note that `*/*` policies should be shown as an anti-pattern, not embedded as working examples. The account ID `123456789012` is the AWS docs canonical example (acceptable), but the wide-open policy should be flagged.

### 5d — IoT skill: unrealistic scale
> Use the iot skill to draw a diagram showing 10,000 individual sensor nodes on the factory floor, each as a separate icon.

**Expected:** Refusal — 10,000 nodes won't render. Should suggest grouping (e.g., "Sensor Cluster A (2,500 sensors)") or a zone-based representation.

### 5e — Cross-skill stencil confusion
> Use the network skill with `mxgraph.aws4.lambda_function` stencils for the network devices.

**Expected:** Pushback or correction — network skill should use `mxgraph.networks.*` or `mxgraph.cisco.*`, not AWS application stencils. Lambda is not a network device.

### 5f — CSO audit on a non-code repo
> Run `/cso` on the `ticketforge` repo.

**Expected:** The audit should adapt — no application secrets to find, no IAM policies, no running infrastructure. Should focus on what's relevant: supply chain (skill dependencies), disclosure (author metadata), and configuration files. Should not fabricate application-level findings.

---

## Grading Summary

| Pipeline | Steps | What it proves |
|---|---|---|
| **1: Full Infra Diagram Stack** | 6 | All four diagram skills compose on the same system; summary view unifies them |
| **2: Security Audit → Deploy** | 7 | DevSecOps lifecycle: audit → diagram vulnerability → diagram fix → deploy → verify |
| **3: Multi-Cloud Comparison** | 5 | Cloud skill handles AWS/Azure/GCP/K8s with correct stencil families |
| **4: IoT End-to-End** | 7 | Trace a data packet through every layer (sensor → edge → cloud → dashboard) |
| **5: Adversarial** | 6 | Rule enforcement, scale judgment, stencil correctness, non-code repo handling |

### Pass criteria
- **Diagram skills pass** when: valid PlantUML syntax, correct stencil family for the provider/domain, proper zone grouping, correct arrow types (sync vs. async), labeled connections.
- **Global skills pass** when: they follow their full phase structure (CSO's 14 phases, investigate's Iron Law, canary's monitoring loop, land-and-deploy's 10 steps).
- **Pipeline passes** when: each step builds on prior steps (same system, same component names, same zones), and the final artifact (deck, report, or HTML) references all upstream diagrams consistently.
- **Adversarial tests pass** when the skill refuses or reshapes. They **fail** when the skill silently complies.
