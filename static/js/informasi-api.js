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
            const response = await fetch(`${this.baseUrl}/news/?limit=${limit}&page=${page}`);
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
            const response = await fetch(`${this.baseUrl}/public/announcements/`);
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
            const response = await fetch(`${this.baseUrl}/contact/`);
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
        this.hasMoreNews = true;
        this.isLoading = false;
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
        const viewMoreButton = document.getElementById('view-more-news');
        if (viewMoreButton) {
            viewMoreButton.addEventListener('click', () => this.loadMoreNews());
        }
    }

    async loadFeaturedNews() {
        try {
            const featuredNews = await this.apiService.getFeaturedNews();
            this.renderFeaturedNews(featuredNews);
        } catch (error) {
            console.error('Error loading featured news:', error);
            this.showFeaturedNewsError();
        }
    }

    async loadNews() {
        try {
            const newsData = await this.apiService.getGeneralNews();
            if (newsData && newsData.results) {
                this.renderNews(newsData.results);
            }
        } catch (error) {
            console.error('Error loading news:', error);
            this.showNewsError();
        }
    }

    async loadLatestNews() {
        try {
            const newsData = await this.apiService.getLatestNews(6, 1);
            if (newsData && newsData.results) {
                this.renderLatestNews(newsData.results);
                
                // Show view more button if there are more news
                const viewMoreButton = document.getElementById('view-more-news');
                if (viewMoreButton && newsData.next) {
                    viewMoreButton.classList.remove('hidden');
                }
            }
        } catch (error) {
            console.error('Error loading latest news:', error);
        }
    }

    async loadMoreNews() {
        if (this.isLoading || !this.hasMoreNews) return;
        
        this.isLoading = true;
        this.currentPage++;
        
        try {
            const newsData = await this.apiService.getLatestNews(6, this.currentPage);
            if (newsData && newsData.results && newsData.results.length > 0) {
                this.appendLatestNews(newsData.results);
                
                // Hide button if no more news
                if (!newsData.next) {
                    this.hasMoreNews = false;
                    const viewMoreButton = document.getElementById('view-more-news');
                    if (viewMoreButton) {
                        viewMoreButton.classList.add('hidden');
                    }
                }
            } else {
                this.hasMoreNews = false;
            }
        } catch (error) {
            console.error('Error loading more news:', error);
        } finally {
            this.isLoading = false;
        }
    }

    async loadAnnouncements() {
        try {
            const announcements = await this.apiService.getAnnouncements();
            if (announcements && announcements.results) {
                this.renderAnnouncements(announcements.results);
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
            console.error('Error loading contact:', error);
        }
    }

    renderFeaturedNews(news) {
        const loadingElement = document.getElementById('featured-loading');
        const containerElement = document.getElementById('featured-news-container');
        
        if (!containerElement) return;

        if (news.length === 0) {
            const noDataHTML = `
                <div class="bg-white rounded-lg shadow-md p-6 text-center">
                    <p class="text-gray-500">Belum ada berita unggulan tersedia.</p>
                </div>
            `;
            containerElement.innerHTML = noDataHTML;
        } else {
            const featuredHTML = news.map(article => {
                const publishDate = new Date(article.created_at).toLocaleDateString('id-ID', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                });
                
                return `
                    <div class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
                        <div class="h-64 bg-blue-100 flex items-center justify-center overflow-hidden">
                            ${article.featured_image ? 
                                `<img src="${article.featured_image}" alt="${article.title}" class="w-full h-full object-cover">` :
                                `<img src="/static/images/feature1.svg" alt="${article.title}" class="w-full h-full object-cover">`
                            }
                        </div>
                        <div class="p-6">
                            <span class="bg-red-600 text-white px-3 py-1 rounded-full text-xs font-semibold mb-3 inline-block">UNGGULAN</span>
                            <h3 class="text-xl font-bold mb-3 line-clamp-2">${article.title}</h3>
                            <p class="text-gray-600 mb-4 line-clamp-3">
                                ${article.excerpt || this.truncateText(article.content, 150)}
                            </p>
                            <div class="flex items-center justify-between text-sm text-gray-500 mb-4">
                                <span class="flex items-center">
                                    <i class="fas fa-calendar mr-1"></i>
                                    ${publishDate}
                                </span>
                                <span class="flex items-center">
                                    <i class="fas fa-eye mr-1"></i>
                                    ${article.views_count || 0} views
                                </span>
                            </div>
                            <button onclick="informasiManager.openNewsDetail('${article.slug}')" class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-full text-sm transition duration-300 transform hover:scale-105">BACA SELENGKAPNYA</button>
                        </div>
                    </div>
                `;
            }).join('');
            
            containerElement.innerHTML = featuredHTML;
        }
        
        // Hide loading and show container
        if (loadingElement) loadingElement.classList.add('hidden');
        containerElement.classList.remove('hidden');
    }

    renderNews(newsList) {
        const newsContainer = document.getElementById('news-container');
        if (!newsContainer) return;
        
        if (newsList.length === 0) {
            newsContainer.innerHTML = `
                <div class="col-span-full text-center py-8">
                    <p class="text-gray-500">Belum ada berita tersedia.</p>
                </div>
            `;
            return;
        }
        
        const newsHTML = newsList.map(article => {
            const publishDate = new Date(article.created_at).toLocaleDateString('id-ID', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
            
            return `
                <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
                    <div class="h-48 bg-blue-100 flex items-center justify-center overflow-hidden">
                        ${article.featured_image ? 
                            `<img src="${article.featured_image}" alt="${article.title}" class="w-full h-full object-cover">` :
                            `<img src="/static/images/feature1.svg" alt="${article.title}" class="w-full h-full object-cover">`
                        }
                    </div>
                    <div class="p-4">
                        <h3 class="text-lg font-semibold mb-2 line-clamp-2">${article.title}</h3>
                        <p class="text-gray-600 text-sm mb-3 line-clamp-3">
                            ${article.excerpt || this.truncateText(article.content, 120)}
                        </p>
                        <div class="flex items-center justify-between text-xs text-gray-500 mb-3">
                            <span class="flex items-center">
                                <i class="fas fa-calendar mr-1"></i>
                                ${publishDate}
                            </span>
                        </div>
                        <button onclick="informasiManager.openNewsDetail('${article.slug}')" class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-full text-sm transition duration-300 transform hover:scale-105">SELENGKAPNYA</button>
                    </div>
                </div>
            `;
        }).join('');
        
        newsContainer.innerHTML = newsHTML;
    }

    renderLatestNews(news) {
        const loadingElement = document.getElementById('latest-loading');
        const containerElement = document.getElementById('latest-news-container');
        
        if (!containerElement) return;

        if (news.length === 0) {
            const noDataHTML = `
                <div class="bg-white rounded-lg shadow-md p-6 text-center">
                    <p class="text-gray-500">Belum ada berita terkini tersedia.</p>
                </div>
            `;
            containerElement.innerHTML = noDataHTML;
        } else {
            const latestHTML = news.map(article => this.createLatestNewsCard(article)).join('');
            containerElement.innerHTML = `<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">${latestHTML}</div>`;
        }
        
        // Hide loading and show container
        if (loadingElement) loadingElement.classList.add('hidden');
        containerElement.classList.remove('hidden');
    }

    appendLatestNews(news) {
        const containerElement = document.getElementById('latest-news-container');
        if (!containerElement) return;
        
        const gridContainer = containerElement.querySelector('.grid');
        if (gridContainer) {
            const newHTML = news.map(article => this.createLatestNewsCard(article)).join('');
            gridContainer.insertAdjacentHTML('beforeend', newHTML);
        }
    }

    createLatestNewsCard(article) {
        const publishDate = new Date(article.created_at).toLocaleDateString('id-ID', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        return `
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
                <div class="h-48 bg-blue-100 flex items-center justify-center overflow-hidden">
                    ${article.featured_image ? 
                        `<img src="${article.featured_image}" alt="${article.title}" class="w-full h-full object-cover">` :
                        `<img src="/static/images/feature1.svg" alt="${article.title}" class="w-full h-full object-cover">`
                    }
                </div>
                <div class="p-4">
                    <h3 class="text-lg font-semibold mb-2 line-clamp-2">${article.title}</h3>
                    <p class="text-gray-600 text-sm mb-3 line-clamp-3">
                        ${article.excerpt || this.truncateText(article.content, 120)}
                    </p>
                    <div class="flex items-center justify-between text-xs text-gray-500 mb-3">
                        <span class="flex items-center">
                            <i class="fas fa-calendar mr-1"></i>
                            ${publishDate}
                        </span>
                        <span class="flex items-center">
                            <i class="fas fa-eye mr-1"></i>
                            ${article.views_count || 0}
                        </span>
                    </div>
                    <button onclick="informasiManager.openNewsDetail('${article.slug}')" class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-full text-sm transition duration-300 transform hover:scale-105">SELENGKAPNYA</button>
                </div>
            </div>
        `;
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
                        <div class="flex items-start justify-between">
                            <div class="flex-1">
                                <div class="flex items-center mb-2">
                                    <i class="${icons[priority]} ${iconColors[priority]} mr-2"></i>
                                    <span class="bg-${priority === 'high' ? 'red' : priority === 'medium' ? 'yellow' : 'blue'}-100 text-${priority === 'high' ? 'red' : priority === 'medium' ? 'yellow' : 'blue'}-800 px-2 py-1 rounded text-xs font-semibold">${priority.toUpperCase()}</span>
                                    <span class="text-gray-500 text-sm ml-3">${this.formatDate(announcement.created_at)}</span>
                                </div>
                                <h3 class="text-xl font-bold mb-3 text-gray-800">${announcement.title}</h3>
                                <p class="text-gray-600 mb-4">
                                    ${announcement.content}
                                </p>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            containerElement.innerHTML = announcementsHTML;
        }
        
        // Hide loading and show container
        if (loadingElement) loadingElement.classList.add('hidden');
        containerElement.classList.remove('hidden');
    }

    renderFooterContact(contact) {
        // Implementation for rendering footer contact information
        const footerContactElements = document.querySelectorAll('.footer-contact');
        if (contact && footerContactElements.length > 0) {
            footerContactElements.forEach(element => {
                element.innerHTML = `
                    <p><i class="fas fa-map-marker-alt mr-2"></i>${contact.address || 'Alamat tidak tersedia'}</p>
                    <p><i class="fas fa-phone mr-2"></i>${contact.phone || 'Telepon tidak tersedia'}</p>
                    <p><i class="fas fa-envelope mr-2"></i>${contact.email || 'Email tidak tersedia'}</p>
                `;
            });
        }
    }

    showFeaturedNewsError() {
        const loadingElement = document.getElementById('featured-loading');
        const containerElement = document.getElementById('featured-news-container');
        
        if (loadingElement) loadingElement.classList.add('hidden');
        if (containerElement) {
            containerElement.innerHTML = `
                <div class="bg-white rounded-lg shadow-md p-6 text-center">
                    <div class="text-red-500 mb-4">
                        <i class="fas fa-exclamation-triangle text-4xl"></i>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">Gagal Memuat Berita Unggulan</h3>
                    <p class="text-gray-600 mb-4">Terjadi kesalahan saat memuat berita unggulan. Silakan coba lagi nanti.</p>
                    <button onclick="informasiManager.loadFeaturedNews()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition duration-300">
                        <i class="fas fa-redo mr-2"></i>Coba Lagi
                    </button>
                </div>
            `;
            containerElement.classList.remove('hidden');
        }
    }

    showNewsError() {
        const newsContainer = document.getElementById('news-container');
        if (newsContainer) {
            newsContainer.innerHTML = `
                <div class="col-span-full bg-white rounded-lg shadow-md p-6 text-center">
                    <div class="text-red-500 mb-4">
                        <i class="fas fa-exclamation-triangle text-4xl"></i>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">Gagal Memuat Berita</h3>
                    <p class="text-gray-600 mb-4">Terjadi kesalahan saat memuat berita. Silakan coba lagi nanti.</p>
                    <button onclick="informasiManager.loadNews()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition duration-300">
                        <i class="fas fa-redo mr-2"></i>Coba Lagi
                    </button>
                </div>
            `;
        }
    }

    showAnnouncementsError() {
        const loadingElement = document.getElementById('announcement-loading');
        const containerElement = document.getElementById('announcement-container');
        
        if (loadingElement) loadingElement.classList.add('hidden');
        if (containerElement) {
            containerElement.innerHTML = `
                <div class="bg-white rounded-lg shadow-md p-6 text-center">
                    <div class="text-red-500 mb-4">
                        <i class="fas fa-exclamation-triangle text-4xl"></i>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">Gagal Memuat Pengumuman</h3>
                    <p class="text-gray-600 mb-4">Terjadi kesalahan saat memuat pengumuman. Silakan coba lagi nanti.</p>
                    <button onclick="informasiManager.loadAnnouncements()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition duration-300">
                        <i class="fas fa-redo mr-2"></i>Coba Lagi
                    </button>
                </div>
            `;
            containerElement.classList.remove('hidden');
        }
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('id-ID', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
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
            container.innerHTML = `<div class="text-center py-8 text-red-500">${message}</div>`;
        }
    }

    truncateText(text, maxLength = 150) {
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }
}

// Initialize when DOM is loaded
let informasiManager;
document.addEventListener('DOMContentLoaded', function() {
    informasiManager = new InformasiPageManager();
    informasiManager.init();
});