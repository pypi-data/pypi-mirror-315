# Introduction

---

This repository include Python scripts that transform raw sensor data collected from Android mobile devices into features of interest for analysis. 

**Current research topic**: identify contextual prompt-level factors that predict response or no response in microEMA. 

**Statistical methodology**: multi-level modeling

**Outcomes**: compliance rate

**Predictors**: 

- Within-person or prompt level: 
  - time of the day
  - day of the week
  - day in study
  - activity level
  - battery level
  - location

- Between-person or person level
  - age
  - gender
  - study mode

# Exploratory Discussions on Factors

---  
  
Detailed discussions on factors can be found [here](https://docs.google.com/presentation/d/1u_p3DPljLYUxwfPMLncl004VjWGq7K16nDx_XGsYmR8/edit?usp=sharing).

# Features Overview

---
**Smartphone**  

| Outcome              | Variable Type                                                                                                                  | Data Source                                                |
| ---------------------|--------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| Answer Status        | Categorical (Completed, CompletedThenDismissed, PartiallyCompleted, Started/NeverStarted, NeverPrompted, OverwrittenByDaily)   | ./logs/PromptResponses.log.csv                             |


| Feature              | Level                                     | Effect Type | Variable Type                                     | Data Source                                                |
| ---------------------|-------------------------------------------|-------------|---------------------------------------------------|------------------------------------------------------------|
| Day of the Week      | Level 1 (Within-person or prompt level)   | Random      | Categorical (Mon-Sat: 0-6)                        | ./logs/.../PromptResponses.log.csv                   |
| Time of the Day      | Level 1 (Within-person or prompt level)   | Random      | Categorical (morning, afternoon, evening/night)   | ./logs/.../PromptResponses.log.csv                   |
| Days in Study        | Level 1 (Within-person or prompt level)   | Random      | Numeric (numeric value of day from the first day) | ./logs (start from the first date of created folder) |
| Battery Level        | Level 1 (Within-person or prompt level)   | Random      | Numeric (Battery%)                                | ./data/.../Battery.##.event.csv                      |
| Charging Status      | Level 1 (Within-person or prompt level)   | Random      | Binary (True/False)                               | ./data/.../Battery.##.event.csv                      |
| Location (LOC)       | Level 1 (Within-person or prompt level)   | Random      | [Latitude, Longitude]                             | ./data/.../GPS.csv                                         |
| Phone Lock           | Level 1 (Within-person or prompt level)   | Random      | Binary (Phone Locked/Phone Unlocked)              | ./data/.../AppEventCounts.csv                              |
| Last Phone Usage Duration| Level 1 (Within-person or prompt level)   | Random  | Numeric (minutes)                                 | ./data/.../AppEventCounts.csv                              |
| Screen Status        | Level 1 (Within-person or prompt level)   | Random      | Binary (Screen On/Screen Off)                     | ./logs/.../SystemBroadcastReceiver.csv                     |
| Wake/Sleep Time      | Level 1 (Within-person or prompt level)   | Random      | Local time (2021-01-01 06:30:00 CST)              | daily report                                               |


---
**Smartwatch**  

| Outcome              | Level                                     | Effect Type | Variable Type                                     | Data Source                                                |
| ---------------------|-------------------------------------------|-------------|---------------------------------------------------|------------------------------------------------------------|
| Compliance Rate      | Level 1 (Within-person or prompt level)   | Random      | Numeric                                           | ./logs-watch/PromptResponses.log.csv                       |
|                      | Level 2 (Between-person or person level)  | Random      |                                                   |                                                            |


| Feature              | Level                                     | Effect Type | Variable Type                                     | Data Source                                                |
| ---------------------|-------------------------------------------|-------------|---------------------------------------------------|------------------------------------------------------------|
| Day of the Week      | Level 1 (Within-person or prompt level)   | Random      | Categorical (Mon-Sat: 0-6)                        | ./logs-watch/.../PromptResponses.log.csv                   |
| Time of the Day      | Level 1 (Within-person or prompt level)   | Random      | Categorical (morning, afternoon, evening/night)   | ./logs-watch/.../PromptResponses.log.csv                   |
| Days in Study        | Level 1 (Within-person or prompt level)   | Random      | Numeric (numeric value of day from the first day) | ./logs-watch (start from the first date of created folder) |
| Battery Level        | Level 1 (Within-person or prompt level)   | Random      | Numeric (Battery%)                                | ./data-watch/.../Battery.##.event.csv                  |
| Location (LOC)       | Level 1 (Within-person or prompt level)   | Random      |                                                   |                                                            |
| Activity Level (ACT) | Level 1 (Within-person or prompt level)   | Random      |                                                   |                                                            |



# Code Usage for Feature Matrix Generation

---
1. This project has been wrapped up as a [Pypi package](https://pypi.org/project/microt-compliance/). Use pip to install.
2. Clone this project and run locally.
```
#!python
python main_ema.py [intermediate_participant_path] [output_dir_path] [date_in_study] [decryption_password]
```
e.g., python main_ema.py G:\...\intermediate_file\participant_id C:\...\output_folder 2021-01-01 password  

**Special Notice**  
- Delete misc folder before running code, if new participants' intermediate folder has been created.
