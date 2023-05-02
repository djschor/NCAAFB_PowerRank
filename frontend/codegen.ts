import { CodegenConfig } from '@graphql-codegen/cli';

const config: CodegenConfig = {
  schema: 'http://127.0.0.1:8000/graphql',
  documents: ['src/**/*.tsx'],
  
  generates: {
    './src/__generated__/': {
      preset: 'client',
      plugins: [ 'typescript'], 
      presetConfig: {
        gqlTagName: 'gql',
        dedupeFragments: true
      },
      
    }
  },
  ignoreNoDocuments: true,
};

export default config;