# Disadvantaged Students Use Case

The Canarian Agency for Quality Assessment and Accreditation (ACCUEE) gathers data to assess the performance of the Canary Islands' educational system through periodic diagnostic reports. This database has information from four academic years (2015-2019). The diagnostic involves two components: 1) evaluating students' academic performance in different subjects (Mathematics, Spanish Language, and English), and 2) administering context questionnaires to students, school principals, families, and teachers.

The data collection process is structured as follows: School principals receive envelopes containing information for each student along with instructions for conducting the academic performance exams. Each envelope includes a numeric code and a QR code for student identification. Academic exams take place in computer rooms, where students input their numeric codes to proceed with each subject's test. The exams are overseen by a committee of teachers, excluding the class tutor and the teacher of the subject being evaluated.

For family and student context questionnaires, students take the envelopes home. Families and students can access and complete the questionnaires using the QR code. Principals and teachers follow a similar process for their context questionnaires. The collected data is anonymized, preserving the confidentiality of individuals and schools, revealing only the province where students attend school.

## General tasks

- Select relevant subsets of features
- Dimensionality reduction
- Feature aggregation/engineering
    - need to aggregate information about school personnel
- Missing data imputation

## Goals (all per subject):

1. [High] select N best students for admission
- ranking problem
    - classification problem
        - avoid sampling the same student more than once

2. [Med] identify below-threshold students which are at risk of drop off
- identify threshold in a data-driven way
    - inferring drop-offs from the data
    - consider historical information about each student
- regression/classification problem

3. [High] identify below-threshold students which are at risk remaining under-performing
- identify definition of under-performing
- regression/classification problem

4. [High] predicting the future score of a student
- classification problem

5. [Low] finding the most likely explanation for under-performance?


## Questions

### Old

- Why multiple IDs?
- How did you select important feature?

### Joseph

- studenti  con stesso id_student_16_19  -> stesso studente OK
- studenti  con stesso id_student_original -> stesso studente NO
    - forse l'identificativo  è id_student_original + id_school
- dipendenza id_school + id_year -> preside SNI
    - dalle analisi manuali SI ma non confermato da quelle automatiche (penso sia un problema di qualità dei dati: alcune tuple hanno – per qualche ragione – alcuni campi con valore diverso)

Perchè stesso studente in anni diversi (stesso id_student_16_19) ha diverso id_school nonostante id_school_16_19 sia uguale? Cos'è id_school se cambia? Anche id_student_original cambia!


## Aggregations

average amount of students per teacher