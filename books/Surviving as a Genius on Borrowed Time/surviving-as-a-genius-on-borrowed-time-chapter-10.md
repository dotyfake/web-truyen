<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Cài đặt header để bật SharedArrayBuffer - Rất quan trọng cho FFmpeg -->
    <meta http-equiv="Cross-Origin-Opener-Policy" content="same-origin" />
    <meta http-equiv="Cross-Origin-Embedder-Policy" content="require-corp" />
    <title>Simple Video Editor</title>
    <link rel="stylesheet" href="style.css">
    <link rel="icon" href="data:,">
</head>
<body>
    <div id="app-container">
        <!-- CỘT TRÁI: ĐIỀU KHIỂN CHUNG VÀ THÊM MỚI -->
        <div class="controls-panel">
            <h2><span class="logo">🎬</span> Video Editor</h2>
            <div class="control-group">
                <h3>Dự án</h3>
                <input type="file" id="audio-input" accept="audio/mp3" hidden>
                <button id="btn-add-audio">1. Thêm Âm Nền (Bắt buộc)</button>
                <button id="btn-save-config">Lưu Cấu hình (JSON)</button>
                <input type="file" id="load-config-input" accept=".json" hidden>
                <button id="btn-load-config">Tải Cấu hình</button>
            </div>
            
            <div id="main-editor-controls" class="control-group disabled">
                <h3>Thêm Lớp & Âm thanh</h3>
                <button id="btn-config-bg">🎨 Nền</button>
                <button id="btn-add-text">ண்ட் Thêm Văn bản</button>
                
                <input type="file" id="media-input" accept="image/*,video/*" hidden>
                <button id="btn-add-media">🖼️ Thêm Media</button>
                <input type="file" id="sfx-input" accept="audio/*" hidden>
                <button id="btn-add-sfx">🔊 Thêm SFX</button>
            </div>

            <div class="control-group disabled" id="export-controls">
                <h3>Xuất Video</h3>
                 <button id="btn-export">🚀 Xuất Video (1080p)</button>
            </div>
        </div>

        <!-- KHU VỰC TRUNG TÂM: PREVIEW VÀ TIMELINE -->
        <div class="center-panel">
            <div id="preview-viewport">
                <div id="preview-area-wrapper">
                    <div id="preview-area" class="aspect-16-9">
                        <!-- Lớp nền sẽ được render bởi JS -->
                        <!-- Các lớp media và text sẽ được thêm vào đây -->
                    </div>
                </div>
            </div>
            <div class="timeline-container">
                <div class="timeline-controls">
                    <button id="btn-play-pause">▶️</button>
                    <span id="time-display">00:00 / 00:00</span>
                </div>
                <input type="range" id="timeline-slider" min="0" value="0" step="0.01">
            </div>
        </div>

        <!-- CỘT PHẢI: DANH SÁCH LỚP VÀ BẢNG THUỘC TÍNH -->
        <div class="properties-panel">
            <div class="layer-list-container">
                <h3>Tài sản Dự án</h3>
                <ul id="layer-list">
                    <!-- Danh sách các lớp và sfx sẽ hiện ở đây -->
                </ul>
            </div>
            <div id="settings-box" class="hidden">
                <h3 id="settings-title">Thuộc tính</h3>
                <div id="settings-content">
                    <!-- Các tùy chọn cấu hình sẽ được render ở đây -->
                </div>
            </div>
        </div>
    </div>

    <!-- CÁC MODAL VÀ OVERLAY -->
    <div id="export-overlay" class="hidden">
        <div class="export-modal">
            <h2 id="export-status-title">Đang xử lý Video...</h2>
            <p id="export-status-message">Vui lòng không đóng tab này.</p>
            <div class="progress-bar-container">
                <div id="export-progress-bar"></div>
            </div>
            <p id="export-log"></p>
        </div>
    </div>
    
    <div id="css-editor-overlay" class="hidden">
        <div class="css-editor-modal">
            <h3>Trình chỉnh sửa CSS tùy chỉnh</h3>
            <p>Thêm các thuộc tính CSS nâng cao cho lớp này.</p>
            <textarea id="css-editor-textarea"></textarea>
            <div class="css-editor-buttons">
                <button id="btn-save-custom-css">Lưu</button>
                <button id="btn-cancel-custom-css">Hủy</button>
            </div>
        </div>
    </div>

    <div id="toast-container"></div>

    <!-- THƯ VIỆN BÊN NGOÀI -->
    <script src="https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.11.6/dist/ffmpeg.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/interactjs/dist/interact.min.js"></script>
    <script src="script.js"></script>
</body>
</html>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       import { state, elements, resetTemplate } from './state.js';
import { createToast } from './utils.js';
import { renderAll } from './rendering.js';
import { updateTimelineDisplay } from './playback.js';

export function saveConfiguration() {
    const config = {
        ...state.template,
        layers: state.template.layers.map(layer => {
            const newLayer = { ...layer };
            if (layer.content && (layer.type === 'image' || layer.type === 'video')) {
                newLayer.content = { fileName: layer.content, type: layer.type };
            }
            if (layer.depthMap) {
                newLayer.depthMap = { fileName: layer.depthMap, type: 'image' };
            }
            return newLayer;
        }),
        sfx: state.template.sfx.map(sfx => ({ ...sfx })),
        mainAudio: state.template.mainAudio ? { fileName: state.template.mainAudio, type: 'audio' } : null,
        cssPresets: { ...state.cssPresets }
    };

    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(config, null, 2));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", "video_config.json");
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
    createToast('Đã lưu cấu hình!', 'success');
}

export async function handleLoadConfig(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = async (e) => {
        try {
            state.pendingConfig = JSON.parse(e.target.result);
            if (!state.pendingConfig.layers || !state.pendingConfig.layers.find(l => l.isBackground)) {
                const initialBg = state.template.layers.find(l => l.isBackground);
                if (!state.pendingConfig.layers) state.pendingConfig.layers = [];
                state.pendingConfig.layers.unshift(JSON.parse(JSON.stringify(initialBg)));
            }
            const filesNeeded = [];
            if (state.pendingConfig.mainAudio) {
                filesNeeded.push({ id: 'main_audio', fileName: state.pendingConfig.mainAudio.fileName, type: 'audio/*' });
            }
            state.pendingConfig.layers.forEach(layer => {
                if (layer.content && typeof layer.content === 'object') {
                    filesNeeded.push({ id: layer.id, fileName: layer.content.fileName, type: layer.content.type === 'image' ? 'image/*' : 'video/*' });
                }
                if (layer.depthMap && typeof layer.depthMap === 'object') {
                    filesNeeded.push({ id: `${layer.id}_depth`, fileName: layer.depthMap.fileName, type: 'image/*' });
                }
            });
            state.pendingConfig.sfx.forEach(sfx => {
                filesNeeded.push({ id: sfx.id, fileName: sfx.fileName, type: 'audio/*' });
            });
            showLoadConfigModal(filesNeeded);
        } catch (err) {
            createToast('File cấu hình không hợp lệ!', 'error');
            console.error(err);
        }
    };
    reader.readAsText(file);
    event.target.value = '';
}

function showLoadConfigModal(filesNeeded) {
    if (filesNeeded.length === 0) {
        confirmLoadConfig();
        return;
    }

    elements.loadConfigFiles.innerHTML = filesNeeded.map(file => `
        <label>
            <span>${file.fileName}:</span> 
            <input type="file" data-id="${file.id}" data-filename="${file.fileName}" accept="${file.type}">
        </label>
    `).join('');
    elements.loadConfigModal.classList.remove('hidden');

    elements.loadConfigFiles.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', (e) => {
            const file = e.target.files[0];
            const originalFilename = e.target.dataset.filename;
            if (file) {
                state.fileCache.set(originalFilename, file);
                e.target.previousElementSibling.textContent = `${originalFilename} (Đã chọn: ${file.name})`;
                e.target.parentElement.style.color = '#28a745';
            }
        });
    });
}

export async function confirmLoadConfig() {
    if (!state.pendingConfig) return;
    try {
        if (state.pendingConfig.mainAudio && !state.fileCache.has(state.pendingConfig.mainAudio.fileName)) {
            return createToast(`Vui lòng chọn file cho: ${state.pendingConfig.mainAudio.fileName}`, 'error');
        }
        for (const layer of state.pendingConfig.layers) {
            if (layer.content && typeof layer.content === 'object' && !state.fileCache.has(layer.content.fileName)) {
                return createToast(`Vui lòng chọn file cho: ${layer.content.fileName}`, 'error');
            }
            if (layer.depthMap && typeof layer.depthMap === 'object' && !state.fileCache.has(layer.depthMap.fileName)) {
                return createToast(`Vui lòng chọn file cho depth map: ${layer.depthMap.fileName}`, 'error');
            }
        }
        for (const sfx of state.pendingConfig.sfx) {
            if (!state.fileCache.has(sfx.fileName)) {
                return createToast(`Vui lòng chọn file cho: ${sfx.fileName}`, 'error');
            }
        }

        resetTemplate();

        state.template = {
            ...state.pendingConfig,
            layers: state.pendingConfig.layers.map(layer => ({
                ...layer,
                content: typeof layer.content === 'object' ? layer.content.fileName : layer.content,
                depthMap: typeof layer.depthMap === 'object' ? layer.depthMap.fileName : layer.depthMap,
                animationState: { in: false, out: false, loop: false },
                unit: layer.unit || (layer.isBackground ? '%' : 'px'),
                opacity: layer.opacity || 1,
                scale: layer.scale || 1,
                rotation: layer.rotation || 0,
                animations: {
                    in: layer.animations?.in || { type: 'none', duration: 0.5 },
                    out: layer.animations?.out || { type: 'none', duration: 0.5 },
                    loop: layer.animations?.loop || { type: 'kenBurns', duration: 10 }
                },
                style: {
                    filterBlur: 0,
                    backgroundOpacity: 0,
                    borderWidth: 0,
                    borderColor: '#000000',
                    borderStyle: 'solid',
                    shadowX: 0,
                    shadowY: 0,
                    shadowBlur: 0,
                    shadowColor: '#000000',
                    ...layer.style,
                },
                keyframes: layer.keyframes || {},
                appliedCssPresets: layer.appliedCssPresets || []
            })),
            sfx: state.pendingConfig.sfx.map(sfx => ({ ...sfx, played: false })),
            mainAudio: state.pendingConfig.mainAudio ? state.pendingConfig.mainAudio.fileName : null
        };

        state.cssPresets = { ...state.pendingConfig.cssPresets || {} };

        if (state.template.mainAudio) {
            const file = state.fileCache.get(state.template.mainAudio);
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const arrayBuffer = await file.arrayBuffer();
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            state.template.duration = audioBuffer.duration;
            elements.timelineSlider.max = state.template.duration;
            state.mainAudio = new Audio(URL.createObjectURL(file));
            elements.mainEditorControls.classList.remove('disabled');
            elements.exportControls.classList.remove('disabled');
        } else {
            state.template.duration = 0;
            state.mainAudio = null;
            elements.mainEditorControls.classList.add('disabled');
            elements.exportControls.classList.add('disabled');
        }

        state.currentTime = 0;
        state.activeElementId = null;
        state.pendingConfig = null;
        elements.loadConfigModal.classList.add('hidden');
        
        renderAll();
        updateTimelineDisplay();
        createToast('Tải cấu hình thành công!', 'success');
    } catch (err) {
        createToast('Lỗi nghiêm trọng khi tải cấu hình. Xem console để biết chi tiết.', 'error');
        console.error(err);
    }
}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                import { state, elements, ffmpeg, setFfmpeg, createFFmpeg } from './state.js';
import { resizePreview, createToast } from './utils.js';
import { renderAll } from './rendering.js';
import { selectElement, saveCustomCss } from './ui.js';
import { togglePlayback, seek, updateTimelineDisplay } from './playback.js';
import { 
    handleAudioUpload, addTextLayer, addBoxLayer, 
    handleMediaUpload, handleSfxUpload 
} from './handlers.js';
import { saveConfiguration, handleLoadConfig, confirmLoadConfig } from './config.js';
import { exportVideo } from './export.js';

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
    window.addEventListener('resize', resizePreview);
}

async function loadFFmpeg() {
    try {
        const ffmpegInstance = createFFmpeg({
            log: true,
            progress: (p) => {
                if (elements.exportOverlay.classList.contains('hidden')) return;
                const progress = Math.min(Math.max(p.ratio, 0), 1);
                elements.exportLog.textContent = `FFmpeg: ${p.ratio ? (progress * 100).toFixed(1) + '%' : '...loading core'}`;
                // This progress is for FFmpeg internal tasks, not the whole export process
            }
        });
        createToast('Đang tải thư viện FFmpeg (~30MB)...');
        await ffmpegInstance.load();
        setFfmpeg(ffmpegInstance);
        createToast('FFmpeg đã sẵn sàng!', 'success');
    } catch (e) {
        console.error("FFmpeg loading error:", e);
        createToast('Không thể tải FFmpeg! Hãy chắc chắn bạn đang dùng Live Server.', 'error');
    }
}

function init() {
    attachEventListeners();
    resizePreview();
    loadFFmpeg();
    renderAll();
    updateTimelineDisplay();
    cr