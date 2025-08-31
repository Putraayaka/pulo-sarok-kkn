// Script for Kampung Pulo Sarok Website

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Offset for header
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add active class to current section in navigation
    function setActiveNavItem() {
        const sections = document.querySelectorAll('section[id]');
        const scrollPosition = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                document.querySelectorAll('a[href*=' + sectionId + ']').forEach(link => {
                    link.classList.add('active');
                });
            } else {
                document.querySelectorAll('a[href*=' + sectionId + ']').forEach(link => {
                    link.classList.remove('active');
                });
            }
        });
    }

    // Call on scroll
    window.addEventListener('scroll', setActiveNavItem);

    // Feature card hover effect enhancement
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 10px 20px rgba(0,0,0,0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
        });
    });

    // Mobile menu toggle functionality is handled at the end of the file

    // UKM Registration Form Handler
    const ukmForm = document.getElementById('ukmRegistrationForm');
    if (ukmForm) {
        ukmForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const data = {};
            
            // Convert FormData to object
            for (let [key, value] of formData.entries()) {
                if (key === 'support[]') {
                    if (!data.support) data.support = [];
                    data.support.push(value);
                } else {
                    data[key] = value;
                }
            }
            
            // Basic validation
            const requiredFields = ['ownerName', 'businessName', 'phone', 'address', 'businessType', 'category', 'description'];
            let isValid = true;
            let missingFields = [];
            
            requiredFields.forEach(field => {
                if (!data[field] || data[field].trim() === '') {
                    isValid = false;
                    missingFields.push(field);
                    document.getElementById(field).classList.add('border-red-500');
                } else {
                    document.getElementById(field).classList.remove('border-red-500');
                }
            });
            
            // Check agreement checkbox
            if (!data.agreement) {
                isValid = false;
                document.getElementById('agreement').classList.add('border-red-500');
            } else {
                document.getElementById('agreement').classList.remove('border-red-500');
            }
            
            if (!isValid) {
                showNotification('Mohon lengkapi semua field yang wajib diisi!', 'error');
                return;
            }
            
            // Show loading state
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Mengirim...';
            submitButton.disabled = true;
            
            // Simulate form submission (replace with actual API call)
            setTimeout(() => {
                // Reset button
                submitButton.textContent = originalText;
                submitButton.disabled = false;
                
                // Show success message
                showNotification('Pendaftaran UKM berhasil dikirim! Tim kami akan menghubungi Anda dalam 3-5 hari kerja.', 'success');
                
                // Reset form
                this.reset();
                
                // Scroll to top of form
                document.getElementById('ukmRegistrationForm').scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 2000);
        });
    }
    
    // Notification function
    function showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(notification => notification.remove());
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-md transition-all duration-300 transform translate-x-full`;
        
        // Set notification style based on type
        if (type === 'success') {
            notification.classList.add('bg-green-500', 'text-white');
        } else if (type === 'error') {
            notification.classList.add('bg-red-500', 'text-white');
        } else {
            notification.classList.add('bg-blue-500', 'text-white');
        }
        
        // Add message
        notification.innerHTML = `
            <div class="flex items-start">
                <div class="flex-1">
                    <p class="text-sm font-medium">${message}</p>
                </div>
                <button class="ml-4 text-white hover:text-gray-200 focus:outline-none" onclick="this.parentElement.parentElement.remove()">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }, 5000);
     }
    
    // Mobile Menu Toggle
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            
            // Toggle hamburger icon
            const icon = this.querySelector('svg');
            if (mobileMenu.classList.contains('hidden')) {
                icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
            } else {
                icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />';
            }
        });
    }
});