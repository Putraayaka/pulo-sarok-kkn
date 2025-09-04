// API Service for Index Page
class IndexApiService {
    constructor() {
        this.baseUrl = 'http://127.0.0.1:8000/api';
    }

    // Fetch tourism data
    async fetchTourismData() {
        try {
            const response = await fetch(`${this.baseUrl}/tourism/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching tourism data:', error);
            throw error;
        }
    }

    // Fetch business units data
    async fetchBusinessUnits() {
        try {
            const response = await fetch(`${this.baseUrl}/business/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching business units:', error);
            throw error;
        }
    }
}

// Page Manager for Index Page
class IndexPageManager {
    constructor() {
        this.apiService = new IndexApiService();
        this.init();
    }

    async init() {
        await this.loadTourismData();
        await this.loadBusinessUnits();
    }

    // Load and render tourism data
    async loadTourismData() {
        const tourismContainer = document.getElementById('tourism-container');
        const tourismLoading = document.getElementById('tourism-loading');
        
        if (!tourismContainer || !tourismLoading) {
            console.warn('Tourism containers not found');
            return;
        }

        try {
            const tourismData = await this.apiService.fetchTourismData();
            
            if (tourismData && tourismData.length > 0) {
                this.renderTourismData(tourismData, tourismContainer);
            } else {
                this.renderNoTourismData(tourismContainer);
            }
            
            // Hide loading and show content
            tourismLoading.classList.add('hidden');
            tourismContainer.classList.remove('hidden');
            
        } catch (error) {
            console.error('Failed to load tourism data:', error);
            this.renderTourismError(tourismContainer);
            tourismLoading.classList.add('hidden');
            tourismContainer.classList.remove('hidden');
        }
    }

    // Load and render business units
    async loadBusinessUnits() {
        const businessContainer = document.getElementById('business-container');
        const businessLoading = document.getElementById('business-loading');
        
        if (!businessContainer || !businessLoading) {
            console.warn('Business containers not found');
            return;
        }

        try {
            const businessData = await this.apiService.fetchBusinessUnits();
            
            if (businessData && businessData.length > 0) {
                this.renderBusinessUnits(businessData, businessContainer);
            } else {
                this.renderNoBusinessData(businessContainer);
            }
            
            // Hide loading and show content
            businessLoading.classList.add('hidden');
            businessContainer.classList.remove('hidden');
            
        } catch (error) {
            console.error('Failed to load business units:', error);
            this.renderBusinessError(businessContainer);
            businessLoading.classList.add('hidden');
            businessContainer.classList.remove('hidden');
        }
    }

    // Render tourism data
    renderTourismData(tourismData, container) {
        const mainTourism = tourismData[0]; // Get the first/main tourism data
        
        container.innerHTML = `
            <div class="max-w-4xl mx-auto">
                <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
                    <div class="md:flex">
                        <div class="md:w-1/2 p-8">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">${mainTourism.name || 'Wisata Kampung'}</h3>
                            <p class="text-gray-600 mb-6 leading-relaxed">
                                ${mainTourism.description || 'Deskripsi wisata tidak tersedia.'}
                            </p>
                            <div class="space-y-3">
                                <h4 class="font-semibold text-gray-800 flex items-center">
                                    <svg class="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                                    </svg>
                                    Fasilitas Tersedia:
                                </h4>
                                <div class="grid grid-cols-2 gap-2 text-sm text-gray-600">
                                    ${this.renderFacilities(mainTourism.facilities)}
                                </div>
                            </div>
                        </div>
                        <div class="md:w-1/2">
                            <img src="${mainTourism.image || '/images/default-tourism.jpg'}" alt="${mainTourism.name || 'Wisata Kampung'}" class="w-full h-64 md:h-full object-cover">
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Render business units
    renderBusinessUnits(businessData, container) {
        const businessItems = businessData.slice(0, 2); // Limit to 2 items for the grid
        
        container.innerHTML = `
            <div class="grid grid-cols-2 gap-6 max-w-2xl">
                ${businessItems.map((business, index) => {
                    const colors = [
                        { bg: 'from-red-400 to-red-600', hover: 'hover:text-red-600', tooltip: 'bg-red-600', border: 'border-t-red-600' },
                        { bg: 'from-orange-400 to-orange-600', hover: 'hover:text-orange-600', tooltip: 'bg-orange-600', border: 'border-t-orange-600' }
                    ];
                    const color = colors[index] || colors[0];
                    
                    return `
                        <div class="relative group">
                            <a href="${business.link || '#'}" class="block">
                                <div class="bg-white p-6 rounded-xl text-center text-gray-800 shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:scale-110 ${index === 0 ? 'hover:rotate-1' : 'hover:-rotate-1'} border-2 border-transparent hover:border-red-300">
                                    <div class="bg-gradient-to-br ${color.bg} rounded-full p-4 inline-block mb-4 group-hover:animate-pulse">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            ${this.getBusinessIcon(business.type)}
                                        </svg>
                                    </div>
                                    <h4 class="font-bold text-lg mb-2 ${color.hover} transition-colors duration-300">${business.name || 'Unit Usaha'}</h4>
                                    <p class="text-sm text-gray-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300">${business.description || 'Deskripsi tidak tersedia'}</p>
                                </div>
                            </a>
                            <div class="absolute -top-12 left-1/2 transform -translate-x-1/2 ${color.tooltip} text-white px-3 py-1 rounded-lg text-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none whitespace-nowrap">
                                Klik untuk info ${business.name}
                                <div class="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent ${color.border}"></div>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }

    // Render facilities list
    renderFacilities(facilities) {
        if (!facilities || facilities.length === 0) {
            return '<span class="col-span-2 text-gray-500">Informasi fasilitas tidak tersedia</span>';
        }
        
        return facilities.map(facility => `<span>• ${facility}</span>`).join('');
    }

    // Get appropriate icon for business type
    getBusinessIcon(type) {
        const icons = {
            'bumg': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />',
            'ukm': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />',
            'default': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />'
        };
        
        return icons[type?.toLowerCase()] || icons.default;
    }

    // Render error states
    renderTourismError(container) {
        container.innerHTML = `
            <div class="max-w-4xl mx-auto">
                <div class="bg-white rounded-2xl shadow-xl p-8 text-center">
                    <div class="text-red-500 mb-4">
                        <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold text-gray-800 mb-2">Gagal Memuat Data Wisata</h3>
                    <p class="text-gray-600">Terjadi kesalahan saat memuat informasi wisata. Silakan coba lagi nanti.</p>
                </div>
            </div>
        `;
    }

    renderBusinessError(container) {
        container.innerHTML = `
            <div class="grid grid-cols-2 gap-6 max-w-2xl">
                <div class="bg-white p-6 rounded-xl text-center shadow-lg">
                    <div class="text-red-500 mb-4">
                        <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <h4 class="font-bold text-lg mb-2 text-gray-800">Error</h4>
                    <p class="text-sm text-gray-600">Gagal memuat data</p>
                </div>
                <div class="bg-white p-6 rounded-xl text-center shadow-lg">
                    <div class="text-red-500 mb-4">
                        <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <h4 class="font-bold text-lg mb-2 text-gray-800">Error</h4>
                    <p class="text-sm text-gray-600">Gagal memuat data</p>
                </div>
            </div>
        `;
    }

    // Render no data states
    renderNoTourismData(container) {
        container.innerHTML = `
            <div class="max-w-4xl mx-auto">
                <div class="bg-white rounded-2xl shadow-xl p-8 text-center">
                    <div class="text-gray-400 mb-4">
                        <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold text-gray-800 mb-2">Belum Ada Data Wisata</h3>
                    <p class="text-gray-600">Informasi wisata kampung belum tersedia saat ini.</p>
                </div>
            </div>
        `;
    }

    renderNoBusinessData(container) {
        container.innerHTML = `
            <div class="grid grid-cols-2 gap-6 max-w-2xl">
                <div class="bg-white p-6 rounded-xl text-center shadow-lg">
                    <div class="text-gray-400 mb-4">
                        <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                        </svg>
                    </div>
                    <h4 class="font-bold text-lg mb-2 text-gray-800">Belum Ada Data</h4>
                    <p class="text-sm text-gray-600">Unit usaha belum tersedia</p>
                </div>
                <div class="bg-white p-6 rounded-xl text-center shadow-lg">
                    <div class="text-gray-400 mb-4">
                        <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                        </svg>
                    </div>
                    <h4 class="font-bold text-lg mb-2 text-gray-800">Belum Ada Data</h4>
                    <p class="text-sm text-gray-600">Unit usaha belum tersedia</p>
                </div>
            </div>
        `;
    }
}