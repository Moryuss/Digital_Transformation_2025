# Conti Ransomware

Ransomware is malicious software designed to deny users access to their data or systems by encrypting files and demanding payment,typically in cryptocurrency, for their restoration.

## Mitre ATT&CK framework analysis

###  Initial Access - TA0001
Techniques that use various entry vectors to gain their initial foothold within a network. 
- Spearphishing campaigns using tailored emails that contain malicious attachments [T1566.001] or malicious links [T1566.002];
- Stolen or weak Remote Desktop Protocol (RDP) credentials [T1078]
- Phone calls;
- Fake software promoted via search engine optimization;
- Other malware distribution networks (e.g., ZLoader); 
- Common vulnerabilities in external assets.

Mitre ATT&CK techniques used:
Valid Accounts - T1078
Phishing: Spearphishing Attachment - T1566.001
Phishing: Spearphishing Attachment - T1566.001

### Execution - TA0002
The adversary is trying to run malicious code.
To be more descreete they got a used uid of another process. Then they run the malicious payload.
Scan of the network and Brute Force [T1110] of routers, cameras, nw-storage.
Kerberos Attacks [T1558.003] are used to get an Admin Hash and do Bruteforce attacks to discover the password.

Mitre ATT&CK techniques used:
Command and Scripting Interpreter: Windows Command Shell - T1059.003
Native Application Programming Interface (API) - T1106
### Persistance - TA0003
The adversary is trying to maintain their foothold.
Conti used legitimate monitor services and management sw as backdoors to keep persistance.

Mitre ATT&CK techniques used:
Valid Accounts - T1078
External Remote Services - T1133
### Privilage Escalation - TA0004
The adversary is trying to gain higher-level permissions.
Thanks to the observation they manged to escalate their privileges.
They obtained these by
- bruteforcing hashes
- SW vulnerabilities [e.g: Windows SMB vulns, Printers vulns, Active Directory vulns] 

Mitre ATT&CK techniques used:
Process Injection: Dynamic-link Library Injection - T1055.001
### Defense Evasion - TA0005
Mitre ATT&CK techniques used:
Obfuscated Files or Information - T1027
Process Injection: Dynamic-link Library Injection - T1055.001
Deobfuscate/Decode Files or Information - T1140
###  Lateral Movement - TA0008
Techniques that adversaries use to enter and control remote systems on a network.
They Searched and found other devices and moved trough the networks

Mitre ATT&CK techniques used:
Remote Services: SMB/Windows Admin Shares - T1021.002 	
Taint Shared Content - T1080


###  Exfiltration - TA0010
Techniques that adversaries may use to steal data from your network
Conti used Rclone as exfiltration medium, an open-source command [*The Swiss army knife of cloud storage*].

# CAPEC - Common Attack Pattern Enumeration and Classification - How a weakness could be exploited
How to leverage CVE for attacks, so most CAPEC entries has an execution flow.

Execution flows generally have three phases:

    Explore: This phase describes various way to find a potential target to attack. All three phases sometimes include more than one step. Each step suggests various techniques for performing that step.
    Experiment: Once a target has been found, techniques in the experiment phase of the execution flow suggest various ways to determine if this target contains the weakness that this CAPEC entry wishes to exploit.
    Exploit: Suggested techniques for conducting the actual attack.

CAPEC entries are presented using views, which are pre-defined arrangements of all the CAPEC entries.
- The “Mechanisms of Attack” view, which can be used to focus on CAPEC entries that can be used to attack **different realm** of cyber security.
- The “Domains of Attack” view, which groups together **similar attack methods**.


## In depth 
Let's see how some Attacks can be mapped to CAPEC patterns:

### Process Injection: Dynamic-link Library Injection - T1055.001
CAPEC-641: DLL Side-Loading
CAPEC-471: Search Order Hijacking

### Taint Shared Content - T1080
CAPEC-562: Modify Shared File

### Brute Force - T1110
CAPEC-112: Brute Force
CAPEC-16: Dictionary-based Password Attack

## ATT&CK Flow
[Conti flow](https://center-for-threat-informed-defense.github.io/attack-flow/ui/?src=https%3A//center-for-threat-informed-defense.github.io/attack-flow/corpus/Conti%20CISA%20Alert.afb)

A flow on how the Conti Ransomware managed to attack, 
