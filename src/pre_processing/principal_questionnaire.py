from src.pre_processing import *
from src.pre_processing.macros import DATA_SPLIT_PATH, DATA_PREPROC_PATH


def preprocess_principal_questionnaire(drop_row: bool = False) -> pd.DataFrame:

    # Loading student questionnaire
    df = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "principal_questionnaire.csv"), low_memory=False
    )
    df = df.set_index("id_student")

    # Load identifiers and change float columns to int
    # ids = pd.read_csv(
    #     os.path.join(DATA_SPLIT_PATH, "identifiers.csv"), low_memory=False
    # )
    # ids = ids.set_index("id_student")
    # int_identifiers = [col for col in ids.columns if col not in ["id_class_group"]]
    # ids[int_identifiers] = ids[int_identifiers].astype("Int64")

    ############################################################################
    # Delete rows with all NaN values (823 rows)
    ############################################################################
    if drop_row:
        nan_rows = df.isnull().all(axis=1)
        df = df[~nan_rows]

    ############################################################################
    # Delete rows with all NaN values but island, capital_island and public_private (7227 rows)
    ############################################################################
    if drop_row:
        nan_rows = (
            df.drop(columns=["island", "capital_island", "public_private"])
            .isnull()
            .all(axis=1)
        )
        df = df[~nan_rows]

    ############################################################################
    # Merge from d16an to d16fn (values from 0 to 2000).
    # Merge function: sum.
    # Treat missing values as NaN.
    # Drop columns after merging.
    # d16an: School resources. Available computers
    # d16bn: School resources. Available computers to students
    # d16cn: School resources. Available computers to teachers
    # d16dn: School resources. Computers for the administrative management of the school
    # d16en: School resources. Tablets/laptops available to students
    # d16fn: School resources. Interactive digital whiteboards or touch screens in classrooms
    ############################################################################

    d16_columns = [f"d16{n}n" for n in "abcdef"]
    df = merge_columns(
        df,
        d16_columns,
        sum_merge_strategy,
        leave_nan_strategy,
        "number_of_school_resources",
    )

    ############################################################################
    # Merge from d17a to d17h (values from 1 to 4).
    # Merge function: mean.
    # Leave missing values as NaN.
    # Drop columns after merging.
    # d17a: Factors that limit the effectiveness of my management. Lack of budget and resources
    # d17b: Factors that limit the effectiveness of my management. Lack of attendance of the teachers
    # d17c: Factors that limit the effectiveness of my management. Lack of participation and support of families
    # d17d: Factors that limit the effectiveness of my management. Lack of teacher training plan in my school for teachers
    # d17e: Factors that limit the effectiveness of my management. Lack of opportunities/support for professional development of the management team
    # d17f: Factors that limit the effectiveness of my management. Lack of agility to cover teacher absences
    # d17g: Factors that limit the effectiveness of my management. Lack of coordination between members of the management team
    # d17h: Factors that limit the effectiveness of my management. Lack of autonomy to make decisions
    ############################################################################

    d17_columns = [f"d17{n}" for n in "abcdefgh"]
    df = merge_columns(
        df,
        d17_columns,
        mean_merge_ignore_nan_strategy,
        leave_nan_strategy,
        "degree_of_factors_limiting_effectiveness",
    )

    ############################################################################
    # Merge from d18a to d18n (values from 1 to 4).
    # Merge function: mean.
    # Leave missing values as NaN.
    # Drop columns after merging.
    # d18a: It is an inconvenience in your school: Lack of good/qualified teachers
    # d18b: It is an inconvenience in your school: Lack of teachers trained to teach students with special educational needs
    # d18c: It is an inconvenience in your school: Lack or inadequate teaching material
    # d18d: It is an inconvenience in your school: Lack or inadequacy of technological devices for teaching
    # d18e: It is an inconvenience in your school: Poor internet connection
    # d18f: It is an inconvenience in your school: Lack or inadequacy of software for teaching
    # d18g: It is an inconvenience in your school: Lack or inadequacy of library materials
    # d18h: It is an inconvenience in your school: Lack of support teachers
    # d18i: It is an inconvenience in your school: Lack of administrative staff
    # d18j: It is an inconvenience in your school: Lack of adequate infrastructure
    # d18k: It is an inconvenience in your school: Lack of teacher collaboration
    # d18l: It is an inconvenience in your school: Lack of collaboration from families
    # d18m: It is an inconvenience in your school: Administrative bureaucracy
    # d18n: It is an inconvenience in your school: Lack of computers in the classroom or for students.
    ############################################################################

    d18_columns = [f"d18{n}" for n in "abcefghijklmn"]
    df = merge_columns(
        df,
        d18_columns,
        mean_merge_ignore_nan_strategy,
        leave_nan_strategy,
        "degree_of_inconveniences",
    )

    ############################################################################
    # Merge from d19a to d19r (values from 1 to 4).
    # Merge function: sum.
    # Leave missing values as NaN.
    # Drop columns after merging.
    # d19a: It is a problem in your school because of the students: Arriving late to the school
    # d19b: It is a problem in your school because of the students: Absenteeism (unexcused absences)
    # d19c: It is a problem in your school because of the students: Disruption of order in class
    # d19d: It is a problem in your school because of the students: Vandalism and theft
    # d19e: It is a problem in your school because of the students: Inappropriate or profanity language
    # d19f: It is a problem in your school because of the students: Intimidation or insults between students or another type of bullying
    # d19g: It is a problem in your school because of the students: Physical aggressions between students
    # d19h: It is a problem in your school because of the students: Lack of respect to teachers
    # d19i: It is a problem in your school because of the students: Intimidation or insults to the teachers or staff of the school
    # d19j: It is a problem in your school because of the teachers: Arriving late to the school
    # d19k: It is a problem in your school because of the teachers: absenteeism (unexcused absences)
    # d19l: It is a problem in your school because of the teachers: Lack of respect towards the students
    # d19m: It is a problem in your school because of the teachers: Lack of respect between teachers
    # d19n: It is a problem in your school because of the teachers: Discrimination based on sex
    # d19o: It is a problem in your school because of the families: Lack of collaboration with the school
    # d19p: It is a problem in your school because of the families: Criticism and opposition to the rules of the school
    # d19q: It is a problem in your school because of the families: Lack of respect towards the teachers and staff of the school
    # d19r: It is a problem in your school because of the families: Lack of respect or discrimination towards other families
    ############################################################################

    d19_columns = [f"d19{n}" for n in "abcdefghijklmnopqr"]
    df = merge_columns(
        df,
        d19_columns,
        mean_merge_ignore_nan_strategy,
        leave_nan_strategy,
        "degree_of_problems",
    )

    ############################################################################
    # Merge from d20a to d20l (values from 1 to 4).
    # Merge function: mean.
    # Leave missing values as NaN.
    # Drop columns after merging.
    # d20a: To what extent does the management of the school: Helps to establish good relations between teachers
    # d20b: To what extent does the management of the school: Take into account the opinions of the teaching staff
    # d20c: To what extent does the management of the school: Stimulate teachers to develop innovative ideas
    # d20d: To what extent does the management of the school: Create a strong sense of identity in the community with the objectives of the school
    # d20e: To what extent does the management of the school: Promote teamwork among teachers
    # d20f: To what extent does the management of the school: Promotes the maximum use of capacities and teacher knowledge
    # d20g: To what extent does the management of the school: Generates procedures for teacher training courses
    # d20h: To what extent does the management of the school: Uses student educational outcomes/achievement to set school goals
    # d20i: To what extent does the management of the school: Checks that the work of teachers is in accordance with the objectives of the school
    # d20j: To what extent does the management of the school: Encourage that teaching practice is based on recent research developments
    # d20k: To what extent does the management of the school: Follow up on disruptive problems in the classrooms
    # d20l: To what extent does the management of the school: Discuss the educational objectives of the school with teachers
    ############################################################################

    d20_columns = [f"d20{n}" for n in "abcdefghijkl"]
    df = merge_columns(
        df,
        d20_columns,
        mean_merge_ignore_nan_strategy,
        leave_nan_strategy,
        "degree_of_management",
    )

    ############################################################################
    # Merge from d21a to d21f (values from 1 to 4).
    # Merge function: mean.
    # Leave missing values as NaN.
    # Drop columns after merging.
    # d21a: Satisfaction level: With teachers
    # d21b: Satisfaction level: With students
    # d21c: Satisfaction level: With families
    # d21d: Satisfaction level: With CEP associates
    # d21e: Satisfaction level: With guidance teams (EOEP)
    # d21f: Satisfaction level: With educational inspection
    ############################################################################

    d21_columns = [f"d21{n}" for n in "abcdef"]
    df = merge_columns(
        df,
        d21_columns,
        mean_merge_ignore_nan_strategy,
        leave_nan_strategy,
        "degree_of_satisfaction",
    )

    ############################################################################
    # Merge from d22a to d22f (values from 1 to 4).
    # Merge function: mean.
    # Leave missing values as NaN.
    # Drop columns after merging.
    # d22a: Degree of agreement: The staff of the school share a common methodological line
    # d22b: Degree of agreement: There is a high level of cooperation between the school and the local community
    # d22c: Degree of agreement: School staff speak openly about difficulties in carrying out their teaching work
    # d22d: Degree of agreement: There is mutual respect for the ideas of colleagues
    # d22e: Degree of agreement: There is a culture of sharing successes and failures
    # d22f: Degree of agreement: Relations between teachers and students are good
    ############################################################################

    d22_columns = [f"d22{n}" for n in "abcdef"]
    df = merge_columns(
        df,
        d22_columns,
        mean_merge_ignore_nan_strategy,
        leave_nan_strategy,
        "degree_of_agreement",
    )

    ############################################################################
    # Drop columns with all missing values (should be 0)
    ############################################################################

    df.dropna(axis=1, how="all", inplace=True)

    ############################################################################
    # Merge columns d30[abdef] with d30[13456] since they refer to the same question
    # The nan values of the first group are filled with non nan values of the second group
    # This operation is done pair wise (e.g., d30a with d301)
    # After that the second group is dropped
    ############################################################################

    d30x_columns = [f"d30{n}" for n in "abdef"]
    d30y_columns = [f"d30{n}" for n in "13456"]
    for x, y in zip(d30x_columns, d30y_columns):
        df[x].fillna(df[y], inplace=True)
    df.drop(columns=d30y_columns, inplace=True)

    ############################################################################
    # Drop columns with more than 600% of missing values (each pair year-grade is 100%)
    # So in total there are 10 pairs year-grade (1000%)
    # Drop from d9d1 to d9h2, d10[abc], d12an, d13n, distnac, distnac_eso4, distnac_pri3, distnac_pri6
    ############################################################################

    d9xy_columns = [f"d9{n}{m}" for n in "defgh" for m in "12"]
    d10_columns = [f"d10{n}" for n in "abc"]
    columns_to_drop = (
        d9xy_columns
        + d10_columns
        + ["d12an", "d13n", "distnac", "distnac_eso4", "distnac_pri3", "distnac_pri6"]
    )
    df.drop(columns=columns_to_drop, inplace=True)

    ############################################################################
    # Renaming of columns
    ############################################################################
    replace_dict = {
        "d1": "sex",
        "d2n": "age",
        "d3n": "years_of_teaching",
        "d4n": "years_in_school",
        "d5n": "years_as_principal",
        "d6n": "years_as_principal_in_school",
        "d7n": "class_hours_per_week",
        "d8n": "number_of_principlas_10_years",
        "d9a1": "number_of_students",
        "d9a2": "number_of_groups",
        "d9b1": "number_of_preschool_students",
        "d9b2": "number_of_preschool_groups",
        "d9c1": "number_of_primary_students",
        "d9c2": "number_of_primary_groups",
        "d11an": "abroad_students_country_no_spanish",
        "d11bn": "abroad_students_country_spanish",
        "d12bn": "teachers_in_school",
        "d14": "teachers_changed_school_last_year",
        "d15": "attitude_teacher_training_courses",
        "d30a": "group_criteria_alphabet",
        "d30b": "group_criteria_gender",
        "d30c": "group_criteria_language",
        "d30d": "group_criteria_performance",
        "d30e": "group_criteria_homogeneity",
        "d30f": "group_criteria_heterogeneity",
        "d31a": "degree_of_agreement_satisfaction_students_results",
        "d31b": "degree_of_agreement_expected_students_results",
        "d31c": "degree_of_agreement_students_improvement",
        "d32a": "school_teacher_training_plan",
        "d33a": "school_teacher_training_plan_main_theme",
        "d121a": "number_of_teachers_1_education",
        "d121b": "number_of_mandatory_teachers_2_education",
        "d131a": "number_of_teachers_1_education_more_5_years",
        "d131b": "number_of_mandatory_teachers_2_education_more_5_years",
        "d302": "group_criteria_random",
        "d307": "group_criteria_subjects",
        "d308": "group_criteria_other",
        "tasa_nac_eso4": "rate_4_grade_mandatory_2_education_students_different_nationality",
        "tasa_nac_pri3": "rate_3_grade_mandatory_2_education_students_different_nationality",
        "tasa_nac_pri6": "rate_6_grade_mandatory_2_education_students_different_nationality",
        "groups": "number_of_groups_evaluated_grade",
        "island": "island",
        "capital_island": "capital_island",
        "public_private": "public_or_private",
    }
    df = df.rename(columns=replace_dict)

    df.to_csv(os.path.join(DATA_PREPROC_PATH, "principal_questionnaire.csv"))
    return df
