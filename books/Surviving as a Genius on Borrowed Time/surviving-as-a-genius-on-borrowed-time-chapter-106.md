:root {
    --bg-dark: #2a2a2a;
    --bg-medium: #333;
    --bg-light: #444;
    --text-light: #f0f0f0;
    --accent-color: #00aaff;
    --danger-color: #ff4d4d;
    --warning-color: #f0ad4e;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg-medium);
    color: var(--text-light);
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    overflow: hidden;
}

.app-container {
    display: flex;
    width: 98vw;
    height: 95vh;
    background-color: var(--bg-light);
    border-radius: 8px;
}

/* Cột điều khiển và thuộc tính */
.main-controls, .properties-panel {
    width: 300px;
    padding: 20px;
    background-color: var(--bg-dark);
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow-y: auto;
}

button, select, input {
    width: 100%;
    padding: 10px;
    border: 1px solid #555;
    background-color: #555;
    color: white;
    cursor: pointer;
    border-radius: 4px;
    box-sizing: border-box;
    font-size: 14px;
}

input[type="color"] { padding: 2px; height: 40px; }
button:hover { background-color: #666; }
button.primary { background-color: var(--accent-color); font-weight: bold; }
button.primary:hover { background-color: #0077b3; }
button.danger { background-color: var(--danger-color); }
button.danger:hover { background-color: #c82333; }

hr {
    border: 0;
    height: 1px;
    background-color: #444;
    margin: 10px 0;
}

/* Khu vực trung tâm */
.center-panel {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    padding: 20px;
}
.preview-container {
    flex-grow: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #202020;
    border-radius: 8px;
    overflow: hidden;
}

#preview-area {
    position: relative;
    overflow: hidden;
    transform-origin: center center;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
    background-color: #000;
}

/* Kích thước preview để tối ưu hiệu năng html2canvas, FFmpeg sẽ upscale khi xuất */
.aspect-16-9 { width: 960px; height: 540px; }
.aspect-9-16 { width: 304px; height: 540px; }
.aspect-1-1 { width: 540px; height: 540px; }


#timeline-controls { padding-top: 20px; }
#progress-bar-container { background-color: #555; border-radius: 5px; padding: 2px; cursor: pointer; }
#progress-bar { width: 0%; height: 10px; background-color: var(--accent-color); border-radius: 3px; pointer-events: none; }
#timeline-controls p { text-align: center; margin-top: 5px; user-select: none; }

/* Panel thuộc tính */
.properties-panel {
    display: flex;
    flex-direction: column;
}
.layer-list-container, .sfx-list-container {
    margin-bottom: 20px;
}

#layer-list, #sfx-list {
    list-style: none;
    padding: 0;
    max-height: 250px;
    overflow-y: auto;
}

#layer-list li, #sfx-list li {
    padding: 8px;
    background-color: #555;
    margin-bottom: 5px;
    cursor: pointer;
    border-radius: 3px;
    border-left: 4px solid transparent;
    font-size: 14px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    transition: background-color 0.2s;
}
#layer-list li { border-left-color: #6c757d; }
#sfx-list li { border-left-color: var(--warning-color); }
#layer-list li.selected, #sfx-list li.selected { border-left-color: var(--accent-color); background-color: #6a6a6a; }

#settings-box {
    margin-top: auto; /* Đẩy box xuống dưới cùng */
    padding: 15px;
    background-color: #383838;
    border-radius: 5px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}
#settings-box h3 { margin: 0 0 10px 0; }
#settings-content { display: flex; flex-direction: column; gap: 10px; }
#settings-content label { display: flex; flex-direction: column; font-size: 12px; gap: 4px; }
#settings-content .two-cols { display: grid; grid-template-columns: 1fr 1f@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

:root {
    --bg-main: #1e1e1e;
    --bg-panel: #2a2a2a;
    --bg-panel-light: #3c3c3c;
    --text-primary: #e0e0e0;
    --text-secondary: #a0a0a0;
    --accent-color: #007bff;
    --accent-hover: #0056b3;
    --danger-color: #dc3545;
    --success-color: #28a745;
    --border-color: #4a4a4a;
    --font-family: 'Roboto', sans-serif;
}

/* --- CẤU TRÚC CƠ BẢN --- */
body {
    font-family: var(--font-family);
    background-color: var(--bg-main);
    color: var(--text-primary);
    margin: 0;
    overflow: hidden;
}

#app-container {
    display: flex;
    height: 100vh;
    width: 100vw;
}

.controls-panel, .properties-panel {
    background-color: var(--bg-panel);
    padding: 20px;
    width: 280px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    overflow-y: auto;
}

.properties-panel {
    width: 320px;
}

.center-panel {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    padding: 15px;
    background-color: var(--bg-main);
}

/* --- CỘT ĐIỀU KHIỂN BÊN TRÁI --- */
.controls-panel .logo { font-size: 1.5rem; }
.control-group { border-top: 1px solid var(--border-color); padding-top: 20px; }
.control-group h3 { margin-top: 0; font-size: 1rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px;}
.controls-panel button {
    width: 100%;
    padding: 12px;
    margin-bottom: 10px;
    border: none;
    border-radius: 5px;
    background-color: var(--bg-panel-light);
    color: var(--text-primary);
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    text-align: left;
    transition: background-color 0.2s;
}
.controls-panel button:hover { background-color: #4a4a4a; }
#btn-export { background-color: var(--accent-color); color: white; font-weight: 700; }
#btn-export:hover { background-color: var(--accent-hover); }
.disabled, .disabled button { pointer-events: none; opacity: 0.5; }

/* --- KHUNG PREVIEW & TIMELINE --- */
.preview-viewport {
    flex-grow: 1;
    display: grid;
    place-items: center;
    overflow: hidden;
}
#preview-area-wrapper {
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    background: #000;
}
#preview-area {
    position: relative;
    overflow: hidden;
    transform-origin: top left;
}
.aspect-16-9 { aspect-ratio: 16 / 9; }

.timeline-container {
    padding: 10px 0;
    display: flex;
    align-items: center;
    gap: 15px;
}
#btn-play-pause {
    background: none;
    border: 1px solid var(--text-secondary);
    color: var(--text-secondary);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
    cursor: pointer;
    line-height: 40px;
    padding: 0;
}
#time-display {
    font-variant-numeric: tabular-nums;
    color: var(--text-secondary);
}
#timeline-slider {
    width: 100%;
    cursor: pointer;
}

/* --- CỘT THUỘC TÍNH BÊN PHẢI --- */
.layer-list-container { flex-shrink: 0; }
.layer-list-container h3 { margin: 0 0 10px 0; }
#layer-list {
    list-style: none;
    padding: 0;
    margin: 0;
    max-height: 40vh;
    overflow-y: auto;
}
#layer-list li {
    padding: 10px;
    background-color: var(--bg-panel-light);
    margin-bottom: 5px;
    border-radius: 4px;
    cursor: pointer;
    border-left: 4px solid transparent;
    transition: background-color 0.2s;
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
#layer-list li:hover { background-color: #4a4a4a; }
#layer-list li.selected {
    background-color: #4a4a4a;
    border-left-color: var(--accent-color);
    font-weight: 500;
}

#settings-box {
    margin-top: 20px;
    border-top: 1px solid var(--border-color);
    padding-top: 20px;
    flex-grow: 1;
    overflow-y: auto;
}
#settings-box.hidden { display: none; }
#settings-content .setting-group {
    margin-bottom: 15px;
    padding: 15px;
    background-color: var(--bg-panel-light);
    border-radius: 5px;
}
#settings-content h4 {
    margin: 0 0 10px 0;
    font-size: 0.9rem;
    color: var(--text-secondary);
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 5px;
}
#settings-content label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 0.9rem;
}
#settings-content input, #settings-content select {
    background-color: #1e1e1e;
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 6px;
    width: 150px;
}
#settings-content input[type="color"] { padding: 2px; width: 40px; }
#settings-content input[type="checkbox"] { width: auto; }
#btn-custom-css {
    width: 100%;
    padding: 8px;
    margin-top: 10px;
    background-color: #555;
}

/* --- CÁC LỚP TRÊN PREVIEW --- */
.layer {
    position: absolute;
    box-sizing: border-box;
    touch-action: none; /* For Interact.js */
    will-change: transform, opacity;
}
.layer.text-layer {
    white-space: pre-wrap; /* Preserve newlines */
    display: flex;
    align-items: center;
    justify-content: center;
}
.layer.media-layer {
    background-size: cover;
    background-position: center;
}
.layer.media-layer video, .layer.media-layer img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.layer:focus {
    outline: 2px dashed var(--accent-color);
}

/* --- OVERLAYS & MODALS --- */
.overlay {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0,0,0,0.7);
    display: grid;
    place-items: center;
    z-index: 1000;
}
.overlay.hidden { display: none; }

#export-overlay .export-modal {
    background: var(--bg-panel);
    padding: 30px 40px;
    border-radius: 8px;
    width: 500px;
    text-align: center;
}
.progress-bar-container {
    width: 100%;
    background: var(--bg-panel-light);
    border-radius: 5px;
    overflow: hidden;
    margin: 20px 0;
}
#export-progress-bar {
    width: 0%;
    height: 20px;
    background: var(--accent-color);
    transition: width 0.3s;
}
#export-log {
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: 15px;
    height: 40px;
}

#css-editor-overlay .css-editor-modal {
    background: var(--bg-panel);
    padding: 20px;
    border-radius: 8px;
    width: 600px;
    display: flex;
    flex-direction: column;
}
#css-editor-textarea {
    width: 100%;
    height: 300px;
    background: #1a1a1a;
    color: #f0f0f0;
    border: 1px solid var(--border-color);
    font-family: monospace;
    font-size: 1rem;
    margin: 15px 0;
    resize: vertical;
}
.css-editor-buttons { text-align: right; }
.css-editor-buttons button { margin-left: 10px; padding: 8px 20px; }

/* --- TOAST NOTIFICATIONS --- */
#toast-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 2000;
}
.toast {
    background-color: var(--bg-panel-light);
    color: var(--text-primary);
    padding: 15px 25px;
    border-radius: 5px;
    margin-bottom: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    border-left: 5px solid var(--accent-color);
    opacity: 0;
    transform: translateX(100%);
    transition: all 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55);
}
.toast.show { opacity: 1; transform: translateX(0); }
.toast.success { border-left-color: var(--success-color); }
.toast.error { border-left-color: var(--danger-color); }

/* --- ANIMATIONS KEYFRAMES --- */
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes fadeOut { from { opacity: 1; } to { opacity: 0; } }
@keyframes slideInUp { from { transform: translateY(100%); opacity: 0; } }
@keyframes slideOutDown { to { transform: translateY(100%); opacity: 0; } }
@keyframes zoomIn { from { transform: scale(0.5); opacity: 0; } }
@keyframes zoomOut { to { transform: scale(0.5); opacity: 0; } }
@keyframes bounceIn {
    0% { transform: scale(0.5); opacity: 0; }
    50% { transform: scale(1.05); }
    70% { transform: scale(0.9); }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes kenBurns {
    0% { transform: scale(1) translate(0, 0); }
    100% { transform: scale(1.2) translate(-5%, 5%); }
}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        den">...</div> <!-- Giữ nguyên -->
                <div id="bg-image-option" class="hidden"><label>Chọn ảnh nền: <input type="file" id="bg-image-input" accept="image/*"></label></div>
                <div id="bg-video-option" class="hidden"><label>Chọn video nền: <input type="file" id="bg-video-input" accept="video/*"></label></div>
            </div>
            <button id="btn-apply-bg" class="primary">Áp dụng</button>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         const { contextBridge, ipcRenderer } = require('electron');
const path = require('path');

// "Phơi bày" các API được bảo vệ ra thế giới renderer (frontend)
// dưới object `window.electronAPI`
contextBridge.exposeInMainWorld('electronAPI', {
  // Hàm để gọi từ frontend -> backend (invoke chờ kết quả trả về)
  exportVideo: (data) => ipcRenderer.invoke('export-video', data),

  // Hàm để nhận tín hiệu từ backend -> frontend (on lắng nghe liên tục)
  onExportProgress: (callback) => {
    // Để tránh memory leak, ta xóa listener cũ nếu có trước khi thêm listener mới
    ipcRenderer.removeAllListeners('export-progress');
    ipcRenderer.on('export-progress', (event, ...args) => callback(...args));
  },
});

// Phơi bày các module Node.js hữu ích một cách an toàn
contextBridge.exposeInMainWorld('path', {
    sep: path.sep,
});                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   