# LicenseHub v1.0 — Software Requirements Specification (SRS)

## 1. Introduction
- Purpose: Define functional/non-functional requirements for LicenseHub.

## 2. System Overview
- FastAPI backend; optional offline flows; license artifacts; Ed25519 (TBD).

## 3. Functional Requirements (excerpt)
- F-1: Activate license `/licenses/activate`.
- F-2: Validate license `/licenses/validate` (online).
- F-3: Generate offline request & process offline ticket (TBD endpoints).
- F-4: Read entitlements `/entitlements/{customer_id}`.
- F-5: Read features `/features/{product}`.
- F-6: Health `/health`.

## 4. Data Models
- Customer, Entitlement, Feature, LicenseTicket (drafts).

## 5. Security Requirements
- Use HTTPS in prod, API keys/Tokens (TBD), audit events (TBD).

## 6. API Spec
- OpenAPI auto via FastAPI at `/docs`.
