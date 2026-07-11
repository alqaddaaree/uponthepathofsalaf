import { getCollection } from 'astro:content';

function stripMarkdown(text) {
  if (!text) return '';  // ← add this guard
  return text
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/\*(.*?)\*/g, '$1')
    .replace(/\[(.*?)\]\(.*?\)/g, '$1')
    .replace(/`(.*?)`/g, '$1')
    .replace(/#{1,6}\s/g, '')
    .replace(/>\s/g, '')
    .replace(/\n/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export async function GET() {
  const allPosts = await getCollection('posts');

  const searchIndex = allPosts.map(post => {
    // Use post.data.body (not post.body) for YAML files
    const cleanBody = stripMarkdown(post.data.body || '');
    const excerpt = cleanBody.slice(0, 200).trim() + (cleanBody.length > 200 ? '…' : '');

    return {
      id: post.id,  // use slug from filename
      title: stripMarkdown(post.data.title),
      excerpt: excerpt,
      topics: post.data.topics || [],
      author: post.data.author || '',
    };
  });

  return new Response(JSON.stringify(searchIndex), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}