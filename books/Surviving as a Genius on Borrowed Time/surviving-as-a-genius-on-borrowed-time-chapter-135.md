document.addEventListener('DOMContentLoaded', () => {

    // =================================================================
    // 1. STATE & CONSTANTS
    // =================================================================
    const { createFFmpeg, fetchFile } = FFmpeg;
    let ffmpeg;
    
    const initialBackgroundLayer = {
        id: 'background', type: 'color', content: '#1a1a1a', 
        gradient: { color1: '#0000ff', color2: '#ff0000', angle: 45 },
        isBackground: true, x: 0, y: 0, width: 100, height: 100,
        startTime: 0, endTime: 9999,
        animations: { in: {type: 'none'}, out: {type: 'none'}, loop: {type: 'none'}},
        style: {}
    };

    let template = {
        duration: 0, aspectRatio: '16:9',
        layers: [initialBackgroundLayer],
        sfx: [],
    };
    
    let activeElementId = null;
    let isPlaying = false;
    let currentTime = 0;
    let animationFrameId;
    let fileCache = new Map();

    const EXPORT_WIDTH = 1920, EXPORT_HEIGHT = 1080, PREVIEW_CAPTURE_WIDTH = 960, FPS = 30;

    // =================================================================
    // 2. DOM ELEMENTS (Không đổi)
    // =================================================================
    const elements = {
        mainEditorControls: document.getElementById('main-editor-controls'),
        exportControls: document.getElementById('export-controls'),
        audioInput: document.getElementById('audio-input'),
        mediaInput: document.getElementById('media-input'),
        sfxInput: document.getElementById('sfx-input'),
        loadConfigInput: document.getElementById('load-config-input'),
        btnAddAudio: document.getElementById('btn-add-audio'),
        btnSaveConfig: document.getElementById('btn-save-config'),
        btnLoadConfig: document.getElementById('btn-load-config'),
        btnConfigBg: document.getElementById('btn-config-bg'),
        btnAddText: document.getElementById('btn-add-text'),
        btnAddMedia: document.getElementById('btn-add-media'),
        btnAddSfx: document.getElementById('btn-add-sfx'),
        btnExport: document.getElementById('btn-export'),
        btnPlayPause: document.getElementById('btn-play-pause'),
        previewViewport: document.getElementById('preview-viewport'), 
        previewAreaWrapper: document.getElementById('preview-area-wrapper'),
        previewArea: document.getElementById('preview-area'),
        timelineSlider: document.getElementById('timeline-slider'),
        timeDisplay: document.getElementById('time-display'),
        layerList: document.getElementById('layer-list'),
        settingsBox: document.getElementById('settings-box'),
        settingsTitle: document.getElementById('settings-title'),
        settingsContent: document.getElementById('settings-content'),
        exportOverlay: document.getElementById('export-overlay'),
        exportStatusTitle: document.getElementById('export-status-title'),
        exportStatusMessage: document.getElementById('export-status-message'),
        exportProgressBar: document.getElementById('export-progress-bar'),
        exportLog: document.getElementById('export-log'),
        cssEditorOverlay: document.getElementById('css-editor-overlay'),
        cssEditorTextarea: document.getElementById('css-editor-textarea'),
        btnSaveCustomCss: document.getElementById('btn-save-custom-css'),
        btnCancelCustomCss: document.getElementById('btn-cancel-custom-css'),
    };
    
    // =================================================================
    // 6. RENDERING ENGINE (THAY ĐỔI LỚN)
    // =================================================================
    
    function renderAll() {
        renderLayers(); // Tạo cấu trúc DOM một lần
        renderLayerList();
        renderPropertiesPanel();
        renderFrameAtTime(currentTime); // Cập nhật trạng thái dựa trên thời gian
    }

    // SỬA LỖI: Hàm này giờ chịu trách nhiệm TẠO các phần tử DOM một lần.
    function renderLayers() {
        elements.previewArea.innerHTML = '';
        
        template.layers.forEach((layer, index) => {
            const el = document.createElement('div');
            el.id = layer.id;
            el.className = `layer ${layer.type}-layer`;
            el.tabIndex = 0;
            el.style.zIndex = layer.isBackground ? 0 : index;
            
            el.addEventListener('click', (e) => { 
                e.stopPropagation(); 
                if (!layer.isBackground) selectElement(layer.id); 
            });

            // Tạo các phần tử con tĩnh (video, image) ngay tại đây
            if (layer.type === 'image' || layer.type === 'video') {
                const file = fileCache.get(layer.content);
                if (file) {
                    const url = URL.createObjectURL(file);
                    if (layer.type === 'image') {
                        // Nếu là ảnh, có thể dùng background hoặc thẻ img
                        el.style.backgroundImage = `url(${url})`;
                        el.style.backgroundSize = 'cover';
                        el.style.backgroundPosition = 'center';
                    } else { // video
                        const videoEl = document.createElement('video');
                        videoEl.src = url;
                        videoEl.muted = true;
                        videoEl.preload = 'auto'; // Tải trước để sẵn sàng play
                        videoEl.loop = layer.isBackground; // Chỉ nền mới lặp
                        videoEl.style.width = '100%';
                        videoEl.style.height = '100%';
                        videoEl.style.objectFit = 'cover';
                        el.appendChild(videoEl);
                    }
                }
            }
            
            elements.previewArea.appendChild(el);
        });
        setupInteraction();
    }
    
    // SỬA LỖI: Hàm này giờ chỉ CẬP NHẬT thuộc tính, không phá hủy/tạo lại DOM.
    function renderFrameAtTime(time) {
        template.layers.forEach(layer => {
            const el = document.getElementById(layer.id);
            if (!el) return;
            
            const isVisible = time >= layer.startTime && time < layer.endTime;
            
            // Xử lý hiện/ẩn
            if (layer.isBackground) {
                el.style.display = 'block';
            } else {
                el.style.display = isVisible ? 'flex' : 'none';
                if (!isVisible) return;
            }

            // Cập nhật vị trí và kích thước
            el.style.left = `${layer.x}%`;
            el.style.top = `${layer.y}%`;
            el.style.width = `${layer.width}%`;
            el.style.height = `${layer.height}%`;
            
            // Cập nhật nội dung/style dựa trên loại layer
            switch(layer.type) {
                case 'text':
                    el.textContent = layer.content;
                    Object.assign(el.style, {
                        fontSize: `${layer.style.fontSize}px`, color: layer.style.color,
                        fontFamily: layer.style.fontFamily, textAlign: layer.style.textAlign,
                        backgroundColor: layer.style.backgroundColor
                    });
                    break;
                case 'color': // Chỉ dành cho nền
                    el.style.backgroundColor = layer.content;
                    break;
                case 'gradient': // Chỉ dành cho nền
                    el.style.background = `linear-gradient(${layer.gradient.angle || 0}deg, ${layer.gradient.color1}, ${layer.gradient.color2})`;
                    break;
                case 'video':
                    const videoEl = el.querySelector('video');
                    if (videoEl) {
                        if (isPlaying && !videoEl.loop) {
                            // Đồng bộ video layer với audio chính
                            const targetTime = time - layer.startTime;
                            // Check để tránh lỗi seek không cần thiết
                            if (Math.abs(videoEl.currentTime - targetTime) > 0.1) {
                                videoEl.currentTime = targetTime;
                            }
                            if (videoEl.paused) videoEl.play().catch(e => {});
                        } else if (!isPlaying && !videoEl.loop) {
                            videoEl.currentTime = time - layer.startTime;
                            if (!videoEl.paused) videoEl.pause();
                        }
                    }
                    break;
            }
            
            if (layer.customCss) el.style.cssText += layer.customCss;

            // Xử lý animation (không áp dụng cho nền)
            if (!layer.isBackground) {
                el.style.animation = 'none';
                el.offsetHeight; // Trigger reflow
                
                const timeInto = time - layer.startTime;
                const timeUntilEnd = layer.endTime - time;
                
                if (timeInto >= 0 && timeInto < layer.animations.in.duration && layer.animations.in.type !== 'none') {
                    el.style.animation = `${layer.animations.in.type} ${layer.animations.in.duration}s ease-out forwards`;
                } else if (timeUntilEnd >= 0 && timeUntilEnd < layer.animations.out.duration && layer.animations.out.type !== 'none') {
                    el.style.animation = `${layer.animations.out.type} ${layer.animations.out.duration}s ease-in forwards`;
                } else if (layer.animations.loop.type !== 'none') {
                    el.style.animation = `${layer.animations.loop.type} ${layer.animations.loop.duration}s ease-in-out infinite alternate`;
                } else {
                    el.style.opacity = 1;
                }
            }
        });

        // Trigger SFX (giữ nguyên)
        template.sfx.forEach(sfx => {
            if(time >= sfx.startTime && !sfx.played) {
                const sfxFile = fileCache.get(sfx.fileName);
                if(sfxFile) new Audio(URL.createObjectURL(sfxFile)).play();
                sfx.played = true;
            }
            if (time < sfx.startTime) sfx.played = false;
        });
    }

    // =================================================================
    // PHẦN CÒN LẠI CỦA FILE (Init, Handlers, State, Playback, Export...)
    // =================================================================
    // Hầu hết các hàm khác không cần thay đổi lớn, tôi sẽ dán toàn bộ file
    // đã được sắp xếp lại để đảm bảo tính nhất quán.

    function init() {
        attachEventListeners();
        resizePreview();
        loadFFmpeg();
        window.addEventListener('resize', resizePreview);
        createToast('Chào mừng đến với Video Editor!', 'success');
        renderAll();
    }

    async function loadFFmpeg() {
        try {
            ffmpeg = createFFmpeg({ 
                log: true,
                progress: (p) => {
                    if(elements.exportOverlay.classList.contains('hidden')) return;
                    const progress = Math.min(Math.max(p.ratio, 0), 1);
                    elements.exportLog.textContent = `FFmpeg: ${p.ratio ? (progress * 100).toFixed(1) + '%' : '...loading core'}`;
                    if (p.ratio) updateExportProgress(progress);
                }
            });
            createToast('Đang tải thư viện FFmpeg (~30MB)...');
            await ffmpeg.load();
            createToast('FFmpeg đã sẵn sàng!', 'success');
        } catch(e) {
            console.error("FFmpeg loading error:", e);
            createToast('Không thể tải FFmpeg! Hãy chắc chắn bạn đang dùng Live Server.', 'error');
        }
    }

    function attachEventListeners() {
        elements.btnAddAudio.addEventListener('click', () => elements.audioInput.click());
        elements.audioInput.addEventListener('change', handleAudioUpload);

        elements.btnSaveConfig.addEventListener('click', saveConfiguration);
        elements.btnLoadConfig.addEventListener('click', () => elements.loadConfigInput.click());
        elements.loadConfigInput.addEventListener('change', loadConfiguration);

        elements.btnConfigBg.addEventListener('click', () => selectElement('background'));
        elements.btnAddText.addEventListener('click', addTextLayer);
        elements.btnAddMedia.addEventListener('click', () => elements.mediaInput.click());
        elements.mediaInput.addEventListener('change', handleMediaUpload);
        elements.btnAddSfx.addEventListener('click', () => elements.sfxInput.click());
        elements.sfxInput.addEventListener('change', handleSfxUpload);

        elements.btnPlayPause.addEventListener('click', togglePlayback);
        elements.timelineSlider.addEventListener('input', () => seek(parseFloat(elements.timelineSlider.value)));

        elements.btnExport.addEventListener('click', exportVideo);
        
        elements.btnSaveCustomCss.addEventListener('click', saveCustomCss);
        elements.btnCancelCustomCss.addEventListener('click', () => elements.cssEditorOverlay.classList.add('hidden'));
    }

    async function handleAudioUpload(event) {
        const file = event.target.files[0];
        if (!file || file.type !== 'audio/mpeg') {
            return createToast('Vui lòng chọn một file MP3 hợp lệ.', 'error');
        }
        try {
            fileCache.set('main_audio.mp3', file);
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const arrayBuffer = await file.arrayBuffer();
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            template.duration = audioBuffer.duration;
            elements.timelineSlider.max = template.duration;
            template.layers.forEach(layer => {
                if (!layer.isBackground && layer.endTime > template.duration) layer.endTime = template.duration;
            });
            elements.mainEditorControls.classList.remove('disabled');
            elements.exportControls.classList.remove('disabled');
            if (mainAudio) mainAudio.src = URL.createObjectURL(file);
            else mainAudio = new Audio(URL.createObjectURL(file));
            updateTimelineDisplay();
            createToast(`Tải âm nền thành công. Thời lượng: ${template.duration.toFixed(2)}s`, 'success');
        } catch (e) {
            createToast('Lỗi khi xử lý file audio.', 'error');
            console.error(e);
        }
    }

    function addTextLayer() {
        const content = prompt("Nhập nội dung văn bản:", "Tiêu đề video");
        if (!content) return;
        const newLayer = { id: `layer_${Date.now()}`, type: 'text', content, x: 10, y: 10, width: 30, height: 10, startTime: 0, endTime: template.duration || 10, style: { fontSize: 48, color: '#ffffff', fontFamily: 'Roboto', textAlign: 'center', backgroundColor: 'rgba(0,0,0,0)', }, animations: { in: { type: 'bounceIn', duration: 0.5 }, out: { type: 'fadeOut', duration: 0.5 }, loop: { type: 'none', duration: 5 } }, customCss: '' };
        template.layers.push(newLayer);
        renderAll();
        selectElement(newLayer.id);
    }
    
    async function handleMediaUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        const type = file.type.startsWith('image') ? 'image' : 'video';
        const fileName = `${type}_${Date.now()}_${file.name}`;
        fileCache.set(fileName, file);
        const newLayer = { id: `layer_${Date.now()}`, type: type, content: fileName, x: 25, y: 25, width: 50, height: 50, startTime: 0, endTime: template.duration || 10, style: {}, animations: { in: { type: 'bounceIn', duration: 0.5 }, out: { type: 'fadeOut', duration: 0.5 }, loop: { type: 'none', duration: 5 } }, customCss: '' };
        template.layers.push(newLayer);
        renderAll();
        selectElement(newLayer.id);
    }

    async function handleSfxUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        const fileName = `sfx_${Date.now()}_${file.name}`;
        fileCache.set(fileName, file);
        const newSfx = { id: `sfx_${Date.now()}`, name: file.name, fileName: fileName, startTime: currentTime, };
        template.sfx.push(newSfx);
        renderAll();
        selectElement(newSfx.id);
    }
    
    function saveConfiguration() {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(template, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "video_config.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
        createToast('Đã lưu cấu hình!', 'success');
    }

    async function loadConfiguration(event) {
        const file = event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = async (e) => {
            try {
                const newTemplate = JSON.parse(e.target.result);
                if (!newTemplate.layers.find(l => l.isBackground)) {
                    newTemplate.layers.unshift(initialBackgroundLayer);
                }
                template = newTemplate;
                fileCache.clear();
                alert("Cấu hình đã được tải. Vui lòng chọn lại tất cả các file media (nhạc nền, ảnh, video, sfx) để dự án hoạt động chính xác.");
                elements.mainEditorControls.classList.add('disabled');
                elements.exportControls.classList.add('disabled');
                currentTime = 0;
                if(mainAudio) mainAudio.src = '';
                renderAll();
                createToast('Tải cấu hình thành công. Vui lòng thêm lại các file.', 'success');
            } catch (err) {
                createToast('File cấu hình không hợp lệ!', 'error');
                console.error(err);
            }
        };
        reader.readAsText(file);
    }

    function updateElementProperty(id, property, value) {
        const target = getElementData(id);
        if (!target) return;
        const keys = property.split('.');
        let obj = target;
        for (let i = 0; i < keys.length - 1; i++) {
            if (!obj[keys[i]]) obj[keys[i]] = {};
            obj = obj[keys[i]];
        }
        const numericProps = ['x', 'y', 'width', 'height', 'fontSize', 'startTime', 'endTime', 'duration', 'angle'];
        if (numericProps.includes(keys[keys.length-1])) {
            value = parseFloat(value) || 0;
        }
        obj[keys[keys.length - 1]] = value;
        renderAll();
        if(activeElementId === id) renderPropertiesPanel();
    }
    
    function getElementData(id) {
        if (id.startsWith('layer_') || id === 'background') return template.layers.find(l => l.id === id);
        if (id.startsWith('sfx_')) return template.sfx.find(s => s.id === id);
        return null;
    }
    
    function renderLayerList() {
        elements.layerList.innerHTML = '';
        const bgLayerData = template.layers.find(l => l.isBackground);
        if (bgLayerData) {
            const bgItem = document.createElement('li');
            bgItem.textContent = '🎨 Nền (Background)';
            bgItem.dataset.id = 'background';
            if (activeElementId === 'background') bgItem.classList.add('selected');
            bgItem.addEventListener('click', () => selectElement('background'));
            elements.layerList.appendChild(bgItem);
        }
        template.layers.filter(l => !l.isBackground).forEach(layer => {
            const item = document.createElement('li');
            item.textContent = `[${layer.type}] ${layer.type === 'text' ? (layer.content || '').substring(0, 20) + '...' : layer.content}`;
            item.dataset.id = layer.id;
            if (activeElementId === layer.id) item.classList.add('selected');
            item.addEventListener('click', () => selectElement(layer.id));
            elements.layerList.appendChild(item);
        });
        template.sfx.forEach(sfx => {
            const item = document.createElement('li');
            item.textContent = `🔊 [SFX] ${sfx.name}`;
            item.dataset.id = sfx.id;
            if (activeElementId === sfx.id) item.classList.add('selected');
            item.addEventListener('click', () => selectElement(sfx.id));
            elements.layerList.appendChild(item);
        });
    }

    function renderPropertiesPanel() {
        if (!activeElementId) {
            elements.settingsBox.classList.add('hidden');
            return;
        }
        elements.settingsBox.classList.remove('hidden');
        const elementData = getElementData(activeElementId);
        elements.settingsContent.innerHTML = '';
        elements.settingsTitle.textContent = `Thuộc tính của: ${elementData.isBackground ? 'Nền' : (elementData.content || elementData.type)}`;
        let html = '';
        if (elementData.isBackground) {
            html += createSettingsGroup('Cấu hình Nền', `<label>Loại: <select data-prop="type"><option value="color" ${elementData.type === 'color' ? 'selected' : ''}>Màu</option><option value="gradient" ${elementData.type === 'gradient' ? 'selected' : ''}>Gradient</option><option value="image" ${elementData.type === 'image' ? 'selected' : ''}>Ảnh</option><option value="video" ${elementData.type === 'video' ? 'selected' : ''}>Video</option></select></label>`);
            if (elementData.type === 'color') {
                html += `<label>Màu: <input type="color" data-prop="content" value="${elementData.content || '#000000'}"></label>`;
            } else if (elementData.type === 'gradient') {
                html += `<label>Màu 1: <input type="color" data-prop="gradient.color1" value="${elementData.gradient.color1 || '#000000'}"></label><label>Màu 2: <input type="color" data-prop="gradient.color2" value="${elementData.gradient.color2 || '#ffffff'}"></label><label>Góc (°): <input type="number" data-prop="gradient.angle" value="${elementData.gradient.angle || 0}"></label>`;
            } else if (elementData.type === 'image' || elementData.type === 'video') {
                html += `<label>File: <input type="file" class="bg-file-input" accept="${elementData.type}/*"></label><span>${elementData.content || 'Chưa chọn file'}</span>`;
            }
        } else if (activeElementId.startsWith('layer_')) {
            html = createSettingsGroup('Vị trí & Kích thước', `<label>X (%): <input type="number" data-prop="x" value="${elementData.x}"></label><label>Y (%): <input type="number" data-prop="y" value="${elementData.y}"></label><label>Rộng (%): <input type="number" data-prop="width" value="${elementData.width}"></label><label>Cao (%): <input type="number" data-prop="height" value="${elementData.height}"></label>`);
            html += createSettingsGroup('Thời gian (giây)', `<label>Bắt đầu: <input type="number" step="0.1" data-prop="startTime" value="${elementData.startTime}"></label><label>Kết thúc: <input type="number" step="0.1" data-prop="endTime" value="${elementData.endTime}"></label>`);
            if (elementData.type === 'text') {
                 html += createSettingsGroup('Thuộc tính Văn bản', `<label>Font: <input type="text" data-prop="style.fontFamily" value="${elementData.style.fontFamily}"></label><label>Cỡ chữ (px): <input type="number" data-prop="style.fontSize" value="${elementData.style.fontSize}"></label><label>Màu chữ: <input type="color" data-prop="style.color" value="${elementData.style.color}"></label><label>Màu nền: <input type="color" data-prop="style.backgroundColor" value="${elementData.style.backgroundColor}"></label><label>Căn chỉnh: <select data-prop="style.textAlign"><option value="left" ${elementData.style.textAlign === 'left' ? 'selected' : ''}>Trái</option><option value="center" ${elementData.style.textAlign === 'center' ? 'selected' : ''}>Giữa</option><option value="right" ${elementData.style.textAlign === 'right' ? 'selected' : ''}>Phải</option></select></label>`);
            }
            html += createSettingsGroup('Hiệu ứng', `<h4>Vào</h4><label>Loại: <select data-prop="animations.in.type">${getAnimOptions(elementData.animations.in.type)}</select></label><label>Thời lượng: <input type="number" step="0.1" data-prop="animations.in.duration" value="${elementData.animations.in.duration}"></label><h4>Ra</h4><label>Loại: <select data-prop="animations.out.type">${getAnimOptions(elementData.animations.out.type)}</select></label><label>Thời lượng: <input type="number" step="0.1" data-prop="animations.out.duration" value="${elementData.animations.out.duration}"></label><h4>Lặp</h4><label>Loại: <select data-prop="animations.loop.type">${getAnimOptions(elementData.animations.loop.type, true)}</select></label><label>Thời lượng: <input type="number" step="0.1" data-prop="animations.loop.duration" value="${elementData.animations.loop.duration}"></label>`);
            html += createSettingsGroup('Nâng cao', `<button id="btn-custom-css">CSS tùy chỉnh</button><button id="btn-delete-layer" class="danger">Xóa Lớp</button>`);
        } else if (activeElementId.startsWith('sfx_')) {
             html += createSettingsGroup('Thuộc tính SFX', `<label>Bắt đầu: <input type="number" step="0.1" data-prop="startTime" value="${elementData.startTime}"></label><button id="btn-delete-sfx" class="danger">Xóa SFX</button>`);
        }
        elements.settingsContent.innerHTML = html;
        elements.settingsContent.addEventListener('input', handlePropertyChange);
        const bgFileInput = elements.settingsContent.querySelector('.bg-file-input');
        if(bgFileInput) bgFileInput.addEventListener('change', handleBgFileChange);
        if(document.getElementById('btn-custom-css')) document.getElementById('btn-custom-css').addEventListener('click', openCssEditor);
        if(document.getElementById('btn-delete-layer')) document.getElementById('btn-delete-layer').addEventListener('click', deleteActiveLayer);
        if(document.getElementById('btn-delete-sfx')) document.getElementById('btn-delete-sfx').addEventListener('click', deleteActiveSfx);
    }
    
    function handleBgFileChange(event) {
        const file = event.target.files[0];
        if(!file) return;
        const elementData = getElementData('background');
        const fileName = `bg_${elementData.type}_${Date.now()}_${file.name}`;
        fileCache.set(fileName, file);
        updateElementProperty('background', 'content', fileName);
    }

    function handlePropertyChange(e) {
        const prop = e.target.dataset.prop;
        if (prop) {
            let value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
            if (prop === 'type' && activeElementId === 'background') {
                updateElementProperty('background', 'type', value);
                renderPropertiesPanel();
            } else {
                 updateElementProperty(activeElementId, prop, value);
            }
        }
    }
    
    function selectElement(id) {
        activeElementId = id;
        renderLayerList();
        renderPropertiesPanel();
        const el = document.getElementById(id);
        if(el && !getElementData(id)?.isBackground) el.focus();
    }
    
    function deleteActiveLayer() { if(confirm('Bạn có chắc muốn xóa lớp này?')) { template.layers = template.layers.filter(l => l.id !== activeElementId); activeElementId = null; renderAll(); } }
    function deleteActiveSfx() { if(confirm('Bạn có chắc muốn xóa SFX này?')) { template.sfx = template.sfx.filter(s => s.id !== activeElementId); activeElementId = null; renderAll(); } }
    function openCssEditor() { const layer = getElementData(activeElementId); elements.cssEditorTextarea.value = layer.customCss || ''; elements.cssEditorOverlay.classList.remove('hidden'); }
    function saveCustomCss() { updateElementProperty(activeElementId, 'customCss', elements.cssEditorTextarea.value); elements.cssEditorOverlay.classList.add('hidden'); renderFrameAtTime(currentTime); }
    let mainAudio;
    function togglePlayback() { if (!mainAudio || !mainAudio.src) { return createToast('Hãy thêm âm thanh nền trước.', 'error'); } isPlaying ? pause() : play(); }
    
    function play() {
        isPlaying = true;
        elements.btnPlayPause.textContent = '❚❚';
        mainAudio.play();

        // Đồng bộ và phát tất cả các video layer
        template.layers.filter(l => l.type === 'video').forEach(l => {
            const el = document.getElementById(l.id);
            const videoEl = el ? el.querySelector('video') : null;
            if(videoEl && videoEl.paused) videoEl.play().catch(e => {});
        });

        animationFrameId = requestAnimationFrame(animationLoop);
    }
    
    function pause() {
        isPlaying = false;
        elements.btnPlayPause.textContent = '▶️';
        if (mainAudio) mainAudio.pause();

        // Dừng tất cả các video layer
        template.layers.filter(l => l.type === 'video').forEach(l => {
            const el = document.getElementById(l.id);
            const videoEl = el ? el.querySelector('video') : null;
            if(videoEl && !videoEl.paused) videoEl.pause();
        });

        cancelAnimationFrame(animationFrameId);
    }
    
    function animationLoop() {
        if (!isPlaying) return;
        currentTime = mainAudio.currentTime;
        if (currentTime >= template.duration) {
            currentTime = template.duration;
            pause();
            seek(0); // Quay về đầu khi hết
        }
        elements.timelineSlider.value = currentTime;
        updateTimelineDisplay();
        renderFrameAtTime(currentTime);
        animationFrameId = requestAnimationFrame(animationLoop);
    }
    
    function seek(time, updateAudio = true) {
        if (!mainAudio) return;
        const wasPlaying = isPlaying;
        if(wasPlaying) pause();
        currentTime = Math.max(0, Math.min(time, template.duration));
        if (updateAudio) {
            mainAudio.currentTime = currentTime;
        }
        elements.timelineSlider.value = currentTime;
        updateTimelineDisplay();
        renderFrameAtTime(currentTime);
        if (wasPlaying) play();
    }
    
    function updateTimelineDisplay() { const formatTime = (sec) => { const minutes = Math.floor(sec / 60); const seconds = Math.floor(sec % 60); return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`; }; elements.timeDisplay.textContent = `${formatTime(currentTime)} / ${formatTime(template.duration)}`; }
    
    function setupInteraction() { interact('.layer:not([id=background])').draggable({ listeners: { start(event) { selectElement(event.target.id); }, move(event) { const target = event.target; const layer = getElementData(target.id); if (!layer) return; const rect = elements.previewArea.getBoundingClientRect(); const x = (parseFloat(target.style.left) || 0) + (event.dx / rect.width * 100); const y = (parseFloat(target.style.top) || 0) + (event.dy / rect.height * 100); layer.x = x; layer.y = y; target.style.left = `${x}%`; target.style.top = `${y}%`; }, end(event) { renderPropertiesPanel(); } }, modifiers: [ interact.modifiers.restrictRect({ restriction: 'parent' }) ] }).styleCursor(true); }
    
    async function exportVideo() { if (!ffmpeg || !ffmpeg.isLoaded()) { return createToast('FFmpeg chưa sẵn sàng...', 'error'); } if (template.duration === 0) { return createToast('Không có âm thanh nền...', 'error'); } pause(); showExportOverlay(true); elements.exportStatusTitle.textContent = "Bắt đầu..."; try { elements.exportStatusMessage.textContent = "Giai đoạn 1/2: Chụp khung hình..."; const originalScale = elements.previewArea.style.transform; const scale = PREVIEW_CAPTURE_WIDTH / elements.previewArea.offsetWidth; elements.previewArea.style.transform = `scale(${scale})`; const totalFrames = Math.floor(template.duration * FPS); for (let i = 0; i < totalFrames; i++) { const time = i / FPS; renderFrameAtTime(time); await new Promise(resolve => setTimeout(resolve, 10)); const canvas = await html2canvas(elements.previewArea, { scale: EXPORT_WIDTH / PREVIEW_CAPTURE_WIDTH, width: EXPORT_WIDTH, height: EXPORT_HEIGHT, useCORS: true, logging: false }); const frameData = await new Promise(res => canvas.toBlob(res, 'image/jpeg', 0.9)); ffmpeg.FS('writeFile', `frame${i.toString().padStart(4,'0')}.jpg`, await fetchFile(frameData)); updateExportProgress((i + 1) / totalFrames); } elements.previewArea.style.transform = originalScale; elements.exportStatusMessage.textContent = "Giai đoạn 2/2: Ghép video và âm thanh..."; elements.exportLog.textContent = "Khởi tạo FFmpeg..."; updateExportProgress(0); const mainAudioFile = fileCache.get('main_audio.mp3'); ffmpeg.FS('writeFile', 'main_audio.mp3', await fetchFile(mainAudioFile)); const sfxFiles = []; for(const sfx of template.sfx){ const sfxFile = fileCache.get(sfx.fileName); if(sfxFile){ ffmpeg.FS('writeFile', sfx.fileName, await fetchFile(sfxFile)); sfxFiles.push(sfx); } } const audioInputs = ['-i', 'main_audio.mp3']; sfxFiles.forEach(sfx => audioInputs.push('-i', sfx.fileName)); let filterComplex = ''; if (sfxFiles.length > 0) { let filter = `[0:a]volume=1.0[aout0];`; sfxFiles.forEach((sfx, index) => { const delayMs = sfx.startTime * 1000; filter += `[${index + 1}:a]adelay=${delayMs}|${delayMs}[sfx${index}];`; }); const mixInputs = sfxFiles.map((s, i) => `[sfx${i}]`).join(''); filter += `[aout0]${mixInputs}amix=inputs=${sfxFiles.length + 1}[aout]`; filterComplex = filter; } const command = [ '-framerate', `${FPS}`, '-i', 'frame%04d.jpg', ...audioInputs ]; if (filterComplex) { command.push('-filter_complex', filterComplex, '-map', '0:v:0', '-map', '[aout]'); } else { command.push('-map', '0:v:0', '-map', '1:a:0'); } command.push('-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-shortest', '-y', 'output.mp4'); await ffmpeg.run(...command); const data = ffmpeg.FS('readFile', 'output.mp4'); const videoBlob = new Blob([data.buffer], { type: 'video/mp4' }); const downloadLink = document.createElement('a'); downloadLink.href = URL.createObjectURL(videoBlob); downloadLink.download = `my-video-${Date.now()}.mp4`; downloadLink.click(); URL.revokeObjectURL(downloadLink.href); elements.exportStatusTitle.textContent = "Hoàn thành!"; elements.exportStatusMessage.textContent = "Video của bạn đã được tải xuống."; createToast('Xuất video thành công!', 'success'); } catch (error) { console.error(error); elements.exportStatusTitle.textContent = "Lỗi!"; elements.exportStatusMessage.textContent = "Đã có lỗi xảy ra..."; createToast('Xuất video thất bại!', 'error'); } finally { try { const files = ffmpeg.FS('readdir', '/'); files.forEach(file => { if(file !== '.' && file !== '..') ffmpeg.FS('unlink', file); }); } catch(e) {} setTimeout(() => showExportOverlay(false), 3000); } }
    
    function showExportOverlay(show) { elements.exportOverlay.classList.toggle('hidden', !show); if (show) { updateExportProgress(0); elements.exportLog.textContent = ''; } }
    function updateExportProgress(ratio) { elements.exportProgressBar.style.width = `${ratio * 100}%`; }
    function createToast(message, type = 'info') { const toastContainer = document.getElementById('toast-container'); const toast = document.createElement('div'); toast.className = `toast ${type}`; toast.textContent = message; toastContainer.appendChild(toast); setTimeout(() => { toast.classList.add('show'); }, 100); setTimeout(() => { toast.classList.remove('show'); setTimeout(() => toast.remove(), 500); }, 4000); }
    function resizePreview() { const viewport = elements.previewViewport; if (!viewport) return; const viewportRatio = viewport.clientWidth / viewport.clientHeight; const videoRatio = 16 / 9; if (viewportRatio > videoRatio) { elements.previewAreaWrapper.style.height = '100%'; elements.previewAreaWrapper.style.width = `${viewport.clientHeight * videoRatio}px`; } else { elements.previewAreaWrapper.style.width = '100%'; elements.previewAreaWrapper.style.height = `${viewport.clientWidth / videoRatio}px`; } }
    function createSettingsGroup(title, content) { return `<div class="setting-group"><h4>${title}</h4>${content}</div>`; }
    function getAnimOptions(selected, isLoop = false) { const options = isLoop ? ['none', 'kenBurns'] : ['none', 'fadeIn', 'fadeOut', 'slideInUp', 'slideOutDown', 'zoomIn', 'zoomOut', 'bounceIn']; return options.map(opt => `<option value="${opt}" ${selected === opt ? 'selected' : ''}>${opt}</option>`).join(''); }

    init();
});                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             