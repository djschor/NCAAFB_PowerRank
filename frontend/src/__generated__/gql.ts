/* eslint-disable */
import * as types from './graphql';
import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';

/**
 * Map of all GraphQL operations in the project.
 *
 * This map has several performance disadvantages:
 * 1. It is not tree-shakeable, so it will include all operations in the project.
 * 2. It is not minifiable, so the string of a GraphQL query will be multiple times inside the bundle.
 * 3. It does not support dead code elimination, so it will add unused operations.
 *
 * Therefore it is highly recommended to use the babel-plugin for production.
 */
const documents = {
    "\n  query GetQBData($player_name: String!, $year: Int) {\n    qbdata(player_name: $player_name, year: $year) {\n      success\n      errors\n      qbWeeklyData {\n        player\n        week\n        year\n        pk\n        team\n        aqs\n        aqs_competitive_rank\n        aqs_relative_rank\n        adpsr\n        adpsr_competitive_rank\n        adpsr_relative_rank\n        crae\n        crae_competitive_rank\n        crae_relative_rank\n        dmi\n        dmi_competitive_rank\n        dmi_relative_rank\n        defense_score\n        defense_score_competitive_rank\n        defense_score_relative_rank\n        ppi\n        ppi_competitive_rank\n        ppi_relative_rank\n        qpi\n        qpi_competitive_rank\n        qpi_relative_rank\n        reer\n        reer_competitive_rank\n        reer_relative_rank\n        sei\n        sei_competitive_rank\n        sei_relative_rank\n        competitive_score_week_rank\n        qb_competitive_score\n        qb_relative_score\n        qb_total_rank\n        qb_total_score\n        total_score_week_rank\n      }\n    }\n  }\n": types.GetQbDataDocument,
};

/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 *
 *
 * @example
 * ```ts
 * const query = gql(`query GetUser($id: ID!) { user(id: $id) { name } }`);
 * ```
 *
 * The query argument is unknown!
 * Please regenerate the types.
 */
export function gql(source: string): unknown;

/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query GetQBData($player_name: String!, $year: Int) {\n    qbdata(player_name: $player_name, year: $year) {\n      success\n      errors\n      qbWeeklyData {\n        player\n        week\n        year\n        pk\n        team\n        aqs\n        aqs_competitive_rank\n        aqs_relative_rank\n        adpsr\n        adpsr_competitive_rank\n        adpsr_relative_rank\n        crae\n        crae_competitive_rank\n        crae_relative_rank\n        dmi\n        dmi_competitive_rank\n        dmi_relative_rank\n        defense_score\n        defense_score_competitive_rank\n        defense_score_relative_rank\n        ppi\n        ppi_competitive_rank\n        ppi_relative_rank\n        qpi\n        qpi_competitive_rank\n        qpi_relative_rank\n        reer\n        reer_competitive_rank\n        reer_relative_rank\n        sei\n        sei_competitive_rank\n        sei_relative_rank\n        competitive_score_week_rank\n        qb_competitive_score\n        qb_relative_score\n        qb_total_rank\n        qb_total_score\n        total_score_week_rank\n      }\n    }\n  }\n"): (typeof documents)["\n  query GetQBData($player_name: String!, $year: Int) {\n    qbdata(player_name: $player_name, year: $year) {\n      success\n      errors\n      qbWeeklyData {\n        player\n        week\n        year\n        pk\n        team\n        aqs\n        aqs_competitive_rank\n        aqs_relative_rank\n        adpsr\n        adpsr_competitive_rank\n        adpsr_relative_rank\n        crae\n        crae_competitive_rank\n        crae_relative_rank\n        dmi\n        dmi_competitive_rank\n        dmi_relative_rank\n        defense_score\n        defense_score_competitive_rank\n        defense_score_relative_rank\n        ppi\n        ppi_competitive_rank\n        ppi_relative_rank\n        qpi\n        qpi_competitive_rank\n        qpi_relative_rank\n        reer\n        reer_competitive_rank\n        reer_relative_rank\n        sei\n        sei_competitive_rank\n        sei_relative_rank\n        competitive_score_week_rank\n        qb_competitive_score\n        qb_relative_score\n        qb_total_rank\n        qb_total_score\n        total_score_week_rank\n      }\n    }\n  }\n"];

export function gql(source: string) {
  return (documents as any)[source] ?? {};
}

export type DocumentType<TDocumentNode extends DocumentNode<any, any>> = TDocumentNode extends DocumentNode<  infer TType,  any>  ? TType  : never;