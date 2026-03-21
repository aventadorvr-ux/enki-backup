# SOC 2 TYPE II - ACCESS CONTROL POLICY

**Document Reference:** ENKI-SEC-ACS-001  
**Version:** 1.0  
**Effective Date:** [DATE]  
**Owner:** IT Security Manager  
**Review Cycle:** Annual  

---

## 1. PURPOSE

This Access Control Policy defines requirements for granting, managing, and revoking access to Enki Real Estate's information systems and data, ensuring the principle of least privilege and separation of duties.

---

## 2. ACCESS CONTROL PRINCIPLES

### 2.1 Least Privilege
Users shall be granted the minimum access necessary to perform their job functions.

### 2.2 Need-to-Know
Access to information shall be granted only to those with a legitimate business need.

### 2.3 Separation of Duties
Critical functions shall be divided among multiple individuals to prevent fraud and errors.

### 2.4 Defense in Depth
Multiple layers of access controls shall be implemented.

---

## 3. USER ACCESS MANAGEMENT

### 3.1 User Registration
1. **Account Request Process:**
   - Manager submits access request form
   - HR verification of employment status
   - Security review for appropriate access level
   - CISO approval for privileged access

2. **Unique User IDs:**
   - Each user assigned unique identifier
   - Shared accounts prohibited (except service accounts with monitoring)
   - Generic accounts prohibited

3. **Background Checks:**
   - Criminal record check for all employees
   - Enhanced checks for privileged access roles
   - Reference verification

### 3.2 Privilege Management

| Privilege Level | Description | Approval Required |
|-----------------|-------------|-------------------|
| Standard User | Basic application access | Department Manager |
| Power User | Elevated non-admin access | Department Head + IT |
| Administrator | System administration | CISO |
| Super Administrator | Critical infrastructure | CISO + CEO |

### 3.3 Access Review Process
- **Quarterly:** Automated access certification campaigns
- **Semi-Annually:** Privileged access review
- **Annually:** Comprehensive access audit
- **Upon Change:** Immediate review when roles change

### 3.4 Access Revocation
- Immediate upon termination notification
- Automated deprovisioning within 4 hours
- Emergency revocation within 1 hour
- Quarterly review of dormant accounts (>90 days)

---

## 4. AUTHENTICATION CONTROLS

### 4.1 Password Requirements
| Parameter | Requirement |
|-----------|-------------|
| Minimum Length | 14 characters |
| Complexity | Upper, lower, number, special character |
| Expiration | 90 days for standard, 60 days for privileged |
| History | Last 24 passwords cannot be reused |
| Lockout | 5 failed attempts = 30-minute lockout |

### 4.2 Multi-Factor Authentication (MFA)
- **Required for:** All remote access, privileged accounts, sensitive systems
- **Methods:** TOTP (authenticator apps), hardware tokens, biometric
- **SMS discouraged** (phishing risk)
- Recovery codes stored securely

### 4.3 Session Management
- Idle timeout: 15 minutes
- Maximum session duration: 8 hours
- Concurrent session limits per user
- Forced re-authentication for sensitive actions

---

## 5. AUTHORIZATION MODELS

### 5.1 Role-Based Access Control (RBAC)
Predefined roles aligned with job functions:

| Role | Systems Access | Data Access |
|------|----------------|-------------|
| Sales Agent | CRM, Property DB | Own listings, assigned leads |
| Property Manager | PM System, CRM | Managed properties, tenant data |
| Accountant | Accounting System | Financial data (read-only reports) |
| Senior Accountant | Accounting System | Full financial access |
| IT Support | Service Desk, AD | System administration (elevated) |
| Executive | All systems | All data (read-only where appropriate) |

### 5.2 Attribute-Based Access Control (ABAC)
Dynamic access based on:
- User attributes (department, location, clearance)
- Resource attributes (classification, sensitivity)
- Environmental attributes (time, location, device trust)

---

## 6. NETWORK ACCESS CONTROL

### 6.1 Network Segmentation
| Zone | Description | Access Controls |
|------|-------------|-----------------|
| DMZ | Public-facing services | Firewall, WAF, limited protocols |
| Corporate | Internal user network | VLANs, NAC, 802.1X |
| Sensitive | Financial, HR, Legal | Strict ACLs, dedicated VLANs |
| Management | Infrastructure management | Jump servers, dedicated VPN |
| Guest | Visitor network | Internet only, isolated |

### 6.2 Remote Access
- VPN required for all remote access
- Zero Trust Network Access (ZTNA) for cloud resources
- Split tunneling disabled
- Device compliance checks mandatory

### 6.3 Wireless Access
- WPA3-Enterprise authentication
- Separate SSIDs for corporate and guest
- Certificate-based authentication where possible

---

## 7. APPLICATION ACCESS CONTROL

### 7.1 API Access
- API keys stored in secure vault (e.g., HashiCorp Vault, AWS Secrets Manager)
- Keys rotated every 90 days
- Rate limiting enforced
- OAuth 2.0 / OpenID Connect for authentication

### 7.2 Service Accounts
- Dedicated service accounts per application
- Passwords automatically rotated
- Regular audit of service account usage
- No interactive logon for service accounts

### 7.3 Third-Party Access
- Vendor risk assessment required
- Contractual security requirements
- Limited access scope
- Regular access review
- Immediate revocation on contract termination

---

## 8. MONITORING AND AUDITING

### 8.1 Access Logging
- All authentication attempts logged
- Privileged access activities logged
- Failed access attempts alerted
- Logs retained for minimum 12 months

### 8.2 Privileged Access Monitoring
- Session recording for administrative access
- Real-time alerting for suspicious privileged activity
- Quarterly review of privileged access logs
- Just-in-time (JIT) access for critical systems

### 8.3 Access Violation Handling
- Automated alerting for policy violations
- Security team investigation within 24 hours
- Incident response process for confirmed breaches
- Documentation of all violations and remediations

---

## 9. COMPLIANCE REQUIREMENTS

### 9.1 SOC 2 Trust Services Criteria
- **CC6.1:** Logical access security
- **CC6.2:** Access removal
- **CC6.3:** Access review
- **CC6.4:** Authentication

### 9.2 Evidence Collection
- Access request forms
- Access review records
- Authentication logs
- Privileged access monitoring reports

---

## 10. ROLES AND RESPONSIBILITIES

| Role | Responsibility |
|------|----------------|
| Identity & Access Management Team | Account provisioning, deprovisioning |
| IT Security | Policy enforcement, monitoring |
| Department Managers | Access approval, quarterly certification |
| HR | Termination notifications, role changes |
| Internal Audit | Annual access control audit |

---

## 11. POLICY EXCEPTIONS

Exceptions must be:
- Documented with business justification
- Approved by CISO (standard) or CEO (privileged)
- Time-bound with expiration date
- Reviewed quarterly

---

## APPROVAL

| Role | Name | Signature | Date |
|------|------|-----------|------|
| CISO | | | |
| IT Director | | | |
| HR Director | | | |
