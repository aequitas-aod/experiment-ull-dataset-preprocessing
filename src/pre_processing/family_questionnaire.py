import os
import pandas as pd
from src.pre_processing.macros import (
    column_groups,
    DATA_PATH,
    DATA_SPLIT_PATH,
    ORIGINAL_DATASET_NAME,
)


def main():
    # Loading student questionnaire
    df = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "family_questionnaire.csv"), low_memory=False
    )
    df = df.set_index("id_student")

    # Load identifiers and change float columns to int
    ids = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "identifiers.csv"), low_memory=False
    )
    ids = ids.set_index("id_student")
    int_identifiers = [col for col in ids.columns if col not in ["id_class_group"]]
    ids[int_identifiers] = ids[int_identifiers].astype("Int64")

    # Merge identifiers and student questionnaire
    df = pd.merge(ids, df, left_index=True, right_index=True)

    numeric_columns = df.select_dtypes(include='number')
    means = numeric_columns.mean().round()
    family_df = df.fillna(means)

    ##############################
    # Deletion of columns
    ##############################
    family_df = family_df.drop('mother_education', axis=1)
    family_df = family_df.drop('father_education', axis=1)
    family_df = family_df.drop('inmigrant', axis=1)
    family_df = family_df.drop('inmigrant2', axis=1)
    family_df = family_df.drop('inmigrant_second_gen', axis=1)
    family_df = family_df.drop('f8ta', axis=1)
    family_df = family_df.drop('f8tm', axis=1)
    family_df = family_df.drop('f11', axis=1)
    family_df = family_df.drop('f13n', axis=1)
    family_df = family_df.drop('f22', axis=1)
    family_df = family_df.drop('f24a', axis=1)
    family_df = family_df.drop('f24b', axis=1)
    family_df = family_df.drop('f33a', axis=1)
    family_df = family_df.drop('f33b', axis=1)
    family_df = family_df.drop('f33c', axis=1)
    family_df = family_df.drop('f33d', axis=1)
    family_df = family_df.drop('f33e', axis=1)
    family_df = family_df.drop('f33f', axis=1)
    family_df = family_df.drop('f33g', axis=1)
    family_df = family_df.drop('f33h', axis=1)
    family_df = family_df.drop('single_parent_household', axis=1)
    family_df = family_df.drop('household_income_q', axis=1)

    ##############################
    # Renaming of columns
    ##############################
    family_df = family_df.rename(columns={'f0': 'respondent'})
    family_df = family_df.rename(columns={'f1n': 'number_of_people_in_household'})
    family_df = family_df.rename(columns={'f2an': 'mother_age'})
    family_df = family_df.rename(columns={'f2bn': 'father_age'})
    family_df = family_df.rename(columns={'f3a': 'mother_education_level'})
    family_df = family_df.rename(columns={'f3b': 'father_education_level'})
    family_df = family_df.rename(columns={'f4a': 'mother_employment_status'})
    family_df = family_df.rename(columns={'f4b': 'father_employment_status'})
    family_df = family_df.rename(columns={'f5a': 'mother_place_of_birth'})
    family_df = family_df.rename(columns={'f5b': 'father_place_of_birth'})
    family_df = family_df.rename(columns={'f5n': 'student_place_of_birth'})
    family_df = family_df.rename(columns={'f6': 'years_in_spanish_education_system'})
    family_df = family_df.rename(columns={'f7': 'language_spoken_at_home'})
    family_df = family_df.rename(columns={'f13n': 'number_of_school_meetings'})
    family_df = family_df.rename(columns={'f20': 'school_recommendation'})
    family_df = family_df.rename(columns={'f21n': 'homework_hours_a_week'})
    family_df = family_df.rename(columns={'f23': 'parental_education_expectations'})
    family_df = family_df.rename(columns={'f30': 'number_of_children_in_household'})
    family_df = family_df.rename(columns={'f31': 'type_of_family_unit'})
    family_df = family_df.rename(columns={'f34': 'monthly_household_income'})

    ##############################
    # Aggregation of columns
    ##############################
    # Aggregation by making mean of the value of all fields measuring the level of reading and literature in the home
    family_df['lecture_at_home_score'] = family_df[['f9a', 'f9b', 'f9c', 'f9h', 'books']].agg('mean', axis=1)
    family_df = family_df.drop(['f9a', 'f9b', 'f9c', 'f9h', 'books'], axis=1)

    # Aggregation by performing mean of the value of all fields that measure the level of technology and
    # electronic devices in the home
    family_df['tech_at_home_score'] = family_df[['f9d', 'f9e', 'f9f', 'f9g', 'f10n']].agg('mean', axis=1)
    family_df = family_df.drop(['f9d', 'f9e', 'f9f', 'f9g', 'f10n'], axis=1)

    # Aggregation that specifies how much students see reading and how much parents read to their children
    family_df['see_adult_read'] = family_df[['f12a', 'f12b']].agg('mean', axis=1)
    family_df = family_df.drop(['f12a', 'f12b'], axis=1)

    # Aggregation by making the sum of all visits the student receives, from mother, father, and other relatives
    family_df['visit_in_school_by_people'] = family_df[['f14a', 'f14b', 'f14c']].agg('mean', axis=1)
    family_df = family_df.drop(['f14a', 'f14b', 'f14c'], axis=1)

    # Aggregation of average parental interest in interviews
    family_df['interest_in_interview'] = family_df[['f15a', 'f15b', 'f15c', 'f15d', 'f15e', 'f15f']].agg('mean', axis=1)
    family_df = family_df.drop(['f15a', 'f15b', 'f15c', 'f15d', 'f15e', 'f15f'], axis=1)

    # Aggregation by averaging the help they receive at home from parents
    family_df['support_at_home'] = family_df[['f16a', 'f16b', 'f16c', 'f16d', 'f16e', 'f16f']].agg('mean', axis=1)
    family_df = family_df.drop(['f16a', 'f16b', 'f16c', 'f16d', 'f16e', 'f16f'], axis=1)

    # Aggregation by averaging the frequency of participation by parents in school activities
    family_df['parent_involved_in_school_activities'] = family_df[['f17a', 'f17b', 'f17c', 'f17d']].agg('mean', axis=1)
    family_df = family_df.drop(['f17a', 'f17b', 'f17c', 'f17d'], axis=1)

    # Aggregation by averaging parents satisfaction about the school
    family_df['family_satisfaction'] = family_df[
        ['f18a', 'f18b', 'f18c', 'f18d', 'f18e', 'f18f', 'f18g', 'f18h', 'f18i']].agg('mean', axis=1)
    family_df = family_df.drop(['f18a', 'f18b', 'f18c', 'f18d', 'f18e', 'f18f', 'f18g', 'f18h', 'f18i'], axis=1)

    # Aggregation by averaging satisfaction from parents with teachers
    family_df['teacher_satisfaction'] = family_df[['f19a', 'f19b', 'f19c', 'f19d', 'f19e']].agg('mean', axis=1)
    family_df = family_df.drop(['f19a', 'f19b', 'f19c', 'f19d', 'f19e'], axis=1)

    family_df.to_csv("../../data/pre_processed/family_questionnaire_pre_processed.csv", index=True)


if __name__ == "__main__":
    main()
