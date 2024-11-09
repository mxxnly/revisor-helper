<h1>Documentation for the "Revisor Helper" Project</h1>
Revisor Helper is a web tool designed to assist auditors (revisors) in reporting their work efficiently. The main goal is to streamline the process of documenting audit results, automating records, and generating reports.

<h2>Website: https://mxxnly.cloud</h2>

<h1>Features Overview</h1>

1. Assigning Stores to Auditors <br>
The admin interface allows assigning specific stores to auditors for inspection.
Once the auditor completes their inspection, they log the results (e.g., item counts, inventory details), which are saved to the database.
After submission, the store is moved to the bottom of the available store list, ready for future inspections.


2. Queue Order for Stores<br>
Stores are organized in a queue based on the last inspection date and time.
This feature ensures an even distribution of inspections, prioritizing stores that haven’t been checked recently.

3. Store Ratings and Multimedia Attachments<br>
Auditors can rate stores and add photos or videos to their reports.
This functionality allows for better documentation of store conditions and issues, providing a visual record.

5. Auditor Information Page<br>
A dedicated page displays detailed information on each auditor, including the number of stores inspected within the month, audits of remote locations, and more.
Real-time updates help managers easily track auditor performance.

6. Work Hours and Salary Tracking<br>
Auditors can log their work hours daily, including the number of hours worked and brief task notes.
The system calculates the auditor’s monthly salary based on logged hours and an hourly rate.
A summary dashboard shows auditors their hours worked, tasks completed, and estimated salary, with a calendar view for reviewing logged hours per day.

7. Auditor Reports<br>
The system generates reports for auditors with an integrated monthly calendar.
The calendar displays daily audit counts, giving a clear view of each auditor’s productivity throughout the month.
A monthly progress chart also allows for easy evaluation of work goals.





<h2>Additional Information</h2> <br>
<b>Technology Stack</b>: Django (backend), HTML, CSS, JS (frontend), SQLite (database). <br>
<b>Authentication</b>: Simple username/password authentication. <br>
<b>Interface</b>: Dark theme with a glassmorphism effect. <br>
<b>Deployment</b>: Configured for VPS hosting on Hostinger, ensuring reliability and accessibility. <br>
<h3>Deployment Details</h3> <br>
<b>Web Server</b>: Nginx <br>
<b>Application Server</b>: Gunicorn <br>
<b>Database</b>: SQLite <br>
