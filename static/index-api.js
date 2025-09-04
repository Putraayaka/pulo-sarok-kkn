// API Service untuk halaman index
class IndexApiService {
    constructor() {
        // Using PUBLIC_API_BASE_URL and ADMIN_API_BASE_URL from config.js
    }

    async fetchData(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Fetch data perangkat desa dari API organization
    async getVillageOfficials() {
        return await this.fetchData(`${ADMIN_API_BASE_URL}/organization/api/perangkat-desa/`);
    }

    // Fetch berita terbaru untuk section informasi
    async getLatestNews(limit = 3) {
        return await this.fetchData(`${PUBLIC_API_BASE_URL}/news/`);
    }

    // Fetch data wisata
    async getTourismData() {
        return await this.fetchData(`${ADMIN_API_BASE_URL}/tourism/api/destinations/`);
    }

    // Fetch data unit usaha (BUMG & UKM)
    async getBusinessData() {
        return await this.fetchData(`${ADMIN_API_BASE_URL}/business/api/businesses/`);
    }

    // Fetch kontak desa
    async getVillageContact() {
        return await this.fetchData(`${PUBLIC_API_BASE_URL}/contact/`);
    }

    // Fetch profil desa untuk visi misi
    async getVillageProfile() {
        return await this.fetchData(`${PUBLIC_API_BASE_URL}/village-profile/`);
    }
}

// Class untuk mengelola halaman index
class IndexPageManager {
    constructor() {
        this.apiService = new IndexApiService();
        this.init();
    }

    async init() {
        this.showLoading();
        
        const loadingPromises = [
            this.loadVillageOfficials().catch(error => {
                console.error('Error loading village officials:', error);
                return null;
            }),
            this.loadLatestNews().catch(error => {
                console.error('Error loading latest news:', error);
                return null;
            }),
            this.loadVillageContact().catch(error => {
                console.error('Error loading village contact:', error);
                return null;
            }),
            this.loadVillageProfile().catch(error => {
                console.error('Error loading village profile:', error);
                return null;
            }),
            this.loadTourismData().catch(error => {
                console.error('Error loading tourism data:', error);
                return null;
            }),
            this.loadBusinessData().catch(error => {
                console.error('Error loading business data:', error);
                return null;
            })
        ];
        
        try {
            const results = await Promise.allSettled(loadingPromises);
            
            // Check if any critical data failed to load
            const failedCount = results.filter(result => result.status === 'rejected').length;
            
            if (failedCount > 0) {
                console.warn(`${failedCount} API calls failed, but continuing with available data`);
            }
            
        } catch (error) {
            console.error('Critical error during initialization:', error);
            this.showError('Terjadi kesalahan saat memuat data. Silakan refresh halaman.');
        } finally {
            this.hideLoading();
        }
    }

    showLoading() {
        // Tampilkan loading indicator
        const loadingHTML = `
            <div id="loading-indicator" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div class="bg-white p-6 rounded-lg shadow-lg text-center">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p class="text-gray-600">Memuat data...</p>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', loadingHTML);
    }

    hideLoading() {
        const loadingElement = document.getElementById('loading-indicator');
        if (loadingElement) {
            loadingElement.remove();
        }
    }

    showError(message) {
        const errorHTML = `
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4" role="alert">
                <strong class="font-bold">Error!</strong>
                <span class="block sm:inline"> ${message}</span>
            </div>
        `;
        document.body.insertAdjacentHTML('afterbegin', errorHTML);
    }

    async loadVillageOfficials() {
        try {
            const officials = await this.apiService.getVillageOfficials();
            if (officials && officials.results && officials.results.length > 0) {
                this.renderVillageOfficials(officials.results);
            } else {
                console.log('No village officials data available');
                // Keep default content if no data
            }
        } catch (error) {
            console.error('Error loading village officials:', error);
            // Keep default content on error
        }
    }

    renderVillageOfficials(officials) {
        const container = document.getElementById('perangkat-desa-container');
        if (!container) return;

        // Filter active officials and limit to 6
        const activeOfficials = officials.filter(official => official.is_active).slice(0, 6);
        
        if (activeOfficials.length === 0) {
            console.log('No active officials found');
            return;
        }

        const officialsHTML = activeOfficials.map(official => {
            const photoUrl = official.photo || 'static/images/default-avatar.svg';
            return `
                <div class="bg-white rounded-xl shadow-lg overflow-hidden transform hover:scale-105 transition-all duration-300">
                    <div class="relative">
                        <img src="${photoUrl}" alt="${official.nama}" class="w-full h-48 object-cover">
                        <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                    </div>
                    <div class="p-6 text-center">
                        <h4 class="text-lg font-bold text-gray-800 mb-2">${official.nama}</h4>
                        <p class="text-red-600 font-medium mb-2">${official.jabatan}</p>
                        ${official.pendidikan ? `<p class="text-sm text-gray-600 mb-1">Pendidikan: ${official.pendidikan}</p>` : ''}
                        ${official.alamat ? `<p class="text-sm text-gray-500">Alamat: ${official.alamat}</p>` : ''}
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = officialsHTML;
    }

    async loadLatestNews() {
        try {
            const newsData = await this.apiService.getLatestNews(3);
            if (newsData && newsData.results && newsData.results.length > 0) {
                this.renderLatestNews(newsData.results);
            } else {
                this.showNewsError();
            }
        } catch (error) {
            console.error('Error loading latest news:', error);
            this.showNewsError();
        }
    }

    showNewsError() {
        const container = document.getElementById('news-container');
        if (container) {
            container.innerHTML = '<p class="text-center text-gray-500 py-8">Tidak ada berita terbaru saat ini.</p>';
        }
    }

    renderLatestNews(newsData) {
        const container = document.getElementById('news-container');
        if (!container) return;

        const newsHTML = newsData.slice(0, 3).map(news => {
            const imageUrl = news.featured_image || 'static/images/default-news.jpg';
            const publishDate = new Date(news.published_at || news.created_at).toLocaleDateString('id-ID', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
            
            return `
                <div class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
                    <img src="${imageUrl}" alt="${news.title}" class="w-full h-48 object-cover">
                    <div class="p-6">
                        <div class="flex items-center text-sm text-gray-500 mb-2">
                            <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"></path>
                            </svg>
                            ${publishDate}
                        </div>
                        <h3 class="text-lg font-bold text-gray-800 mb-3 line-clamp-2">${news.title}</h3>
                        <p class="text-gray-600 text-sm line-clamp-3 mb-4">${news.excerpt || news.content?.substring(0, 150) + '...' || 'Tidak ada ringkasan tersedia.'}</p>
                        <a href="/berita/${news.slug || news.id}/" class="inline-flex items-center text-red-600 hover:text-red-700 font-medium text-sm">
                            Baca Selengkapnya
                            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                            </svg>
                        </a>
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = newsHTML;
    }

    async loadVillageContact() {
        try {
            const contactData = await this.apiService.getVillageContact();
            if (contactData && contactData.results && contactData.results.length > 0) {
                const contact = contactData.results[0];
                
                // Update contact information in footer or contact section
                const phoneElements = document.querySelectorAll('[data-contact="phone"]');
                const emailElements = document.querySelectorAll('[data-contact="email"]');
                const addressElements = document.querySelectorAll('[data-contact="address"]');
                
                if (contact.phone && phoneElements.length > 0) {
                    phoneElements.forEach(el => {
                        el.textContent = contact.phone;
                        el.href = `tel:${contact.phone}`;
                    });
                }
                
                if (contact.email && emailElements.length > 0) {
                    emailElements.forEach(el => {
                        el.textContent = contact.email;
                        el.href = `mailto:${contact.email}`;
                    });
                }
                
                if (contact.address && addressElements.length > 0) {
                    addressElements.forEach(el => {
                        el.textContent = contact.address;
                    });
                }
                
                // Update contact section if exists
                const contactSection = document.getElementById('contact-info');
                if (contactSection && contact.address) {
                    contactSection.innerHTML = `
                        <div class="flex items-start space-x-3">
                            <svg class="w-5 h-5 text-red-600 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            </svg>
                            <div>
                                <p class="font-medium text-gray-800">Alamat Kantor Desa</p>
                                <p class="text-gray-600 text-sm">${contact.address}</p>
                                ${contact.phone ? `
                                    <div class="flex items-center mt-2">
                                        <svg class="w-4 h-4 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                                        </svg>
                                        <span class="text-sm text-gray-600">${contact.phone}</span>
                                    </div>
                                ` : ''}
                                ${contact.email ? `
                                    <div class="flex items-center mt-1">
                                        <svg class="w-4 h-4 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                                        </svg>
                                        <span class="text-sm text-gray-600">${contact.email}</span>
                                    </div>
                                ` : ''}
                            </div>
                        </div>
                    `;
                }
            } else {
                this.setDefaultContactInfo();
            }
        } catch (error) {
            console.error('Error loading village contact:', error);
            this.setDefaultContactInfo();
        }
    }

    setDefaultContactInfo() {
        // Set default contact info if API fails
        const phoneElements = document.querySelectorAll('[data-contact="phone"]');
        phoneElements.forEach(el => {
            el.textContent = '+62 812-3456-7890';
            el.href = 'tel:+6281234567890';
        });
        
        const emailElements = document.querySelectorAll('[data-contact="email"]');
        emailElements.forEach(el => {
            el.textContent = 'info@pulosarok.desa.id';
            el.href = 'mailto:info@pulosarok.desa.id';
        });
        
        const addressElements = document.querySelectorAll('[data-contact="address"]');
        addressElements.forEach(el => {
            el.textContent = 'Kampung Pulo Sarok, Kecamatan Singkil, Kabupaten Aceh Singkil';
        });
    }

    async loadVillageProfile() {
        try {
            const profileData = await this.apiService.getVillageProfile();
            if (profileData && profileData.results && profileData.results.length > 0) {
                this.renderVillageProfile(profileData.results[0]);
            } else {
                this.setDefaultVisionMission();
            }
        } catch (error) {
            console.error('Error loading village profile:', error);
            this.setDefaultVisionMission();
        }
    }

    setDefaultVisionMission() {
        // Set default vision and mission if API fails
        const visionElement = document.getElementById('village-vision');
        const missionElement = document.getElementById('village-mission');
        
        if (visionElement) {
            visionElement.innerHTML = `
                <p class="text-gray-600 leading-relaxed">
                    Menjadi kampung yang maju, mandiri, dan sejahtera dengan tetap melestarikan nilai-nilai budaya lokal dan kearifan lingkungan.
                </p>
            `;
        }
        
        if (missionElement) {
            missionElement.innerHTML = `
                <div class="text-gray-600 space-y-3">
                    <div class="flex items-start mb-3">
                        <span class="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">1</span>
                        <span>Meningkatkan kualitas sumber daya manusia melalui pendidikan dan pelatihan</span>
                    </div>
                    <div class="flex items-start mb-3">
                        <span class="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">2</span>
                        <span>Mengembangkan potensi ekonomi lokal</span>
                    </div>
                    <div class="flex items-start mb-3">
                        <span class="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">3</span>
                        <span>Melestarikan budaya dan lingkungan</span>
                    </div>
                    <div class="flex items-start mb-3">
                        <span class="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">4</span>
                        <span>Meningkatkan pelayanan publik yang berkualitas</span>
                    </div>
                </div>
            `;
        }
    }

    renderVillageProfile(profile) {
        const visionElement = document.getElementById('village-vision');
        const missionElement = document.getElementById('village-mission');
        
        if (visionElement && profile.vision) {
            visionElement.innerHTML = `
                <p class="text-gray-600 leading-relaxed">${profile.vision}</p>
            `;
        }
        
        if (missionElement) {
            if (profile.mission) {
                // Check if mission is an array or string
                let missionContent = '';
                if (Array.isArray(profile.mission)) {
                    missionContent = profile.mission.map((mission, index) => 
                        `<div class="flex items-start mb-3">
                            <span class="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">${index + 1}</span>
                            <span>${mission}</span>
                        </div>`
                    ).join('');
                } else if (profile.mission) {
                    // If it's a string, try to split by common delimiters
                    const missions = profile.mission.split(/[\n\r]+|\d+\.|[•-]/).filter(m => m.trim());
                    if (missions.length > 1) {
                        missionContent = missions.map((mission, index) => 
                            `<div class="flex items-start mb-3">
                                <span class="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">${index + 1}</span>
                                <span>${mission.trim()}</span>
                            </div>`
                        ).join('');
                    } else {
                        missionContent = `<p class="text-gray-600 leading-relaxed">${profile.mission}</p>`;
                    }
                }
                
                if (missionContent) {
                    missionElement.innerHTML = `<div class="text-gray-600 space-y-3">${missionContent}</div>`;
                } else {
                    // Fallback to default
                    missionElement.innerHTML = `
                        <div class="text-gray-600 space-y-3">
                            <div class="flex items-start mb-3">
                                <span class="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">1</span>
                                <span>Meningkatkan kualitas sumber daya manusia melalui pendidikan dan pelatihan</span>
                            </div>
                            <div class="flex items-start mb-3">
                                <span class="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">2</span>
                                <span>Mengembangkan potensi ekonomi lokal</span>
                            </div>
                            <div class="flex items-start mb-3">
                                <span class="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">3</span>
                                <span>Melestarikan budaya dan lingkungan</span>
                            </div>
                            <div class="flex items-start mb-3">
                                <span class="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">4</span>
                                <span>Meningkatkan pelayanan publik yang berkualitas</span>
                            </div>
                        </div>
                    `;
                }
            }
        }
    }

    async loadTourismData() {
        try {
            const tourismData = await this.apiService.getTourismData();
            if (tourismData && tourismData.results && tourismData.results.length > 0) {
                this.renderTourismData(tourismData.results);
            } else {
                console.log('No tourism data available, keeping default content');
                this.renderDefaultTourismContent();
            }
        } catch (error) {
            console.error('Error loading tourism data:', error);
            this.renderDefaultTourismContent();
        }
    }

    renderTourismData(destinations) {
        const tourismContainer = document.getElementById('tourism-container');
        if (!tourismContainer) return;

        // Filter active destinations and limit to 3
        const activeDestinations = destinations.filter(dest => dest.is_active !== false).slice(0, 3);
        
        if (activeDestinations.length === 0) {
            this.renderDefaultTourismContent();
            return;
        }

        const tourismHTML = `
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                ${activeDestinations.map(destination => `
                    <div class="bg-white/10 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-105">
                        ${destination.featured_image ? `
                            <img src="${destination.featured_image}" alt="${destination.title || destination.name}" class="w-full h-48 object-cover">
                        ` : `
                            <div class="w-full h-48 bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center">
                                <svg class="w-16 h-16 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                                </svg>
                            </div>
                        `}
                        <div class="p-6">
                            <h4 class="text-xl font-bold text-white mb-3">${destination.title || destination.name}</h4>
                            <p class="text-green-200 text-sm leading-relaxed">
                                ${destination.short_description || destination.description || 'Destinasi wisata yang menawarkan pengalaman tak terlupakan dengan keindahan alam dan budaya lokal.'}
                            </p>
                            ${destination.facilities ? `
                                <div class="mt-3 flex flex-wrap gap-2">
                                    ${destination.facilities.split(',').slice(0, 3).map(facility => `
                                        <span class="bg-green-600 text-white text-xs px-2 py-1 rounded-full">${facility.trim()}</span>
                                    `).join('')}
                                </div>
                            ` : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        tourismContainer.innerHTML = tourismHTML;
    }

    renderDefaultTourismContent() {
        const tourismContainer = document.getElementById('tourism-container');
        if (!tourismContainer) return;

        const defaultHTML = `
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div class="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                    <h4 class="text-xl font-bold text-white mb-3">Wisata Alam</h4>
                    <p class="text-green-200 text-sm leading-relaxed">
                        Jelajahi keindahan alam pegunungan dengan pemandangan yang menakjubkan dan udara segar yang menyegarkan.
                    </p>
                </div>
                <div class="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                    <h4 class="text-xl font-bold text-white mb-3">Wisata Sejarah</h4>
                    <p class="text-green-200 text-sm leading-relaxed">
                        Temukan jejak sejarah dan warisan budaya yang masih terjaga dengan baik di berbagai situs bersejarah.
                    </p>
                </div>
                <div class="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                    <h4 class="text-xl font-bold text-white mb-3">Wisata Kuliner</h4>
                    <p class="text-green-200 text-sm leading-relaxed">
                        Nikmati kelezatan kuliner khas daerah yang autentik dengan cita rasa yang tak terlupakan.
                    </p>
                </div>
            </div>
        `;

        tourismContainer.innerHTML = defaultHTML;
    }

    async loadBusinessData() {
        try {
            const businessData = await this.apiService.getBusinessData();
            if (businessData && businessData.results && businessData.results.length > 0) {
                this.renderBusinessData(businessData.results);
            } else {
                console.log('No business data available, keeping default content');
                this.renderDefaultBusinessContent();
            }
        } catch (error) {
            console.error('Error loading business data:', error);
            this.renderDefaultBusinessContent();
        }
    }

    renderBusinessData(businesses) {
        const businessContainer = document.getElementById('business-container');
        if (!businessContainer) return;

        // Filter active businesses and limit to 6
        const activeBusinesses = businesses.filter(business => business.is_active !== false).slice(0, 6);
        
        if (activeBusinesses.length === 0) {
            this.renderDefaultBusinessContent();
            return;
        }

        const businessHTML = `
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                ${activeBusinesses.map(business => `
                    <div class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:scale-105">
                        ${business.logo || business.image ? `
                            <img src="${business.logo || business.image}" alt="${business.name}" class="w-full h-32 object-cover">
                        ` : `
                            <div class="w-full h-32 bg-gradient-to-br from-red-400 to-red-600 flex items-center justify-center">
                                <svg class="w-12 h-12 text-white/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                                </svg>
                            </div>
                        `}
                        <div class="p-4 text-center">
                            <h4 class="font-bold text-lg mb-2 text-red-900">${business.name}</h4>
                            <p class="text-gray-600 text-sm mb-3">
                                ${business.description || 'Unit usaha yang berkontribusi dalam perekonomian kampung.'}
                            </p>
                            ${business.category ? `
                                <span class="inline-block bg-red-100 text-red-600 text-xs px-3 py-1 rounded-full mb-2">
                                    ${business.category}
                                </span>
                            ` : ''}
                            ${business.contact_phone ? `
                                <div class="flex items-center justify-center text-sm text-gray-500 mt-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                                    </svg>
                                    <span>${business.contact_phone}</span>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        businessContainer.innerHTML = businessHTML;
    }

    renderDefaultBusinessContent() {
        const businessContainer = document.getElementById('business-container');
        if (!businessContainer) return;

        const defaultHTML = `
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                    <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                        </svg>
                    </div>
                    <h4 class="font-bold text-lg mb-2 text-red-900">BUMG Pulo Sarok</h4>
                    <p class="text-gray-600 text-sm mb-3">Badan Usaha Milik Gampong yang mengelola berbagai unit usaha untuk kesejahteraan masyarakat.</p>
                    <span class="inline-block bg-red-100 text-red-600 text-xs px-3 py-1 rounded-full">BUMG</span>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                    <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <h4 class="font-bold text-lg mb-2 text-red-900">UKM Kerajinan</h4>
                    <p class="text-gray-600 text-sm mb-3">Usaha Kecil Menengah yang menghasilkan berbagai produk kerajinan tangan khas daerah.</p>
                    <span class="inline-block bg-red-100 text-red-600 text-xs px-3 py-1 rounded-full">UKM</span>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                    <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
                        </svg>
                    </div>
                    <h4 class="font-bold text-lg mb-2 text-red-900">Toko Kelontong</h4>
                    <p class="text-gray-600 text-sm mb-3">Usaha perdagangan yang menyediakan kebutuhan sehari-hari masyarakat kampung.</p>
                    <span class="inline-block bg-red-100 text-red-600 text-xs px-3 py-1 rounded-full">Perdagangan</span>
                </div>
            </div>
        `;

        businessContainer.innerHTML = defaultHTML;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize IndexPageManager
    new IndexPageManager();
});