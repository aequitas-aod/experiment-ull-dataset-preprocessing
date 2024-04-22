# This file describes the choices made for preprocessing the "family" portion of the dataset.

## Elimination of non-relevant columns
- _mother_education_: removed, derived from column f3a;
- _father_education_: removed, derived from column f3b;
- _inmigrant_: removed, derived from column f5n;
- _inmigrant2_: removed, derived from column f5n;
- _inmigrant_second_gen_: removed, derived from column f5n;
- _f6_: removed, too much missing data;
- _f8ta_: removed, as there is a better aggregated column: "_start_schooling_age_";
- _f8tm_: removed, as there is a better aggregated column: "_start_schooling_age_";
- _f11_: removed, the column "_books_" provides the same informative content, better;
- _f13_: removed, too much missing data;
- _f22_: removed, the column is very similar to _"f21n"_
- _f24a_: removed, duplicate of _mother_occupation_
- _f24b_: removed, duplicate of _father_occupation_
- _parent_household_: removed, duplicate of _f31_
- household_income_q: removed, we calculate a custom value based on previous columns for income

## Aggregation of columns
- _f9a_ -> _f10n_ and _books_: aggregated into 2 new columns "_lecture_at_home_score_" and "_tech_at_home_score_"
  - for both scores, a simple sum of values related to "reading" and a sum of values related to "technology" was performed.
- _f12a_ and _f12b_: aggregated into a new column "_see_adult_read_"
  - a sum operation applied
- _f13n_ -> _f14c_: aggregated into a new column "_visit_in_school_by_people_"
  - a sum operation applied
- _f15a_ -> _f15f_: aggregated into a new column "_interest_in_interview_"
  - to calculate this column, the average of values regarding the family's interest in various aspects was taken.
- _f16a_ -> _f16f_: aggregated into a new column "_support_at_home_"
  - to calculate this column, the average of values to understand the average support the family provides at home was taken.
- _f17a_ -> _f17d_: aggregated into a new column "_parent_involved_in_school_activities_"
  - a mean operation applied
- _f18a_ -> _f18i_: aggregated into a new column "_family_satisfaction_"
  - a mean operation applied, measuring the family's average satisfaction based on some parameters described in individual columns.
- _f19a_ -> _f19e_: aggregated into a new column "_teacher_satisfaction_"
  - a mean operation applied, measuring the family's average satisfaction with teachers.