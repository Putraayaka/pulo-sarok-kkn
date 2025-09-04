// API Service for Profile Page
class ProfilApiService {
    constructor() {
        // Using PUBLIC_API_BASE_URL from config.js
    }

    // Fetch village officials data
    async getVillageOfficials() {
        try {
            const response = await fetch(`${PUBLIC_API_BASE_URL}/organization/perangkat-desa/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching village officials:', error);
            throw error;
        }
    }

    // Fetch village data (general information and facilities)
    async getVillageData() {
        try {
            const response = await fetch(`${PUBLIC_API_BASE_URL}/village-profile/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching village data:', error);
            throw error;
        }
    }

    // Fetch village vision and mission
    async getVillageVisionMission() {
        try {
            const response = await fetch(`${PUBLIC_API_BASE_URL}/village-profile/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching village vision and mission:', error);
            throw error;
        }
    }

    // Fetch village history
    async getVillageHistory() {
        try {
            const response = await fetch(`${PUBLIC_API_BASE_URL}/village-history/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching village history:', error);
            throw error;
        }
    }
}

// Page Manager for Profile Page
class ProfilPageManager {
    constructor() {
        this.apiService = new ProfilApiService();
        this.officialsContainer = document.getElementById('officials-container');
        this.officialsLoading = document.getElementById('officials-loading');
        this.villageDataContainer = document.getElementById('village-data-container');
        this.villageDataLoading = document.getElementById('village-data-loading');
        this.visiContainer = document.getElementById('visi-container');
        this.visiLoading = document.getElementById('visi-loading');
        this.misiContainer = document.getElementById('misi-container');
        this.misiLoading = document.getElementById('misi-loading');
    }

    async init() {
        await Promise.all([
            this.loadVillageOfficials(),
            this.loadVillageData(),
            this.loadVisionMission()
        ]);
    }

    async loadVillageOfficials() {
        try {
            const officials = await this.apiService.getVillageOfficials();
            this.renderVillageOfficials(officials);
        } catch (error) {
            console.error('Failed to load village officials:', error);
            this.showOfficialsError();
        }
    }

    async loadVillageData() {
        try {
            const villageData = await this.apiService.getVillageData();
            this.renderVillageData(villageData);
        } catch (error) {
            console.error('Failed to load village data:', error);
            this.showVillageDataError();
        }
    }

    async loadVisionMission() {
        try {
            const visionMission = await this.apiService.getVillageVisionMission();
            this.renderVisionMission(visionMission);
        } catch (error) {
            console.error('Failed to load vision and mission:', error);
            this.showVisionMissionError();
        }
    }

    renderVillageOfficials(officials) {
        if (!this.officialsContainer || !this.officialsLoading) return;

        const officialsHtml = `
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                ${officials.map(official => `
                    <div class="bg-white p-5 rounded-lg shadow-sm text-center">
                        <div class="w-24 h-24 rounded-full bg-gray-200 mx-auto mb-3 overflow-hidden">
                            <img src="${official.photo || 'asset/person-placeholder.svg'}" alt="${official.position}" class="w-full h-full object-cover">
                        </div>
                        <h4 class="text-lg font-semibold text-gray-800">${official.name}</h4>
                        <p class="text-blue-600 font-medium">${official.position}</p>
                    </div>
                `).join('')}
            </div>
        `;

        this.officialsContainer.innerHTML = officialsHtml;
        this.officialsLoading.classList.add('hidden');
        this.officialsContainer.classList.remove('hidden');
    }

    renderVillageData(villageData) {
        if (!this.villageDataContainer || !this.villageDataLoading) return;

        const villageDataHtml = `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <h4 class="text-lg font-semibold mb-3 text-gray-800">Informasi Umum</h4>
                    <ul class="space-y-2">
                        <li class="flex">
                            <span class="font-medium w-40">Luas Wilayah</span>
                            <span>: ${villageData.area || 'N/A'}</span>
                        </li>
                        <li class="flex">
                            <span class="font-medium w-40">Jumlah Penduduk</span>
                            <span>: ${villageData.population || 'N/A'}</span>
                        </li>
                        <li class="flex">
                            <span class="font-medium w-40">Jumlah KK</span>
                            <span>: ${villageData.households || 'N/A'}</span>
                        </li>
                        <li class="flex">
                            <span class="font-medium w-40">Batas Utara</span>
                            <span>: ${villageData.north_border || 'N/A'}</span>
                        </li>
                        <li class="flex">
                            <span class="font-medium w-40">Batas Selatan</span>
                            <span>: ${villageData.south_border || 'N/A'}</span>
                        </li>
                        <li class="flex">
                            <span class="font-medium w-40">Batas Timur</span>
                            <span>: ${villageData.east_border || 'N/A'}</span>
                        </li>
                        <li class="flex">
                            <span class="font-medium w-40">Batas Barat</span>
                            <span>: ${villageData.west_border || 'N/A'}</span>
                        </li>
                    </ul>
                </div>
                
                <div>
                    <h4 class="text-lg font-semibold mb-3 text-gray-800">Fasilitas</h4>
                    <ul class="space-y-2">
                        ${villageData.facilities ? villageData.facilities.map(facility => `
                            <li class="flex">
                                <span class="font-medium w-40">${facility.name}</span>
                                <span>: ${facility.count} ${facility.unit || 'unit'}</span>
                            </li>
                        `).join('') : '<li>Data fasilitas tidak tersedia</li>'}
                    </ul>
                </div>
            </div>
        `;

        this.villageDataContainer.innerHTML = villageDataHtml;
        this.villageDataLoading.classList.add('hidden');
        this.villageDataContainer.classList.remove('hidden');
    }

    renderVisionMission(visionMission) {
        if (this.visiContainer && this.visiLoading) {
            this.visiContainer.innerHTML = `<p class="text-gray-700 leading-relaxed">${visionMission.vision || 'Visi tidak tersedia'}</p>`;
            this.visiLoading.classList.add('hidden');
            this.visiContainer.classList.remove('hidden');
        }

        if (this.misiContainer && this.misiLoading) {
            const missionHtml = visionMission.missions && visionMission.missions.length > 0 
                ? `<ul class="list-disc list-inside space-y-2 text-gray-700">
                    ${visionMission.missions.map(mission => `<li>${mission}</li>`).join('')}
                   </ul>`
                : '<p class="text-gray-700">Misi tidak tersedia</p>';
            
            this.misiContainer.innerHTML = missionHtml;
            this.misiLoading.classList.add('hidden');
            this.misiContainer.classList.remove('hidden');
        }
    }

    showOfficialsError() {
        if (!this.officialsContainer || !this.officialsLoading) return;
        
        this.officialsContainer.innerHTML = `
            <div class="text-center py-8">
                <p class="text-red-600 mb-4">Gagal memuat data struktur pemerintahan</p>
                <button onclick="location.reload()" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                    Coba Lagi
                </button>
            </div>
        `;
        this.officialsLoading.classList.add('hidden');
        this.officialsContainer.classList.remove('hidden');
    }

    showVillageDataError() {
        if (!this.villageDataContainer || !this.villageDataLoading) return;
        
        this.villageDataContainer.innerHTML = `
            <div class="text-center py-8">
                <p class="text-red-600 mb-4">Gagal memuat data kampung</p>
                <button onclick="location.reload()" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                    Coba Lagi
                </button>
            </div>
        `;
        this.villageDataLoading.classList.add('hidden');
        this.villageDataContainer.classList.remove('hidden');
    }

    showVisionMissionError() {
        if (this.visiContainer && this.visiLoading) {
            this.visiContainer.innerHTML = `
                <div class="text-center py-4">
                    <p class="text-red-600 mb-2">Gagal memuat visi</p>
                    <button onclick="location.reload()" class="bg-blue-600 text-white px-2 py-1 text-sm rounded hover:bg-blue-700">
                        Coba Lagi
                    </button>
                </div>
            `;
            this.visiLoading.classList.add('hidden');
            this.visiContainer.classList.remove('hidden');
        }

        if (this.misiContainer && this.misiLoading) {
            this.misiContainer.innerHTML = `
                <div class="text-center py-4">
                    <p class="text-red-600 mb-2">Gagal memuat misi</p>
                    <button onclick="location.reload()" class="bg-blue-600 text-white px-2 py-1 text-sm rounded hover:bg-blue-700">
                        Coba Lagi
                    </button>
                </div>
            `;
            this.misiLoading.classList.add('hidden');
            this.misiContainer.classList.remove('hidden');
        }
    }
}