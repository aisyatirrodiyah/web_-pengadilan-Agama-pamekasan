/**
 * script.js - Pengadilan Agama Pamekasan Premium
 * Optimized for performance and smooth UX
 */

document.addEventListener('DOMContentLoaded', () => {
    initStickyNav();
    initScrollReveal();
    initWelcomeVoice();
    initMobileMenu();
});

/**
 * Sticky Navigation Effect
 */
function initStickyNav() {
    const navBar = document.querySelector('.nav-bar');
    if (!navBar) return;

    const handleScroll = () => {
        if (window.scrollY > 50) {
            navBar.classList.add('scrolled');
        } else {
            navBar.classList.remove('scrolled');
        }
    };

    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Initial check
}

/**
 * Enhanced Scroll Reveal Animation
 * Uses Intersection Observer for better performance
 */
function initScrollReveal() {
    const reveals = document.querySelectorAll('.reveal');
    if (reveals.length === 0) return;

    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    };

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                // Unobserve after it's revealed to keep animations sticking
                // revealObserver.unobserve(entry.target); 
            }
        });
    }, observerOptions);

    reveals.forEach(el => revealObserver.observe(el));
}

/**
 * Text to Speech (Welcome Voice)
 * Providing a warm greeting to visitors
 */
function initWelcomeVoice() {
    const textToRead = "Selamat Datang di Website Resmi Pengadilan Agama Pamekasan. Anda Memasuki Zona Integritas Wilayah Bebas Korupsi dan Wilayah Birokrasi Bersih dan Melayani.";

    window.playWelcomeSpeech = function () {
        if (!window.speechSynthesis) {
            console.error("Speech synthesis not supported.");
            return;
        }

        window.speechSynthesis.cancel();

        const speech = new SpeechSynthesisUtterance();
        speech.text = textToRead;
        speech.lang = 'id-ID';
        speech.volume = 1;
        speech.rate = 1;
        speech.pitch = 1;

        // Find Indonesian voice
        const voices = window.speechSynthesis.getVoices();
        const indoVoice = voices.find(voice => voice.lang.includes('id'));
        if (indoVoice) speech.voice = indoVoice;

        window.speechSynthesis.speak(speech);
    };

    // Voice setup listener for some browsers
    if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = () => {
            // Pre-load voices if needed
        };
    }
}

/**
 * Smooth Scroll Utility
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;

        const targetEl = document.querySelector(targetId);
        if (targetEl) {
            e.preventDefault();
            targetEl.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
/**
 * Accessibility: Adjust Font Size
 */
window.adjustFontSize = function (size) {
    const html = document.documentElement;
    if (size === 'large') {
        html.style.fontSize = '20px';
    } else {
        html.style.fontSize = '16px';
    }
};

/**
 * Accessibility: Toggle High Contrast
 */
window.toggleContrast = function () {
    document.body.classList.toggle('high-contrast');
};
/**
 * Mobile Menu Toggle
 */
function initMobileMenu() {
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const navContainer = document.querySelector('.nav-pro-container');

    if (menuBtn && navContainer) {
        menuBtn.addEventListener('click', () => {
            navContainer.classList.toggle('active');
            const icon = menuBtn.querySelector('i');
            if (icon.classList.contains('fa-bars')) {
                icon.classList.replace('fa-bars', 'fa-times');
            } else {
                icon.classList.replace('fa-times', 'fa-bars');
            }
        });
    }
}
