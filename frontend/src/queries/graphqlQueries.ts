// import { gql } from '@apollo/client';



// export const QB_DATA = gql`
//   query GetQBData($player_name: String!, $year: Int) {
//     qbdata(player_name: $player_name, year: $year) {
//       success
//       errors
//       qbWeeklyData {
//         player
//         week
//         year
//         pk
//         team
//         aqs
//         aqs_competitive_rank
//         aqs_relative_rank
//         adpsr
//         adpsr_competitive_rank
//         adpsr_relative_rank
//         crae
//         crae_competitive_rank
//         crae_relative_rank
//         dmi
//         dmi_competitive_rank
//         dmi_relative_rank
//         defense_score
//         defense_score_competitive_rank
//         defense_score_relative_rank
//         ppi
//         ppi_competitive_rank
//         ppi_relative_rank
//         qpi
//         qpi_competitive_rank
//         qpi_relative_rank
//         reer
//         reer_competitive_rank
//         reer_relative_rank
//         sei
//         sei_competitive_rank
//         sei_relative_rank
//         competitive_score_week_rank
//         qb_competitive_score
//         qb_relative_score
//         qb_total_rank
//         qb_total_score
//         total_score_week_rank
//       }
//     }
//   }
// `;

// export const QB_OVERALL = gql`
//   query GetQBOverall($top_x: Int, $field: String) {
//     qboverall(top_x: $top_x, field: $field) {
//       success
//       errors
//       QBOverallRanking {
//         player
//         year
//         competitive_score_rank
//         total_score_rank
//         avg_qb_competitive_score
//         avg_qb_total_score
//       }
//     }
//   }
// `;

// export const QB_WEEK = gql`
//   query GetQBWeek($week: Int!, $top_x: Int) {
//     qbweek(week: $week, top_x: $top_x) {
//       success
//       errors
//       qbWeeklyRankings {
//         pk
//         player
//         team
//         year
//         week
//         adpsr
//         adpsr_competitive_rank
//         adpsr_relative_rank
//         aqs
//         aqs_competitive_rank
//         aqs_relative_rank
//         competitive_score_week_rank
//         crae
//         crae_competitive_rank
//         crae_relative_rank
//         defense_score
//         defense_score_competitive_rank
//         defense_score_relative_rank
//         dmi
//         dmi_competitive_rank
//         dmi_relative_rank
//         ppi
//         ppi_competitive_rank
//         ppi_relative_rank
//         qb_competitive_score
//         qb_relative_score
//         qb_total_rank
//         qb_total_score
//         qpi
//         qpi_competitive_rank
//         qpi_relative_rank
//         reer
//         reer_competitive_rank
//         reer_relative_rank
//         sei
//         sei_competitive_rank
//         sei_relative_rank
//         trend_score
//         volume_score
//         technical_score
//       }
//     }
//   }
// `;