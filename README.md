# Anti-ARA

This framework is used to measure the ability of dynamic analysis tools to resist and handle Anti-Runtime Analysis (ARA) technology in Android applications.

## Dataset and Reproducibility

The dataset used in our study consists of 993 benign and 991 malicious Android APKs. The analysis reports for each sample are available in the `Dataset` folder in this repository. 

To facilitate reproducibility, you can obtain the corresponding APK samples by using the unique hash values of each sample, which are provided in the analysis reports. These APKs can be retrieved from **AnDroZoo** (https://androzoo.uni.lu/).

### How to Access the Dataset

1. Navigate to the [AnDroZoo](https://androzoo.uni.lu/).
2. Use the unique hash values from the analysis reports in the `Dataset` folder to download the corresponding benign and malicious APK samples.

## Usage Instructions

1. Put the APKs you wish to analyze in the `apks` directory.
2. Run `autoacv.py` to start the analysis.

This setup allows you to replicate the experiments and evaluate the effectiveness of dynamic analysis tools in handling ARA technologies.


# Investigated Tools Overview

In this section, we provide an overview of all the investigated dynamic analysis tools. The tools are categorized based on their availability, relevance, and the reasons why they were selected or excluded from the study.

# Investigated Tools Overview

In this section, we provide an overview of all the investigated dynamic analysis tools. The tools are categorized based on their availability, relevance, and the reasons why they were selected or excluded from the study.

## Tools Summary

| **Category**                          | **Tool Name**                                                                 |
|---------------------------------------|-------------------------------------------------------------------------------|
| **Not Available**                     | TaintART, De-LADY, DL-Droid, DirectDroid, EnDroid, Droid-AntiRM, Ninja, Bolt, SMARTGEN, Deep4maldroid, Harvester, ARTist, DroidADDMiner, Dagger, Boxify, Droid-sec, DroidTrace, DroidTrack, SCSdroid, VetDroid, MADAM, ProfileDroid, Crowdroid, CRePE, Dexmonitor, GroddDroid, juGULAR, AppsPlayground, Puma, TriggerScope, Difuzer, Curiousdroid |
| **Not Relevant to Dynamic Analysis**  | Humanoid, ADAMANT, EHBDroid, Stoat, DroidBot, IntelliDroid, Dynodroid, Monkey, Active, Flowdroid, sapienz |
| **Cannot Be Reproduced / Not Working**| TaintDroid, DroidHook, CuckooDroid, FuzzDroid, Malton, Maline, BareDroid, ConDroid, AndroidHooker, SwiftHand, DroidScope, AppAudit, NDroid |
| **Links Inaccessible**                | ARTDroid, Copperdroid, EvoDroid                                               |
| **Selected Tools**                    | DroidDissector, DroidCat, APIMonitor, ESdroid, AndroidSlicer, T-Recs           |

## Further Explanation

- **Not Available**: These tools were included in the original investigation but could not be used due to unavailability. Some of them are no longer maintained, or the authors did not provide any working links.
- **Not Relevant**: These tools were excluded from our study because they do not align with the focus and scope of this research.
- **Cannot Be Reproduced / Not Working**: We encountered issues when trying to reproduce the results using these tools. They failed to work on our setup, and therefore could not be used in the study.
- **Links Inaccessible**: Some tools had broken or outdated access links, making it impossible to download and use them.
- **Selected Tools**: These are the tools that we ultimately selected for our study.




