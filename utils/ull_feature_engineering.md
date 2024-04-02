# Feature Engineering

## Student Questionnaire

### a1, a2 [Sex, Birth year]:
	- a1
		- missing values = 4%
		- corr score_LEN = 0.15
	- a2
		- missing values = 34%
		- corr score_LEN < 0.06
### a3a, a3b, living_with_father_mother, a3c, a3d, a3et [Living with]:
	- a3a, a3b, living_with_father_mother, a3c, a3d
		- missing values between 39% and 68%
		- corr < 0.1
	- a3f all nans
### a4, repeater, a5 [Repeat year, Skip class]:
	- a4, repeter
		- missing values = 20%
		- corr between 0.17 and 0.25
	- a5
		- missing values = 20%
		- corr < 0.15
### a6nm, a7 [Homeworks]:
	- a6nm:
		- missing values = 65%
		- corr < 0.4
	- a7
		- missing values = 19%
		- corr < 0.8
### a8a, a8b, a8c [Computer frequency]:
	- missing values < 20%
	- corr < 0.07
### a09a, a09b, a09c, a09d, a09e [Classroom condition]
	- missing values = 92%
	- corr < 0.1

## Liam's Suggesstions
ideas about which features to combine:

	- combine features from d16an to d16fn to compute school's resources
	- combine features from d17a to d17h to compute factors that limits the principal's ability to manage the school
	- combine features from d18a to d18n to compute school's inconveniences
	- combine features from d19a to d19r to compute school's problems due to students and teachers' behaviour (actually this can be summarised into two features)
	- combine features from d20a to d20l to compute positive effects of the school management
	- combine features from d21a to d21f to compute satisfaction level
	- combine features from p27b to p27h to compute how a teacher's work is hampered in general
	- combine features from p34a to p34g to compute how much the school management is invested in allowing teachers to flourish
	- same for features from p311a to p311h to get an idea of how good the relations between different people in the school are
	- same for features from p7an to p7gn (exluding p7fn) to compute the total number of students with cognitve conditions that might make their teaching more challenging and potentially less effective for everyone
	- same for features from p21a to p21f to evaluate how invested/motivated the students are in their learning
	- same for features from p24a to p24k to evaluate how meticolous the teacher is in their work, specifically when it comes to evaluating the students
	- same for features from p32a to p32e to evaluate the teacher's overall opinion on the school they work in
	- same for features from d18a to d18n to evaluate the amount of inconveniences that a school principal has to face
	- same for features from f14a to f14c to evaluate how often a student is visited during school by people they know
	- same for features from f16a to f16f to evaluate the "school" support a student receives by their family when at home
	- same for features from f17a to f17d to estimate how frequently the parent is involved in school activities
		- they are important features so it might not be right to aggregate them
	- same for features from f18a to f18h to estimate a parent's degree of satisfaction towards the school in general (same as f18i? scales would be different)
	- same for features from f19a to f19e to estimate a parent's overall degree of satisfaction towards the teacher
	- same for features from f33a to f33f to estimate the overall sources of income for the family
		- binary
	- same for features from a09a to a09e to estimate the overall behaviour of the class
	- same for features from a13a to a13e to estimate how positively the class view their relationship with the teacher
	- same for features from a14c to a14f to estimate how negative the relationship between the student and the rest of the class is
		- important features
	- same for features a14b, a14g, a14h to estimate how positive the relationship between the student and the rest of the class is
		- important features

