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
                console.warn(`${failedCount} data sources failed to load, but continuing with available data`);
            }
            
            console.log('Page initialization completed successfully');
        } catch (error) {
            console.error('Critical error during page initialization:', error);
            this.showError('Terjadi kesalahan saat memuat halaman. Beberapa data mungkin tidak tersedia.');
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
        const loadingElement = document.getElementById('officials-loading');
        const containerElement = document.getElementById('officials-container');
        const errorElement = document.getElementById('officials-error');
        
        try {
            // Show loading state
            if (loadingElement) loadingElement.classList.remove('hidden');
            if (containerElement) containerElement.classList.add('hidden');
            if (errorElement) errorElement.classList.add('hidden');
            
            const officials = await this.apiService.getVillageOfficials();
            
            // Hide loading and show content
            if (loadingElement) loadingElement.classList.add('hidden');
            
            if (officials && officials.length > 0) {
                this.renderVillageOfficials(officials);
                if (containerElement) containerElement.classList.remove('hidden');
            } else {
                // Show empty state or error
                if (errorElement) {
                    errorElement.querySelector('p').textContent = 'Tidak ada data perangkat desa';
                    errorElement.classList.remove('hidden');
                }
            }
        } catch (error) {
            console.error('Error loading village officials:', error);
            
            // Hide loading and show error
            if (loadingElement) loadingElement.classList.add('hidden');
            if (errorElement) errorElement.classList.remove('hidden');
        }
    }

    renderVillageOfficials(officials) {
        const officialsGrid = document.getElementById('officials-grid');
        if (!officialsGrid || !officials || officials.length === 0) return;

        const colors = [
            'from-blue-500 to-blue-600',
            'from-green-500 to-green-600', 
            'from-purple-500 to-purple-600',
            'from-red-500 to-red-600',
            'from-indigo-500 to-indigo-600',
            'from-yellow-500 to-yellow-600'
        ];

        const officialsHTML = officials.map((official, index) => {
            const colorClass = colors[index % colors.length];
            const textColorClass = colorClass.includes('yellow') ? 'text-yellow-800' : 'text-white';
            const bgColorClass = colorClass.includes('yellow') ? 'text-yellow-100' : 
                               colorClass.includes('blue') ? 'text-blue-100' :
                               colorClass.includes('green') ? 'text-green-100' :
                               colorClass.includes('purple') ? 'text-purple-100' :
                               colorClass.includes('red') ? 'text-red-100' : 'text-indigo-100';
            
            return `
                <div class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition duration-300">
                    <div class="bg-gradient-to-r ${colorClass} p-6 text-center">
                        <div class="w-24 h-24 bg-white rounded-full mx-auto mb-4 flex items-center justify-center">
                            ${official.foto_profil ? 
                                `<img src="${official.foto_profil}" alt="${official.nama}" class="w-20 h-20 rounded-full object-cover">` :
                                `<svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 ${colorClass.includes('yellow') ? 'text-yellow-500' : colorClass.includes('blue') ? 'text-blue-500' : colorClass.includes('green') ? 'text-green-500' : colorClass.includes('purple') ? 'text-purple-500' : colorClass.includes('red') ? 'text-red-500' : 'text-indigo-500'}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>`
                            }
                        </div>
                        <h3 class="text-xl font-bold ${textColorClass} mb-2">${official.nama}</h3>
                        <p class="${bgColorClass}">${official.jabatan}</p>
                    </div>
                    <div class="p-6">
                        <p class="text-gray-600 text-sm mb-4">
                            ${official.deskripsi_tugas || 'Melayani masyarakat dengan dedikasi tinggi.'}
                        </p>
                        ${official.kontak_whatsapp ? `
                            <div class="flex items-center text-sm text-gray-500">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                                </svg>
                                <span>${official.kontak_whatsapp}</span>
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;
        }).join('');

        officialsGrid.innerHTML = officialsHTML;
    }

    async loadLatestNews() {
        try {
            const news = await this.apiService.getLatestNews(3);
            this.renderLatestNews(news);
        } catch (error) {
            console.error('Error loading latest news:', error);
            this.showNewsError();
        }
    }

    showNewsError() {
        const newsContainer = document.getElementById('news-container');
        const newsLoading = document.getElementById('news-loading');
        const newsError = document.getElementById('news-error');
        
        if (newsLoading) newsLoading.classList.add('hidden');
        if (newsError) newsError.classList.remove('hidden');
    }

    renderLatestNews(newsData) {
        const newsContainer = document.getElementById('news-container');
        const newsLoading = document.getElementById('news-loading');
        const newsError = document.getElementById('news-error');
        
        if (!newsContainer) return;
        
        // Hide loading
        if (newsLoading) newsLoading.classList.add('hidden');
        
        if (!newsData || !newsData.results || newsData.results.length === 0) {
            // Show no news message
            newsContainer.innerHTML = `
                <div class="col-span-full text-center py-8">
                    <p class="text-gray-500">Belum ada berita terkini.</p>
                </div>
            `;
            return;
        }

        const newsHTML = newsData.results.slice(0, 3).map(article => {
            const publishDate = new Date(article.created_at).toLocaleDateString('id-ID', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
            
            return `
                <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
                    <div class="h-48 bg-blue-100 flex items-center justify-center overflow-hidden">
                        ${article.image ? 
                            `<img src="${article.image}" alt="${article.title}" class="w-full h-full object-cover">` :
                            `<img src="asset/feature1.svg" alt="${article.title}" class="w-full h-full object-cover">`
                        }
                    </div>
                    <div class="p-4">
                        <h3 class="text-lg font-semibold mb-2 line-clamp-2">${article.title}</h3>
                        <p class="text-gray-600 text-sm mb-3 line-clamp-3">
                            ${article.excerpt || article.content.substring(0, 120) + '...'}
                        </p>
                        <div class="flex items-center justify-between text-xs text-gray-500 mb-3">
                            <span class="flex items-center">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                                ${publishDate}
                            </span>
                        </div>
                        <a href="/informasi/" class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-full text-sm inline-block transition duration-300 transform hover:scale-105">SELENGKAPNYA</a>
                    </div>
                </div>
            `;
        }).join('');

        newsContainer.innerHTML = newsHTML;
    }

    async loadVillageContact() {
        try {
            const contactData = await this.apiService.getVillageContact();
            
            if (contactData && contactData.results && contactData.results.length > 0) {
                const contact = contactData.results[0];
                
                // Update phone number - find by placeholder text
                const phoneElements = document.querySelectorAll('a[href^="tel:"]');
                for (let phoneElement of phoneElements) {
                    if (phoneElement.textContent.includes('+62 XXX-XXXX-XXXX') || phoneElement.textContent.includes('0XXX-XXXX-XXXX')) {
                        if (contact.phone) {
                            phoneElement.href = `tel:${contact.phone}`;
                            phoneElement.textContent = contact.phone;
                        } else {
                            phoneElement.href = 'tel:+6281234567890';
                            phoneElement.textContent = '+62 812-3456-7890';
                        }
                        break;
                    }
                }
                
                // Update office hours - find by text content
                const textElements = document.querySelectorAll('p, div, span');
                for (let element of textElements) {
                    if (element.textContent.includes('Senin - Jumat: 08:00 - 16:00')) {
                        if (contact.office_hours) {
                            element.innerHTML = `<strong>Jam Operasional:</strong><br>${contact.office_hours}`;
                        } else {
                            element.innerHTML = '<strong>Jam Operasional:</strong><br>Senin - Jumat: 08:00 - 16:00 WIB<br>Sabtu: 08:00 - 12:00 WIB';
                        }
                        break;
                    }
                }
                
                // Update email if available
                if (contact.email) {
                    const emailElements = document.querySelectorAll('a[href^="mailto:"]');
                    for (let emailElement of emailElements) {
                        emailElement.href = `mailto:${contact.email}`;
                        emailElement.textContent = contact.email;
                        break;
                    }
                }
                
                // Update address if available
                if (contact.address) {
                    const addressElements = document.querySelectorAll('p, div, span');
                    for (let element of addressElements) {
                        if (element.textContent.includes('Jl. Raya Pulo Sarok') || element.textContent.includes('Alamat:')) {
                            element.innerHTML = `<strong>Alamat:</strong><br>${contact.address}`;
                            break;
                        }
                    }
                }
            } else {
                // Set default contact info if no data available
                this.setDefaultContactInfo();
            }
        } catch (error) {
            console.error('Error loading village contact:', error);
            // Set default contact info on error
            this.setDefaultContactInfo();
        }
    }

    setDefaultContactInfo() {
        // Set default phone number
        const phoneElements = document.querySelectorAll('a[href^="tel:"]');
        for (let phoneElement of phoneElements) {
            if (phoneElement.textContent.includes('+62 XXX-XXXX-XXXX') || phoneElement.textContent.includes('0XXX-XXXX-XXXX')) {
                phoneElement.href = 'tel:+6281234567890';
                phoneElement.textContent = '+62 812-3456-7890';
                break;
            }
        }
        
        // Set default office hours
        const textElements = document.querySelectorAll('p, div, span');
        for (let element of textElements) {
            if (element.textContent.includes('Senin - Jumat: 08:00 - 16:00')) {
                element.innerHTML = '<strong>Jam Operasional:</strong><br>Senin - Jumat: 08:00 - 16:00 WIB<br>Sabtu: 08:00 - 12:00 WIB';
                break;
            }
        }
    }

    async loadVillageProfile() {
        try {
            const profileData = await this.apiService.getVillageProfile();
            
            if (profileData && profileData.results && profileData.results.length > 0) {
                const profile = profileData.results[0];
                this.renderVillageProfile(profile);
            } else {
                // Set default content if no data available
                this.setDefaultVisionMission();
            }
        } catch (error) {
            console.error('Error loading village profile:', error);
            // Set default content on error
            this.setDefaultVisionMission();
        }
    }

    setDefaultVisionMission() {
        // Set default vision
        const visionElements = document.querySelectorAll('p');
        for (let element of visionElements) {
            if (element.textContent.includes('Memuat visi...')) {
                element.textContent = 'Mewujudkan Kampung Pulo Sarok yang maju, mandiri, dan sejahtera.';
                break;
            }
        }
        
        // Set default mission
        const missionElements = document.querySelectorAll('p');
        for (let element of missionElements) {
            if (element.textContent.includes('Memuat misi...')) {
                element.innerHTML = `
                    1. Meningkatkan kualitas sumber daya manusia<br>
                    2. Mengembangkan potensi ekonomi lokal<br>
                    3. Melestarikan budaya dan lingkungan<br>
                    4. Meningkatkan pelayanan publik yang berkualitas
                `;
                break;
            }
        }
    }

    renderVillageProfile(profile) {
        if (!profile) {
            this.setDefaultVisionMission();
            return;
        }

        // Update vision - find element by text content more reliably
        const visionElements = document.querySelectorAll('p');
        for (let element of visionElements) {
            if (element.textContent.includes('Memuat visi...')) {
                if (profile.vision) {
                    element.textContent = `"${profile.vision}"`;
                } else {
                    element.textContent = '"Mewujudkan Kampung Pulo Sarok yang maju, mandiri, dan sejahtera."';
                }
                element.className = 'text-gray-600 leading-relaxed text-lg';
                break;
            }
        }
        
        // Update mission - find element by text content more reliably
        const missionElements = document.querySelectorAll('p');
        for (let element of missionElements) {
            if (element.textContent.includes('Memuat misi...')) {
                if (profile.mission || (profile.missions && profile.missions.length > 0)) {
                    let missionContent = '';
                    
                    if (profile.missions && Array.isArray(profile.missions)) {
                        // Handle array of missions
                        missionContent = profile.missions.map((mission, index) => 
                            `<div class="flex items-start mb-3">
                                <span class="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">${index + 1}</span>
                                <span>${mission}</span>
                            </div>`
                        ).join('');
                    } else if (profile.mission) {
                        // Handle string mission
                        const missions = profile.mission.split('\n').filter(m => m.trim());
                        if (missions.length > 1) {
                            missionContent = missions.map((mission, index) => 
                                `<div class="flex items-start mb-3">
                                    <span class="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">${index + 1}</span>
                                    <span>${mission.trim()}</span>
                                </div>`
                            ).join('');
                        } else {
                            missionContent = `<div class="text-gray-600">${profile.mission}</div>`;
                        }
                    }
                    
                    element.innerHTML = missionContent;
                } else {
                    element.innerHTML = `
                        <div class="flex items-start mb-3">
                            <span class="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">1</span>
                            <span>Meningkatkan kualitas sumber daya manusia</span>
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
                    `;
                }
                element.className = 'text-gray-600 space-y-3';
                break;
            }
        }
    }

    async loadTourismData() {
        const loadingElement = document.getElementById('tourism-loading');
        const containerElement = document.getElementById('tourism-container');
        
        try {
            // Show loading state
            if (loadingElement) loadingElement.classList.remove('hidden');
            if (containerElement) containerElement.classList.add('hidden');
            
            const tourismData = await this.apiService.getTourismData();
            
            // Hide loading and show content
            if (loadingElement) loadingElement.classList.add('hidden');
            
            if (tourismData && tourismData.results && tourismData.results.length > 0) {
                this.renderTourismData(tourismData.results);
                if (containerElement) containerElement.classList.remove('hidden');
            } else {
                // Show default content if no data
                this.renderDefaultTourismContent();
                if (containerElement) containerElement.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Error loading tourism data:', error);
            // Show default content on error
            this.renderDefaultTourismContent();
            if (loadingElement) loadingElement.classList.add('hidden');
            if (containerElement) containerElement.classList.remove('hidden');
        }
    }

    renderTourismData(destinations) {
        const tourismContainer = document.getElementById('tourism-container');
        if (!tourismContainer || !destinations || destinations.length === 0) {
            this.renderDefaultTourismContent();
            return;
        }

        const tourismHTML = `
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
                <!-- Deskripsi Wisata -->
                <div>
                    <h3 class="text-2xl font-bold mb-6 text-white">Destinasi Wisata Unggulan</h3>
                    <p class="text-green-200 mb-6 leading-relaxed">
                        Kampung Pulo Sarok menawarkan berbagai destinasi wisata alam yang memukau dengan
                        keindahan panorama pegunungan dan kearifan budaya lokal yang masih terjaga.
                    </p>
                    <p class="text-green-200 mb-6 leading-relaxed">
                        Nikmati udara segar pegunungan, jelajahi keunikan budaya setempat, dan rasakan
                        keramahan masyarakat yang akan membuat kunjungan Anda tak terlupakan.
                    </p>
                </div>
                
                <!-- Fitur Wisata -->
                <div class="space-y-6">
                    ${destinations.slice(0, 3).map(destination => `
                        <div class="bg-white/10 backdrop-blur-sm rounded-xl p-6 hover:bg-white/20 transition duration-300">
                            <h4 class="text-xl font-bold text-white mb-3">${destination.name}</h4>
                            <p class="text-green-200 text-sm leading-relaxed">
                                ${destination.description || 'Destinasi wisata yang menawarkan pengalaman tak terlupakan dengan keindahan alam dan budaya lokal.'}
                            </p>
                            ${destination.facilities ? `
                                <div class="mt-3 flex flex-wrap gap-2">
                                    ${destination.facilities.split(',').slice(0, 3).map(facility => `
                                        <span class="bg-green-600 text-white text-xs px-2 py-1 rounded-full">${facility.trim()}</span>
                                    `).join('')}
                                </div>
                            ` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        tourismContainer.innerHTML = tourismHTML;
    }

    renderDefaultTourismContent() {
        const tourismContainer = document.getElementById('tourism-container');
        if (!tourismContainer) return;

        const defaultHTML = `
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
                <!-- Deskripsi Wisata -->
                <div>
                    <h3 class="text-2xl font-bold mb-6 text-white">Keindahan Alam Pulo Sarok</h3>
                    <p class="text-green-200 mb-6 leading-relaxed">
                        Kampung Pulo Sarok menawarkan keindahan alam yang memukau dengan panorama pegunungan
                        yang hijau dan udara segar yang menyegarkan. Tempat ini cocok untuk wisata alam
                        dan menikmati ketenangan jauh dari hiruk pikuk kota.
                    </p>
                    <p class="text-green-200 mb-6 leading-relaxed">
                        Nikmati keramahan masyarakat setempat, jelajahi kearifan budaya lokal, dan rasakan
                        pengalaman wisata yang autentik di tengah keindahan alam Aceh Singkil.
                    </p>
                </div>
                
                <!-- Fitur Wisata -->
                <div class="space-y-6">
                    <div class="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                        <h4 class="text-xl font-bold text-white mb-3">Wisata Alam</h4>
                        <p class="text-green-200 text-sm leading-relaxed">
                            Jelajahi keindahan alam pegunungan dengan pemandangan yang menakjubkan dan udara segar yang menyegarkan.
                        </p>
                    </div>
                    <div class="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                        <h4 class="text-xl font-bold text-white mb-3">Budaya Lokal</h4>
                        <p class="text-green-200 text-sm leading-relaxed">
                            Rasakan kearifan budaya lokal dan keramahan masyarakat Kampung Pulo Sarok yang masih terjaga.
                        </p>
                    </div>
                </div>
            </div>
        `;

        tourismContainer.innerHTML = defaultHTML;
    }

    async loadBusinessData() {
        const loadingElement = document.getElementById('business-loading');
        const containerElement = document.getElementById('business-container');
        
        try {
            // Show loading state
            if (loadingElement) loadingElement.classList.remove('hidden');
            if (containerElement) containerElement.classList.add('hidden');
            
            const businessData = await this.apiService.getBusinessData();
            
            // Hide loading and show content
            if (loadingElement) loadingElement.classList.add('hidden');
            
            if (businessData && businessData.results && businessData.results.length > 0) {
                this.renderBusinessData(businessData.results);
                if (containerElement) containerElement.classList.remove('hidden');
            } else {
                // Show default content if no data
                this.renderDefaultBusinessContent();
                if (containerElement) containerElement.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Error loading business data:', error);
            // Show default content on error
            this.renderDefaultBusinessContent();
            if (loadingElement) loadingElement.classList.add('hidden');
            if (containerElement) containerElement.classList.remove('hidden');
        }
    }

    renderBusinessData(businesses) {
        const businessContainer = document.getElementById('business-container');
        if (!businessContainer || !businesses || businesses.length === 0) {
            this.renderDefaultBusinessContent();
            return;
        }

        const businessHTML = `
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl">
                ${businesses.slice(0, 6).map(business => `
                    <div class="bg-white p-6 rounded-xl text-center shadow-lg hover:shadow-xl transition duration-300 transform hover:scale-105">
                        <div class="w-16 h-16 bg-gradient-to-br from-red-500 to-red-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                            ${business.logo ? 
                                `<img src="${business.logo}" alt="${business.name}" class="w-12 h-12 rounded-full object-cover">` :
                                `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                </svg>`
                            }
                        </div>
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
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                                </svg>
                                <span>${business.contact_phone}</span>
                            </div>
                        ` : ''}
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
            <div class="grid grid-cols-2 gap-6 max-w-2xl">
                <div class="bg-white p-6 rounded-xl text-center shadow-lg hover:shadow-xl transition duration-300 transform hover:scale-105">
                    <div class="w-16 h-16 bg-gradient-to-br from-red-500 to-red-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                    </div>
                    <h4 class="font-bold text-lg mb-2 text-red-900">BUMG</h4>
                    <p class="text-gray-600 text-sm">Badan Usaha Milik Gampong yang mengelola berbagai unit usaha untuk kesejahteraan masyarakat.</p>
                    <a href="bumg.html" class="inline-block mt-4 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg text-sm transition duration-300">Selengkapnya</a>
                </div>
                <div class="bg-white p-6 rounded-xl text-center shadow-lg hover:shadow-xl transition duration-300 transform hover:scale-105">
                    <div class="w-16 h-16 bg-gradient-to-br from-red-500 to-red-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                        </svg>
                    </div>
                    <h4 class="font-bold text-lg mb-2 text-red-900">UKM</h4>
                    <p class="text-gray-600 text-sm">Usaha Kecil Menengah yang dikelola masyarakat untuk meningkatkan perekonomian lokal.</p>
                    <a href="ukm.html" class="inline-block mt-4 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg text-sm transition duration-300">Selengkapnya</a>
                </div>
            </div>
        `;

        businessContainer.innerHTML = defaultHTML;
    }
}

// Initialize ketika DOM loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Initializing Index Page Manager');
    
    function initializePageManager() {
        try {
            if (typeof window.CONFIG !== 'undefined') {
                console.log('Config loaded, initializing page manager');
                const pageManager = new IndexPageManager();
                return true;
            } else {
                console.warn('Config not yet loaded, waiting...');
                return false;
            }
        } catch (error) {
            console.error('Error initializing page manager:', error);
            // Show fallback content or error message
            const errorDiv = document.createElement('div');
            errorDiv.className = 'fixed top-4 right-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded z-50';
            errorDiv.innerHTML = `
                <strong>Error:</strong> Gagal menginisialisasi halaman.<br>
                <small>Silakan refresh halaman atau hubungi administrator.</small>
            `;
            document.body.appendChild(errorDiv);
            
            // Auto hide error after 10 seconds
            setTimeout(() => {
                if (errorDiv.parentNode) {
                    errorDiv.parentNode.removeChild(errorDiv);
                }
            }, 10000);
            return false;
        }
    }
    
    // Try to initialize immediately
    if (!initializePageManager()) {
        // If config not loaded, try again with increasing delays
        let attempts = 0;
        const maxAttempts = 10;
        
        const retryInit = () => {
            attempts++;
            console.log(`Retry attempt ${attempts}/${maxAttempts}`);
            
            if (initializePageManager()) {
                console.log('Page manager initialized successfully on retry');
                return;
            }
            
            if (attempts < maxAttempts) {
                setTimeout(retryInit, attempts * 100); // Increasing delay
            } else {
                console.error('Failed to initialize page manager after maximum attempts');
                // Show persistent error message
                const errorDiv = document.createElement('div');
                errorDiv.className = 'fixed top-4 right-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded z-50';
                errorDiv.innerHTML = `
                    <strong>Error:</strong> Tidak dapat memuat konfigurasi halaman.<br>
                    <small>Silakan refresh halaman.</small>
                    <button onclick="location.reload()" class="ml-2 bg-red-500 text-white px-2 py-1 rounded text-xs hover:bg-red-600">Refresh</button>
                `;
                document.body.appendChild(errorDiv);
            }
        };
        
        setTimeout(retryInit, 100);
    }
});