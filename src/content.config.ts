import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const postsCollection = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    id: z.string(),
    title: z.string(),
    date: z.string(),
    author: z.string().nullable().optional(),
    quotedAuthor: z.string().nullable().optional(),
    topics: z.array(z.string()).default([]),
    type: z.enum(['message', 'article', 'translation']).default('message'),
    edited: z.string().nullable().optional(),
    forwarded_from: z.string().nullable().optional(),
    has_audio: z.boolean().default(false),
    has_file: z.boolean().default(false),
  }),
});

export const collections = {
  posts: postsCollection,
};
