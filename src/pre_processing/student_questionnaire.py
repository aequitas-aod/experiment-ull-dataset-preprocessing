import os

import pandas as pd

from macros import (
    column_groups,
    DATA_PATH,
    DATA_SPLIT_PATH,
    DATA_PREPROC_PATH,
    ORIGINAL_DATASET_NAME,
)


def main():

    # Loading student questionnaire
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
        "living_in_foster": ["a3f"],
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

    to_rename = {
        "gender": "a1",
        "birth_year": "a2",
        "repeat": "a4",
        "skip": "a5",
        "homeworks": "a7",
        "country_iso_cnac": "birth_country",
        "country_iso_nac": "nazionality_country",
    }

    df = df.rename(columns={v: k for k, v in to_rename.items()})

    # print(df)

    to_aggregate = {
        "frequency_of_computer": ["mean", ["a8a", "a8b", "a8c"]],
        "frequency_of_internet": [
            "mean",
            ["a9a", "a9b", "a9c", "a9d", "a9e", "a9f", "a9g"],
        ],
        "work_with_teachers": [
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
                "a10k",
                "a10l",
                "a10m",
                "a10n",
            ],
        ],
        "materials_in_class": [
            "mean",
            [
                "a11a",
                "a11b",
                "a11c",
                "a11d",
                "a11e",
                "a11f",
                "a11g",
                "a11h",
            ],
        ],
        "evaluation": [
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
        "teacher_performance": [
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
        "class_vibe": [
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

    to_lambdate = {
        "living_with": lambda x: (
            0  # "BOTH_PARENTS"
            if x["living_with_father_mother"] == 1.0 and x["a3d"] == 2.0  # only parents
            else (
                1  # "BOTH_PARENTS_RELATIVES"
                if x["living_with_father_mother"] == 1.0
                and x["a3d"] == 1.0  # parents and relatives
                else (
                    2  # "SINGLE_PARENT"
                    if x["a3a"] + x["a3b"] == 3.0
                    and x["a3d"] == 2.0  # one parent and no relatives
                    else (
                        3  # "SINGLE_PARENT_RELATIVES"
                        if x["a3a"] + x["a3b"] == 3.0
                        and x["a3d"] == 1.0  # one parent and no relatives
                        else (
                            4  # "ONLY_RELATIVES"
                            if x["a3a"] + x["a3b"] == 4.0
                            and x["a3d"] == 1.0  # one parent and no relatives
                            else (5)  # "OTHER"
                        )
                    )
                )
            )
        ),
        "classmate_relationships": lambda x: (
            x[
                [
                    "a14a",
                    "a14b",
                    "a14g",
                    "a14h",
                ]
            ].sum()
            + (
                4 * 5
                - x[
                    [
                        "a14c",
                        "a14d",
                        "a14e",
                        "a14f",
                    ]
                ].sum()
            )
        )
        / 8,
        "school": lambda x: (
            x[
                [
                    "a17a",
                    "a17b",
                    "a17c",
                    "a17e",
                    "a17f",
                    "a17g",
                    "a17h",
                ]
            ].sum()
            + (5 - x["a17d"])
        )
        / 8,
        "math": lambda x: (
            x[["a20a", "a20e"]].sum() + (3 * 5 - x[["a20b", "a20c", "a20d"]].sum())
        )
        / 5,
    }

    for new_column, lambda_rule in to_lambdate.items():
        df[new_column] = df.apply(lambda_rule, axis=1)

    # print(df)

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
        "repeater",
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
        # classroom_condition
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
        # teacher_relationship
        "a13a",
        "a13b",
        "a13c",
        "a13d",
        "a13e",
        # classmate_relationships
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
        "a166f",
        #
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
        # classes
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
        "a17h",
        #
        "a171h",
        # math
        "a20a",
        "a20b",
        "a20c",
        "a20d",
        "a20e",
        # reading
        "a21a",
        "a21b",
        "a21c",
        "a21d",
        "a21e",
        #
        "a211a",
        # natural_sciences
        "a22a",
        "a22b",
        "a22c",
        "a22d",
        #
        "a222b",
        # misc
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
        # next_studies
        "a24",
        # social_media
        "a40a",
        "a40b",
        "a40c",
        "a40d",
        # activity
        "a111a",
        # english
        "a160k",
        "a162k",
        "a163k",
        "a166k",
    ]

    df = df.drop(to_drop, axis=1)

    # print(df)

    df.to_csv(os.path.join(DATA_PREPROC_PATH, "student_questionnaire.csv"))


if __name__ == "__main__":
    main()
