class PengajuanSuratApiService {
    constructor() {
        // Using direct fetch calls with proper endpoints
    }

    async getLetterTypes() {
        try {
            const response = await fetch(`${ADMIN_API_BASE_URL}/letters/api/types/`);
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            return data.results || [];
        } catch (error) {
            console.error('Error fetching letter types:', error);
            return [];
        }
    }

    async submitLetterRequest(formData) {
        try {
            const response = await fetch(`${ADMIN_API_BASE_URL}/letters/api/create/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            if (!response.ok) throw new Error('Network response was not ok');
            return await response.json();
        } catch (error) {
            console.error('Error submitting letter request:', error);
            throw error;
        }
    }

    async trackLetterRequest(trackingCode) {
        try {
            const response = await fetch(`${ADMIN_API_BASE_URL}/letters/api/track/${trackingCode}/`);
            if (!response.ok) throw new Error('Network response was not ok');
            return await response.json();
        } catch (error) {
            console.error('Error tracking letter request:', error);
            throw error;
        }
    }

    async getVillageContact() {
        try {
            const response = await fetch(`${PUBLIC_API_BASE_URL}/contact/`);
            if (!response.ok) throw new Error('Network response was not ok');
            return await response.json();
        } catch (error) {
            console.error('Error fetching village contact:', error);
            return null;
        }
    }

    async getVillageOfficials() {
        try {
            const response = await fetch(`${PUBLIC_API_BASE_URL}/organization/perangkat-desa/`);
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            return data.results || [];
        } catch (error) {
            console.error('Error fetching village officials:', error);
            return [];
        }
    }
}

class PengajuanSuratPageManager {
    constructor() {
        this.apiService = new PengajuanSuratApiService();
        this.letterForm = null;
        this.trackingForm = null;
    }

    async init() {
        this.initializeForms();
        await Promise.all([
            this.loadLetterTypes(),
            this.loadContactInfo()
        ]);
    }

    initializeForms() {
        this.letterForm = document.getElementById('letter-form');
        this.trackingForm = document.getElementById('tracking-form');

        if (this.letterForm) {
            this.letterForm.addEventListener('submit', this.handleLetterSubmit.bind(this));
        }

        if (this.trackingForm) {
            this.trackingForm.addEventListener('submit', this.handleTrackingSubmit.bind(this));
        }
    }

    async loadLetterTypes() {
        try {
            const letterTypes = await this.apiService.getLetterTypes();
            this.renderLetterTypes(letterTypes);
        } catch (error) {
            console.error('Error loading letter types:', error);
            this.showLetterTypesError();
        }
    }

    async loadContactInfo() {
        try {
            const [villageContact, officials] = await Promise.all([
                this.apiService.getVillageContact(),
                this.apiService.getVillageOfficials()
            ]);
            this.renderContactInfo(villageContact, officials);
        } catch (error) {
            console.error('Error loading contact info:', error);
        }
    }

    renderLetterTypes(letterTypes) {
        const selectElement = document.getElementById('letter-type');
        if (!selectElement) return;

        // Clear existing options except the first one
        selectElement.innerHTML = '<option value="">-- Pilih Jenis Surat --</option>';

        if (letterTypes.length === 0) {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'Tidak ada jenis surat tersedia';
            option.disabled = true;
            selectElement.appendChild(option);
            return;
        }

        letterTypes.forEach(letterType => {
            const option = document.createElement('option');
            option.value = letterType.id;
            option.textContent = letterType.name;
            selectElement.appendChild(option);
        });
    }

    renderContactInfo(villageContact, officials) {
        const loadingElement = document.getElementById('contact-loading');
        const containerElement = document.getElementById('contact-container');
        
        if (!containerElement) return;

        // Find secretary from officials
        const secretary = officials.find(official => 
            official.position && official.position.toLowerCase().includes('sekretaris')
        );

        const contactHTML = `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="flex items-center">
                    <div class="bg-blue-100 rounded-full p-2 mr-3">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                        </svg>
                    </div>
                    <div>
                        <p class="font-semibold text-gray-800">${secretary ? secretary.name : 'Sekretaris Desa'}</p>
                        <p class="text-sm text-gray-600">${secretary && secretary.phone ? secretary.phone : (villageContact && villageContact.phone ? villageContact.phone : '+62 XXX-XXXX-XXXX')}</p>
                    </div>
                </div>
                <div class="flex items-center">
                    <div class="bg-blue-100 rounded-full p-2 mr-3">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                    </div>
                    <div>
                        <p class="font-semibold text-gray-800">Balai Desa</p>
                        <p class="text-sm text-gray-600">${villageContact && villageContact.address ? villageContact.address : 'Jl. Raya Pulo Sarok No. 1'}</p>
                    </div>
                </div>
            </div>
        `;

        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
        containerElement.innerHTML = contactHTML;
        containerElement.classList.remove('hidden');
    }

    showLetterTypesError() {
        const selectElement = document.getElementById('letter-type');
        if (!selectElement) return;

        selectElement.innerHTML = `
            <option value="">-- Pilih Jenis Surat --</option>
            <option value="" disabled>Error: Gagal memuat jenis surat</option>
        `;
    }

    async handleLetterSubmit(event) {
        event.preventDefault();
        
        const submitButton = event.target.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        
        try {
            // Show loading state
            submitButton.disabled = true;
            submitButton.innerHTML = `
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Mengirim...
            `;

            // Collect form data
            const formData = new FormData(event.target);
            const data = {
                name: formData.get('name'),
                nik: formData.get('nik'),
                phone: formData.get('phone'),
                address: formData.get('address'),
                letter_type: formData.get('letter_type'),
                purpose: formData.get('purpose'),
                notes: formData.get('notes') || ''
            };

            // Validate required fields
            const requiredFields = ['name', 'nik', 'phone', 'address', 'letter_type', 'purpose'];
            for (const field of requiredFields) {
                if (!data[field] || data[field].trim() === '') {
                    throw new Error(`Field ${field} harus diisi`);
                }
            }

            // Submit to API
            const response = await this.apiService.submitLetterRequest(data);
            
            // Show success message
            this.showSuccessMessage(response);
            
            // Reset form
            event.target.reset();
            
        } catch (error) {
            console.error('Error submitting letter request:', error);
            this.showErrorMessage(error.message || 'Terjadi kesalahan saat mengirim pengajuan');
        } finally {
            // Restore button state
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    }

    async handleTrackingSubmit(event) {
        event.preventDefault();
        
        const submitButton = event.target.querySelector('button[type="submit"]');
        const trackingCodeInput = document.getElementById('tracking-code');
        const resultContainer = document.getElementById('tracking-result');
        const originalText = submitButton.textContent;
        
        try {
            // Show loading state
            submitButton.disabled = true;
            submitButton.textContent = 'Mencari...';
            
            const trackingCode = trackingCodeInput.value.trim();
            if (!trackingCode) {
                throw new Error('Kode tracking harus diisi');
            }

            // Track letter request
            const result = await this.apiService.trackLetterRequest(trackingCode);
            
            // Show tracking result
            this.showTrackingResult(result, resultContainer);
            
        } catch (error) {
            console.error('Error tracking letter request:', error);
            this.showTrackingError(error.message || 'Kode tracking tidak ditemukan', resultContainer);
        } finally {
            // Restore button state
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    }

    showSuccessMessage(response) {
        const message = `
            <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4" role="alert">
                <div class="flex">
                    <div class="py-1">
                        <svg class="fill-current h-6 w-6 text-green-500 mr-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                            <path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z"/>
                        </svg>
                    </div>
                    <div>
                        <p class="font-bold">Pengajuan Berhasil Dikirim!</p>
                        <p class="text-sm">Kode tracking: <strong>${response.tracking_code || 'Akan diberikan via SMS/WhatsApp'}</strong></p>
                        <p class="text-sm">Surat akan diproses dalam 1-3 hari kerja.</p>
                    </div>
                </div>
            </div>
        `;
        
        // Insert message before the form
        const form = document.getElementById('letter-form');
        if (form) {
            form.insertAdjacentHTML('beforebegin', message);
            
            // Auto-remove message after 10 seconds
            setTimeout(() => {
                const alertElement = form.previousElementSibling;
                if (alertElement && alertElement.classList.contains('bg-green-100')) {
                    alertElement.remove();
                }
            }, 10000);
        }
    }

    showErrorMessage(message) {
        const errorHtml = `
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4" role="alert">
                <div class="flex">
                    <div class="py-1">
                        <svg class="fill-current h-6 w-6 text-red-500 mr-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                            <path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm1.41-1.41A8 8 0 1 0 15.66 4.34 8 8 0 0 0 4.34 15.66zm9.9-8.49L11.41 10l2.83 2.83-1.41 1.41L10 11.41l-2.83 2.83-1.41-1.41L8.59 10 5.76 7.17l1.41-1.41L10 8.59l2.83-2.83 1.41 1.41z"/>
                        </svg>
                    </div>
                    <div>
                        <p class="font-bold">Terjadi Kesalahan!</p>
                        <p class="text-sm">${message}</p>
                    </div>
                </div>
            </div>
        `;
        
        // Insert message before the form
        const form = document.getElementById('letter-form');
        if (form) {
            form.insertAdjacentHTML('beforebegin', errorHtml);
            
            // Auto-remove message after 8 seconds
            setTimeout(() => {
                const alertElement = form.previousElementSibling;
                if (alertElement && alertElement.classList.contains('bg-red-100')) {
                    alertElement.remove();
                }
            }, 8000);
        }
    }

    showTrackingResult(result, container) {
        const statusColors = {
            'pending': 'bg-yellow-100 text-yellow-800',
            'processing': 'bg-blue-100 text-blue-800',
            'ready': 'bg-green-100 text-green-800',
            'completed': 'bg-gray-100 text-gray-800',
            'rejected': 'bg-red-100 text-red-800'
        };

        const statusTexts = {
            'pending': 'Menunggu Verifikasi',
            'processing': 'Sedang Diproses',
            'ready': 'Siap Diambil',
            'completed': 'Selesai',
            'rejected': 'Ditolak'
        };

        const statusColor = statusColors[result.status] || 'bg-gray-100 text-gray-800';
        const statusText = statusTexts[result.status] || result.status;

        const resultHtml = `
            <div class="bg-white border border-gray-200 rounded-lg p-4 mt-4">
                <div class="flex items-center justify-between mb-3">
                    <h4 class="text-lg font-semibold text-gray-800">Status Pengajuan</h4>
                    <span class="px-3 py-1 rounded-full text-sm font-medium ${statusColor}">
                        ${statusText}
                    </span>
                </div>
                <div class="space-y-2 text-sm">
                    <div class="flex justify-between">
                        <span class="text-gray-600">Nama:</span>
                        <span class="font-medium">${result.name}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Jenis Surat:</span>
                        <span class="font-medium">${result.letter_type_name || result.letter_type}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Tanggal Pengajuan:</span>
                        <span class="font-medium">${this.formatDate(result.created_at)}</span>
                    </div>
                    ${result.estimated_completion ? `
                        <div class="flex justify-between">
                            <span class="text-gray-600">Estimasi Selesai:</span>
                            <span class="font-medium">${this.formatDate(result.estimated_completion)}</span>
                        </div>
                    ` : ''}
                    ${result.notes ? `
                        <div class="mt-3">
                            <span class="text-gray-600">Catatan:</span>
                            <p class="text-gray-800 mt-1">${result.notes}</p>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;

        container.innerHTML = resultHtml;
    }

    showTrackingError(message, container) {
        const errorHtml = `
            <div class="bg-red-50 border border-red-200 rounded-lg p-4 mt-4">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                        </svg>
                    </div>
                    <div class="ml-3">
                        <h3 class="text-sm font-medium text-red-800">Pencarian Gagal</h3>
                        <p class="text-sm text-red-700 mt-1">${message}</p>
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = errorHtml;
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
}