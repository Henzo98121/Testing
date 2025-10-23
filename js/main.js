// Register GSAP plugins
gsap.registerPlugin(ScrollTrigger);

// Initialize animations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initNavAnimation();
    initHeroAnimation();
    initScrollIndicator();
    initSectionAnimations();
    initProjectAnimations();
    initSmoothScroll();
});

// Navigation animation on scroll
function initNavAnimation() {
    const nav = document.querySelector('.nav');

    ScrollTrigger.create({
        start: 'top -100',
        end: 99999,
        toggleClass: {
            className: 'nav-scrolled',
            targets: nav
        }
    });
}

// Hero section animations
function initHeroAnimation() {
    const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

    // Animate hero title lines
    tl.from('.hero-title .line', {
        y: 100,
        opacity: 0,
        duration: 1.2,
        stagger: 0.2
    })
    // Animate subtitle
    .from('.hero-subtitle', {
        y: 30,
        opacity: 0,
        duration: 0.8
    }, '-=0.6')
    // Animate CTA button
    .from('.cta-button', {
        y: 30,
        opacity: 0,
        duration: 0.8
    }, '-=0.4')
    // Animate scroll indicator
    .from('.scroll-indicator', {
        opacity: 0,
        duration: 0.8
    }, '-=0.4');
}

// Scroll indicator animation
function initScrollIndicator() {
    gsap.to('.scroll-line', {
        scaleY: 0,
        transformOrigin: 'top',
        scrollTrigger: {
            start: 'top top',
            end: '+=500',
            scrub: true
        }
    });

    // Fade out scroll indicator
    gsap.to('.scroll-indicator', {
        opacity: 0,
        scrollTrigger: {
            start: 'top top',
            end: '+=300',
            scrub: true
        }
    });
}

// Section reveal animations
function initSectionAnimations() {
    // Animate section titles
    gsap.utils.toArray('.section-title').forEach(title => {
        gsap.from(title, {
            y: 60,
            opacity: 0,
            duration: 1,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: title,
                start: 'top 80%',
                end: 'top 50%',
                toggleActions: 'play none none reverse'
            }
        });
    });

    // Animate about text
    gsap.from('.about-text', {
        y: 40,
        opacity: 0,
        duration: 1,
        ease: 'power3.out',
        scrollTrigger: {
            trigger: '.about-text',
            start: 'top 80%',
            toggleActions: 'play none none reverse'
        }
    });

    // Animate skills
    gsap.from('.skill-item', {
        y: 30,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1,
        ease: 'power3.out',
        scrollTrigger: {
            trigger: '.skills',
            start: 'top 80%',
            toggleActions: 'play none none reverse'
        }
    });

    // Animate contact text
    gsap.from('.contact-text', {
        y: 40,
        opacity: 0,
        duration: 1,
        ease: 'power3.out',
        scrollTrigger: {
            trigger: '.contact-text',
            start: 'top 80%',
            toggleActions: 'play none none reverse'
        }
    });

    // Animate contact links
    gsap.from('.contact-link', {
        y: 30,
        opacity: 0,
        duration: 0.8,
        stagger: 0.15,
        ease: 'power3.out',
        scrollTrigger: {
            trigger: '.contact-links',
            start: 'top 80%',
            toggleActions: 'play none none reverse'
        }
    });
}

// Project cards animations
function initProjectAnimations() {
    const projectCards = gsap.utils.toArray('.project-card');

    projectCards.forEach((card, index) => {
        // Entrance animation
        gsap.from(card, {
            x: -50,
            opacity: 0,
            duration: 1,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: card,
                start: 'top 85%',
                toggleActions: 'play none none reverse'
            }
        });

        // Hover animation for project number
        const number = card.querySelector('.project-number');
        card.addEventListener('mouseenter', () => {
            gsap.to(number, {
                x: 10,
                duration: 0.3,
                ease: 'power2.out'
            });
        });

        card.addEventListener('mouseleave', () => {
            gsap.to(number, {
                x: 0,
                duration: 0.3,
                ease: 'power2.out'
            });
        });
    });
}

// Smooth scroll for navigation links
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');

            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (target) {
                gsap.to(window, {
                    duration: 1.5,
                    scrollTo: {
                        y: target,
                        offsetY: 0
                    },
                    ease: 'power3.inOut'
                });
            }
        });
    });
}

// Parallax effect on hero
ScrollTrigger.create({
    trigger: '.hero',
    start: 'top top',
    end: 'bottom top',
    scrub: true,
    onUpdate: (self) => {
        gsap.to('.hero-content', {
            y: self.progress * 200,
            opacity: 1 - self.progress,
            ease: 'none'
        });
    }
});

// Mouse follower effect (subtle)
let mouseX = 0;
let mouseY = 0;
let posX = 0;
let posY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
});

gsap.ticker.add(() => {
    posX += (mouseX - posX) * 0.1;
    posY += (mouseY - posY) * 0.1;

    // Apply subtle parallax to project cards
    gsap.utils.toArray('.project-card').forEach((card, i) => {
        const speed = (i + 1) * 0.002;
        gsap.to(card, {
            x: (posX - window.innerWidth / 2) * speed,
            y: (posY - window.innerHeight / 2) * speed,
            duration: 0.5,
            overwrite: 'auto'
        });
    });
});
