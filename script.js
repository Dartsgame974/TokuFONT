document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.getElementById('fonts-grid');
    const franchiseSelect = document.getElementById('franchise-select');
    const searchInput = document.getElementById('search-input');
    const modal = document.getElementById('font-modal');
    const closeModalBtn = document.getElementById('close-modal');
    
    // Modal Elements
    const modalImage = document.getElementById('modal-image');
    const modalTitle = document.getElementById('modal-title');
    const modalSeason = document.getElementById('modal-season');
    const modalAuthor = document.getElementById('modal-author-link');
    const modalDesc = document.getElementById('modal-description');
    const officialBtn = document.getElementById('official-btn');
    const directDownloads = document.getElementById('direct-downloads');
    const prevImgBtn = document.getElementById('prev-img');
    const nextImgBtn = document.getElementById('next-img');
    const carouselControls = document.getElementById('carousel-controls');

    let fontsData = [];
    let franchisesData = [];
    let currentCarouselImages = [];
    let currentImageIndex = 0;

    // Load Data
    try {
        const [fontsRes, franchisesRes] = await Promise.all([
            fetch('fonts.json'),
            fetch('franchises.json')
        ]);
        fontsData = await fontsRes.json();
        franchisesData = await franchisesRes.json();
        
        populateFranchises();
        renderCards(fontsData);
    } catch (error) {
        console.error('Error loading data:', error);
        grid.innerHTML = '<p>Error loading fonts data.</p>';
    }

    function getSeasonNameByCode(code) {
        for (const franchise of franchisesData) {
            for (const series of franchise.series) {
                if (series.code === code) {
                    return series.name;
                }
            }
        }
        return code; // Fallback
    }

    function populateFranchises() {
        franchisesData.forEach(franchise => {
            const optgroup = document.createElement('optgroup');
            optgroup.label = franchise.name;
            
            franchise.series.forEach(series => {
                // Only add series that have fonts, or you can add all
                const option = document.createElement('option');
                option.value = series.code;
                option.textContent = series.name;
                optgroup.appendChild(option);
            });
            
            franchiseSelect.appendChild(optgroup);
        });
    }

    function renderCards(data) {
        grid.innerHTML = '';
        if (data.length === 0) {
            grid.innerHTML = '<p>No fonts found for this selection.</p>';
            return;
        }

        data.forEach(font => {
            const card = document.createElement('div');
            card.className = 'card';
            
            const seasonName = getSeasonNameByCode(font.season_code);
            
            card.innerHTML = `
                <div class="card-image-wrapper">
                    <img src="${font.main_thumbnail}" alt="${font.title} Thumbnail" loading="lazy">
                </div>
                <div class="card-content">
                    <span class="card-season">${seasonName}</span>
                    <h3 class="card-title">${font.title}</h3>
                </div>
            `;

            card.addEventListener('click', () => openModal(font));
            grid.appendChild(card);
        });
    }

    function filterCards() {
        const selectedCode = franchiseSelect.value;
        const query = searchInput.value.toLowerCase().trim();

        const filtered = fontsData.filter(font => {
            const matchesSelect = selectedCode === 'all' || font.season_code === selectedCode;
            
            const seasonName = getSeasonNameByCode(font.season_code).toLowerCase();
            const fontTitle = font.title.toLowerCase();
            const fontDesc = font.description.toLowerCase();
            
            const matchesQuery = query === '' || 
                fontTitle.includes(query) || 
                seasonName.includes(query) || 
                fontDesc.includes(query);

            return matchesSelect && matchesQuery;
        });

        renderCards(filtered);
    }

    franchiseSelect.addEventListener('change', filterCards);
    searchInput.addEventListener('input', filterCards);

    function openModal(font) {
        const seasonName = getSeasonNameByCode(font.season_code);
        
        modalTitle.textContent = font.title;
        modalSeason.textContent = seasonName;
        modalAuthor.textContent = font.author;
        modalAuthor.href = font.author_url;
        modalDesc.textContent = font.description;
        
        officialBtn.href = font.official_source_url;
        
        // Setup direct downloads & zip
        directDownloads.innerHTML = '';
        if (font.zip_file) {
            const zipBtn = document.createElement('a');
            zipBtn.href = font.zip_file;
            zipBtn.className = 'btn btn-secondary';
            zipBtn.textContent = `Download Direct (.zip)`;
            directDownloads.appendChild(zipBtn);
        } else {
            font.downloads.forEach(dl => {
                const a = document.createElement('a');
                a.href = dl.file;
                a.className = 'btn btn-secondary';
                a.textContent = `Download Direct (${dl.name})`;
                directDownloads.appendChild(a);
            });
        }

        // Setup font preview
        const previewCustom = document.getElementById('preview-custom');
        const previewUpper = document.getElementById('preview-upper');
        const previewLower = document.getElementById('preview-lower');
        const previewNumbers = document.getElementById('preview-numbers');
        const previewInput = document.getElementById('preview-input');
        const previewSelect = document.getElementById('preview-font-select');
        
        // Clear previous font family
        const previewElements = [previewCustom, previewUpper, previewLower, previewNumbers, previewInput];
        previewElements.forEach(el => el.style.fontFamily = 'Satoshi, sans-serif');

        // Setup font selection dropdown
        previewSelect.innerHTML = '';
        if (font.downloads && font.downloads.length > 1) {
            previewSelect.classList.remove('hidden');
            font.downloads.forEach((dl, index) => {
                const option = document.createElement('option');
                option.value = index;
                option.textContent = dl.name;
                previewSelect.appendChild(option);
            });
        } else {
            previewSelect.classList.add('hidden');
        }

        if (!window.loadedFontsCache) {
            window.loadedFontsCache = new Set();
        }
        
        function applyFont(index) {
            if (!font.downloads || font.downloads.length === 0) return;
            const dl = font.downloads[index];
            const fontUrl = dl.file;
            const fontName = 'PreviewFont_' + font.id.replace(/[^a-zA-Z0-9]/g, '') + '_' + index;
            
            if (window.loadedFontsCache.has(fontName)) {
                previewElements.forEach(el => el.style.fontFamily = `'${fontName}', 'Satoshi', sans-serif`);
                return;
            }
            
            const newFont = new FontFace(fontName, `url("${fontUrl}")`);
            newFont.load().then(function(loadedFace) {
                document.fonts.add(loadedFace);
                window.loadedFontsCache.add(fontName);
                previewElements.forEach(el => el.style.fontFamily = `'${fontName}', 'Satoshi', sans-serif`);
            }).catch(function(error) {
                console.error("Font loading failed:", error);
            });
        }
        
        if (font.downloads && font.downloads.length > 0) {
            applyFont(0);
        }

        const newPreviewSelect = previewSelect.cloneNode(true);
        previewSelect.parentNode.replaceChild(newPreviewSelect, previewSelect);
        newPreviewSelect.addEventListener('change', (e) => {
            applyFont(e.target.value);
        });
        
        // Remove old listener to avoid memory leaks/multiple events
        const newPreviewInput = previewInput.cloneNode(true);
        previewInput.parentNode.replaceChild(newPreviewInput, previewInput);
        newPreviewInput.addEventListener('input', (e) => {
            previewCustom.textContent = e.target.value;
        });

        // Setup Carousel
        currentCarouselImages = font.thumbnails || [font.main_thumbnail];
        if (currentCarouselImages.length === 0) {
            currentCarouselImages = [font.main_thumbnail];
        }
        currentImageIndex = 0;
        updateCarouselImage();
        
        if (currentCarouselImages.length > 1) {
            carouselControls.classList.remove('hidden');
        } else {
            carouselControls.classList.add('hidden');
        }

        modal.showModal();
        document.body.style.overflow = 'hidden'; // Prevent scrolling background
    }

    function closeModal() {
        modal.close();
        document.body.style.overflow = '';
    }

    function updateCarouselImage() {
        modalImage.src = currentCarouselImages[currentImageIndex];
    }

    prevImgBtn.addEventListener('click', () => {
        currentImageIndex = (currentImageIndex - 1 + currentCarouselImages.length) % currentCarouselImages.length;
        updateCarouselImage();
    });

    nextImgBtn.addEventListener('click', () => {
        currentImageIndex = (currentImageIndex + 1) % currentCarouselImages.length;
        updateCarouselImage();
    });

    closeModalBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
});
