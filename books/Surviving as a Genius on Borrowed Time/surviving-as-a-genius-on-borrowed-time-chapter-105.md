import { state, elements, getElementData, updateElementProperty, addKeyframe, addCssPreset, toggleCssPreset } from './state.js';
import { getAnimOptions, createSettingsGroup, createToast } from './utils.js';
import { renderAll, renderFrameAtTime } from './rendering.js';
import { handleBgFileChange, deleteActiveLayer, deleteActiveSfx, handleDepthMapUpload } from './handlers.js';

export function renderLayerList() {
    elements.layerList.innerHTML = '';
    
    const bgLayerData = state.template.layers.find(l => l.isBackground);
    if (bgLayerData) {
        const bgItem = document.createElement('li');
        bgItem.textContent = '🎨 Nền (Background)';
        bgItem.dataset.id = 'background';
        if (state.activeElementId === 'background') bgItem.classList.add('selected');
        bgItem.addEventListener('click', () => selectElement('background'));
        elements.layerList.appendChild(bgItem);
    }

    state.template.layers.filter(l => !l.isBackground).forEach(layer => {
        const item = document.createElement('li');
        const displayName = layer.type === 'text' ? (layer.content || '').substring(0, 20) + '...' : (layer.content || `Layer ${layer.id.slice(-4)}`);
        item.textContent = `[${layer.type}] ${displayName}`;
        item.dataset.id = layer.id;
        if (state.activeElementId === layer.id) item.classList.add('selected');
        item.addEventListener('click', () => selectElement(layer.id));
        elements.layerList.appendChild(item);
    });

    state.template.sfx.forEach(sfx => {
        const item = document.createElement('li');
        item.textContent = `🔊 [SFX] ${sfx.name}`;
        item.dataset.id = sfx.id;
        if (state.activeElementId === sfx.id) item.classList.add('selected');
        item.addEventListener('click', () => selectElement(sfx.id));
        elements.layerList.appendChild(item);
    });
}

export function selectElement(id) {
    state.activeElementId = id;
    renderLayerList();
    renderPropertiesPanel();
    const el = document.getElementById(id);
    if (el && !getElementData(id)?.isBackground) {
        el.focus();
    }
}

export function openCssEditor() {
    const layer = getElementData(state.activeElementId);
    if (!layer) return;
    elements.cssEditorTextarea.value = layer.customCss || '';
    elements.cssEditorOverlay.classList.remove('hidden');
    elements.cssEditorTextarea.focus();
}

export function saveCustomCss() {
    const layer = getElementData(state.activeElementId);
    if (!layer) return;
    const css = elements.cssEditorTextarea.value.trim();
    const presetName = prompt('Nhập tên cho preset CSS (để trống để chỉ lưu cho layer):', '');
    if (presetName) {
        const presetId = addCssPreset(presetName, css);
        toggleCssPreset(state.activeElementId, presetId);
    } else {
        updateElementProperty(state.activeElementId, 'customCss', css);
    }
    elements.cssEditorOverlay.classList.add('hidden');
    renderPropertiesPanel();
    renderFrameAtTime(state.currentTime);
}

export function renderPropertiesPanel() {
    if (!state.activeElementId) {
        elements.settingsBox.classList.add('hidden');
        return;
    }
    
    const elementData = getElementData(state.activeElementId);
    if (!elementData) {
        elements.settingsBox.classList.add('hidden');
        return;
    }
    
    elements.settingsBox.classList.remove('hidden');
    const name = elementData.isBackground ? 'Nền' : (elementData.name || elementData.content?.substring(0, 20) || elementData.type);
    elements.settingsTitle.textContent = `Thuộc tính của: ${name}`;
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
            <label>Thời lượng (s): <input type="number" step="0.1" data-prop="animations.loop.duration" value="${elementData.animations.loop.duration || 10}"></label>
        `);
        html += createSettingsGroup('Nâng cao', `<button id="btn-custom-css">CSS tùy chỉnh</button>`);
    } else if (state.activeElementId.startsWith('layer_')) {
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
            <label>Độ mờ: <input type="number" step="0.01" min="0" max="1" data-prop="opacity" value="${elementData.opacity || 1}"></label>
            <label>Tỷ lệ: <input type="number" step="0.1" min="0.1" data-prop="scale" value="${elementData.scale || 1}"></label>
            <label>Xoay (°): <input type="number" data-prop="rotation" value="${elementData.rotation || 0}"></label>
        `);
        html += createSettingsGroup('Thời gian (giây)', `
            <label>Bắt đầu: <input type="number" step="0.1" min="0" max="${state.template.duration}" data-prop="startTime" value="${elementData.startTime}"></label>
            <label>Kết thúc: <input type="number" step="0.1" min="0" max="${state.template.duration}" data-prop="endTime" value="${elementData.endTime}"></label>
        `);
        if (elementData.type === 'text') {
            html += createSettingsGroup('Thuộc tính Văn bản', `
                <label style="flex-direction: column; align-items: flex-start;">Nội dung: <textarea data-prop="content" rows="3" style="width: 100%; margin-top: 5px;">${elementData.content}</textarea></label>
                <label>Font: <input type="text" data-prop="style.fontFamily" value="${elementData.style.fontFamily}"></label>
                <label>Cỡ chữ (px): <input type="number" data-prop="style.fontSize" value="${elementData.style.fontSize}"></label>
                <label>Màu chữ: <input type="color" data-prop="style.color" value="${elementData.style.color}"></label>
                <label>Căn chỉnh: 
                    <select data-prop="style.textAlign">
                        <option value="left" ${elementData.style.textAlign === 'left' ? 'selected' : ''}>Trái</option>
                        <option value="center" ${elementData.style.textAlign === 'center' ? 'selected' : ''}>Giữa</option>
                        <option value="right" ${elementData.style.textAlign === 'right' ? 'selected' : ''}>Phải</option>
                    </select>
                </label>
                <hr style="border-color: var(--border-color); margin: 10px 0;">
                <label>Màu nền: <input type="color" data-prop="style.backgroundColor" value="${elementData.style.backgroundColor}"></label>
                <label>Độ mờ nền: <input type="number" step="0.01" min="0" max="1" data-prop="style.backgroundOpacity" value="${elementData.style.backgroundOpacity || 0}"></label>
                <hr style="border-color: var(--border-color); margin: 10px 0;">
                <label>Độ dày viền (px): <input type="number" data-prop="style.borderWidth" value="${elementData.style.borderWidth || 0}"></label>
                <label>Màu viền: <input type="color" data-prop="style.borderColor" value="${elementData.style.borderColor || '#000000'}"></label>
                <label>Kiểu viền: 
                    <select data-prop="style.borderStyle">
                        <option value="solid" ${elementData.style.borderStyle === 'solid' ? 'selected' : ''}>Liền</option>
                        <option value="dashed" ${elementData.style.borderStyle === 'dashed' ? 'selected' : ''}>Nét đứt</option>
                        <option value="dotted" ${elementData.style.borderStyle === 'dotted' ? 'selected' : ''}>Chấm</option>
                    </select>
                </label>
                <hr style="border-color: var(--border-color); margin: 10px 0;">
                <label>Bóng X (px): <input type="number" data-prop="style.shadowX" value="${elementData.style.shadowX || 0}"></label>
                <label>Bóng Y (px): <input type="number" data-prop="style.shadowY" value="${elementData.style.shadowY || 0}"></label>
                <label>Độ mờ bóng (px): <input type="number" data-prop="style.shadowBlur" value="${elementData.style.shadowBlur || 0}"></label>
                <label>Màu bóng: <input type="color" data-prop="style.shadowColor" value="${elementData.style.shadowColor || '#000000'}"></label>
            `);
        } else if (elementData.type === 'box') {
            html += createSettingsGroup('Thuộc tính Box', `
                <label>Màu nền: <input type="color" data-prop="style.backgroundColor" value="${elementData.style.backgroundColor}"></label>
            `);
        } else if (elementData.type === 'image') {
            html += createSettingsGroup('Thuộc tính Hình ảnh', `
                <label>Depth Map: <input type="file" class="depth-map-input" accept="image/*"></label>
                <span>${elementData.depthMap || 'Chưa chọn depth map'}</span>
            `);
        }
        
        html += createSettingsGroup('Keyframes', `
            <label>Thêm Keyframe tại thời gian (s): <input type="number" step="0.1" id="keyframe-time" value="${state.currentTime}"></label>
            <label>Thuộc tính:
                <select id="keyframe-property">
                    <option value="x">X</option>
                    <option value="y">Y</option>
                    <option value="width">Rộng</option>
                    <option value="height">Cao</option>
                    <option value="opacity">Độ mờ</option>
                    <option value="scale">Tỷ lệ</option>
                    <option value="rotation">Xoay</option>
                </select>
            </label>
            <label>Easing:
                <select id="keyframe-easing">
                    <option value="linear">Linear</option>
                    <option value="ease-in">Ease In</option>
                    <option value="ease-out">Ease Out</option>
                    <option value="ease-in-out">Ease In Out</option>
                </select>
            </label>
            <button id="btn-add-keyframe">Thêm Keyframe</button>
            <div id="keyframe-list"></div>
        `);

        html += createSettingsGroup('Hiệu ứng Lọc', `
            <label>Độ mờ (px): <input type="number" step="0.1" data-prop="style.filterBlur" value="${elementData.style.filterBlur || 0}"></label>
        `);

        html += createSettingsGroup('Hiệu ứng', `
            <h4>Vào</h4>
            <label>Loại: <select data-prop="animations.in.type">${getAnimOptions(elementData.animations.in.type)}</select></label>
            <label>Thời lượng (s): <input type="number" step="0.1" data-prop="animations.in.duration" value="${elementData.animations.in.duration}"></label>
            <h4>Ra</h4>
            <label>Loại: <select data-prop="animations.out.type">${getAnimOptions(elementData.animations.out.type)}</select></label>
            <label>Thời lượng (s): <input type="number" step="0.0" data-prop="animations.out.duration" value="${elementData.animations.out.duration}"></label>
            <h4>Lặp</h4>
            <label>Loại: <select data-prop="animations.loop.type">${getAnimOptions(elementData.animations.loop.type, true)}</select></label>
            <label>Thời lượng (s): <input type="number" step="0.1" data-prop="animations.loop.duration" value="${elementData.animations.loop.duration}"></label>
        `);

        html += createSettingsGroup('CSS Tùy chỉnh Đã Lưu', `
            <div id="css-preset-buttons" style="display: flex; flex-wrap: wrap; gap: 5px;">
                ${Object.entries(state.cssPresets).map(([presetId, preset]) => `
                    <button data-id="${presetId}" style="background-color: ${elementData.appliedCssPresets.includes(presetId) ? '#28a745' : '#444'}; padding: 5px 10px; border: none; border-radius: 3px; cursor: pointer;">
                        ${preset.name}
                    </button>
                `).join('\n')}
            </div>
        `);

        html += createSettingsGroup('Nâng cao', `
            <button id="btn-custom-css">CSS tùy chỉnh</button>
            <button id="btn-delete" class="danger">Xóa Lớp</button>
        `);
    } else if (state.activeElementId.startsWith('sfx_')) {
        html += createSettingsGroup('Thuộc tính SFX', `
            <label>Tên: <input type="text" value="${elementData.name}" disabled></label>
            <label>Bắt đầu (s): <input type="number" step="0.1" min="0" max="${state.template.duration}" data-prop="startTime" value="${elementData.startTime}"></label>
            <button id="btn-delete" class="danger">Xóa SFX</button>
        `);
    }

    elements.settingsContent.innerHTML = html;
    
    const bgFileInput = elements.settingsContent.querySelector('.bg-file-input');
    if (bgFileInput) bgFileInput.addEventListener('change', handleBgFileChange);
    
    const depthMapInput = elements.settingsContent.querySelector('.depth-map-input');
    if (depthMapInput) depthMapInput.addEventListener('change', handleDepthMapUpload);

    if (document.getElementById('btn-custom-css')) document.getElementById('btn-custom-css').addEventListener('click', openCssEditor);
    if (document.getElementById('btn-delete')) {
        document.getElementById('btn-delete').addEventListener('click', () => {
            if (state.activeElementId.startsWith('sfx_')) deleteActiveSfx();
            else deleteActiveLayer();
        });
    }
    if (document.getElementById('btn-add-keyframe')) {
        document.getElementById('btn-add-keyframe').addEventListener('click', () => {
            const time = parseFloat(document.getElementById('keyframe-time').value) || state.currentTime;
            const property = document.getElementById('keyframe-property').value;
            const easing = document.getElementById('keyframe-easing').value;
            const value = parseFloat(elements.settingsContent.querySelector(`[data-prop="${property}"]`)?.value || 0);
            addKeyframe(state.activeElementId, property, time, value, easing);
            renderKeyframeList();
            renderFrameAtTime(state.currentTime);
        });
    }

    const presetButtons = elements.settingsContent.querySelectorAll('#css-preset-buttons button');
    presetButtons.forEach(button => {
        button.addEventListener('click', () => {
            const presetId = button.dataset.id;
            toggleCssPreset(state.activeElementId, presetId);
            renderPropertiesPanel();
            renderFrameAtTime(state.currentTime);
        });
    });

    elements.settingsContent.addEventListener('input', (e) => {
        const prop = e.target.dataset.prop;
        if (prop) {
            const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
            
            if (state.activeElementId === 'background' && prop === 'type') {
                const bgLayer = getElementData('background');
                if (value === 'color') {
                    bgLayer.content = bgLayer.content || '#1a1a1a';
                } else if (value === 'image' || value === 'video') {
                    bgLayer.content = '';
                }
                updateElementProperty(state.activeElementId, prop, value);
                renderPropertiesPanel();
            } else {
                updateElementProperty(state.activeElementId, prop, value);
            }

            renderFrameAtTime(state.currentTime);
            if (prop === 'content' || prop === 'type') {
                renderLayerList();
            }
        }
    });

    renderKeyframeList();
}

function renderKeyframeList() {
    const elementData = getElementData(state.activeElementId);
    if (!elementData || elementData.isBackground) return;
    const keyframeList = document.getElementById('keyframe-list');
    if (!keyframeList) return;
    let html = '<h4>Danh sách Keyframes</h4>';
    for (const [property, keyframes] of Object.entries(elementData.keyframes)) {
        html += `<div><strong>${property}</strong>: ${keyframes.map(kf => `Thời gian: ${kf.time}s, Giá trị: ${kf.value}, Easing: ${kf.easing}`).join('; ')}</div>`;
    }
    keyframeList.innerHTML = html || '<div>Chưa có keyframes</div>';
}

export function setupInteraction() {
    if (typeof interact === 'undefined') {
        createToast('Interact.js không được tải. Kéo thả không hoạt động!', 'error');
        console.error('Interact.js library is not loaded.');
        return;
    }

    interact('.layer:not(#background)').draggable({
        listeners: {
            start(event) {
                selectElement(event.target.id);
            },
            move(event) {
                const target = event.target;
                const layer = getElementData(target.id);
                if (!layer) return;

                const previewRect = elements.previewArea.getBoundingClientRect();
                const scale = previewRect.width / 1920;

                let newX, newY;
                if (layer.unit === 'px') {
                    newX = layer.x + (event.dx / scale);
                    newY = layer.y + (event.dy / scale);
                } else {
                    newX = layer.x + (event.dx / previewRect.width * 100);
                    newY = layer.y + (event.dy / previewRect.height * 100);
                }

                updateElementProperty(layer.id, 'x', newX);
                updateElementProperty(layer.id, 'y', newY);
                addKeyframe(layer.id, 'x', state.currentTime, newX);
                addKeyframe(layer.id, 'y', state.currentTime, newY);
                renderFrameAtTime(state.currentTime);
            },
            end() {
                renderPropertiesPanel();
            }
        },
        modifiers: [
            interact.modifiers.restrict({
                restriction: 'parent'
            })
        ]
    }).styleCursor(true);
}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 