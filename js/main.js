/**
 * FLIGHT DECK - Main JavaScript
 * Dynamic scroll animations, parallax effects, and interactions
 */

(function() {
    'use strict';

    // ==========================================
    // 1. INITIALIZATION
    // ==========================================

    document.addEventListener('DOMContentLoaded', function() {
        initNavigation();
        initScrollAnimations();
        initParallaxEffects();
        initDataVisualizations();
        initSmoothScroll();
        initTickerAnimation();
        initCursorEffects();
    });

    // ==========================================
    // 2. NAVIGATION
    // ==========================================

    function initNavigation() {
        const nav = document.querySelector('.nav');
        let lastScroll = 0;

        window.addEventListener('scroll', function() {
            const currentScroll = window.pageYOffset;

            // Add scrolled class for styling
            if (currentScroll > 100) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }

            // Hide/show nav on scroll direction
            if (currentScroll > lastScroll && currentScroll > 500) {
                nav.style.transform = 'translateY(-100%)';
            } else {
                nav.style.transform = 'translateY(0)';
            }

            lastScroll = currentScroll;
        });
    }

    // ==========================================
    // 3. SMOOTH SCROLL
    // ==========================================

    function initSmoothScroll() {
        const links = document.querySelectorAll('a[href^="#"]');

        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;

                const targetSection = document.querySelector(targetId);
                if (targetSection) {
                    const navHeight = document.querySelector('.nav').offsetHeight;
                    const targetPosition = targetSection.offsetTop - navHeight;

                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    // ==========================================
    // 4. SCROLL ANIMATIONS (Intersection Observer)
    // ==========================================

    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                }
            });
        }, observerOptions);

        // Observe all sections for fade-in
        const sections = document.querySelectorAll('.section');
        sections.forEach(section => {
            section.classList.add('fade-in-section');
            observer.observe(section);
        });

        // Observe individual elements
        const animateElements = document.querySelectorAll(
            '.deliverable-item, .mechanics-card, .forecast-item, .contact-item'
        );
        animateElements.forEach(el => observer.observe(el));
    }

    // ==========================================
    // 5. PARALLAX EFFECTS
    // ==========================================

    function initParallaxEffects() {
        const parallaxElements = [
            { selector: '.hero-content', speed: 0.3 },
            { selector: '.grid-overlay', speed: 0.5 },
            { selector: '.data-viz', speed: 0.2 },
            { selector: '.blueprint-overlay', speed: 0.15 },
            { selector: '.timeline-viz', speed: 0.25 }
        ];

        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;

            parallaxElements.forEach(item => {
                const element = document.querySelector(item.selector);
                if (element) {
                    const elementTop = element.getBoundingClientRect().top;
                    const elementOffset = elementTop + scrolled;

                    if (elementTop < window.innerHeight && elementTop > -element.offsetHeight) {
                        const yPos = (scrolled - elementOffset) * item.speed;
                        element.style.transform = `translateY(${yPos}px)`;
                    }
                }
            });
        });
    }

    // ==========================================
    // 6. DATA VISUALIZATIONS (Animated)
    // ==========================================

    function initDataVisualizations() {
        // Animate SVG path drawing
        const signalViz = document.querySelector('#signal-viz polyline');
        if (signalViz) {
            const length = signalViz.getTotalLength();
            signalViz.style.strokeDasharray = length;
            signalViz.style.strokeDashoffset = length;

            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        signalViz.style.transition = 'stroke-dashoffset 2s ease-in-out';
                        signalViz.style.strokeDashoffset = '0';
                    }
                });
            }, { threshold: 0.5 });

            observer.observe(document.querySelector('#signal-viz'));
        }

        // Animate data points
        const dataPoints = document.querySelectorAll('.viz-data circle');
        dataPoints.forEach((point, index) => {
            point.style.opacity = '0';
            point.style.transition = 'opacity 0.5s ease, transform 0.5s ease';

            setTimeout(() => {
                point.style.opacity = '0.8';
                point.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    point.style.transform = 'scale(1)';
                }, 200);
            }, index * 200);
        });
    }

    // ==========================================
    // 7. TICKER ANIMATION
    // ==========================================

    function initTickerAnimation() {
        const ticker = document.querySelector('.ticker-content');
        if (!ticker) return;

        // Clone ticker content for seamless loop
        const tickerContent = ticker.innerHTML;
        ticker.innerHTML = tickerContent + tickerContent;

        // Pause on hover
        ticker.addEventListener('mouseenter', function() {
            this.style.animationPlayState = 'paused';
        });

        ticker.addEventListener('mouseleave', function() {
            this.style.animationPlayState = 'running';
        });
    }

    // ==========================================
    // 8. CURSOR EFFECTS
    // ==========================================

    function initCursorEffects() {
        // Custom cursor trail (optional - for extra polish)
        const cursorTrail = [];
        const trailLength = 5;

        document.addEventListener('mousemove', function(e) {
            cursorTrail.push({ x: e.clientX, y: e.clientY });
            if (cursorTrail.length > trailLength) {
                cursorTrail.shift();
            }
        });

        // Add interactive hover effects
        const interactiveElements = document.querySelectorAll(
            '.btn, .nav-link, .mechanics-card, .contact-item'
        );

        interactiveElements.forEach(el => {
            el.addEventListener('mouseenter', function() {
                this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            });
        });
    }

    // ==========================================
    // 9. HORIZONTAL SCROLL EFFECTS
    // ==========================================

    function initHorizontalScroll() {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;

            // Ticker horizontal movement based on scroll
            const ticker = document.querySelector('.ticker-content');
            if (ticker) {
                const offset = (scrolled * 0.5) % ticker.offsetWidth;
                ticker.style.transform = `translateX(-${offset}px)`;
            }

            // Grid overlay horizontal shift
            const grid = document.querySelector('.grid-overlay');
            if (grid) {
                const gridOffset = (scrolled * 0.1) % 50;
                grid.style.backgroundPosition = `${gridOffset}px ${gridOffset}px`;
            }
        });
    }

    // ==========================================
    // 10. NUMBER COUNTING ANIMATION
    // ==========================================

    function animateNumbers() {
        const numberElements = document.querySelectorAll('.card-number');

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    const finalNumber = parseInt(target.textContent);
                    let currentNumber = 0;
                    const duration = 1000; // 1 second
                    const steps = 20;
                    const increment = finalNumber / steps;
                    const stepDuration = duration / steps;

                    const counter = setInterval(() => {
                        currentNumber += increment;
                        if (currentNumber >= finalNumber) {
                            target.textContent = String(finalNumber).padStart(2, '0');
                            clearInterval(counter);
                        } else {
                            target.textContent = String(Math.floor(currentNumber)).padStart(2, '0');
                        }
                    }, stepDuration);

                    observer.unobserve(target);
                }
            });
        }, { threshold: 0.5 });

        numberElements.forEach(el => observer.observe(el));
    }

    // ==========================================
    // 11. TIMELINE PROGRESS ANIMATION
    // ==========================================

    function initTimelineAnimation() {
        const timeline = document.querySelector('.timeline-line');
        if (!timeline) return;

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    timeline.style.width = '0%';
                    timeline.style.transition = 'width 2s ease-in-out';

                    setTimeout(() => {
                        timeline.style.width = '100%';
                    }, 100);

                    // Animate markers
                    const markers = document.querySelectorAll('.timeline-marker');
                    markers.forEach((marker, index) => {
                        marker.style.opacity = '0';
                        marker.style.transform = 'translateX(-50%) translateY(20px)';
                        marker.style.transition = 'opacity 0.5s ease, transform 0.5s ease';

                        setTimeout(() => {
                            marker.style.opacity = '1';
                            marker.style.transform = 'translateX(-50%) translateY(0)';
                        }, 500 + (index * 200));
                    });

                    observer.unobserve(timeline);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(timeline);
    }

    // ==========================================
    // 12. DYNAMIC GRID MOVEMENT
    // ==========================================

    function initDynamicGrid() {
        const grid = document.querySelector('.grid-overlay');
        if (!grid) return;

        let mouseX = 0;
        let mouseY = 0;
        let currentX = 0;
        let currentY = 0;

        document.addEventListener('mousemove', function(e) {
            mouseX = e.clientX / window.innerWidth;
            mouseY = e.clientY / window.innerHeight;
        });

        function animateGrid() {
            // Smooth interpolation
            currentX += (mouseX - currentX) * 0.05;
            currentY += (mouseY - currentY) * 0.05;

            const offsetX = currentX * 20;
            const offsetY = currentY * 20;

            grid.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
            requestAnimationFrame(animateGrid);
        }

        animateGrid();
    }

    // ==========================================
    // 13. GLITCH EFFECT ON HOVER (Optional)
    // ==========================================

    function initGlitchEffect() {
        const glitchElements = document.querySelectorAll('.hero-title, .section-title');

        glitchElements.forEach(el => {
            el.addEventListener('mouseenter', function() {
                this.style.textShadow = `
                    2px 2px 0 rgba(69, 162, 158, 0.5),
                    -2px -2px 0 rgba(255, 255, 255, 0.3)
                `;
            });

            el.addEventListener('mouseleave', function() {
                this.style.textShadow = 'none';
            });
        });
    }

    // ==========================================
    // 14. PERFORMANCE OPTIMIZATION
    // ==========================================

    // Throttle scroll events
    function throttle(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Debounce resize events
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // ==========================================
    // 15. WINDOW RESIZE HANDLER
    // ==========================================

    window.addEventListener('resize', debounce(function() {
        // Recalculate positions on resize
        initParallaxEffects();
    }, 250));

    // ==========================================
    // 16. INITIALIZE ADDITIONAL EFFECTS
    // ==========================================

    // Call additional animations
    animateNumbers();
    initTimelineAnimation();
    initDynamicGrid();
    initGlitchEffect();
    initHorizontalScroll();

    // ==========================================
    // 17. INTELLIGENCE CATALOG & MODAL
    // ==========================================

    function initCatalogModal() {
        const modal = document.getElementById('study-modal');
        const closeBtn = document.querySelector('.modal-close');

        // Google Sheets CSV URL
        const SHEET_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRt89B1UIpgjRog4xWEzQ8FQSp9VuT8Z_ry68vb5pvD7OAB9O8AkJ4OVE034JyUE6oTYOgnjSnxv_5i/pub?output=csv';

        let studyData = {};

        // Function to parse CSV (handles multiline fields and proper quoting)
        function parseCSV(csv) {
            const data = {};
            const rows = [];
            let currentRow = [];
            let currentField = '';
            let insideQuotes = false;

            // Parse CSV character by character to handle multiline fields
            for (let i = 0; i < csv.length; i++) {
                const char = csv[i];
                const nextChar = csv[i + 1];

                if (char === '"') {
                    if (insideQuotes && nextChar === '"') {
                        // Escaped quote
                        currentField += '"';
                        i++; // Skip next quote
                    } else {
                        // Toggle quote state
                        insideQuotes = !insideQuotes;
                    }
                } else if (char === ',' && !insideQuotes) {
                    // End of field
                    currentRow.push(currentField.trim());
                    currentField = '';
                } else if ((char === '\n' || char === '\r') && !insideQuotes) {
                    // End of row
                    if (currentField || currentRow.length > 0) {
                        currentRow.push(currentField.trim());
                        if (currentRow.some(field => field !== '')) {
                            rows.push(currentRow);
                        }
                        currentRow = [];
                        currentField = '';
                    }
                    // Skip \r\n combinations
                    if (char === '\r' && nextChar === '\n') {
                        i++;
                    }
                } else {
                    currentField += char;
                }
            }

            // Push last field and row if any
            if (currentField || currentRow.length > 0) {
                currentRow.push(currentField.trim());
                if (currentRow.some(field => field !== '')) {
                    rows.push(currentRow);
                }
            }

            // Skip header row and parse data rows
            console.log('Total CSV rows (including header):', rows.length);
            for (let i = 1; i < rows.length; i++) {
                const values = rows[i];
                const id = values[0];
                console.log(`Row ${i}: id="${id}", columns=${values.length}`);

                if (id && id.trim()) {
                    data[id] = {
                        tag: values[1] || '',
                        title: values[2] || '',
                        date: values[3] || '',
                        description: values[4] || '',
                        includes: values[5] ? values[5].split('|').map(item => item.trim()) : []
                    };
                }
            }

            console.log('Final parsed data object:', data);
            return data;
        }

        // Function to create a catalog card HTML
        function createCatalogCard(id, study) {
            // Truncate description to ~100 chars for preview
            const preview = study.description.length > 120
                ? study.description.substring(0, 120) + '...'
                : study.description;

            return `
                <div class="catalog-card" data-study="${id}">
                    <div class="card-tag mono">${study.tag}</div>
                    <h3 class="catalog-card-title">${study.title}</h3>
                    <p class="catalog-card-date mono">${study.date}</p>
                    <p class="catalog-card-preview">${preview}</p>
                    <div class="catalog-card-cta">
                        <span class="card-click-hint mono">&gt; CLICK FOR DETAILS</span>
                    </div>
                </div>
            `;
        }

        // Function to populate catalog with cards
        function populateCatalog(data) {
            const catalogContainer = document.getElementById('catalog-scroll');
            if (!catalogContainer) return;

            // Build cards HTML - simple grid layout, no duplication needed
            let cardsHTML = '';
            const studyIds = Object.keys(data);
            console.log('Building cards for study IDs:', studyIds);

            studyIds.forEach(id => {
                console.log('Creating card for study:', id, data[id].title);
                cardsHTML += createCatalogCard(id, data[id]);
            });

            // Display cards in grid (no duplication needed)
            catalogContainer.innerHTML = cardsHTML;

            console.log(`Total cards displayed: ${studyIds.length} studies`);
        }

        // Fetch data from Google Sheets with cache-busting
        fetch(SHEET_URL + '&t=' + Date.now())
            .then(response => response.text())
            .then(csv => {
                console.log('Raw CSV received:', csv);
                studyData = parseCSV(csv);
                console.log('Studies loaded from Google Sheets:', studyData);
                console.log('Number of studies loaded:', Object.keys(studyData).length);

                // Populate catalog with dynamic cards
                populateCatalog(studyData);

                // Initialize modal handlers after cards are created
                initializeModalHandlers();
            })
            .catch(error => {
                console.error('Error loading studies from Google Sheets:', error);
                // Fallback to empty data
                studyData = {};
            });

        // Store onboarding data
        let onboardingData = {};

        // Reset modal to initial state (onboarding form)
        function resetModalView() {
            document.getElementById('onboarding-section').style.display = 'block';
            document.getElementById('pricing-section').style.display = 'none';
            document.getElementById('booking-section').style.display = 'none';
            document.getElementById('study-form').style.display = 'none';
            document.getElementById('onboarding-form').reset();
            onboardingData = {};
        }

        // Initialize modal handlers (called after data is loaded)
        function initializeModalHandlers() {
            // Re-query cards after they've been dynamically created
            const cards = document.querySelectorAll('.catalog-card');

            // Click handler for cards
            cards.forEach(card => {
                card.addEventListener('click', function() {
                    const studyId = this.getAttribute('data-study');
                    const study = studyData[studyId];

                if (study) {
                    // Populate modal
                    document.getElementById('modal-tag').textContent = study.tag;
                    document.getElementById('modal-title').textContent = study.title;
                    document.getElementById('modal-date').textContent = study.date;
                    document.getElementById('modal-description').innerHTML = `<p>${study.description}</p>`;

                    // Populate includes list
                    const includesList = document.getElementById('modal-includes');
                    includesList.innerHTML = study.includes.map(item => `<li>${item}</li>`).join('');

                    // Update hidden form field with study title
                    document.getElementById('form-study-title').value = study.title;

                    // Show modal with onboarding section first
                    resetModalView();
                    modal.classList.add('active');
                    document.body.style.overflow = 'hidden';
                }
            });
        });

        // Handle onboarding form submission
        const onboardingForm = document.getElementById('onboarding-form');
        if (onboardingForm) {
            onboardingForm.addEventListener('submit', function(e) {
                e.preventDefault();

                // Capture onboarding data
                onboardingData = {
                    name: document.getElementById('onboard-name').value,
                    email: document.getElementById('onboard-email').value,
                    company: document.getElementById('onboard-company').value,
                    experience: document.getElementById('onboard-experience').value,
                    companyType: document.getElementById('onboard-company-type').value,
                    position: document.getElementById('onboard-position').value,
                    geography: document.getElementById('onboard-geography').value,
                    usage: document.getElementById('onboard-usage').value
                };

                console.log('Onboarding data captured:', onboardingData);

                // Hide onboarding, show pricing options
                document.getElementById('onboarding-section').style.display = 'none';
                document.getElementById('pricing-section').style.display = 'grid';
            });
        }

        // Handle "Book 30-Min Brief" button
        const briefBookingBtn = document.querySelector('.brief-booking-btn');
        if (briefBookingBtn) {
            briefBookingBtn.addEventListener('click', function(e) {
                e.preventDefault();

                // Hide pricing, show booking section
                document.getElementById('pricing-section').style.display = 'none';
                document.getElementById('booking-section').style.display = 'block';

                // Load Calendly
                loadCalendly();
            });
        }

        // Handle "Request Summary" button for Full Study
        const fullStudyBtn = document.querySelector('.full-study-btn');
        if (fullStudyBtn) {
            fullStudyBtn.addEventListener('click', function(e) {
                e.preventDefault();

                // Populate hidden fields with onboarding data
                document.getElementById('form-name').value = onboardingData.name;
                document.getElementById('form-email').value = onboardingData.email;
                document.getElementById('form-company').value = onboardingData.company;
                document.getElementById('form-experience').value = onboardingData.experience;
                document.getElementById('form-company-type').value = onboardingData.companyType;
                document.getElementById('form-position').value = onboardingData.position;
                document.getElementById('form-geography').value = onboardingData.geography;
                document.getElementById('form-usage').value = onboardingData.usage;

                // Populate summary display
                document.getElementById('summary-name').textContent = onboardingData.name;
                document.getElementById('summary-email').textContent = onboardingData.email;
                document.getElementById('summary-company').textContent = onboardingData.company;
                document.getElementById('summary-position').textContent = onboardingData.position;

                // Hide pricing, show full study form
                document.getElementById('pricing-section').style.display = 'none';
                document.getElementById('study-form').style.display = 'block';
            });
        }

        // Handle "Back to Options" from full study form
        const formBackBtn = document.querySelector('.form-back-btn');
        if (formBackBtn) {
            formBackBtn.addEventListener('click', function() {
                document.getElementById('study-form').style.display = 'none';
                document.getElementById('pricing-section').style.display = 'grid';
            });
        }

        // Handle "Back to Options" from booking section
        const backToPricingBtn = document.querySelector('.back-to-pricing-btn');
        if (backToPricingBtn) {
            backToPricingBtn.addEventListener('click', function() {
                document.getElementById('booking-section').style.display = 'none';
                document.getElementById('pricing-section').style.display = 'grid';
            });
        }

        // Function to load Calendly
        function loadCalendly() {
            const calendlyContainer = document.getElementById('calendly-container');

            // PLACEHOLDER: Replace 'YOUR_CALENDLY_URL_HERE' with your actual Calendly booking URL
            const calendlyUrl = 'YOUR_CALENDLY_URL_HERE';

            if (calendlyUrl === 'YOUR_CALENDLY_URL_HERE') {
                // Show placeholder when Calendly URL not configured
                calendlyContainer.innerHTML = `
                    <div style="text-align: center; padding: 3rem 2rem; background: rgba(31, 40, 51, 0.3); border: 1px solid rgba(69, 162, 158, 0.2); border-radius: 4px;">
                        <p class="mono" style="color: var(--cyan); font-size: 1.2rem; margin-bottom: 1rem;">⚠️ Calendly Integration Pending</p>
                        <p style="color: var(--silver); font-size: 0.95rem; margin-bottom: 0.5rem;">
                            Please provide your Calendly booking URL to enable calendar scheduling.
                        </p>
                        <p style="color: var(--silver); font-size: 0.85rem; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(69, 162, 158, 0.1);">
                            <strong>User Details:</strong><br>
                            ${onboardingData.name} (${onboardingData.email})<br>
                            ${onboardingData.company} - ${onboardingData.position}
                        </p>
                    </div>
                `;
            } else {
                // Load actual Calendly iframe when URL is configured
                const prefill = `?name=${encodeURIComponent(onboardingData.name)}&email=${encodeURIComponent(onboardingData.email)}`;
                calendlyContainer.innerHTML = `
                    <iframe src="${calendlyUrl}${prefill}"
                            width="100%"
                            height="600"
                            frameborder="0"
                            style="border: 1px solid rgba(69, 162, 158, 0.2); border-radius: 4px;">
                    </iframe>
                `;
            }
        }

        // Close modal
        closeBtn.addEventListener('click', function() {
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
            resetModalView();
        });

        // Close on outside click
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.classList.remove('active');
                document.body.style.overflow = 'auto';
                resetModalView();
            }
        });

        // Close on ESC key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && modal.classList.contains('active')) {
                modal.classList.remove('active');
                document.body.style.overflow = 'auto';
                resetModalView();
            }
        });
        } // End initializeModalHandlers
    } // End initCatalogModal

    // ==========================================
    // 18. PAGE LOAD ANIMATION
    // ==========================================

    window.addEventListener('load', function() {
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.5s ease';

        setTimeout(() => {
            document.body.style.opacity = '1';
        }, 100);
    });

    // ==========================================
    // 19. INITIALIZE CATALOG
    // ==========================================

    initCatalogModal();

})();
