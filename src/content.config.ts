import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    date: z.coerce.date(),
    draft: z.boolean().default(true),
    featured: z.boolean().default(false),
    tags: z.array(z.string()).default([]),
    thumbnail: z.string().optional(),
    thumbnailAlt: z.string().optional(),
    artifactSummary: z.string().optional(),
    artifactUrl: z.string().optional(),
    repoUrl: z.union([z.string().url(), z.literal('')]).optional(),
    caption: z.string().optional(),
    updatedDate: z.preprocess((value) => value === '' ? undefined : value, z.coerce.date().optional()),
  }),
});

export const collections = { posts };
