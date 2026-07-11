// src/utils/renderCard.ts

// Simple HTML escaper
function esc(str: string): string {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

export interface CardData {
  id: number;
  title: string;
  excerpt: string;
  topics: string[];
  author?: string;
  date?: string;
  featured?: boolean;
  url?: string;
}

export function renderCardHTML(item: CardData): string {
  const topicTag = item.topics.length > 0
    ? `<span class="card-topic-tag">${esc(item.topics[0])}</span>`
    : '';

  const authorHTML = item.author
    ? `<span class="card-author">${esc(item.author)}</span>`
    : '';

  const featuredClass = item.featured ? ' featured' : '';

  return `
    <article class="post-card${featuredClass}">
      <div class="card-bar"></div>
      <div class="card-body">
        <div class="card-meta">
          ${topicTag}
          ${item.date ? `<span class="card-date">${esc(item.date)}</span>` : ''}
        </div>
        <h3 class="card-title">${esc(item.title)}</h3>
        <p class="card-excerpt">${esc(item.excerpt)}</p>
        <div class="card-footer">
          ${authorHTML}
          <span class="card-cta">
            Read
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </span>
        </div>
      </div>
    </article>
  `;
}