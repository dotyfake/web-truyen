document.addEventListener('DOMContentLoaded', () => {
    // =================================================================
    // 1. STATE & CONSTANTS
    // =================================================================
    const { createFFmpeg, fetchFile } = FFmpeg;
    let ffmpeg;

    const initialBackgroundLayer = {
        id: 'background', type: 'color', content: '#1a1a1a',
        gradient: { color1: '#0000ff', color2: '#ff0000', angle: 45 },
        isBackground: true, x: 0, y: 0, width: 100, height: 100, unit: '%',
        startTime: 0, endTime: 9999,
        animations: { in: { type: 'none', duration: 0.5 }, out: { type: 'none', duration: 0.5 }, loop: { type: 'kenBurns', duration: 10 } },
        style: { filterBlur: 0 },
        customCss: '',
        animationState: { in: false, out: false, loop: false }
    };

    let template = {
        duration: 0, aspectRatio: '16:9',
        layers: [initialBackgroundLayer],
        sfx: [],
        mainAudio: null
    };

    let activeElementId = null;
    let isPlaying = false;
    let currentTime = 0;
    let animationFrameId;
    let fileCache = new Map();
    let mainAudio;
    let lastRenderTime = 0;
    let pendingConfig = null;

    const EXPORT_WIDTH = 1920, EXPORT_HEIGHT = 1080, PREVIEW_CAPTURE_WIDTH = 960, FPS = 30;

    // =================================================================
    // 2. DOM ELEMENTS
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
        btnAddBox: document.getElementById('btn-add-box'),
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
        loadConfigModal: document.getElementById('load-config-modal'),
        loadConfigFiles: document.getElementById('load-config-files'),
        btnConfirmLoadConfig: document.getElementById('btn-confirm-load-config'),
        btnCancelLoadConfig: document.getElementById('btn-cancel-load-config'),
        toastContainer: document.getElementById('toast-container')
    };

    // =================================================================
    // 3. HELPER FUNCTIONS
    // =================================================================
    function createToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        elements.toastContainer.appendChild(toast);
        setTimeout(() => toast.classList.add('show'), 100);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    }

    function hexToRgba(hex, opacity) {
        hex = hex.replace('#', '');
        const r = parseInt(hex.substring(0, 2), 16);
        const g = parseInt(hex.substring(2, 4), 16);
        const b = parseInt(hex.substring(4, 6), 16);
        return `rgba(${r}, ${g}, ${b}, ${opacity})`;
    }

    function createSettingsGroup(title, content) {
        return `<div class="setting-group"><h4>${title}</h4>${content}</div>`;
    }

    function getAnimOptions(selected, includeLoop = false) {
        const options = [
            { value: 'none', label: 'Không' },
            { value: 'fadeIn', label: 'Mờ dần vào' },
            { value: 'fadeOut', label: 'Mờ dần ra' },
            { value: 'slideInUp', label: 'Trượt lên' },
            { value: 'slideOutDown', label: 'Trượt xuống' },
            { value: 'zoomIn', label: 'Phóng to' },
            { value: 'zoomOut', label: 'Thu nhỏ' },
            { value: 'bounceIn', label: 'Nảy vào' }
        ];
        if (includeLoop) options.push({ value: 'kenBurns', label: 'Ken Burns' });
        return options.map(opt => `<option value="${opt.value}" ${opt.value === selected ? 'selected' : ''}>${opt.label}</option>`).join('');
    }

    function resizePreview() {
        const viewportRect = elements.previewViewport.getBoundingClientRect();
        const aspect = 16 / 9;
        let width = viewportRect.width * 0.9;
        let height = width / aspect;
        if (height > viewportRect.height * 0.9) {
            height = viewportRect.height * 0.9;
            width = height * aspect;
        }
        elements.previewAreaWrapper.style.width = `${width}px`;
        elements.previewAreaWrapper.style.height = `${height}px`;
        const scale = width / EXPORT_WIDTH;
        elements.previewArea.style.transform = `scale(${scale})`;
    }

    function updateExportProgress(progress) {
        elements.exportProgressBar.style.width = `${progress * 100}%`;
    }

    function showExportOverlay(show) {
        elements.exportOverlay.classList.toggle('hidden', !show);
        if (!show) {
            elements.exportStatusTitle.textContent = 'Đang xử lý Video...';
            elements.exportStatusMessage.textContent = '';
            elements.exportProgressBar.style.width = '0%';
            elements.exportLog.textContent = '';
        }
    }

    // =================================================================
    // 4. RENDERING ENGINE
    // =================================================================
    function renderAll() {
        renderLayers();
        renderLayerList();
        renderPropertiesPanel();
        renderFrameAtTime(currentTime);
    }

    function renderLayers() {
        elements.previewArea.innerHTML = '';

        template.layers.forEach((layer, index) => {
            const el = document.createElement('div');
            el.id = layer.id;
            el.className = `layer ${layer.type}-layer`;
            el.tabIndex = 0;
            el.style.zIndex = index;

            el.addEventListener('click', (e) => {
                e.stopPropagation();
                selectElement(layer.id);
            });

            el.addEventListener('animationend', () => {
                if (layer.animationState.in) layer.animationState.in = false;
                if (layer.animationState.out) layer.animationState.out = false;
                renderFrameAtTime(currentTime);
            });

            if (layer.type === 'image' || layer.type === 'video') {
                const file = fileCache.get(layer.content);
                if (file) {
                    const url = URL.createObjectURL(file);
                    if (layer.type === 'image') {
                        el.style.backgroundImage = `url(${url})`;
                        el.style.backgroundSize = 'cover';
                        el.style.backgroundPosition = 'center';
                    } else {
                        const videoEl = document.createElement('video');
                        videoEl.src = url;
                        videoEl.muted = true;
                        videoEl.preload = 'auto';
                        videoEl.loop = layer.isBackground;
                        videoEl.style.width = '100%';
                        videoEl.style.height = '100%';
                        videoEl.style.objectFit = 'cover';
                        el.appendChild(videoEl);
                    }
                }
            } else if (layer.type === 'box') {
                el.style.backgroundColor = layer.style.backgroundColor || 'rgba(255, 255, 255, 0.5)';
            }

            elements.previewArea.appendChild(el);
        });
        setupInteraction();
    }

    function renderFrameAtTime(time) {
        const previewWidth = 1920;
        const previewHeight = 1080;

        template.layers.forEach(layer => {
            const el = document.getElementById(layer.id);
            if (!el) return;

            const isVisible = layer.isBackground || (time >= layer.startTime && time <= layer.endTime);
            el.style.display = isVisible ? (layer.type === 'text' ? 'flex' : 'block') : 'none';
            if (!isVisible && !layer.isBackground) return;

            const x = layer.unit === 'px' ? `${(layer.x / previewWidth) * 100}%` : `${layer.x}%`;
            const y = layer.unit === 'px' ? `${(layer.y / previewHeight) * 100}%` : `${layer.y}%`;
            const width = layer.unit === 'px' ? `${(layer.width / previewWidth) * 100}%` : `${layer.width}%`;
            const height = layer.unit === 'px' ? `${(layer.height / previewHeight) * 100}%` : `${layer.height}%`;

            el.style.left = x;
            el.style.top = y;
            el.style.width = width;
            el.style.height = height;

            switch (layer.type) {
                case 'text':
                    el.textContent = layer.content;
                    const rgba = hexToRgba(layer.style.backgroundColor, layer.style.backgroundOpacity || 0);
                    Object.assign(el.style, {
                        fontSize: layer.unit === 'px' ? `${layer.style.fontSize}px` : `${(layer.style.fontSize / previewHeight) * 100}%`,
                        color: layer.style.color,
                        fontFamily: layer.style.fontFamily,
                        justifyContent: layer.style.textAlign === 'left' ? 'flex-start' : layer.style.textAlign === 'right' ? 'flex-end' : 'center',
                        backgroundColor: rgba,
                        filter: `blur(${layer.style.filterBlur || 0}px)`,
                        border: `${layer.style.borderWidth || 0}px solid ${layer.style.borderColor || '#000000'}`,
                        textShadow: `${layer.style.shadowX || 0}px ${layer.style.shadowY || 0}px ${layer.style.shadowBlur || 0}px ${layer.style.shadowColor || '#000000'}`
                    });
                    break;
                case 'color':
                    el.style.background = layer.content;
                    el.style.filter = `blur(${layer.style.filterBlur || 0}px)`;
                    break;
                case 'gradient':
                    el.style.background = `linear-gradient(${layer.gradient.angle || 0}deg, ${layer.gradient.color1}, ${layer.gradient.color2})`;
                    el.style.filter = `blur(${layer.style.filterBlur || 0}px)`;
                    break;
                case 'video':
                    const videoEl = el.querySelector('video');
                    if (videoEl) {
                        const targetTime = Math.max(0, time - layer.startTime);
                        if (isPlaying && !videoEl.loop) {
                            if (Math.abs(videoEl.currentTime - targetTime) > 0.1) {
                                videoEl.currentTime = targetTime;
                            }
                            if (videoEl.paused) videoEl.play().catch(() => {});
                        } else if (!isPlaying && !videoEl.loop) {
                            videoEl.currentTime = targetTime;
                            if (!videoEl.paused) videoEl.pause();
                        }
                    }
                    el.style.filter = `blur(${layer.style.filterBlur || 0}px)`;
                    break;
                case 'image':
                    el.style.filter = `blur(${layer.style.filterBlur || 0}px)`;
                    break;
                case 'box':
                    el.style.backgroundColor = layer.style.backgroundColor;
                    el.style.filter = `blur(${layer.style.filterBlur || 0}px)`;
                    break;
            }

            if (layer.customCss) el.style.cssText += `;${layer.customCss}`;

            const timeInto = time - layer.startTime;
            const timeUntilEnd = layer.endTime - time;

            if (layer.animations.in.type !== 'none' && timeInto < layer.animations.in.duration && !layer.animationState.in) {
                layer.animationState.in = true;
                el.style.animation = `${layer.animations.in.type} ${layer.animations.in.duration}s ease-in-out forwards`;
            } else if (layer.animations.out.type !== 'none' && timeUntilEnd <= layer.animations.out.duration && timeUntilEnd >= 0 && !layer.animationState.out) {
                layer.animationState.out = true;
                el.style.animation = `${layer.animations.out.type} ${layer.animations.out.duration}s ease-in-out forwards`;
            } else if (layer.animations.loop.type !== 'none' && timeInto >= 0 && !layer.animationState.in && !layer.animationState.out) {
                if (!layer.animationState.loop) {
                    layer.animationState.loop = true;
                    el.style.animation = `${layer.animations.loop.type} ${layer.animations.loop.duration}s ease-in-out infinite alternate`;
                }
            } else if (!layer.animationState.in && !layer.animationState.out && !layer.animationState.loop) {
                el.style.animation = 'none';
                el.style.opacity = 1;
                el.style.transform = 'none';
            }
        });

        template.sfx.forEach(sfx => {
            if (time >= sfx.startTime && !sfx.played) {
                const sfxFile = fileCache.get(sfx.fileName);
                if (sfxFile) {
                    const audio = new Audio(URL.createObjectURL(sfxFile));
                    audio.play().catch(() => {});
                }
                sfx.played = true;
            }
            if (time < sfx.startTime) sfx.played = false;
        });

        lastRenderTime = time;
    }

    // =================================================================
    // 5. INITIALIZATION
    // =================================================================
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
                    if (elements.exportOverlay.classList.contains('hidden')) return;
                    const progress = Math.min(Math.max(p.ratio, 0), 1);
                    elements.exportLog.textContent = `FFmpeg: ${p.ratio ? (progress * 100).toFixed(1) + '%' : '...loading core'}`;
                    if (p.ratio) updateExportProgress(progress);
                }
            });
            createToast('Đang tải thư viện FFmpeg (~30MB)...');
            await ffmpeg.load();
            createToast('FFmpeg đã sẵn sàng!', 'success');
        } catch (e) {
            console.error("FFmpeg loading error:", e);
            createToast('Không thể tải FFmpeg! Hãy chắc chắn bạn đang dùng Live Server.', 'error');
        }
    }

    function attachEventListeners() {
        elements.btnAddAudio.addEventListener('click', () => elements.audioInput.click());
        elements.audioInput.addEventListener('change', handleAudioUpload);
        elements.btnSaveConfig.addEventListener('click', saveConfiguration);
        elements.btnLoadConfig.addEventListener('click', () => elements.loadConfigInput.click());
        elements.loadConfigInput.addEventListener('change', handleLoadConfig);
        elements.btnConfigBg.addEventListener('click', () => selectElement('background'));
        elements.btnAddText.addEventListener('click', addTextLayer);
        elements.btnAddBox.addEventListener('click', addBoxLayer);
        elements.btnAddMedia.addEventListener('click', () => elements.mediaInput.click());
        elements.mediaInput.addEventListener('change', handleMediaUpload);
        elements.btnAddSfx.addEventListener('click', () => elements.sfxInput.click());
        elements.sfxInput.addEventListener('change', handleSfxUpload);
        elements.btnExport.addEventListener('click', exportVideo);
        elements.btnPlayPause.addEventListener('click', togglePlayback);
        elements.timelineSlider.addEventListener('input', () => seek(parseFloat(elements.timelineSlider.value)));
        elements.btnSaveCustomCss.addEventListener('click', saveCustomCss);
        elements.btnCancelCustomCss.addEventListener('click', () => elements.cssEditorOverlay.classList.add('hidden'));
        elements.btnConfirmLoadConfig.addEventListener('click', confirmLoadConfig);
        elements.btnCancelLoadConfig.addEventListener('click', () => elements.loadConfigModal.classList.add('hidden'));
    }

    // =================================================================
    // 6. EVENT HANDLERS
    // =================================================================
    async function handleAudioUpload(event) {
        const file = event.target.files[0];
        if (!file || file.type !== 'audio/mpeg') {
            return createToast('Vui lòng chọn file MP3 hợp lệ.', 'error');
        }
        try {
            fileCache.set('main_audio.mp3', file);
            template.mainAudio = 'main_audio.mp3';
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
        const newLayer = {
            id: `layer_${Date.now()}`, type: 'text', content,
            x: 10, y: 10, width: 200, height: 100, unit: 'px',
            startTime: 0, endTime: template.duration || 10,
            style: {
                fontSize: 48, color: '#ffffff', fontFamily: 'Roboto', textAlign: 'center',
                backgroundColor: '#000000', backgroundOpacity: 0, filterBlur: 0,
                borderWidth: 0, borderColor: '#000000',
                shadowX: 0, shadowY: 0, shadowBlur: 0, shadowColor: '#000000'
            },
            animations: {
                in: { type: 'bounceIn', duration: 0.5 },
                out: { type: 'fadeOut', duration: 0.5 },
                loop: { type: 'none', duration: 5 }
            },
            customCss: '',
            animationState: { in: false, out: false, loop: false }
        };
        template.layers.push(newLayer);
        renderAll();
        selectElement(newLayer.id);
    }

    function addBoxLayer() {
        const newLayer = {
            id: `layer_${Date.now()}`, type: 'box',
            x: 0, y: 0, width: 100, height: 100, unit: 'px',
            startTime: 0, endTime: template.duration || 10,
            style: { backgroundColor: 'rgba(255, 255, 255, 0.5)', filterBlur: 0 },
            animations: {
                in: { type: 'bounceIn', duration: 0.5 },
                out: { type: 'fadeOut', duration: 0.5 },
                loop: { type: 'none', duration: 5 }
            },
            customCss: '',
            animationState: { in: false, out: false, loop: false }
        };
        template.layers.push(newLayer);
        renderAll();
        selectElement(newLayer.id);
    }

    async function handleMediaUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        const type = file.type.startsW