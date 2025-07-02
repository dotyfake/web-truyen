       downloadAnchorNode.remove();
        createToast('Đã lưu cấu hình!', 'success');
    }
    

    async function handleLoadConfig(event) {
        const file = event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = async (e) => {
            try {
                pendingConfig = JSON.parse(e.target.result);
                if (!pendingConfig.layers.find(l => l.isBackground)) {
                    pendingConfig.layers.unshift(initialBackgroundLayer);
                }
                const filesNeeded = [];
                if (pendingConfig.mainAudio) {
                    filesNeeded.push({ id: 'main_audio', fileName: pendingConfig.mainAudio.fileName, type: 'audio/mpeg' });
                }
                pendingConfig.layers.forEach(layer => {
                    if (layer.content && typeof layer.content === 'object') {
                        filesNeeded.push({ id: layer.id, fileName: layer.content.fileName, type: layer.content.type === 'image' ? 'image/*' : 'video/*' });
                    }
                });
                pendingConfig.sfx.forEach(sfx => {
                    filesNeeded.push({ id: sfx.id, fileName: sfx.fileName, type: 'audio/*' });
                });
                showLoadConfigModal(filesNeeded);
            } catch (err) {
                createToast('File cấu hình không hợp lệ!', 'error');
                console.error(err);
            }
        };
        reader.readAsText(file);
    }

    function showLoadConfigModal(filesNeeded) {
        elements.loadConfigFiles.innerHTML = filesNeeded.map(file => `
            <label>${file.fileName}: <input type="file" data-id="${file.id}" accept="${file.type}"></label>
        `).join('');
        elements.loadConfigModal.classList.remove('hidden');
        elements.loadConfigFiles.querySelectorAll('input[type="file"]').forEach(input => {
            input.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    fileCache.set(e.target.dataset.id === 'main_audio' ? 'main_audio.mp3' : file.fileName, file);
                }
            });
        });
    }

    async function confirmLoadConfig() {
        if (!pendingConfig) return;
        try {
            if (pendingConfig.mainAudio && !fileCache.has('main_audio.mp3')) {
                createToast('Vui lòng chọn file âm thanh nền!', 'error');
                return;
            }
            pendingConfig.layers.forEach(layer => {
                if (layer.content && typeof layer.content === 'object' && !fileCache.has(layer.content.fileName)) {
                    createToast(`Vui lòng chọn file cho ${layer.content.fileName}!`, 'error');
                    throw new Error('Missing file');
                }
            });
            pendingConfig.sfx.forEach(sfx => {
                if (!fileCache.has(sfx.fileName)) {
                    createToast(`Vui lòng chọn file cho ${sfx.fileName}!`, 'error');
                    throw new Error('Missing file');
                }
            });

            template = {
                ...pendingConfig,
                layers: pendingConfig.layers.map(layer => ({
                    ...layer,
                    content: typeof layer.content === 'object' ? layer.content.fileName : layer.content,
                    animationState: layer.animationState || { in: false, out: false, loop: false },
                    unit: layer.unit || (layer.isBackground ? '%' : 'px'),
                    animations: {
                        in: layer.animations?.in || { type: 'none', duration: 0.5 },
                        out: layer.animations?.out || { type: 'none', duration: 0.5 },
                        loop: layer.animations?.loop || { type: 'kenBurns', duration: 10 }
                    },
                    style: {
                        ...layer.style,
                        backgroundOpacity: layer.style?.backgroundOpacity || 0,
                        borderWidth: layer.style?.borderWidth || 0,
                        borderColor: layer.style?.borderColor || '#000000',
                        shadowX: layer.style?.shadowX || 0,
                        shadowY: layer.style?.shadowY || 0,
                        shadowBlur: layer.style?.shadowBlur || 0,
                        shadowColor: layer.style?.shadowColor || '#000000'
                    }
                })),
                sfx: pendingConfig.sfx.map(sfx => ({ ...sfx, played: false })),
                mainAudio: pendingConfig.mainAudio ? 'main_audio.mp3' : null
            };

            if (template.mainAudio) {
                const file = fileCache.get('main_audio.mp3');
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const arrayBuffer = await file.arrayBuffer();
                const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
                template.duration = audioBuffer.duration;
                elements.timelineSlider.max = template.duration;
                mainAudio = new Audio(URL.createObjectURL(file));
            } else {
                template.duration = 0;
                elements.mainEditorControls.classList.add('disabled');
                elements.exportControls.classList.add('disabled');
            }

            currentTime = 0;
            activeElementId = null;
            elements.loadConfigModal.classList.add('hidden');
            renderAll();
            createToast('Tải cấu hình thành công!', 'success');
        } catch (err) {
            console.error(err);
        }
    }

    function updateElementProperty(id, property, value, inputElement = null) {
        const target = getElementData(id);
        if (!target) return;
        const keys = property.split('.');
        let obj = target;
        for (let i = 0; i < keys.length - 1; i++) {
            if (!obj[keys[i]]) obj[keys[i]] = {};
            obj = obj[keys[i]];
        }
        const numericProps = ['x', 'y', 'width', 'height', 'fontSize', 'startTime', 'endTime', 'duration', 'angle', 'filterBlur', 'backgroundOpacity', 'borderWidth', 'shadowX', 'shadowY', 'shadowBlur'];
        if (numericProps.includes(keys[keys.length - 1])) {
            value = parseFloat(value) || 0;
        }
        obj[keys[keys.length - 1]] = value;

        if (inputElement) {
            inputElement.value = value;
        }

        if (id === 'background' && property === 'type') {
            if (value === 'color') {
                target.content = '#1a1a1a';
                target.gradient = { color1: '#0000ff', color2: '#ff0000', angle: 45 };
                target.content = '';
            } else if (value === 'gradient') {
                target.content = '';
                target.gradient = target.gradient || { color1: '#0000ff', color2: '#ff0000', angle: 45 };
            } else if (value === 'image' || value === 'video') {
                target.content = '';
                target.gradient = { color1: '#0000ff', color2: '#ff0000', angle: 45 };
            }
            renderPropertiesPanel();
        }

        renderFrameAtTime(currentTime);
        renderLayerList();
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
            item.textContent = `[${layer.type}] ${layer.type === 'text' ? (layer.content || '').substring(0, 20) + '...' : layer.content || 'Layer ' + layer.id.slice(-4)}`;
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
        elements.settingsTitle.textContent = `Thuộc tính của: ${elementData.isBackground ? 'Nền' : (elementData.content || elementData.type)}`;
        let html = '';

        if (elementData.isBackground) {
            html += createSettingsGroup('Cấu hình Nền', `
                <label>Loại: 
                    <select data-prop="type">
                        <option value="color" ${elementData.type === 'color' ? 'selected' : ''}>Màu</option>
                        <option value="gradient" ${elementData.type === 'gradient' ? 'selected' : ''}>Gradient</option>
                        <option value="image" ${elementData.type === 'image' ? 'selected' : ''}>Ảnh</option>
                        <option value="video" ${elementData.type === 'video' ? 'selected' : ''}>Video</option>
                    </select>
                </label>
                ${elementData.type === 'color' ? `<label>Màu: <input type="color" data-prop="content" value="${elementData.content || '#1a1a1a'}"></label>` : ''}
                ${elementData.type === 'gradient' ? `
                    <label>Màu 1: <input type="color" data-prop="gradient.color1" value="${elementData.gradient.color1 || '#0000ff'}"></label>
                    <label>Màu 2: <input type="color" data-prop="gradient.color2" value="${elementData.gradient.color2 || '#ff0000'}"></label>
                    <label>Góc (°): <input type="number" data-prop="gradient.angle" value="${elementData.gradient.angle || 45}"></label>
                ` : ''}
                ${elementData.type === 'image' || elementData.type === 'video' ? `
                    <label>File: <input type="file" class="bg-file-input" accept="${elementData.type}/*"></label>
                    <span>${elementData.content || 'Chưa chọn file'}</span>
                ` : ''}
            `);
            html += createSettingsGroup('Hiệu ứng Lọc', `
                <label>Độ mờ (px): <input type="number" step="0.1" data-prop="style.filterBlur" value="${elementData.style.filterBlur || 0}"></label>
            `);
            html += createSettingsGroup('Hiệu ứng', `
                <h4>Lặp</h4>
                <label>Loại: <select data-prop="animations.loop.type">${getAnimOptions(elementData.animations.loop.type, true)}</select></label>
                <label>Thời lượng: <input type="number" step="0.1" data-prop="animations.loop.duration" value="${elementData.animations.loop.duration}"></label>
            `);
            html += createSettingsGroup('Nâng cao', `<button id="btn-custom-css">CSS tùy chỉnh</button>`);
        } else if (activeElementId.startsWith('layer_')) {
            html += createSettingsGroup('Vị trí & Kích thước', `
                <label>Đơn vị: 
                    <select data-prop="unit">
                        <option value="%" ${elementData.unit === '%' ? 'selected' : ''}>%</option>
                        <option value="px" ${elementData.unit === 'px' ? 'selected' : ''}>px</option>
                    </select>
                </label>
                <label>X (${elementData.unit}): <input type="number" data-prop="x" value="${elementData.x}"></label>
                <label>Y (${elementData.unit}): <input type="number" data-prop="y" value="${elementData.y}"></label>
                <label>Rộng (${elementData.unit}): <input type="number" data-prop="width" value="${elementData.width}"></label>
                <label>Cao (${elementData.unit}): <input type="number" data-prop="height" value="${elementData.height}"></label>
            `);
            html += createSettingsGroup('Thời gian (giây)', `
                <label>Bắt đầu: <input type="number" step="0.1" data-prop="startTime" value="${elementData.startTime}"></label>
                <label>Kết thúc: <input type="number" step="0.1" data-prop="endTime" value="${elementData.endTime}"></label>
            `);
            if (elementData.type === 'text') {
                html += createSettingsGroup('Thuộc tính Văn bản', `
                    <label>Font: <input type="text" data-prop="style.fontFamily" value="${elementData.style.fontFamily}"></label>
                    <label>Cỡ chữ (${elementData.unit}): <input type="number" data-prop="style.fontSize" value="${elementData.style.fontSize}"></label>
                    <label>Độ mờ (px): <input type="number" step="0.1" data-prop="style.filterBlur" value="${elementData.style.filterBlur || 0}"></label>
                    <label>Màu chữ: <input type="color" data-prop="style.color" value="${elementData.style.color}"></label>
                    <label>Màu nền: <input type="color" data-prop="style.backgroundColor" value="${elementData.style.backgroundColor}"></label>
                    <label>Độ mờ nền: <input type="number" step="0.01" min="0" max="1" data-prop="style.backgroundOpacity" value="${elementData.style.backgroundOpacity || 0}"></label>
                    <label>Căn chỉnh: 
                        <select data-prop="style.textAlign">
                            <option value="left" ${elementData.style.textAlign === 'left' ? 'selected' : ''}>Trái</option>
                            <option value="center" ${elementData.style.textAlign === 'center' ? 'selected' : ''}>Giữa</option>
                            <option value="right" ${elementData.style.textAlign === 'right' ? 'selected' : ''}>Phải</option>
                        </select>
                    </label>
                    <label>Độ dày viền (px): <input type="number" data-prop="style.borderWidth" value="${elementData.style.borderWidth || 0}"></label>
                    <label>Màu viền: <input type="color" data-prop="style.borderColor" value="${elementData.style.borderColor || '#000000'}"></label>
                    <label>Bóng X (px): <input type="number" data-prop="style.shadowX" value="${elementData.style.shadowX || 0}"></label>
                    <label>Bóng Y (px): <input type="number" data-prop="style.shadowY" value="${elementData.style.shadowY || 0}"></label>
                    <label>Độ mờ bóng (px): <input type="number" data-prop="style.shadowBlur" value="${elementData.style.shadowBlur || 0}"></label>
                    <label>Màu bóng: <input type="color" data-prop="style.shadowColor" value="${elementData.style.shadowColor || '#000000'}"></label>
                `);
            } else if (elementData.type === 'box') {
                html += createSettingsGroup('Thuộc tính Box', `
                    <label>Màu nền: <input type="color" data-prop="style.backgroundColor" value="${elementData.style.backgroundColor}"></label>
                    <label>Độ mờ (px): <input type="number" step="0.1" data-prop="style.filterBlur" value="${elementData.style.filterBlur || 0}"></label>
                `);
            } else {
                html += createSettingsGroup('Hiệu ứng Lọc', `
                    <label>Độ mờ (px): <input type="number" step="0.1" data-prop="style.filterBlur" value="${elementData.style.filterBlur || 0}"></label>
                `);
            }
            html += createSettingsGroup('Hiệu ứng', `
                <h4>Vào</h4>
                <label>Loại: <select data-prop="animations.in.type">${getAnimOptions(elementData.animations.in.type)}</select></label>
                <label>Thời lượng: <input type="number" step="0.1" data-prop="animations.in.duration" value="${elementData.animations.in.duration}"></label>
                <h4>Ra</h4>
                <label>Loại: <select data-prop="animations.out.type">${getAnimOptions(elementData.animations.out.type)}</select></label>
                <label>Thời lượng: <input type="number" step="0.1" data-prop="animations.out.duration" value="${elementData.animations.out.duration}"></label>
                <h4>Lặp</h4>
                <label>Loại: <select data-prop="animations.loop.type">${getAnimOptions(elementData.animations.loop.type, true)}</select></label>
                <label>Thời lượng: <input type="number" step="0.1" data-prop="animations.loop.duration" value="${elementData.animations.loop.duration}"></label>
            `);
            html += createSettingsGroup('Nâng cao', `
                <button id="btn-custom-css">CSS tùy chỉnh</button>
                <button id="btn-delete-layer" class="danger">Xóa Lớp</button>
            `);
        } else if (activeElementId.startsWith('sfx_')) {
            html += createSettingsGroup('Thuộc tính SFX', `
                <label>Bắt đầu: <input type="number" step="0.1" data-prop="startTime" value="${elementData.startTime}"></label>
                <button id="btn-delete-sfx" class="danger">Xóa SFX</button>
            `);
        }
        elements.settingsContent.innerHTML = html;
        elements.settingsContent.addEventListener('input', (e) => {
            const prop = e.target.dataset.prop;
            if (prop) {
                const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
                updateElementProperty(activeElementId, prop, value, e.target);
            }
        });
        const bgFileInput = elements.settingsContent.querySelector('.bg-file-input');
        if (bgFileInput) bgFileInput.addEventListener('change', handleBgFileChange);
        if (document.getElementById('btn-custom-css')) document.getElementById('btn-custom-css').addEventListener('click', openCssEditor);
        if (document.getElementById('btn-delete-layer')) document.getElementById('btn-delete-layer').addEventListener('click', deleteActiveLayer);
        if (document.getElementById('btn-delete-sfx')) document.getElementById('btn-delete-sfx').addEventListener('click', deleteActiveSfx);
    }

    async function handleBgFileChange(event) {
        const file = event.target.files[0];
        if (!file) return;
        const elementData = getElementData('background');
        const fileName = `bg_${elementData.type}_${Date.now()}_${file.name}`;
        fileCache.set(fileName, file);
        updateElementProperty('background', 'content', fileName);
        renderAll();
    }

    function selectElement(id) {
        activeElementId = id;
        renderLayerList();
        renderPropertiesPanel();
        const el = document.getElementById(id);
        if (el && !getElementData(id)?.isBackground) el.focus();
    }

    function deleteActiveLayer() {
        if (!confirm('Bạn chắc chắn muốn xóa lớp này?')) return;
        template.layers = template.layers.filter(l => l.id !== activeElementId);
        activeElementId = null;
        renderAll();
    }

    function deleteActiveSfx() {
        if (!confirm('Bạn chắc chắn muốn xóa SFX này?')) return;
        template.sfx = template.sfx.filter(s => s.id !== activeElementId);
        activeElementId = null;
        renderAll();
    }

    function openCssEditor() {
        const layer = getElementData(activeElementId);
        if (!layer) return;
        elements.cssEditorTextarea.value = layer.customCss || '';
        elements.cssEditorOverlay.classList.remove('hidden');
    }

    function saveCustomCss() {
        const layer = getElementData(activeElementId);
        if (!layer) return;
        updateElementProperty(activeElementId, 'customCss', elements.cssEditorTextarea.value);
        elements.cssEditorOverlay.classList.add('hidden');
    }

    function togglePlayback() {
        if (!mainAudio || !mainAudio.src) {
            return createToast('Hãy thêm âm thanh nền trước!', 'error');
        }
        isPlaying ? pause() : play();
    }

    function play() {
        isPlaying = true;
        elements.btnPlayPause.textContent = '❚❚';
        mainAudio.play().catch(() => {});
        template.layers.forEach(layer => {
            layer.animationState = { in: false, out: false, loop: false };
            const el = document.getElementById(layer.id);
            if (el) el.style.animation = 'none';
            if (layer.type === 'video') {
                const videoEl = el ? el.querySelector('video') : null;
                if (videoEl && !videoEl.loop) {
                    videoEl.currentTime = Math.max(0, currentTime - layer.startTime);
                    videoEl.play().catch(() => {});
                }
            }
        });
        animationFrameId = requestAnimationFrame(animationLoop);
    }

    function pause() {
        isPlaying = false;
        elements.btnPlayPause.textContent = '▶️';
        if (mainAudio) mainAudio.pause();
        template.layers.filter(l => l.type === 'video').forEach(l => {
            const el = document.getElementById(l.id);
            const videoEl = el ? el.querySelector('video') : null;
            if (videoEl && !videoEl.paused) videoEl.pause();
        });
        cancelAnimationFrame(animationFrameId);
    }

    function animationLoop(timestamp) {
        if (!isPlaying) return;
        currentTime = mainAudio.currentTime;
        if (currentTime >= template.duration) {
            currentTime = template.duration;
            pause();
            seek(0);
        }
        elements.timelineSlider.value = currentTime;
        updateTimelineDisplay();
        renderFrameAtTime(currentTime);
        animationFrameId = requestAnimationFrame(animationLoop);
    }

    function seek(time, updateAudio = true) {
        if (!mainAudio) return;
        const wasPlaying = isPlaying;
        if (wasPlaying) pause();
        currentTime = Math.max(0, Math.min(time, template.duration));
        if (updateAudio) {
            mainAudio.currentTime = currentTime;
        }
        template.layers.forEach(layer => {
            layer.animationState = { in: false, out: false, loop: false };
            const el = document.getElementById(layer.id);
            if (el) el.style.animation = 'none';
            if (layer.type === 'video') {
                const videoEl = el ? el.querySelector('video') : null;
                if (videoEl && !videoEl.loop) {
                    videoEl.currentTime = Math.max(0, currentTime - layer.startTime);
                }
            }
        });
        elements.timelineSlider.value = currentTime;
        updateTimelineDisplay();
        renderFrameAtTime(currentTime);
        if (wasPlaying) play();
    }

    function updateTimelineDisplay() {
        const formatTime = (sec) => {
            const minutes = Math.floor(sec / 60);
            const seconds = Math.floor(sec % 60);
            return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        };
        elements.timeDisplay.textContent = `${formatTime(currentTime)} / ${formatTime(template.duration)}`;
    }

    function setupInteraction() {
        interact('.layer').draggable({
            listeners: {
                start(event) {
                    selectElement(event.target.id);
                },
                move(event) {
                    const target = event.target;
                    const layer = getElementData(target.id);
                    if (!layer) return;
                    const rect = elements.previewArea.getBoundingClientRect();
                    const x = (parseFloat(target.style.left) || 0) + (event.dx / rect.width * 100);
                    const y = (parseFloat(target.style.top) || 0) + (event.dy / rect.height * 100);
                    layer.x = layer.unit === 'px' ? x * rect.width / 100 : x;
                    layer.y = layer.unit === 'px' ? y * rect.height / 100 : y;
                    target.style.left = `${x}%`;
                    target.style.top = `${y}%`;
                },
                end(event) {
                    renderPropertiesPanel();
                }
            },
            modifiers: [
                interact.modifiers.restrictRect({
                    restriction: 'parent'
                })
            ]
        }).styleCursor(true);
    }

    async function exportVideo() {
        if (!ffmpeg || !ffmpeg.isLoaded()) {
            return createToast('FFmpeg chưa sẵn sàng!', 'error');
        }
        if (template.duration === 0) {
            return createToast('Vui lòng thêm âm thanh nền!', 'error');
        }
        pause();
        showExportOverlay(true);
        try {
            elements.exportStatusTitle.textContent = 'Bắt đầu...';
            elements.exportStatusMessage.textContent = 'Giai đoạn 1/2: Chụp khung hình...';
            const originalScale = elements.previewArea.style.transform;
            const scale = PREVIEW_CAPTURE_WIDTH / elements.previewArea.offsetWidth;
            elements.previewArea.style.transform = `scale(${scale})`;
            const totalFrames = Math.floor(template.duration * FPS);
            for (let i = 0; i < totalFrames; i++) {
                const time = i / FPS;
                renderFrameAtTime(time);
                await new Promise(resolve => setTimeout(resolve, 10));
                const canvas = await html2canvas(elements.previewArea, {
                    scale: EXPORT_WIDTH / PREVIEW_CAPTURE_WIDTH,
                    width: EXPORT_WIDTH,
                    height: EXPORT_HEIGHT,
                    useCORS: true,
                    logging: false
                });
                const frameData = await new Promise(res => canvas.toBlob(res, 'image/jpeg', 0.9));
                ffmpeg.FS('writeFile', `frame${i.toString().padStart(4, '0')}.jpg`, await fetchFile(frameData));
                updateExportProgress((i + 1) / totalFrames);
            }
            elements.previewArea.style.transform = originalScale;
            elements.exportStatusMessage.textContent = 'Giai đoạn 2/2: Ghép video và âm thanh...';
            elements.exportLog.textContent = 'Khởi tạo FFmpeg...';
            updateExportProgress(0);
            const mainAudioFile = fileCache.get('main_audio.mp3');
            ffmpeg.FS('writeFile', 'main_audio.mp3', await fetchFile(mainAudioFile));
            const sfxFiles = [];
            for (const sfx of template.sfx) {
                const sfxFile = fileCache.get(sfx.fileName);
                if (sfxFile) {
                    ffmpeg.FS('writeFile', sfx.fileName, await fetchFile(sfxFile));
                    sfxFiles.push(sfx);
                }
            }
            const audioInputs = ['-i', 'main_audio.mp3'];
            sfxFiles.forEach(sfx => audioInputs.push('-i', sfx.fileName));
            let filterComplex = '';
            if (sfxFiles.length > 0) {
                let filter = `[0:a]volume=1.0[aout0];`;
                sfxFiles.forEach((sfx, index) => {
                    const delayMs = sfx.startTime * 1000;
                    filter += `[${index + 1}:a]adelay=${delayMs}|${delayMs}[sfx${index}];`;
                });
                const mixInputs = sfxFiles.map((s, i) => `[sfx${i}]`).join('');
                filter += `[aout0]${mixInputs}amix=inputs=${sfxFiles.length + 1}[aout]`;
                filterComplex = filter;
            }
            const command = [
                '-framerate', `${FPS}`,
                '-i', 'frame%04d.jpg',
                ...audioInputs
            ];
            if (filterComplex) {
                command.push('-filter_complex', filterComplex, '-map', '0:v:0', '-map', '[aout]');
            } else {
                command.push('-map', '0:v:0', '-map', '1:a:0');
            }
            command.push('-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-shortest', '-y', 'output.mp4');
            await ffmpeg.run(...command);
            const data = ffmpeg.FS('readFile', 'output.mp4');
            const videoBlob = new Blob([data.buffer], { type: 'video/mp4' });
            const downloadLink = document.createElement('a');
            downloadLink.href = URL.createObjectURL(videoBlob);
            downloadLink.download = `my-video-${Date.now()}.mp4`;
            document.body.appendChild(downloadLink);
            downloadLink.click();
            downloadLink.remove();
            createToast('Xuất video thành công!', 'success');
        } catch (e) {
            console.error("Export error:", e);
            createToast('Lỗi khi xuất video!', 'error');
        } finally {
            showExportOverlay(false);
            for (let i = 0; i < Math.floor(template.duration * FPS); i++) {
                try { ffmpeg.FS('unlink', `frame${i.toString().padStart(4, '0')}.jpg`); } catch (e) {}
            }
            try { ffmpeg.FS('unlink', 'main_audio.mp3'); } catch (e) {}
            template.sfx.forEach(sfx => {
                try { ffmpeg.FS('unlink', sfx.fileName); } catch (e) {}
            });
            try { ffmpeg.FS('unlink', 'output.mp4'); } catch (e) {}
        }
    }

    // Initialize the application
    init();
});                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  {
  "name": "gar",
  "version": "1.0.4",
  "description": "The lightweight Node arguments parser",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Tested before deployment.\" && exit 0",
    "test-dev": "npm install && node test.js",
    "prepublishOnly": "npm run test-dev"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/ethanent/gar.git"
  },
  "keywords": [
    "argument",
    "args",
    "argv",
    "parse",
    "cli",
    "command-line",
    "parser",
    "command",
    "lightweight"
  ],
  "author": "Ethan Davis",
  "license": "MIT",
  "bugs": {
    "url": "https://github.com/ethanent/gar/issues"
  },
  "homepage": "https://github.com/ethanent/gar#readme",
  "devDependencies": {
    "whew": "^1.1.3"
  },
  "files": [
    "index.js",
    "LICENSE"
  ]
}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 