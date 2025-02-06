# Anti-ARA

This framework is used to measure the ability of dynamic analysis tools to resist and handle Anti-Runtime Analysis (ARA) technology in Android applications.

## Dataset and Reproducibility

The dataset used in our study consists of 1,000 benign and 1,000 malicious Android APKs. The analysis reports for each sample are available in the `Dataset` folder in this repository. 

To facilitate reproducibility, you can obtain the corresponding APK samples by using the unique hash values of each sample, which are provided in the analysis reports. These APKs can be retrieved from **AnDroZoo** (https://androzoo.uni.lu/).

### How to Access the Dataset

1. Navigate to the [AnDroZoo](https://androzoo.uni.lu/).
2. Use the unique hash values from the analysis reports in the `Dataset` folder to download the corresponding benign and malicious APK samples.

## Usage Instructions

1. Put the APKs you wish to analyze in the `apks` directory.
2. Run `autoacv.py` to start the analysis.

This setup allows you to replicate the experiments and evaluate the effectiveness of dynamic analysis tools in handling ARA technologies.



