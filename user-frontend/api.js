// API Integration for Kampung Pulo Sarok Frontend
// Import config
const API_BASE_URL = "http://127.0.0.1:8000/pulosarok";

// Utility function for API calls
class ApiService {
    static async fetchData(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            ...options
        };

        try {
            const response = await fetch(url, defaultOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Get news/berita
    static async getNews() {
        return await this.fetchData('/news/news/');
    }

    // Get announcements
    static async getAnnouncements() {
        return await this.fetchData('/news/public/announcements/');
    }

    // Submit letter request
    static async submitLetterRequest(data) {
        return await this.fetchData('/letters/api/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    // Track letter
    static async trackLetter(trackingCode) {
        return await this.fetchData(`/letters/api/track/${trackingCode}/`);
    }

    // Get letter types
    static async getLetterTypes() {
        return await this.fetchData('/letters/api/jenis-surat/');
    }
}

// News page functionality
class NewsPage {
    constructor() {
        this.newsContainer = document.getElementById('news-container');
        this.announcementContainer = document.getElementById('announcement-container');
        this.loadingElement = document.getElementById('loading');
    }

    showLoading() {
        if (this.loadingElement) {
            this.loadingElement.style.display = 'block';
        }
    }

    hideLoading() {
        if (this.loadingElement) {
            this.loadingElement.style.display = 'none';
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4';
        errorDiv.innerHTML = `
            <strong>Error:</strong> ${message}
            <p class="text-sm mt-2">Pastikan backend server berjalan di ${API_BASE_URL}</p>
        `;
        
        if (this.newsContainer) {
            this.newsContainer.insertBefore(errorDiv, this.newsContainer.firstChild);
        }
    }

    formatDate(dateString) {
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            timeZone: 'Asia/Jakarta'
        };
        return new Date(dateString).toLocaleDateString('id-ID', options);
    }

    createNewsCard(news) {
        return `
            <article class="bg-gray-50 rounded-lg shadow-md overflow-hidden hover:shadow-lg transition duration-300">
                <img src="${news.image || 'asset/news-placeholder.svg'}" alt="${news.title}" class="w-full h-48 object-cover">
                <div class="p-6">
                    <div class="flex items-center mb-3">
                        <span class="bg-blue-500 text-white px-2 py-1 rounded text-xs font-semibold mr-2">${news.category || 'BERITA'}</span>
                        <span class="text-gray-500 text-sm">${this.formatDate(news.created_at || news.date)}</span>
                    </div>
                    <h3 class="text-lg font-bold mb-3 text-gray-800">${news.title}</h3>
                    <p class="text-gray-600 text-sm mb-4">
                        ${news.excerpt || news.content?.substring(0, 150) + '...' || 'Tidak ada deskripsi tersedia.'}
                    </p>
                    <a href="#" class="text-blue-600 hover:text-blue-800 font-semibold text-sm" onclick="NewsPage.viewDetail(${news.id})">
                        Baca Selengkapnya <i class="fas fa-arrow-right ml-1"></i>
                    </a>
                </div>
            </article>
        `;
    }

    async loadNews() {
        try {
            this.showLoading();
            const newsData = await ApiService.getNews();
            
            if (this.newsContainer && newsData && newsData.length > 0) {
                this.newsContainer.innerHTML = newsData.map(news => this.createNewsCard(news)).join('');
            } else if (this.newsContainer) {
                this.newsContainer.innerHTML = `
                    <div class="col-span-full text-center py-8">
                        <p class="text-gray-500">Belum ada berita tersedia.</p>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error loading news:', error);
            this.showError('Gagal memuat berita. Silakan coba lagi nanti.');
        } finally {
            this.hideLoading();
        }
    }

    async loadAnnouncements() {
        try {
            const announcements = await ApiService.getAnnouncements();
            
            if (this.announcementContainer && announcements && announcements.length > 0) {
                this.announcementContainer.innerHTML = announcements.map(announcement => `
                    <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
                        <div class="flex">
                            <div class="flex-shrink-0">
                                <i class="fas fa-bullhorn text-yellow-400"></i>
                            </div>
                            <div class="ml-3">
                                <h4 class="text-sm font-medium text-yellow-800">${announcement.title}</h4>
                                <p class="mt-1 text-sm text-yellow-700">${announcement.content}</p>
                                <p class="mt-2 text-xs text-yellow-600">${this.formatDate(announcement.created_at)}</p>
                            </div>
                        </div>
                    </div>
                `).join('');
            }
        } catch (error) {
            console.error('Error loading announcements:', error);
        }
    }

    static viewDetail(newsId) {
        // Implement news detail view
        alert(`Viewing news detail for ID: ${newsId}`);
    }

    init() {
        if (document.getElementById('news-container') || document.getElementById('announcement-container')) {
            this.loadNews();
            this.loadAnnouncements();
        }
    }
}

// Letter form functionality
class LetterForm {
    constructor() {
        this.form = document.getElementById('letter-form');
        this.letterTypeSelect = document.getElementById('letter-type');
        this.trackingForm = document.getElementById('tracking-form');
        this.init();
    }

    async loadLetterTypes() {
        try {
            const letterTypes = await ApiService.getLetterTypes();
            
            if (this.letterTypeSelect && letterTypes) {
                this.letterTypeSelect.innerHTML = '<option value="">Pilih Jenis Surat</option>' +
                    letterTypes.map(type => `<option value="${type.id}">${type.name}</option>`).join('');
            }
        } catch (error) {
            console.error('Error loading letter types:', error);
        }
    }

    async submitForm(formData) {
        try {
            const result = await ApiService.submitLetterRequest(formData);
            
            // Show success message
            this.showMessage('success', `Pengajuan surat berhasil! Kode tracking: ${result.tracking_code}`);
            
            // Reset form
            if (this.form) {
                this.form.reset();
            }
            
            return result;
        } catch (error) {
            console.error('Error submitting form:', error);
            this.showMessage('error', 'Gagal mengajukan surat. Silakan coba lagi.');
            throw error;
        }
    }

    async trackLetter(trackingCode) {
        try {
            const result = await ApiService.trackLetter(trackingCode);
            
            // Display tracking result
            this.displayTrackingResult(result);
            
            return result;
        } catch (error) {
            console.error('Error tracking letter:', error);
            this.showMessage('error', 'Kode tracking tidak ditemukan.');
            throw error;
        }
    }

    showMessage(type, message) {
        const messageDiv = document.createElement('div');
        const bgColor = type === 'success' ? 'bg-green-100 border-green-400 text-green-700' : 'bg-red-100 border-red-400 text-red-700';
        
        messageDiv.className = `${bgColor} border px-4 py-3 rounded mb-4`;
        messageDiv.innerHTML = message;
        
        // Insert at top of form
        if (this.form) {
            this.form.insertBefore(messageDiv, this.form.firstChild);
            
            // Remove after 5 seconds
            setTimeout(() => {
                if (messageDiv.parentNode) {
                    messageDiv.parentNode.removeChild(messageDiv);
                }
            }, 5000);
        }
    }

    displayTrackingResult(result) {
        const resultDiv = document.getElementById('tracking-result');
        if (resultDiv) {
            resultDiv.innerHTML = `
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h4 class="font-semibold text-blue-800 mb-2">Status Pengajuan Surat</h4>
                    <p><strong>Jenis Surat:</strong> ${result.letter_type}</p>
                    <p><strong>Status:</strong> <span class="px-2 py-1 rounded text-sm ${this.getStatusClass(result.status)}">${result.status}</span></p>
                    <p><strong>Tanggal Pengajuan:</strong> ${this.formatDate(result.created_at)}</p>
                    ${result.notes ? `<p><strong>Catatan:</strong> ${result.notes}</p>` : ''}
                </div>
            `;
        }
    }

    getStatusClass(status) {
        const statusClasses = {
            'pending': 'bg-yellow-200 text-yellow-800',
            'processing': 'bg-blue-200 text-blue-800',
            'completed': 'bg-green-200 text-green-800',
            'rejected': 'bg-red-200 text-red-800'
        };
        return statusClasses[status] || 'bg-gray-200 text-gray-800';
    }

    formatDate(dateString) {
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            timeZone: 'Asia/Jakarta'
        };
        return new Date(dateString).toLocaleDateString('id-ID', options);
    }

    init() {
        // Load letter types
        this.loadLetterTypes();
        
        // Handle form submission
        if (this.form) {
            this.form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = new FormData(this.form);
                const data = Object.fromEntries(formData.entries());
                
                await this.submitForm(data);
            });
        }
        
        // Handle tracking form
        if (this.trackingForm) {
            this.trackingForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const trackingCode = document.getElementById('tracking-code').value;
                if (trackingCode) {
                    await this.trackLetter(trackingCode);
                }
            });
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize news page if on informasi.html
    if (window.location.pathname.includes('informasi.html') || document.getElementById('news-container')) {
        const newsPage = new NewsPage();
        newsPage.init();
    }
    
    // Initialize letter form if on pengajuan-surat.html
    if (window.location.pathname.includes('pengajuan-surat.html') || document.getElementById('letter-form')) {
        new LetterForm();
    }
});

// Export for global use
window.ApiService = ApiService;
window.NewsPage = NewsPage;
window.LetterForm = LetterForm;