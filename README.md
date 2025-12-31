# script-analyze-tweetmilei
# Milei Securitization Discourse Analysis

## Overview

This repository contains the Python analysis code and data processing scripts used in the doctoral thesis **"Building the Enemy: 
Mapping Securitization Discourse in Milei's Argentina (2022-2025)"** by Davide Butti, analyzing Javier Milei's political discourse.

## Research Context

The thesis examines how Argentine libertarian populist leader Javier Milei constructed security narratives through strategic identification and mobilization of internal and external enemies during his rise to power (2022-2025). This computational analysis focuses on systematic discourse analysis of 8,383 tweets across four critical years.


## Key Features

### Security Intensity Score Calculation

The analysis employs systematic keyword-counting methodology to measure securitization intensity:

```python
Security Intensity Score = Total Enemy Keywords + Total Economic Keywords + Total War Keywords
```

### Analytical Categories

**Enemy Categories:**
- La casta (the political class)
- Kirchnerismo (Peronist movement)
- State apparatus
- Media
- Progressives
- International actors
- Social movements

**Economic Securitization Frames:**
- Fiscal terrorism
- Emergency language
- Crisis/existential threats

**Supporting Frames:**
- War/military language
- Liberty frames

```

## Requirements

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.10.0
```

## Disclaimer

This is academic research analyzing public political discourse. All tweets analyzed were publicly available. The analysis represents scholarly interpretation and does not constitute political endorsement.

---

**Last Updated:** January 2025  
**Status:** Thesis submission version  
**Python Version:** 3.9+
