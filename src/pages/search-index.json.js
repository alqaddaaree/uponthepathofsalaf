import { getCollection } from 'astro:content';

function stripMarkdown(text: string): string {
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
    // Strip markdown from body
    const cleanBody = stripMarkdown(post.body);
    const excerpt = cleanBody.slice(0, 200).trim() + '…';

    return {
      id: post.data.id,
      title: stripMarkdown(post.data.title),
      excerpt: excerpt,
      topics: post.data.topics || [],
      author: post.data.author || post.data.quotedAuthor || '',
    };
  });

  return new Response(JSON.stringify(searchIndex), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
