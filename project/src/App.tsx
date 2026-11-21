import { FormEvent, useEffect, useState } from 'react';
import {
  ArrowDownRight,
  ArrowRight,
  ArrowUpRight,
  CalendarDays,
  Check,
  Instagram,
  Mail,
  Menu,
  Minus,
  Phone,
  Search,
  Sparkles,
  X,
} from 'lucide-react';

type Page = 'home' | 'about' | 'gallery' | 'contact' | 'blog';
type GalleryFilter = 'all' | 'ceremony' | 'floral' | 'destination' | 'celebration';

type GalleryItem = {
  title: string;
  category: Exclude<GalleryFilter, 'all'>;
  className: string;
  size: 'large' | 'tall' | 'standard';
};

const galleryItems: GalleryItem[] = [
  { title: 'The garden ceremony', category: 'ceremony', className: 'art-garden', size: 'large' },
  { title: 'Petals in the atrium', category: 'floral', className: 'art-rose', size: 'tall' },
  { title: 'A quiet shoreline', category: 'destination', className: 'art-shore', size: 'standard' },
  { title: 'The welcome dinner', category: 'celebration', className: 'art-dinner', size: 'standard' },
  { title: 'Candlelight vows', category: 'ceremony', className: 'art-candle', size: 'standard' },
  { title: 'A table in bloom', category: 'floral', className: 'art-table', size: 'large' },
  { title: 'The afterglow', category: 'destination', className: 'art-sunset', size: 'tall' },
  { title: 'Gathered together', category: 'celebration', className: 'art-gathering', size: 'standard' },
];

const blogPosts = [
  { number: '01', title: 'How to plan a wedding that feels like you', category: 'The guide', date: 'May 14, 2024', className: 'art-rose' },
  { number: '02', title: 'The art of the destination celebration', category: 'Journeys', date: 'Apr 29, 2024', className: 'art-shore' },
  { number: '03', title: 'Flowers that set the whole mood', category: 'Details', date: 'Apr 06, 2024', className: 'art-table' },
];

function getPage(): Page {
  const path = window.location.pathname.replace(/\/$/, '');
  if (path === '/about') return 'about';
  if (path === '/gallery') return 'gallery';
  if (path === '/contact') return 'contact';
  if (path === '/blog') return 'blog';
  return 'home';
}

function App() {
  const [page, setPage] = useState<Page>(getPage);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [galleryFilter, setGalleryFilter] = useState<GalleryFilter>('all');
  const [activeGallery, setActiveGallery] = useState<GalleryItem | null>(null);
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    const onPopState = () => setPage(getPage());
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  const navigate = (nextPage: Page) => {
    const path = nextPage === 'home' ? '/' : `/${nextPage}`;
    window.history.pushState({}, '', path);
    setPage(nextPage);
    setMobileOpen(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleContact = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="site-shell">
      <header className="site-header">
        <button className="wordmark" onClick={() => navigate('home')} aria-label="EverAfter Events home">
          <span>Ever</span><em>After</em>
          <small>Events &amp; celebrations</small>
        </button>
        <nav className={`main-nav ${mobileOpen ? 'is-open' : ''}`}>
          {(['home', 'about', 'gallery', 'contact', 'blog'] as Page[]).map((item) => (
            <button key={item} className={page === item ? 'active' : ''} onClick={() => navigate(item)}>
              {item === 'home' ? 'Home' : item[0].toUpperCase() + item.slice(1)}
            </button>
          ))}
          <button className="nav-cta" onClick={() => navigate('contact')}>Plan with us <ArrowUpRight size={14} /></button>
        </nav>
        <div className="header-actions">
          <button className="icon-button" aria-label="Search"><Search size={17} strokeWidth={1.5} /></button>
          <button className="menu-button" onClick={() => setMobileOpen(!mobileOpen)} aria-label="Toggle menu">
            {mobileOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </header>

      <main>
        {page === 'home' && <Home navigate={navigate} />}
        {page === 'about' && <About navigate={navigate} />}
        {page === 'gallery' && <Gallery filter={galleryFilter} setFilter={setGalleryFilter} active={activeGallery} setActive={setActiveGallery} />}
        {page === 'contact' && <Contact submitted={submitted} onSubmit={handleContact} />}
        {page === 'blog' && <Blog navigate={navigate} />}
      </main>

      <footer className="site-footer">
        <div className="footer-top">
          <div>
            <p className="eyebrow">EverAfter Events</p>
            <h2>Let&apos;s make<br /><em>something beautiful.</em></h2>
          </div>
          <button className="circle-arrow" onClick={() => navigate('contact')} aria-label="Go to contact"><ArrowUpRight size={23} /></button>
        </div>
        <div className="footer-bottom">
          <div className="footer-brand">E/A <span>EST. 2012</span></div>
          <div className="footer-links">
            <button onClick={() => navigate('about')}>Our story</button>
            <button onClick={() => navigate('gallery')}>The work</button>
            <button onClick={() => navigate('contact')}>Inquire</button>
          </div>
          <div className="footer-social"><Instagram size={16} /> <span>Follow along</span></div>
          <p className="copyright">© 2024 EverAfter Events</p>
        </div>
      </footer>
    </div>
  );
}

function Home({ navigate }: { navigate: (page: Page) => void }) {
  return (
    <>
      <section className="hero">
        <div className="hero-art art-bride"><div className="sun-disc" /><div className="portrait-arc" /><span className="hero-flower flower-one" /><span className="hero-flower flower-two" /></div>
        <div className="hero-copy">
          <p className="eyebrow">Wedding &amp; event studio · since 2012</p>
          <h1>Where your<br /><em>forever</em> begins.</h1>
          <p className="hero-intro">We compose celebrations with a little more feeling, a little more beauty, and all of the meaning.</p>
          <div className="hero-actions"><button className="button button-light" onClick={() => navigate('contact')}>Start a conversation <ArrowUpRight size={15} /></button><button className="text-button light-text" onClick={() => navigate('gallery')}>View our work <ArrowRight size={15} /></button></div>
        </div>
        <div className="hero-note"><span>Scroll to explore</span><ArrowDownRight size={19} /></div>
        <div className="hero-side">01 <Minus size={16} /> 04</div>
      </section>

      <section className="intro section-pad">
        <div className="section-label">01 <span>Our approach</span></div>
        <div className="intro-grid">
          <div className="intro-title"><p className="eyebrow">The EverAfter difference</p><h2>Thoughtful by<br /><em>nature.</em></h2></div>
          <div className="intro-copy"><p>We believe the best celebrations are the ones that feel like home — personal, artful and entirely yours. From the first sketch to the final toast, we bring a calm, considered energy to every beautiful detail.</p><button className="text-button" onClick={() => navigate('about')}>Discover our story <ArrowUpRight size={15} /></button></div>
        </div>
      </section>

      <section className="services section-pad section-dark">
        <div className="section-heading"><div><p className="eyebrow">What we do</p><h2>All the details.<br /><em>None of the stress.</em></h2></div><button className="text-button light-text" onClick={() => navigate('contact')}>Plan your day <ArrowUpRight size={15} /></button></div>
        <div className="service-grid">
          {['Full-service weddings', 'Destination celebrations', 'Design & florals', 'Intimate gatherings'].map((service, index) => <div className="service-card" key={service}><span>0{index + 1}</span><Sparkles size={22} strokeWidth={1.2} /><h3>{service}</h3><p>{['From the first moodboard to the last dance.', 'Beautifully considered, wherever you are.', 'Spaces that feel like your kind of magic.', 'The little moments deserve a big feeling.'][index]}</p><ArrowUpRight className="service-arrow" size={18} /></div>)}
        </div>
      </section>

      <section className="feature section-pad">
        <div className="feature-art art-garden"><span className="art-caption">The garden ceremony · Udaipur</span></div>
        <div className="feature-copy"><p className="eyebrow">Made for your moment</p><h2>Every celebration<br />has a <em>story.</em></h2><p>Our work lives between the beautifully planned and the wonderfully unexpected. We listen closely, design intentionally and make room for the kind of moments you could never plan.</p><button className="text-button" onClick={() => navigate('gallery')}>See the stories <ArrowUpRight size={15} /></button></div>
      </section>

      <section className="gallery-preview section-pad">
        <div className="section-heading"><div><p className="eyebrow">A glimpse of the magic</p><h2>Moments to<br /><em>remember.</em></h2></div><button className="text-button" onClick={() => navigate('gallery')}>View full gallery <ArrowUpRight size={15} /></button></div>
        <div className="preview-grid"><div className="art-rose" /><div className="art-shore" /><div className="art-table" /><div className="art-candle" /></div>
      </section>

      <section className="quote-block"><p className="eyebrow">Kind words</p><blockquote>“They didn&apos;t just plan our wedding.<br /><em>They understood us.</em>”</blockquote><div className="quote-author"><span /> Priya &amp; Arjun · Jaipur, 2023</div></section>
      <section className="journal-tease section-pad"><div className="section-heading"><div><p className="eyebrow">From the journal</p><h2>Notes on love,<br /><em>style &amp; gathering.</em></h2></div><button className="text-button" onClick={() => navigate('blog')}>Read the journal <ArrowUpRight size={15} /></button></div><div className="journal-list">{blogPosts.map((post) => <button key={post.number} className="journal-row" onClick={() => navigate('blog')}><span>{post.number}</span><strong>{post.title}</strong><small>{post.category} · {post.date}</small><ArrowUpRight size={18} /></button>)}</div></section>
    </>
  );
}

function PageIntro({ eyebrow, title, italic, description }: { eyebrow: string; title: string; italic: string; description: string }) {
  return <section className="page-intro section-pad"><p className="eyebrow">{eyebrow}</p><h1>{title}<br /><em>{italic}</em></h1><p className="page-lede">{description}</p></section>;
}

function About({ navigate }: { navigate: (page: Page) => void }) {
  return <>
    <PageIntro eyebrow="Our story · 01" title="A little more" italic="feeling." description="EverAfter is a full-service wedding and event studio for people who care about the way a moment feels." />
    <section className="about-story section-pad"><div className="about-art art-gathering"><span className="art-caption">A gathering in bloom</span></div><div className="about-copy"><p className="eyebrow">It started with a table</p><h2>Beautiful things<br />begin with <em>meaning.</em></h2><p>EverAfter began around a long dinner table in 2012, with a belief that the most memorable celebrations are never about having more. They are about choosing better — a flower with a story, a room with a point of view, a pause before the music starts.</p><p>Today, our studio creates weddings and gatherings across India and wherever your people are. Our team is small by design, so every celebration gets the attention it deserves.</p><button className="text-button" onClick={() => navigate('contact')}>Come say hello <ArrowUpRight size={15} /></button></div></section>
    <section className="values section-pad section-dark"><div className="section-label">02 <span>What matters to us</span></div><div className="values-grid"><div><h2>Calm in the<br /><em>beautiful chaos.</em></h2></div><div>{['Listen first', 'Make it personal', 'Leave room for wonder'].map((value, index) => <div className="value-row" key={value}><span>0{index + 1}</span><h3>{value}</h3><p>{['Your story is the best starting point.', 'No two celebrations should feel the same.', 'The best moments are the ones no one planned.'][index]}</p></div>)}</div></div></section>
    <section className="team section-pad"><div className="section-heading"><div><p className="eyebrow">The people behind the scenes</p><h2>Small team.<br /><em>Big heart.</em></h2></div></div><div className="team-grid"><div className="team-card art-rose"><strong>Amara Mehta</strong><span>Founder &amp; creative director</span></div><div className="team-card art-sunset"><strong>Rohan Kapoor</strong><span>Planning &amp; production</span></div><div className="team-card art-table"><strong>Nisha Jain</strong><span>Design &amp; florals</span></div></div></section>
  </>;
}

function Gallery({ filter, setFilter, active, setActive }: { filter: GalleryFilter; setFilter: (value: GalleryFilter) => void; active: GalleryItem | null; setActive: (value: GalleryItem | null) => void }) {
  const filtered = filter === 'all' ? galleryItems : galleryItems.filter((item) => item.category === filter);
  return <>
    <PageIntro eyebrow="The work · 02" title="A feeling worth" italic="remembering." description="A collection of celebrations, places and little details that stayed with us long after the last guest went home." />
    <section className="gallery-page section-pad"><div className="filter-row">{(['all', 'ceremony', 'floral', 'destination', 'celebration'] as GalleryFilter[]).map((item) => <button key={item} className={filter === item ? 'selected' : ''} onClick={() => setFilter(item)}>{item}</button>)}</div><div className="gallery-masonry">{filtered.map((item) => <button key={item.title} className={`gallery-tile ${item.size} ${item.className}`} onClick={() => setActive(item)}><span>{item.title}</span><ArrowUpRight size={18} /></button>)}</div></section>
    {active && <div className="lightbox" onClick={() => setActive(null)}><button className="lightbox-close" onClick={() => setActive(null)} aria-label="Close gallery"><X /></button><div className={`lightbox-art ${active.className}`} onClick={(event) => event.stopPropagation()}><span>{active.title}</span></div></div>}
  </>;
}

function Contact({ submitted, onSubmit }: { submitted: boolean; onSubmit: (event: FormEvent<HTMLFormElement>) => void }) {
  return <>
    <PageIntro eyebrow="Let&apos;s talk · 03" title="Your day starts" italic="here." description="Tell us a little about what you are imagining. We will be in touch within two working days." />
    <section className="contact-layout section-pad"><div className="contact-details"><p className="eyebrow">Find us here</p><h2>Let&apos;s make<br /><em>some magic.</em></h2><div className="detail-list"><div><Mail size={18} /><span>hello@everafter.events</span></div><div><Phone size={18} /><span>+91 98200 41212</span></div><div><CalendarDays size={18} /><span>Mon–Fri · 10am–6pm IST</span></div></div><div className="contact-note"><Sparkles size={18} /><p>We take on a limited number of celebrations each year, so we can stay close to every story.</p></div></div><form className="contact-form" onSubmit={onSubmit}><div className="form-row"><label>My name is<input required name="name" placeholder="Your full name" /></label><label>You can email me at<input required type="email" name="email" placeholder="you@email.com" /></label></div><div className="form-row"><label>We&apos;re planning a<select name="event"><option>Wedding celebration</option><option>Destination wedding</option><option>Intimate gathering</option><option>Corporate event</option></select></label><label>Our date is<input type="date" name="date" /></label></div><label>Tell us everything<textarea required name="message" placeholder="A little about you, your people and the feeling you want to create..." rows={5} /></label><button className="button button-dark" type="submit">Send inquiry <ArrowUpRight size={15} /></button>{submitted && <p className="form-success"><Check size={16} /> Thank you. Your note is on its way to our studio.</p>}</form></section>
  </>;
}

function Blog({ navigate }: { navigate: (page: Page) => void }) {
  return <>
    <PageIntro eyebrow="The journal · 04" title="Notes from" italic="the heart." description="Ideas, advice and inspiration for making a celebration feel unmistakably yours." />
    <section className="blog-page section-pad"><div className="featured-post"><div className="featured-art art-candle"><span className="art-caption">The EverAfter edit · 01</span></div><div className="featured-copy"><p className="eyebrow">Featured story · Planning</p><h2>The beauty of a<br /><em>well-held moment.</em></h2><p>There is an art to making space for a celebration — and a quiet confidence in knowing when to let the room do the talking.</p><button className="text-button" onClick={() => navigate('blog')}>Read the story <ArrowUpRight size={15} /></button></div></div><div className="blog-grid">{blogPosts.map((post) => <article key={post.number}><div className={`blog-card-art ${post.className}`}><span>{post.number}</span></div><p className="eyebrow">{post.category} · {post.date}</p><h3>{post.title}</h3><button className="text-button" onClick={() => navigate('blog')}>Read more <ArrowRight size={15} /></button></article>)}</div><div className="blog-subscribe"><div><p className="eyebrow">A note, now and then</p><h2>Join our <em>journal.</em></h2></div><div><p>Thoughtful ideas for meaningful celebrations, delivered occasionally.</p><div className="subscribe-form"><input type="email" placeholder="Your email address" aria-label="Your email address" /><button aria-label="Subscribe"><ArrowUpRight size={17} /></button></div></div></div></section>
  </>;
}

export default App;
