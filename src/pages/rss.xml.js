import { getCollection } from 'astro:content';

export async function GET() {
  const posts = await getCollection('posts');
  const sortedPosts = posts.sort((a, b) => new Date(b.data.date) - new Date(a.data.date));
  const siteUrl = import.meta.env.SITE || 'https://uponthepathofsalaf.vercel.app';

  const items = sortedPosts.map(post => {
    // Use post.data.body instead of post.body
    const body = post.data.body || '';
    const description = body.slice(0, 500).replace(/\n/g, ' ').trim();
    
    return `
    <item>
      <title><![CDATA[${post.data.title}]]></title>
      <link>${siteUrl}/posts/${post.id}</link>
      <guid>${siteUrl}/posts/${post.id}</guid>
      <pubDate>${new Date(post.data.date).toUTCString()}</pubDate>
      <description><![CDATA[${description}]]></description>
    </item>
  `}).join('');

  const rss = `<?xml version="1.0" encoding="UTF-8" ?>
  <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
      <title><![CDATA[The Salaf's Path]]></title>
      <description><![CDATA[Islamic content from the Quran, Sunnah, and the scholars of Ahl al-Sunnah.]]></description>
      <link>${siteUrl}</link>
      <atom:link href="${siteUrl}/rss.xml" rel="self" type="application/rss+xml" />
      <language>en</language>
      <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
      ${items}
    </channel>
  </rss>`;

  return new Response(rss, {
    headers: {
      'Content-Type': 'application/xml',
    },
  });
}