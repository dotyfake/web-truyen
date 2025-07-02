import { state, elements, getElementData, updateElementProperty, addKeyframe, addCssPreset, toggleCssPreset, deleteCssPreset, saveCssPresets, loadCssPresets } from './state.js';
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

export function applyCustomCss() {
    const layer = getElementData(state.activeElementId);
    if (!layer) return;
    updateElementProperty(state.activeElementId, 'customCss', elements.cssEditorTextarea.value.trim());
    elements.cssEditorOverlay.classList.add('hidden');
    renderPropertiesPanel();
    renderFrameAtTime(state.currentTime);
    createToast('Đã áp dụng CSS tùy chỉnh!', 'success');
}

export function saveCustomCss() {
    const layer = getElementData(state.activeElementId);
    if (!layer) return;
    const css = elements.cssEditorTextarea.value.trim();
    const presetName = prompt('Nhập tên cho preset CSS:', '');
    if (presetName) {
        const presetId = addCssPreset(presetName, css);
        toggleCssPreset(state.activeElementId, presetId);
        renderPropertiesPanel();
        renderFrameAtTime(state.currentTime);
        createToast(`Đã lưu preset CSS "${presetName}"!`, 'success');
    }
    elements.cssEditorOverlay.classList.add('hidden');
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
                <label>Độ dày viền chữ (px): <input type="number" step="0.1" data-prop="style.textStrokeWidth" value="${elementData.style.textStrokeWidth || 0}"></label>
                <label>Màu viền chữ: <input type="color" data-prop="style.textStrokeColor" value="${elementData.style.textStrokeColor || '#000000'}"></label>
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
            <label>Thời lượng (s): <input type="number" step="0.1" data-prop="animations.out.duration" value="${elementData.animations.out.duration}"></label>
            <h4>Lặp</h4>
            <label>Loại: <select data-prop="animations.loop.type">${getAnimOptions(elementData.animations.loop.type, true)}</select></label>
            <label>Thời lượng (s): <input type="number" step="0.1" data-prop="animations.loop.duration" value="${elementData.animations.loop.duration}"></label>
        `);

        html += createSettingsGroup('CSS Tùy chỉnh Đã Lưu', `
            <div id="css-preset-buttons" style="display: flex; flex-wrap: wrap; gap: 5px;">
                ${Object.entries(state.cssPresets).map(([presetId, preset]) => `
                    <div class="css-preset-container">
                        <button data-id="${presetId}" style="background-color: ${elementData.appliedCssPresets.includes(presetId) ? '#28a745' : '#444'}; padding: 5px 10px; border: none; border-radius: 3px; cursor: pointer;">
                            ${preset.name}
                        </button>
                        <button class="delete-preset" data-id="${presetId}" title="Xóa preset">X</button>
                    </div>
                `).join('\n')}
            </div>
        `);

        html += createSettingsGroup('Nâng cao', `
            <button id="btn-custom-css">CSS tùy chỉnh</button>
            <button id="btn-save-css-presets">Lưu CSS Presets</button>
            <button id="btn-load-css-presets">Tải CSS Presets</button>
            <input type="file" id="css-presets-input" accept=".json" hidden>
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
    if (document.getElementById('btn-apply-custom-css')) document.getElementById('btn-apply-custom-css').addEventListener('click', applyCustomCss);
    if (document.getElementById('btn-save-custom-css')) document.getElementById('btn-save-custom-css').addEventListener('click', saveCustomCss);
    if (document.getElementById('btn-cancel-custom-css')) document.getElementById('btn-cancel-custom-css').addEventListener('click', () => {
        elements.cssEditorOverlay.classList.add('hidden');
    });
    if (document.getElementById('btn-save-css-presets')) document.getElementById('btn-save-css-presets').addEventListener('click', () => {
        saveCssPresets();
        createToast('Đã lưu CSS presets!', 'success');
    });
    if (document.getElementById('btn-load-css-presets')) document.getElementById('btn-load-css-presets').addEventListener('click', () => {
        elements.cssPresetsInput.click();
    });
    if (document.getElementById('css-presets-input')) document.getElementById('css-presets-input').addEventListener('change', async (event) => {
        try {
            await loadCssPresets(event.target.files[0]);
            renderPropertiesPanel();
            createToast('Tải CSS presets thành công!', 'success');
        } catch (err) {
            createToast('Lỗi khi tải CSS presets!', 'error');
            console.error(err);
        }
        event.target.value = '';
    });
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

    const presetButtons = elements.settingsContent.querySelectorAll('#css-preset-buttons button:not(.delete-preset)');
    presetButtons.forEach(button => {
        button.addEventListener('click', () => {
            const presetId = button.dataset.id;
            toggleCssPreset(state.activeElementId, presetId);
            renderPropertiesPanel();
            renderFrameAtTime(state.currentTime);
        });
    });

    const deletePresetButtons = elements.settingsContent.querySelectorAll('#css-preset-buttons .delete-preset');
    deletePresetButtons.forEach(button => {
        button.addEventListener('click', () => {
            const presetId = button.dataset.id;
            deleteCssPreset(presetId);
            renderPropertiesPanel();
            renderFrameAtTime(state.currentTime);
            createToast('Đã xóa preset CSS!', 'success');
        });
    });

    elements.settingsContent.querySelectorAll('[data-prop]').forEach(input => {
        input.addEventListener('input', () => {
            updateElementProperty(state.activeElementId, input.dataset.prop, input.value);
            renderFrameAtTime(state.currentTime);
        });
    });

    renderKeyframeList();
}

function renderKeyframeList() {
    const elementData = getElementData(state.activeElementId);
    if (!elementData || !document.getElementById('keyframe-list')) return;
    let html = '';
    Object.entries(elementData.keyframes).forEach(([prop, keyframes]) => {
        keyframes.forEach(kf => {
            html += `<div style="margin: 5px 0; font-size: 0.8rem;">
                ${prop} @ ${kf.time}s: ${kf.value} (${kf.easing})
                <button class="delete-keyframe" data-prop="${prop}" data-time="${kf.time}" style="margin-left: 10px; padding: 2px 6px; background: #dc3545; border: none; border-radius: 3px; color: white; cursor: pointer;">X</button>
            </div>`;
        });
    });
    document.getElementById('keyframe-list').innerHTML = html;

    document.querySelectorAll('.delete-keyframe').forEach(button => {
        button.addEventListener('click', () => {
            const prop = button.dataset.prop;
            const time = parseFloat(button.dataset.time);
            const layer = getElementData(state.activeElementId);
            if (layer && layer.keyframes[prop]) {
                layer.keyframes[prop] = layer.keyframes[prop].filter(kf => kf.time !== time);
                if (layer.keyframes[prop].length === 0) delete layer.keyframes[prop];
                renderKeyframeList();
                renderFrameAtTime(state.currentTime);
            }
        });
    });
}

export function setupInteract() {
    if (!window.interact) {
        console.error('Interact.js not loaded');
        c