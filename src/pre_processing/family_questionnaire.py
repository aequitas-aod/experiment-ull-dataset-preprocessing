from src.pre_processing import *
from src.pre_processing.macros import (
    column_groups,
    DATA_PATH,
    DATA_SPLIT_PATH,
    DATA_PREPROC_PATH,
    ORIGINAL_DATASET_NAME,
)


def preprocess_family_questionnaire(load=False):

    if load:
        df = pd.read_csv(os.path.join(DATA_PREPROC_PATH, "family_questionnaire.csv"))
        return df.set_index("id_student")

    # Loading student questionnaire
    df = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "family_questionnaire.csv"), low_memory=False
    )
    family_df = df.set_index("id_student")

    # Load identifiers and change float columns to int
    # ids = pd.read_csv(
    #     os.path.join(DATA_SPLIT_PATH, "identifiers.csv"), low_memory=False
    # )
    # ids = ids.set_index("id_student")
    # int_identifiers = [col for col in ids.columns if col not in ["id_class_group"]]
    # ids[int_identifiers] = ids[int_identifiers].astype("Int64")

    # Merge identifiers and student questionnaire

    # family_df = pd.merge(ids, df, left_index=True, right_index=True)

    ##############################
    # Deletion of columns
    ##############################
    family_df = family_df.drop("mother_education", axis=1)
    family_df = family_df.drop("father_education", axis=1)
    family_df = family_df.drop("inmigrant", axis=1)
    family_df = family_df.drop("inmigrant2", axis=1)
    family_df = family_df.drop("inmigrant_second_gen", axis=1)
    family_df = family_df.drop("f8ta", axis=1)
    family_df = family_df.drop("f8tm", axis=1)
    family_df = family_df.drop("f9a", axis=1)
    family_df = family_df.drop("f9e", axis=1)
    family_df = family_df.drop("f9g", axis=1)
    family_df = family_df.drop("books", axis=1)
    family_df = family_df.drop("f13n", axis=1)
    family_df = family_df.drop("f14c", axis=1)
    family_df = family_df.drop("f22", axis=1)
    family_df = family_df.drop("f24a", axis=1)
    family_df = family_df.drop("f24b", axis=1)
    family_df = family_df.drop("single_parent_household", axis=1)
    family_df = family_df.drop("f33a", axis=1)
    family_df = family_df.drop("f33b", axis=1)
    family_df = family_df.drop("f33c", axis=1)
    family_df = family_df.drop("f33d", axis=1)
    family_df = family_df.drop("f33e", axis=1)
    family_df = family_df.drop("f33f", axis=1)
    family_df = family_df.drop("f33g", axis=1)
    family_df = family_df.drop("f33h", axis=1)
    family_df = family_df.drop("household_income_q", axis=1)
    family_df = family_df.drop("nhousehold", axis=1)

    ##############################
    # Renaming of columns
    ##############################
    family_df = family_df.rename(columns={"f0": "respondent"})
    family_df = family_df.rename(columns={"f1n": "number_of_people_in_household"})
    family_df = family_df.rename(columns={"f2an": "mother_age"})
    family_df = family_df.rename(columns={"f2bn": "father_age"})
    family_df = family_df.rename(columns={"f3a": "mother_education_level"})
    family_df = family_df.rename(columns={"f3b": "father_education_level"})
    family_df = family_df.rename(columns={"f4a": "mother_employment_status"})
    family_df = family_df.rename(columns={"f4b": "father_employment_status"})
    family_df = family_df.rename(columns={"f5a": "mother_place_of_birth"})
    family_df = family_df.rename(columns={"f5b": "father_place_of_birth"})
    family_df = family_df.rename(columns={"f5n": "student_place_of_birth"})
    family_df = family_df.rename(
        columns={"f6": "degree_of_years_in_spanish_education_system"}
    )
    family_df = family_df.rename(columns={"f7": "language_spoken_at_home"})
    family_df = family_df.rename(columns={"f10n": "number_of_tech_at_home"})
    family_df = family_df.rename(columns={"f11": "extent_of_books_at_home"})
    family_df = family_df.rename(
        columns={"start_schooling_age": "degree_of_start_schooling_age"}
    )
    family_df = family_df.rename(columns={"f14a": "visits_in_school_by_mother"})
    family_df = family_df.rename(columns={"f14b": "visits_in_school_by_father"})
    family_df = family_df.rename(columns={"f20": "has_been_recommended_school"})
    family_df = family_df.rename(columns={"f21n": "number_of_homework_hours_a_week"})
    family_df = family_df.rename(columns={"f23": "parental_education_expectations"})
    family_df = family_df.rename(columns={"f30": "number_of_children_in_household"})
    family_df = family_df.rename(columns={"f31": "type_of_family_unit"})
    family_df = family_df.rename(columns={"f34": "monthly_household_income"})
    # family_df = family_df.rename(
    #     columns={"nhousehold": "number_of_people_in_household"}
    # )

    ##############################
    # Custom transformations of columns
    ##############################

    family_df["respondent"] = family_df["respondent"].apply(
        lambda x: (
            "MOTHER"
            if x == 1
            else ("FATHER" if x == 2 else ("OTHER" if x == 3 else np.nan))
        )
    )

    for col in [
        "mother_place_of_birth",
        "father_place_of_birth",
        "student_place_of_birth",
    ]:
        family_df[col] = family_df[col].apply(
            lambda x: (
                "CANARY_ISLANDS"
                if x == 1
                else (
                    "SPAIN_NO_CANARY_ISLANDS"
                    if x == 2
                    else (
                        "ANOTHER_EU"
                        if x == 3
                        else ("ANOTHER_NON_EU" if x == 4 else np.nan)
                    )
                )
            )
        )

    family_df["language_spoken_at_home"] = family_df["language_spoken_at_home"].apply(
        lambda x: "SPANISH" if x == 1 else ("OTHER" if x == 2 else np.nan)
    )

    for col in ["visits_in_school_by_mother", "visits_in_school_by_father"]:
        family_df[col] = family_df[col].apply(
            lambda x: (
                "NEVER"
                if x == 1
                else (
                    "SOMETIMES"
                    if x == 2
                    else (
                        "ONCE_PER_MONTH"
                        if x == 3
                        else (
                            "ONCE_PER_WEEK"
                            if x == 4
                            else ("DONT_KNOW" if x == 5 else np.nan)
                        )
                    )
                )
            )
        )

    family_df["has_been_recommended_school"] = (
        family_df["has_been_recommended_school"]
        .apply(lambda x: 0 if x == 2 else x)
        .astype("boolean")
    )

    family_df["parental_education_expectations"] = family_df[
        "parental_education_expectations"
    ].apply(
        lambda x: (
            "4_ESO"
            if x == 1
            else (
                "INT_FP"
                if x == 2
                else (
                    "BACH_ATO"
                    if x == 3
                    else (
                        "UP_FP"
                        if x == 4
                        else (
                            "BACH_DEG"
                            if x == 5
                            else ("DONT_KNOW" if x == 9 else np.nan)
                        )
                    )
                )
            )
        )
    )

    family_df["type_of_family_unit"] = family_df["type_of_family_unit"].apply(
        lambda x: (
            "MOTHER_FATHER_CHILDREN"
            if x == 1
            else (
                "MOTHER_PARTNER_CHILDREN"
                if x == 2
                else (
                    "FATHER_PARTNER_CHILDREN"
                    if x == 3
                    else (
                        "MOTHER_CHILDREN"
                        if x == 4
                        else (
                            "FATHER_CHILDREN"
                            if x == 5
                            else (
                                "RELATIVES_CHILDREN"
                                if x == 6
                                else ("OTHERS" if x == 7 else np.nan)
                            )
                        )
                    )
                )
            )
        )
    )

    family_df["monthly_household_income"] = family_df["monthly_household_income"].apply(
        lambda x: (
            "NO_INCOME"
            if x == 1
            else (
                "UP_TO_500"
                if x == 2
                else (
                    "UP_TO_1000"
                    if x == 3
                    else (
                        "UP_TO_1500"
                        if x == 4
                        else (
                            "UP_TO_2000"
                            if x == 5
                            else (
                                "UP_TO_2500"
                                if x == 6
                                else (
                                    "UP_TO_3000"
                                    if x == 7
                                    else (
                                        "UP_TO_3500"
                                        if x == 8
                                        else (
                                            "MORE_THAN_3500"
                                            if x == 9
                                            else ("NO_ANSWER" if x == 10 else np.nan)
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )

    ##############################
    # Aggregation of columns
    ##############################
    # Aggregation by making mean of the value of all fields measuring the level of reading and literature in the home
    family_df["frequency_of_books_at_home"] = family_df[["f9b", "f9c", "f9h"]].agg(
        "mean", axis=1
    )
    family_df = family_df.drop(["f9b", "f9c", "f9h"], axis=1)

    # Aggregation by performing mean of the value of all fields that measure the level of technology and
    # electronic devices in the home
    family_df["frequency_of_tech_at_home"] = family_df[["f9d", "f9f"]].agg(
        "mean", axis=1
    )
    family_df = family_df.drop(["f9d", "f9f"], axis=1)

    # Aggregation that specifies how much students see reading and how much parents read to their children
    family_df["frequency_of_see_adult_read"] = family_df[["f12a", "f12b"]].agg(
        "mean", axis=1
    )
    family_df = family_df.drop(["f12a", "f12b"], axis=1)

    # Aggregation by making the sum of all visits the student receives, from mother, father, and other relatives
    # family_df["frequency_of_visit_in_school_by_people"] = family_df[
    #     ["f14a", "f14b"]
    # ].agg("mean", axis=1)
    # family_df = family_df.drop(["f14a", "f14b"], axis=1)

    # Aggregation of average parental interest in interviews
    family_df["extent_of_interest_in_interview"] = family_df[
        ["f15a", "f15b", "f15d", "f15f"]
    ].agg("mean", axis=1)
    family_df = family_df.drop(["f15a", "f15b", "f15c", "f15d", "f15e", "f15f"], axis=1)

    # Aggregation by averaging the help they receive at home from parents
    family_df["frequency_of_support_at_home"] = family_df[
        ["f16a", "f16b", "f16c", "f16d", "f16e", "f16f"]
    ].agg("mean", axis=1)
    family_df = family_df.drop(["f16a", "f16b", "f16c", "f16d", "f16e", "f16f"], axis=1)

    # Aggregation by averaging the frequency of participation by parents in school activities
    family_df["frequency_of_parent_involved_in_school_activities"] = family_df[
        ["f17a", "f17b", "f17c", "f17d"]
    ].agg("mean", axis=1)
    family_df = family_df.drop(["f17a", "f17b", "f17c", "f17d"], axis=1)

    # Aggregation by averaging parents satisfaction about the school
    family_df["extent_of_family_satisfaction"] = family_df[
        ["f18a", "f18b", "f18e", "f18f", "f18g", "f18h"]
    ].agg("mean", axis=1)
    family_df = family_df.drop(
        ["f18a", "f18b", "f18c", "f18d", "f18e", "f18f", "f18g", "f18h", "f18i"], axis=1
    )

    # Aggregation by averaging satisfaction from parents with teachers
    family_df["extent_of_teacher_satisfaction"] = family_df[
        ["f19a", "f19b", "f19c", "f19d", "f19e"]
    ].agg("mean", axis=1)
    family_df = family_df.drop(["f19a", "f19b", "f19c", "f19d", "f19e"], axis=1)

    df.to_csv(os.path.join(DATA_PREPROC_PATH, "family_questionnaire.csv"))

    return family_df
