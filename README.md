UPI Fraud Detection with Behavioral Profiling


This project simulates a UPI transaction dashboard to detect potential fraudulent activities. The system uses behavioral profiling and anomaly detection techniques to identify unusual patterns in user transactions. It compares the current transaction behavior with the user’s historical transaction patterns to calculate Z-scores for key features like amount and hour.

Key features of the project include:

1. Behavioral Profiling: Tracks typical transaction patterns (e.g., amount, hour) to understand what is "normal" for a user.

2. Anomaly Detection: Flags transactions that deviate significantly from the normal behavior based on calculated Z-scores.

3. Real-Time Alerts: Notifies users of suspicious activity when the Z-scores of a transaction are beyond a certain threshold.

4. Visual Score Interpretation: Displays a bar plot that highlights the deviation from the user’s historical behavior, helping users easily interpret if a transaction is out of the ordinary.

This system aims to enhance security by providing real-time fraud detection using simple but effective methods like Z-score visualization, allowing users to easily see how their transaction compares to past behavior.
