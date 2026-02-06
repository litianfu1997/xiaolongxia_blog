import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
	type: 'content',
	// Type-check frontmatter using a schema
	schema: ({ image }) => z.object({
		title: z.string(),
		description: z.string(),
		// Transform string to Date object
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		heroImage: image().optional(),
		heroAlt: z.string().optional(),
		tags: z.array(z.string()).optional(),
		// Add category field - optional for now to avoid breaking build, but we will fill it
		category: z.enum(['AI热点资讯', '模型Token消耗排行榜', '技术杂谈', '生活日常']).optional(),
	}),
});

export const collections = { blog };
