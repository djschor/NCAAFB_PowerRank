/* eslint-disable */
import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
};

export type Qb = {
  __typename?: 'QB';
  adpsr?: Maybe<Scalars['Float']>;
  adpsr_competitive_rank?: Maybe<Scalars['Int']>;
  adpsr_relative_rank?: Maybe<Scalars['Int']>;
  aqs?: Maybe<Scalars['Float']>;
  aqs_competitive_rank?: Maybe<Scalars['Int']>;
  aqs_relative_rank?: Maybe<Scalars['Int']>;
  competitive_score_week_rank?: Maybe<Scalars['Int']>;
  crae?: Maybe<Scalars['Float']>;
  crae_competitive_rank?: Maybe<Scalars['Int']>;
  crae_relative_rank?: Maybe<Scalars['Int']>;
  defense_score?: Maybe<Scalars['Float']>;
  defense_score_competitive_rank?: Maybe<Scalars['Int']>;
  defense_score_relative_rank?: Maybe<Scalars['Int']>;
  dmi?: Maybe<Scalars['Float']>;
  dmi_competitive_rank?: Maybe<Scalars['Int']>;
  dmi_relative_rank?: Maybe<Scalars['Int']>;
  pk?: Maybe<Scalars['String']>;
  player?: Maybe<Scalars['String']>;
  ppi?: Maybe<Scalars['Float']>;
  ppi_competitive_rank?: Maybe<Scalars['Int']>;
  ppi_relative_rank?: Maybe<Scalars['Int']>;
  qb_competitive_score?: Maybe<Scalars['Float']>;
  qb_relative_score?: Maybe<Scalars['Float']>;
  qb_total_rank?: Maybe<Scalars['Int']>;
  qb_total_score?: Maybe<Scalars['Float']>;
  qpi?: Maybe<Scalars['Float']>;
  qpi_competitive_rank?: Maybe<Scalars['Int']>;
  qpi_relative_rank?: Maybe<Scalars['Int']>;
  reer?: Maybe<Scalars['Float']>;
  reer_competitive_rank?: Maybe<Scalars['Int']>;
  reer_relative_rank?: Maybe<Scalars['Int']>;
  sei?: Maybe<Scalars['Float']>;
  sei_competitive_rank?: Maybe<Scalars['Int']>;
  sei_relative_rank?: Maybe<Scalars['Int']>;
  team?: Maybe<Scalars['String']>;
  total_score_week_rank?: Maybe<Scalars['Int']>;
  week?: Maybe<Scalars['Int']>;
  year?: Maybe<Scalars['Int']>;
};

export type QbOverallRanking = {
  __typename?: 'QBOverallRanking';
  avg_qb_competitive_score?: Maybe<Scalars['Float']>;
  avg_qb_total_score?: Maybe<Scalars['Float']>;
  competitive_score_rank?: Maybe<Scalars['Float']>;
  player: Scalars['String'];
  total_score_rank?: Maybe<Scalars['Float']>;
  year: Scalars['Int'];
};

export type QbOverallRankingResult = {
  __typename?: 'QBOverallRankingResult';
  QBOverallRanking?: Maybe<Array<Maybe<QbOverallRanking>>>;
  errors?: Maybe<Array<Maybe<Scalars['String']>>>;
  success: Scalars['Boolean'];
};

export type QbResult = {
  __typename?: 'QBResult';
  errors?: Maybe<Array<Maybe<Scalars['String']>>>;
  qbWeeklyData?: Maybe<Array<Maybe<Qb>>>;
  success: Scalars['Boolean'];
};

export type QbWeeklyRanking = {
  __typename?: 'QBWeeklyRanking';
  adpsr?: Maybe<Scalars['Float']>;
  adpsr_competitive_rank?: Maybe<Scalars['Float']>;
  adpsr_relative_rank?: Maybe<Scalars['Float']>;
  aqs?: Maybe<Scalars['Float']>;
  aqs_competitive_rank?: Maybe<Scalars['Float']>;
  aqs_relative_rank?: Maybe<Scalars['Float']>;
  competitive_score_week_rank?: Maybe<Scalars['Float']>;
  crae?: Maybe<Scalars['Float']>;
  crae_competitive_rank?: Maybe<Scalars['Float']>;
  crae_relative_rank?: Maybe<Scalars['Float']>;
  defense_score?: Maybe<Scalars['Float']>;
  defense_score_competitive_rank?: Maybe<Scalars['Float']>;
  defense_score_relative_rank?: Maybe<Scalars['Float']>;
  dmi?: Maybe<Scalars['Float']>;
  dmi_competitive_rank?: Maybe<Scalars['Float']>;
  dmi_relative_rank?: Maybe<Scalars['Float']>;
  pk: Scalars['String'];
  player: Scalars['String'];
  ppi?: Maybe<Scalars['Float']>;
  ppi_competitive_rank?: Maybe<Scalars['Float']>;
  ppi_relative_rank?: Maybe<Scalars['Float']>;
  qb_competitive_score?: Maybe<Scalars['Float']>;
  qb_relative_score?: Maybe<Scalars['Float']>;
  qb_total_rank?: Maybe<Scalars['Float']>;
  qb_total_score?: Maybe<Scalars['Float']>;
  qpi?: Maybe<Scalars['Float']>;
  qpi_competitive_rank?: Maybe<Scalars['Float']>;
  qpi_relative_rank?: Maybe<Scalars['Float']>;
  reer?: Maybe<Scalars['Float']>;
  reer_competitive_rank?: Maybe<Scalars['Float']>;
  reer_relative_rank?: Maybe<Scalars['Float']>;
  sei?: Maybe<Scalars['Float']>;
  sei_competitive_rank?: Maybe<Scalars['Float']>;
  sei_relative_rank?: Maybe<Scalars['Float']>;
  team?: Maybe<Scalars['String']>;
  technical_score?: Maybe<Scalars['Float']>;
  trend_score?: Maybe<Scalars['Float']>;
  volume_score?: Maybe<Scalars['Float']>;
  week?: Maybe<Scalars['Int']>;
  year?: Maybe<Scalars['Int']>;
};

export type QbWeeklyRankingResult = {
  __typename?: 'QBWeeklyRankingResult';
  errors?: Maybe<Array<Maybe<Scalars['String']>>>;
  qbWeeklyRankings?: Maybe<Array<Maybe<QbWeeklyRanking>>>;
  success: Scalars['Boolean'];
};

export type Query = {
  __typename?: 'Query';
  qbdata?: Maybe<QbResult>;
  qboverall?: Maybe<QbOverallRankingResult>;
  qbweek?: Maybe<QbWeeklyRankingResult>;
};


export type QueryQbdataArgs = {
  player_name: Scalars['String'];
  year?: InputMaybe<Scalars['Int']>;
};


export type QueryQboverallArgs = {
  field?: InputMaybe<Scalars['String']>;
  top_x?: InputMaybe<Scalars['Int']>;
};


export type QueryQbweekArgs = {
  top_x?: InputMaybe<Scalars['Int']>;
  week: Scalars['Int'];
};

export type GetQbDataQueryVariables = Exact<{
  player_name: Scalars['String'];
  year?: InputMaybe<Scalars['Int']>;
}>;


export type GetQbDataQuery = { __typename?: 'Query', qbdata?: { __typename?: 'QBResult', success: boolean, errors?: Array<string | null> | null, qbWeeklyData?: Array<{ __typename?: 'QB', player?: string | null, week?: number | null, year?: number | null, pk?: string | null, team?: string | null, aqs?: number | null, aqs_competitive_rank?: number | null, aqs_relative_rank?: number | null, adpsr?: number | null, adpsr_competitive_rank?: number | null, adpsr_relative_rank?: number | null, crae?: number | null, crae_competitive_rank?: number | null, crae_relative_rank?: number | null, dmi?: number | null, dmi_competitive_rank?: number | null, dmi_relative_rank?: number | null, defense_score?: number | null, defense_score_competitive_rank?: number | null, defense_score_relative_rank?: number | null, ppi?: number | null, ppi_competitive_rank?: number | null, ppi_relative_rank?: number | null, qpi?: number | null, qpi_competitive_rank?: number | null, qpi_relative_rank?: number | null, reer?: number | null, reer_competitive_rank?: number | null, reer_relative_rank?: number | null, sei?: number | null, sei_competitive_rank?: number | null, sei_relative_rank?: number | null, competitive_score_week_rank?: number | null, qb_competitive_score?: number | null, qb_relative_score?: number | null, qb_total_rank?: number | null, qb_total_score?: number | null, total_score_week_rank?: number | null } | null> | null } | null };


export const GetQbDataDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"GetQBData"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"player_name"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"year"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"qbdata"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"player_name"},"value":{"kind":"Variable","name":{"kind":"Name","value":"player_name"}}},{"kind":"Argument","name":{"kind":"Name","value":"year"},"value":{"kind":"Variable","name":{"kind":"Name","value":"year"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"success"}},{"kind":"Field","name":{"kind":"Name","value":"errors"}},{"kind":"Field","name":{"kind":"Name","value":"qbWeeklyData"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"player"}},{"kind":"Field","name":{"kind":"Name","value":"week"}},{"kind":"Field","name":{"kind":"Name","value":"year"}},{"kind":"Field","name":{"kind":"Name","value":"pk"}},{"kind":"Field","name":{"kind":"Name","value":"team"}},{"kind":"Field","name":{"kind":"Name","value":"aqs"}},{"kind":"Field","name":{"kind":"Name","value":"aqs_competitive_rank"}},{"kind":"Field","name":{"kind":"Name","value":"aqs_relative_rank"}},{"kind":"Field","name":{"kind":"Name","value":"adpsr"}},{"kind":"Field","name":{"kind":"Name","value":"adpsr_competitive_rank"}},{"kind":"Field","name":{"kind":"Name","value":"adpsr_relative_rank"}},{"kind":"Field","name":{"kind":"Name","value":"crae"}},{"kind":"Field","name":{"kind":"Name","value":"crae_competitive_rank"}},{"kind":"Field","name":{"kind":"Name","value":"crae_relative_rank"}},{"kind":"Field","name":{"kind":"Name","value":"dmi"}},{"kind":"Field","name":{"kind":"Name","value":"dmi_competitive_rank"}},{"kind":"Field","name":{"kind":"Name","value":"dmi_relative_rank"}},{"kind":"Field","name":{"kind":"Name","value":"defense_score"}},{"kind":"Field","name":{"kind":"Name","value":"defense_score_competitive_rank"}},{"kind":"Field","name":{"kind":"Name","value":"defense_score_relative_rank"}},{"kind":"Field","name":{"kind":"Name","value":"ppi"}},{"kind":"Field","name":{"kind":"Name","value":"ppi_competitive_rank"}},{"kind":"Field","name":{"kind":"Name","value":"ppi_relative_rank"}},{"kind":"Field","name":{"kind":"Name","value":"qpi"}},{"kind":"Field","name":{"kind":"Name","value":"qpi_competitive_rank"}},{"kind":"Field","name":{"kind":"Name","value":"qpi_relative_rank"}},{"kind":"Field","name":{"kind":"Name","value":"reer"}},{"kind":"Field","name":{"kind":"Name","value":"reer_competitive_rank"}},{"kind":"Field","name":{"kind":"Name","value":"reer_relative_rank"}},{"kind":"Field","name":{"kind":"Name","value":"sei"}},{"kind":"Field","name":{"kind":"Name","value":"sei_competitive_rank"}},{"kind":"Field","name":{"kind":"Name","value":"sei_relative_rank"}},{"kind":"Field","name":{"kind":"Name","value":"competitive_score_week_rank"}},{"kind":"Field","name":{"kind":"Name","value":"qb_competitive_score"}},{"kind":"Field","name":{"kind":"Name","value":"qb_relative_score"}},{"kind":"Field","name":{"kind":"Name","value":"qb_total_rank"}},{"kind":"Field","name":{"kind":"Name","value":"qb_total_score"}},{"kind":"Field","name":{"kind":"Name","value":"total_score_week_rank"}}]}}]}}]}}]} as unknown as DocumentNode<GetQbDataQuery, GetQbDataQueryVariables>;
/** All built-in and custom scalars, mapped to their actual values */
