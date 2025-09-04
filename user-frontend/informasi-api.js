class InformasiApiService {
    constructor() {
        this.baseUrl = PUBLIC_API_BASE_URL;
    }

    async getFeaturedNews() {
        try {
            const response = await fetch(`${this.baseUrl}/public/news/featured/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching featured news:', error);
            throw error;
        }
    }

    async getGeneralNews() {
        try {
            const response = await fetch(`${this.baseUrl}/news/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching general news:', error);
            throw error;
        }
    }

    async getLatestNews(limit = 6, page = 1) {
        try {
            const response = await fetch(`${this.baseUrl}/public/news/?limit=${limit}&page=${page}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching latest news:', error);
            throw error;
        }
    }

    async getNewsDetail(slug) {
        try {
            const response = await fetch(`${this.baseUrl}/public/news/${slug}/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching news detail:', error);
            throw error;
        }
    }

    async getAnnouncements() {
        try {
            const response = await fetch(`${this.baseUrl}/news/public/announcements/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching announcements:', error);
            throw error;
        }
    }

    async getContact() {
        try {
            const response = await fetch(`${this.baseUrl}/village-profile/contact/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching contact:', error);
            throw error;
        }
    }
}

class InformasiPageManager {
    constructor() {
        this.apiService = new InformasiApiService();
        this.currentPage = 1;
        this.isLoading = false;
        this.hasMoreNews = true;
    }

    async init() {
        try {
            await Promise.all([
                this.loadFeaturedNews(),
                this.loadNews(),
                this.loadLatestNews(),
                this.loadAnnouncements(),
                this.loadContact()
            ]);
            this.setupEventListeners();
        } catch (error) {
            console.error('Error initializing page:', error);
        }
    }

    setupEventListeners() {
        const viewMoreBtn = document.getElementById('view-more-news');
        if (viewMoreBtn) {
            viewMoreBtn.addEventListener('click', () => this.loadMoreNews());
        }
    }

    async loadFeaturedNews() {
        try {
            const response = await this.apiService.getFeaturedNews();
            if (response.success && response.results.length > 0) {
                this.renderFeaturedNews(response.results[0]);
            }
        } catch (error) {
            console.error('Error loading featured news:', error);
            this.showFeaturedNewsError();
        } finally {
            this.hideLoading('featured-news-loading');
        }
    }

    async loadNews() {
        try {
            const loadingElement = document.getElementById('loading');
            if (loadingElement) {
                loadingElement.style.display = 'block';
            }

            const response = await this.apiService.getGeneralNews();
            if (response.results) {
                this.renderNews(response.results);
            }

            if (loadingElement) {
                loadingElement.style.display = 'none';
            }
        } catch (error) {
            console.error('Error loading news:', error);
            this.showNewsError();
        }
    }

    async loadLatestNews() {
        try {
            const response = await this.apiService.getLatestNews(6, 1);
            if (response.success && response.results) {
                this.renderLatestNews(response.results);
                this.hasMoreNews = response.pagination.has_next;
                if (this.hasMoreNews) {
                    document.getElementById('view-more-news').classList.remove('hidden');
                }
            }
        } catch (error) {
            console.error('Error loading latest news:', error);
            this.showError('latest-news-container', 'Gagal memuat informasi terkini');
        } finally {
            this.hideLoading('latest-news-loading');
        }
    }

    async loadMoreNews() {
        if (this.isLoading || !this.hasMoreNews) return;
        
        this.isLoading = true;
        this.currentPage++;
        
        try {
            const response = await this.apiService.getLatestNews(6, this.currentPage);
            if (response.success && response.results) {
                this.appendLatestNews(response.results);
                this.hasMoreNews = response.pagination.has_next;
                if (!this.hasMoreNews) {
                    document.getElementById('view-more-news').classList.add('hidden');
                }
            }
        } catch (error) {
            console.error('Error loading more news:', error);
        } finally {
            this.isLoading = false;
        }
    }

    async loadAnnouncements() {
        try {
            const response = await this.apiService.getAnnouncements();
            if (response.results) {
                this.renderAnnouncements(response.results);
            }
        } catch (error) {
            console.error('Error loading announcements:', error);
            this.showAnnouncementsError();
        }
    }

    async loadContact() {
        try {
            const contact = await this.apiService.getContact();
            this.renderFooterContact(contact);
        } catch (error) {
            console.error('Error loading footer contact:', error);
        }
    }

    renderFeaturedNews(news) {
        const loadingElement = document.getElementById('featured-loading');
        const containerElement = document.getElementById('featured-news-container');
        
        if (!news) {
            this.showFeaturedNewsError();
            return;
        }

        const featuredHTML = `
            <div class="bg-white rounded-lg shadow-xl overflow-hidden mb-8 news-card">
                <div class="md:flex">
                    <div class="md:w-1/2 overflow-hidden">
                        <img src="${news.image || 'asset/news-placeholder.svg'}" alt="${news.title}" class="w-full h-64 md:h-full object-cover news-image">
                    </div>
                    <div class="md:w-1/2 p-8">
                        <div class="flex items-center mb-4">
                            <span class="category-badge text-white px-3 py-1 rounded-full text-sm font-semibold mr-3">UTAMA</span>
                            <span class="text-gray-500 text-sm">${this.formatDate(news.created_at)}</span>
                        </div>
                        <h3 class="text-2xl font-bold mb-4 text-gray-800 line-clamp-2">${news.title}</h3>
                        <p class="text-gray-600 mb-6 leading-relaxed line-clamp-3">
                            ${news.excerpt || news.content.substring(0, 200) + '...'}
                        </p>
                        <a href="#" class="inline-flex items-center bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300 transform hover:scale-105">
                            Baca Selengkapnya
                            <i class="fas fa-arrow-right ml-2"></i>
                        </a>
                    </div>
                </div>
            </div>
        `;

        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
        if (containerElement) {
            containerElement.innerHTML = featuredHTML;
            containerElement.classList.remove('hidden');
        }
    }

    renderNews(newsList) {
        const container = document.getElementById('news-container');
        if (!container) return;

        if (newsList.length === 0) {
            container.innerHTML = `
                <div class="col-span-full text-center py-8">
                    <p class="text-gray-500">Belum ada berita tersedia.</p>
                </div>
            `;
            return;
        }

        const newsHTML = newsList.map(news => `
            <div class="bg-white rounded-lg shadow-md overflow-hidden news-card">
                <div class="overflow-hidden">
                    <img src="${news.image || 'asset/news-placeholder.svg'}" alt="${news.title}" class="w-full h-48 object-cover news-image">
                </div>
                <div class="p-6">
                    <div class="flex items-center mb-3">
                        <span class="category-badge text-white px-2 py-1 rounded-full text-xs font-semibold mr-2">BERITA</span>
                        <span class="text-gray-500 text-sm">${this.formatDate(news.created_at)}</span>
                    </div>
                    <h3 class="text-lg font-bold mb-3 text-gray-800 line-clamp-2">${news.title}</h3>
                    <p class="text-gray-600 text-sm mb-4 line-clamp-3">
                        ${news.excerpt || news.content.substring(0, 120) + '...'}
                    </p>
                    <a href="#" class="inline-flex items-center text-blue-600 hover:text-blue-700 font-semibold text-sm transition duration-300 transform hover:translate-x-1">
                        Baca Selengkapnya
                        <i class="fas fa-arrow-right ml-1 text-xs"></i>
                    </a>
                </div>
            </div>
        `).join('');

        container.innerHTML = newsHTML;
    }

    renderLatestNews(news) {
        const container = document.getElementById('latest-news-container');
        if (!container) return;

        container.innerHTML = '';
        
        if (!news || news.length === 0) {
            container.innerHTML = '<p class="text-center text-gray-500">Tidak ada informasi terkini tersedia.</p>';
            return;
        }

        const newsGrid = document.createElement('div');
        newsGrid.className = 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6';

        news.forEach(item => {
            const newsCard = this.createLatestNewsCard(item);
            newsGrid.appendChild(newsCard);
        });

        container.appendChild(newsGrid);
        container.classList.remove('hidden');
    }

    appendLatestNews(news) {
        const container = document.getElementById('latest-news-container');
        if (!container) return;

        const newsGrid = container.querySelector('.grid');
        if (!newsGrid) return;

        news.forEach(item => {
            const newsCard = this.createLatestNewsCard(item);
            newsGrid.appendChild(newsCard);
        });
    }

    createLatestNewsCard(news) {
        const card = document.createElement('div');
        card.className = 'bg-white rounded-lg shadow-md overflow-hidden news-card cursor-pointer';
        card.onclick = () => this.openNewsDetail(news.slug);

        const imageUrl = news.featured_image || 'assets/images/default-news.jpg';
        const categoryColor = news.category?.color || '#667eea';
        const publishedDate = news.published_date ? new Date(news.published_date).toLocaleDateString('id-ID', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }) : '';

        card.innerHTML = `
            <div class="relative overflow-hidden">
                <img src="${imageUrl}" alt="${news.title}" class="w-full h-48 object-cover news-image" onerror="this.src='assets/images/default-news.jpg'">
                ${news.is_featured ? '<div class="absolute top-2 left-2"><span class="category-badge text-white px-2 py-1 rounded-full text-xs font-semibold"><i class="fas fa-star mr-1"></i>Unggulan</span></div>' : ''}
                ${news.is_breaking ? '<div class="absolute top-2 right-2"><span class="bg-red-600 text-white px-2 py-1 rounded-full text-xs font-semibold animate-pulse"><i class="fas fa-bolt mr-1"></i>Breaking</span></div>' : ''}
            </div>
            <div class="p-6">
                ${news.category ? `<span class="category-badge text-white px-3 py-1 rounded-full text-xs font-semibold mb-2 inline-block">${news.category.name}</span>` : ''}
                <h3 class="text-lg font-bold text-gray-800 mb-2 line-clamp-2">${news.title}</h3>
                <p class="text-gray-600 text-sm mb-4 line-clamp-3">${news.excerpt || news.content}</p>
                <div class="flex justify-between items-center text-xs text-gray-500">
                    <span><i class="fas fa-user mr-1"></i>${news.author}</span>
                    <span><i class="fas fa-calendar mr-1"></i>${publishedDate}</span>
                </div>
                <div class="flex justify-between items-center mt-2 text-xs text-gray-500">
                    <span><i class="fas fa-eye mr-1"></i>${news.views_count || 0} views</span>
                    <span><i class="fas fa-heart mr-1"></i>${news.likes_count || 0} likes</span>
                </div>
            </div>
        `;

        return card;
    }

    openNewsDetail(slug) {
        // Redirect to news detail page or open modal
        window.open(`view.html?slug=${slug}`, '_blank');
    }

    renderAnnouncements(announcements) {
        const loadingElement = document.getElementById('announcement-loading');
        const containerElement = document.getElementById('announcement-container');
        
        if (!containerElement) return;

        if (announcements.length === 0) {
            const noDataHTML = `
                <div class="bg-white rounded-lg shadow-md p-6 text-center">
                    <p class="text-gray-500">Belum ada pengumuman tersedia.</p>
                </div>
            `;
            containerElement.innerHTML = noDataHTML;
        } else {
            const announcementsHTML = announcements.map(announcement => {
                const priorityColors = {
                    'high': 'border-red-500',
                    'medium': 'border-yellow-500', 
                    'low': 'border-blue-500'
                };
                const iconColors = {
                    'high': 'text-red-500',
                    'medium': 'text-yellow-500',
                    'low': 'text-blue-500'
                };
                const icons = {
                    'high': 'fas fa-exclamation-triangle',
                    'medium': 'fas fa-info-circle',
                    'low': 'fas fa-bullhorn'
                };
                
                const priority = announcement.priority || 'low';
                
                return `
                    <div class="bg-white rounded-lg shadow-md p-6 border-l-4 ${priorityColors[priority]}">
                        <div class="flex items-start">
                            <div class="flex-shrink-0">
                                <i class="${icons[priority]} ${iconColors[priority]} text-2xl"></i>
                            </div>
                            <div class="ml-4 flex-1">
                                <h3 class="text-lg font-bold text-gray-800 mb-2">${announcement.title}</h3>
                                <p class="text-gray-600 mb-3">
                                    ${announcement.content}
                                </p>
                                <div class="flex items-center text-sm text-gray-500">
                                    <i class="fas fa-calendar mr-2"></i>
                                    <span>Dipublikasikan: ${this.formatDate(announcement.created_at)}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            containerElement.innerHTML = announcementsHTML;
        }

        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
        containerElement.classList.remove('hidden');
    }

    renderFooterContact(contact) {
        const footerContactElement = document.getElementById('footer-contact');
        if (!footerContactElement || !contact) return;

        const contactHTML = `
            <h3 class="text-lg font-bold mb-4">Kontak</h3>
            <div class="text-gray-300 text-sm space-y-2">
                <p><i class="fas fa-phone mr-2"></i>${contact.phone || '+62 XXX-XXXX-XXXX'}</p>
                <p><i class="fas fa-envelope mr-2"></i>${contact.email || 'info@kampungpulosarok.id'}</p>
                <p><i class="fas fa-map-marker-alt mr-2"></i>${contact.address || 'Kampung Pulo Sarok, Aceh Singkil'}</p>
            </div>
        `;

        footerContactElement.innerHTML = contactHTML;
    }

    showFeaturedNewsError() {
        const loadingElement = document.getElementById('featured-loading');
        const containerElement = document.getElementById('featured-news-container');
        
        const errorHTML = `
            <div class="bg-white rounded-lg shadow-xl overflow-hidden mb-8 p-8 text-center">
                <div class="text-gray-500">
                    <i class="fas fa-exclamation-triangle text-4xl mb-4"></i>
                    <p>Gagal memuat berita utama. Silakan coba lagi nanti.</p>
                </div>
            </div>
        `;

        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
        if (containerElement) {
            containerElement.innerHTML = errorHTML;
            containerElement.classList.remove('hidden');
        }
    }

    showNewsError() {
        const container = document.getElementById('news-container');
        const loadingElement = document.getElementById('loading');
        
        if (container) {
            container.innerHTML = `
                <div class="col-span-full text-center py-8">
                    <div class="text-gray-500">
                        <i class="fas fa-exclamation-triangle text-4xl mb-4"></i>
                        <p>Gagal memuat berita. Silakan coba lagi nanti.</p>
                    </div>
                </div>
            `;
        }
        
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
    }

    showAnnouncementsError() {
        const loadingElement = document.getElementById('announcement-loading');
        const containerElement = document.getElementById('announcement-container');
        
        const errorHTML = `
            <div class="bg-white rounded-lg shadow-md p-6 text-center">
                <div class="text-gray-500">
                    <i class="fas fa-exclamation-triangle text-4xl mb-4"></i>
                    <p>Gagal memuat pengumuman. Silakan coba lagi nanti.</p>
                </div>
            </div>
        `;

        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
        if (containerElement) {
            containerElement.innerHTML = errorHTML;
            containerElement.classList.remove('hidden');
        }
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric'
        };
        return date.toLocaleDateString('id-ID', options);
    }

    hideLoading(loadingId) {
        const loadingElement = document.getElementById(loadingId);
        if (loadingElement) {
            loadingElement.classList.add('hidden');
        }
    }

    showError(containerId, message) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `<div class="text-center py-8"><p class="text-gray-500">${message}</p></div>`;
            container.classList.remove('hidden');
        }
    }

    truncateText(text, maxLength = 150) {
        if (!text) return '';
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }
}