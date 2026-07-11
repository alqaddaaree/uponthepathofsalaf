// src/content.config.ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const postsCollection = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    date: z.string(),
    author: z.string().nullable().optional(),
    topics: z.array(z.string()).default([]),  // stores topic slugs
    type: z.enum(['message', 'article', 'translation']).default('message'),
    forwarded_from: z.string().nullable().optional(),
    has_audio: z.boolean().default(false),
    has_file: z.boolean().default(false),
    body: z.string().optional(),
    isIndex: z.boolean().default(false),
  }),
});

const topicsCollection = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/topics' }),
  schema: z.object({
    name: z.string(),
    slug: z.string(),
    description: z.string().optional(),
    icon: z.string().optional(),
    order: z.number().default(999),
  }),
});

export const collections = {
  posts: postsCollection,
  topics: topicsCollection,
};