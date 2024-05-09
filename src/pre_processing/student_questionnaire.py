from src.pre_processing import *
from src.pre_processing.macros import (
    column_groups,
    DATA_PATH,
    DATA_SPLIT_PATH,
    DATA_PREPROC_PATH,
    ORIGINAL_DATASET_NAME,
)


def preprocess_student_questionnaire():

    # Loading student questionnaire
    print("\t\tLoading data")

    df = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "student_questionnaire.csv"), low_memory=False
    )
    df = df.set_index("id_student")

    # # Load identifiers and change float columns to int
    # ids = pd.read_csv(
    #     os.path.join(DATA_SPLIT_PATH, "identifiers.csv"), low_memory=False
    # )
    # ids = ids.set_index("id_student")
    # int_identifiers = [col for col in ids.columns if col not in ["id_class_group"]]
    # ids[int_identifiers] = ids[int_identifiers].astype("Int64")

    # # Load identifiers and change float columns to int
    # scores = pd.read_csv(
    #     os.path.join(DATA_SPLIT_PATH, "student_scores.csv"), low_memory=False
    # )
    # scores = scores.set_index("id_student")

    # # Merge identifiers, scores, and student questionnaire
    # ids = pd.merge(ids, scores, left_index=True, right_index=True)
    # df = pd.merge(ids, df, left_index=True, right_index=True)

    # print(df)

    groups = {
        "gender": ["a1"],
        "birth_year": ["a2"],
        "living_with": [
            "a3a",
            "a3b",
            "living_with_father_mother",
            "a3c",
            "a3d",
            "a3et",
            "a3f",
        ],
        "repeat": [
            "a4",
            "repeater",
            #
            "a41",
            "a42",
        ],
        "skip": ["a5", "a51"],
        "homeworks": [
            "a6nm",
            "a7",
            #
            "a61",
            "a71",
        ],
        "frequency_of_computer": ["a8a", "a8b", "a8c"],
        "classroom_condition": ["a09a", "a09b", "a09c", "a09d", "a09e"],
        "frequency_of_internet": ["a9a", "a9b", "a9c", "a9d", "a9e", "a9f", "a9g"],
        "work_with_teachers": [
            "a10a",
            "a10b",
            "a10c",
            "a10d",
            "a10e",
            "a10f",
            "a10g",
            "a10h",
            "a10i",
            "a10j",
            "a10k",
            "a10l",
            "a10m",
            "a10n",
        ],
        "materials_in_class": [
            "a11a",
            "a11b",
            "a11c",
            "a11d",
            "a11e",
            "a11f",
            "a11g",
            "a11h",
        ],
        "evaluation": [
            "a12a",
            "a12b",
            "a12c",
            "a12d",
            "a12e",
            "a12f",
            "a12g",
            "a12h",
            "a12i",
        ],
        "teacher_relationship": ["a13a", "a13b", "a13c", "a13d", "a13e"],
        "classmate_relationships": [
            "a14a",
            "a14b",
            "a14c",
            "a14d",
            "a14e",
            "a14f",
            "a14g",
            "a14h",
            #
            "a141g",
            "a144d",
            "a144h",
            "166f",
            #
            "a177d",
        ],
        "teacher_performance": [
            "a15a",
            "a15b",
            "a15c",
            "a15d",
            "a15e",
            "a15f",
            "a15g",
            "a15h",
            "a15i",
            "a15j",
        ],
        "class_vibe": [
            "a16a",
            "a16b",
            "a16c",
            "a16d",
            "a16e",
            "a16f",
            "a16g",
            "a16h",
        ],
        "classes": ["a16i", "a16j", "a16k", "a16l"],
        "school": [
            "a17a",
            "a17b",
            "a17c",
            "a17d",
            "a17e",
            "a17f",
            "a17g",
            "a17h",
            #
            "a171h",
        ],
        "math": ["a20a", "a20b", "a20c", "a20d", "a20e"],
        "reading": [
            "a21a",
            "a21b",
            "a21c",
            "a21d",
            "a21e",
            #
            "a211a",
        ],
        "natural_sciences": [
            "a22a",
            "a22b",
            "a22c",
            "a22d",
            #
            "a222b",
        ],
        "misc": [
            "a23a",
            "a23b",
            "a23c",
            "a23d",
            "a23e",
            "a23f",
            "a23g",
            "a23h",
            "a23i",
            "a23j",
            "a23k",
        ],
        "next_studies": ["a24"],
        "social_media": ["a40a", "a40b", "a40c", "a40d"],
        "activity": ["a111a"],
        "english": ["a160k", "a162k", "a163k", "a166k"],
        "birth_country": ["country_iso_cnac"],
        "nazionality_country": ["country_iso_nac"],
    }

    # Renaming
    print("\t\tRenaming")

    to_rename = {
        "gender": "a1",
        "birth_year": "a2",
        "is_living_with_mother": "a3a",
        "is_living_with_father": "a3b",
        "is_living_with_sibling": "a3c",
        "is_living_with_other_relatives": "a3d",
        "has_repeated": "repeater",
        "frequency_of_skips": "a5",
        "homeworks_day_per_week": "a7",
        "extent_of_teachers_affinity": "a13e",
        "birth_country": "country_iso_cnac",
        "nazionality_country": "country_iso_nac",
        "weight": "subsample_fair_weight",
    }

    df = df.rename(columns={v: k for k, v in to_rename.items()})

    # print(df)

    # Aggregating
    print("\t\tAggregating")
    print("\t\t\tSimple")

    to_aggregate = {
        "frequency_of_computer_usage": ["mean", ["a8a", "a8b", "a8c"]],
        "frequency_of_internet_usage": [
            "mean",
            ["a9a", "a9b", "a9c", "a9d", "a9e", "a9g"],
        ],
        "frequency_of_work_with_teachers": [
            "mean",
            [
                "a10a",
                "a10b",
                "a10c",
                "a10d",
                "a10e",
                "a10f",
                "a10g",
                "a10h",
                "a10i",
                "a10j",
                # "a10k",
                # "a10l",
                # "a10m",
                # "a10n",
            ],
        ],
        "frequency_of_materials_in_class": [
            "mean",
            [
                "a11a",
                "a11b",
                "a11c",
                "a11d",
                "a11e",
                "a11f",
                # "a11g",
                "a11h",
            ],
        ],
        "frequency_of_evaluations": [
            "mean",
            [
                "a12a",
                "a12b",
                "a12c",
                "a12d",
                "a12e",
                "a12f",
                "a12g",
                "a12h",
                "a12i",
            ],
        ],
        "extent_of_teacher_performance": [
            "mean",
            [
                "a15a",
                "a15b",
                "a15c",
                "a15d",
                "a15e",
                "a15f",
                "a15g",
                "a15h",
                "a15i",
                "a15j",
            ],
        ],
        "extent_of_class_env": [
            "mean",
            [
                "a16a",
                "a16b",
                "a16c",
                "a16d",
                "a16e",
                "a16f",
                "a16g",
                "a16h",
            ],
        ],
    }

    for new_column, aggregation_details in to_aggregate.items():
        df[new_column] = df[aggregation_details[1]].agg(aggregation_details[0], axis=1)

    # print(df)

    print("\t\t\tGood/Bad")

    max_degree_of_agreement = 4
    aggregation_map = {
        "good": {
            "extent_of_classmates_affinity": [
                "a14a",
                "a14b",
                "a14g",
                "a14h",
            ],
            "extent_of_school_satisfaction": [
                "a17a",
                "a17b",
                "a17c",
                "a17e",
                "a17h",
            ],
            "extent_of_math_affinity": ["a20a", "a20e"],
            "extent_of_reading_affinity": ["a21b"],
        },
        "bad": {
            "extent_of_classmates_affinity": [
                # "a14c",
                "a14d",
                "a14e",
                "a14f",
            ],
            "extent_of_school_satisfaction": ["a17d"],
            "extent_of_math_affinity": ["a20b", "a20c", "a20d"],
            "extent_of_reading_affinity": ["a21c", "a21d", "a21e"],
        },
    }

    def get_good_bad_agg(row, group):
        # if row[aggregation_map["good"][group]].isna().sum() == len(aggregation_map["good"][group]):
        #     print("#### RAW GOOD  ####")
        #     print(row[aggregation_map["good"][group]])
        #     print("#### RAW BAD  ####")
        #     print(row[aggregation_map["bad"][group]])

        #     print("#### SUM GOOD  ####")
        #     print(row[aggregation_map["good"][group]].sum())
        #     print("#### SUM BAD  ####")
        #     print(row[aggregation_map["bad"][group]].sum())
        #     print()
        #     print(
        #         (
        #             row[aggregation_map["good"][group]].sum()
        #             + (
        #                 (
        #                     len(aggregation_map["bad"][group])
        #                     * (max_degree_of_agreement + 1)
        #                 )
        #                 - row[aggregation_map["bad"][group]].sum()
        #             )
        #         )
        #         / (
        #             len(aggregation_map["good"][group])
        #             + len(aggregation_map["bad"][group])
        #         )
        #     )
        #     print()
        #     print()

        no_good = (
            len(aggregation_map["good"][group])
            - row[aggregation_map["good"][group]].isna().sum()
        )
        no_bad = (
            len(aggregation_map["bad"][group])
            - row[aggregation_map["bad"][group]].isna().sum()
        )

        if no_good == 0 and no_bad == 0:
            return np.nan
        else:
            return (
                row[aggregation_map["good"][group]].sum()
                + (
                    (no_bad * (max_degree_of_agreement + 1))
                    - row[aggregation_map["bad"][group]].sum()
                )
            ) / (no_good + no_bad)

    # Custom (Lambda)
    print("\t\tLambda")

    to_lambdate = {
        "gender": lambda x: "MALE" if x == 1 else ("FEMALE" if x == 2 else np.nan),
        "is_living_with_mother": lambda x: 0 if x == 2 else x,
        "is_living_with_father": lambda x: 0 if x == 2 else x,
        "is_living_with_siblings": lambda x: 0 if x == 2 else x,
        "is_living_with_other_relatives": lambda x: 0 if x == 2 else x,
        "has_repeated": lambda x: 0 if x == 1 else (1 if x == 2 else np.nan),
        "extent_of_classmates_affinity": lambda x: get_good_bad_agg(
            x, group="extent_of_classmates_affinity"
        ),
        "extent_of_school_satisfaction": lambda x: get_good_bad_agg(
            x, group="extent_of_school_satisfaction"
        ),
        "extent_of_math_affinity": lambda x: get_good_bad_agg(
            x, group="extent_of_math_affinity"
        ),
        "extent_of_reading_affinity": lambda x: get_good_bad_agg(
            x, group="extent_of_reading_affinity"
        ),
    }

    for new_column, lambda_rule in to_lambdate.items():
        df[new_column] = df.apply(lambda_rule, axis=1)

    print("\t\tConverting to booleans")
    to_boolean = [
        "has_repeated",
        "is_living_with_mother",
        "is_living_with_father",
        "is_living_with_sibling",
        "is_living_with_other_relatives",
    ]
    for column in to_boolean:
        df[column] = df[column].astype("boolean")

    # print(df)

    # Dropping
    print("\t\tDropping")

    to_drop = [
        # living_with
        "a3a",
        "a3b",
        "living_with_father_mother",
        "a3c",
        "a3d",
        "a3et",
        # living_in_foster
        "a3f",
        # repeat
        "a4",
        "a41",
        "a42",
        # skip
        "a51",
        # homeworks
        "a6nm",
        "a61",
        "a71",
        # frequency_of_computer
        "a8a",
        "a8b",
        "a8c",
        # classroom_condition for too many missing values
        "a09a",
        "a09b",
        "a09c",
        "a09d",
        "a09e",
        # frequency_of_internet
        "a9a",
        "a9b",
        "a9c",
        "a9d",
        "a9e",
        "a9f",
        "a9g",
        # work_with_teacher
        "a10a",
        "a10b",
        "a10c",
        "a10d",
        "a10e",
        "a10f",
        "a10g",
        "a10h",
        "a10i",
        "a10j",
        "a10k",
        "a10l",
        "a10m",
        "a10n",
        # materials_in_class
        "a11a",
        "a11b",
        "a11c",
        "a11d",
        "a11e",
        "a11f",
        "a11g",
        "a11h",
        # evaluation
        "a12a",
        "a12b",
        "a12c",
        "a12d",
        "a12e",
        "a12f",
        "a12g",
        "a12h",
        "a12i",
        # teacher_relationship for too many missing values
        "a13a",
        "a13b",
        "a13c",
        "a13d",
        # "a13e",
        # classmate_relationships
        "a14a",
        "a14b",
        "a14c",
        "a14d",
        "a14e",
        "a14f",
        "a14g",
        "a14h",
        # drop for too many missing values
        "a141g",
        "a144d",
        "a144h",
        "a166f",
        # #
        "a177d",
        # teacher_performance
        "a15a",
        "a15b",
        "a15c",
        "a15d",
        "a15e",
        "a15f",
        "a15g",
        "a15h",
        "a15i",
        "a15j",
        # class_vibe
        "a16a",
        "a16b",
        "a16c",
        "a16d",
        "a16e",
        "a16f",
        "a16g",
        "a16h",
        # classes for too many missing values
        "a16i",
        "a16j",
        "a16k",
        "a16l",
        # school
        "a17a",
        "a17b",
        "a17c",
        "a17d",
        "a17e",
        "a17f",
        "a17g",
        # drop for too many missing values
        "a17h",
        #
        "a171h",
        # math
        "a20a",
        "a20b",
        "a20c",
        "a20d",
        "a20e",
        # reading for too many missing values
        "a21a",
        "a21b",
        "a21c",
        "a21d",
        "a21e",
        #
        "a211a",
        # natural_sciences for too many missing values
        "a22a",
        "a22b",
        "a22c",
        "a22d",
        # #
        "a222b",
        # misc for too many missing values
        "a23a",
        "a23b",
        "a23c",
        "a23d",
        "a23e",
        "a23f",
        "a23g",
        "a23h",
        "a23i",
        "a23j",
        "a23k",
        # next_studies for too many missing values
        "a24",
        # social_media for too many missing values
        "a40a",
        "a40b",
        "a40c",
        "a40d",
        # activity for too many missing values
        "a111a",
        # english for too many missing values
        "a160k",
        "a162k",
        "a163k",
        "a166k",
        # birth_country for too many missing values
        # "country_iso_cnac",
        # nazionality_country for too many missing values
        # "country_iso_nac",
        # weight for too many missing values
        # "weight",
    ]

    df = df.drop(to_drop, axis=1)

    # print(df)

    # Saving
    print("\t\tSaving")

    df.to_csv(os.path.join(DATA_PREPROC_PATH, "student_questionnaire.csv"))
    return df
