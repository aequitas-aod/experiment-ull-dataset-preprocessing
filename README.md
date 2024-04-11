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

***RAW***

- studenti  con stesso id_student_16_19  -> stesso studente OK
- studenti  con stesso id_student_original -> stesso studente NO
    - forse l'identificativo  è id_student_original + id_school
- dipendenza id_school + id_year -> preside SNI
    - dalle analisi manuali SI ma non confermato da quelle automatiche (penso sia un problema di qualità dei dati: alcune tuple hanno – per qualche ragione – alcuni campi con valore diverso)

- Perchè stesso studente in anni diversi (stesso id_student_16_19) ha diverso id_school nonostante id_school_16_19 sia uguale? Cos'è id_school se cambia? Anche id_student_original cambia!

- from a9a to a9g, le attività si devono intendere come svolte con il docente o come trasgressione?

***ELABORATED***

*IDs*

- We say that id_student_16_19 identifies a student because, when we find the same id_student_16_19 in two different rows, we know that they correspond to the same student in different years (i.e., 16-19 respectivelly). For the same rows, id_school_16_19 is also the same. Yet, for the same identical rows, if we look at id_student_original and id_school, they differ. Why so?
- Analogously, id_student_original seem to not identify a student uniquely, does id_student_original identify a student only when id_school is taken in consideration as well? (i.e., two rows have been filled by the same student when they have the same id_stiudent_original and id_school)
- Does the identifier for principals work the same? Can we say that id_school + id_year identify the principal in charge for a certain school in a certain year? (i.e., two rows have been filled by the same principal when they have the same id_school and id_year, assuming that different grades -- in the same school and year -- have the same principal)

*Student Questionnaire*

- What does the weight column refer to?


## Aggregations

average amount of students per teacher