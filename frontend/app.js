// ===================================================
// VLearn Grounded Tutor — Frontend Application Logic
// Nhóm BTN — Track A1
// ===================================================

const API_BASE = "";

// App State
let apiKey = localStorage.getItem("vlearn_gemini_api_key") || "";
let selectedModel = localStorage.getItem("vlearn_gemini_model") || "gemini-1.5-flash";
let lectureSections = [];
let selectedQuoteText = "";
let inspectorLogs = [];

// DOM Elements
const connectionStatus = document.getElementById("connectionStatus");
const statusText = document.getElementById("statusText");
const btnOpenConfig = document.getElementById("btnOpenConfig");
const btnCloseConfig = document.getElementById("btnCloseConfig");
const configModal = document.getElementById("configModal");
const apiKeyInput = document.getElementById("apiKeyInput");
const modelSelect = document.getElementById("modelSelect");
const btnTestApi = document.getElementById("btnTestApi");
const btnSaveConfig = document.getElementById("btnSaveConfig");
const testResultBox = document.getElementById("testConnectionResult");
const btnToggleKey = document.getElementById("btnToggleKeyVisibility");

const btnOpenInspector = document.getElementById("btnOpenInspector");
const btnCloseInspector = document.getElementById("btnCloseInspector");
const inspectorModal = document.getElementById("inspectorModal");
const inspectorContent = document.getElementById("inspectorContent");
const inspectorCount = document.getElementById("inspectorCount");

const lectureSectionsContainer = document.getElementById("lectureSectionsContainer");
const searchInput = document.getElementById("searchInput");
const chatContainer = document.getElementById("chatContainer");
const chatForm = document.getElementById("chatForm");
const queryInput = document.getElementById("queryInput");
const btnSend = document.getElementById("btnSend");

const selectedTextPreview = document.getElementById("selectedTextPreview");
const selectedSnippet = document.getElementById("selectedSnippet");
const btnClearSelection = document.getElementById("btnClearSelection");

const preset1 = document.getElementById("preset1");
const preset2 = document.getElementById("preset2");
const preset3 = document.getElementById("preset3");

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
  initUI();
  fetchStatus();
  fetchLecture();
  setupEventListeners();
});

function initUI() {
  if (apiKey) apiKeyInput.value = apiKey;
  if (selectedModel) modelSelect.value = selectedModel;
}

// 1. Fetch System Status
async function fetchStatus() {
  try {
    const res = await fetch(`${API_BASE}/api/status`);
    const data = await res.json();
    if (data.has_env_key && !apiKey) {
      updateStatus(true, "Gemini API sẵn sàng (từ .env)");
    } else if (apiKey) {
      updateStatus(true, "Gemini API đã lưu");
    } else {
      updateStatus(false, "Chưa có API Key");
    }
  } catch (err) {
    updateStatus(false, "Mất kết nối Backend");
  }
}

function updateStatus(isConnected, text) {
  if (isConnected) {
    connectionStatus.className = "status-indicator connected";
    statusText.innerText = text || "Gemini 1.5 Flash Connected";
  } else {
    connectionStatus.className = "status-indicator not-connected";
    statusText.innerText = text || "Chưa có API Key";
  }
}

// 2. Fetch Lecture Material
async function fetchLecture() {
  try {
    const res = await fetch(`${API_BASE}/api/lecture`);
    const data = await res.json();
    lectureSections = data.sections || [];
    renderLectureSections(lectureSections);
  } catch (err) {
    lectureSectionsContainer.innerHTML = `
      <div class="empty-state">
        <p>Không thể tải tài liệu bài giảng. Vui lòng kiểm tra backend.</p>
      </div>
    `;
  }
}

function renderLectureSections(sections) {
  if (!sections.length) {
    lectureSectionsContainer.innerHTML = `<div class="empty-state"><p>Không tìm thấy nội dung phù hợp.</p></div>`;
    return;
  }

  lectureSectionsContainer.innerHTML = sections.map(sec => `
    <div class="lecture-card" id="card-${sec.id}">
      <div class="card-header-row">
        <span class="segment-badge">[${sec.id}]</span>
        <button class="btn-quote" onclick="selectSection('${sec.id}', \`${escapeText(sec.content)}\`)">
          ❝ Chọn đoạn này để hỏi
        </button>
      </div>
      <div class="card-title">${sec.title}</div>
      <div class="card-content">${sec.content}</div>
    </div>
  `).join("");
}

function escapeText(str) {
  return (str || "").replace(/"/g, '&quot;').replace(/'/g, "\\'").replace(/\n/g, " ");
}

// 3. Highlight Lecture Section by ID
window.highlightSection = function(sectionId) {
  const card = document.getElementById(`card-${sectionId}`);
  if (card) {
    // Remove previous highlights
    document.querySelectorAll(".lecture-card.highlighted").forEach(el => el.classList.remove("highlighted"));
    
    // Highlight & scroll
    card.classList.add("highlighted");
    card.scrollIntoView({ behavior: "smooth", block: "center" });

    setTimeout(() => {
      card.classList.remove("highlighted");
    }, 6000);
  }
};

window.selectSection = function(sectionId, text) {
  selectedQuoteText = text.substring(0, 300);
  selectedSnippet.innerText = `[${sectionId}] ${selectedQuoteText}...`;
  selectedTextPreview.style.display = "flex";
  queryInput.focus();
};

// 4. Send Message & Chat Flow
async function handleSendMessage(customText) {
  const question = (customText || queryInput.value || "").trim();
  if (!question) return;

  // Append user message
  appendUserMessage(question);
  queryInput.value = "";

  // Show typing indicator
  const typingId = appendTypingIndicator();

  const payload = {
    question: question,
    selected_text: selectedQuoteText,
    api_key: apiKey,
    model: selectedModel
  };

  try {
    const startTime = performance.now();
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    removeTypingIndicator(typingId);

    if (data.status === "error") {
      appendErrorMessage(data.error || "Có lỗi xảy ra khi gọi Gemini API");
      return;
    }

    // Success response
    appendAssistantMessage(data);

    // Save to inspector logs
    inspectorLogs.unshift({
      timestamp: new Date().toLocaleTimeString(),
      question: question,
      response: data
    });
    inspectorCount.innerText = inspectorLogs.length;

    // Clear quote selection banner
    clearQuote();

  } catch (err) {
    removeTypingIndicator(typingId);
    appendErrorMessage("Lỗi kết nối máy chủ backend: " + err.message);
  }
}

function appendUserMessage(text) {
  const msg = document.createElement("div");
  msg.className = "chat-message user";
  msg.innerHTML = `
    <div class="avatar">🧑‍🎓</div>
    <div class="bubble">
      <div class="message-text">${escapeHtml(text)}</div>
    </div>
  `;
  chatContainer.appendChild(msg);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function appendTypingIndicator() {
  const id = "typing-" + Date.now();
  const msg = document.createElement("div");
  msg.className = "chat-message assistant";
  msg.id = id;
  msg.innerHTML = `
    <div class="avatar">🤖</div>
    <div class="bubble">
      <div style="display:flex; align-items:center; gap:8px; color:var(--text-dim); font-size:13px;">
        <span class="spinner"></span>
        <span>AI Tutor đang tra cứu tài liệu bài giảng qua Gemini API...</span>
      </div>
    </div>
  `;
  chatContainer.appendChild(msg);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  return id;
}

function removeTypingIndicator(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function appendAssistantMessage(data) {
  const decision = (data.decision || "GROUNDED").toUpperCase();
  let decisionClass = "grounded";
  let decisionLabel = "✓ CÓ CĂN CỨ TRONG BÀI";

  if (decision === "CLARIFY") {
    decisionClass = "clarify";
    decisionLabel = "? CẦN LÀM RÕ (HAX G10)";
  } else if (decision === "OUT_OF_BOUNDS") {
    decisionClass = "out_of_bounds";
    decisionLabel = "⛔ NGOÀI PHẠM VI BÀI HỌC";
  }

  // Citations Pills
  let citationsHtml = "";
  if (data.citations && data.citations.length) {
    citationsHtml = `
      <div class="citations-group">
        <span class="citation-label">Trích dẫn kiểm chứng:</span>
        ${data.citations.map(c => `
          <span class="citation-pill" onclick="highlightSection('${c}')" title="Bấm để cuộn đến đoạn bài giảng">
            📌 [${c}]
          </span>
        `).join("")}
      </div>
    `;
  }

  // Clarify Options
  let clarifyHtml = "";
  if (data.clarify_options && data.clarify_options.length) {
    clarifyHtml = `
      <div class="clarify-options-group">
        <span class="citation-label">Gợi ý lựa chọn để trả lời chính xác:</span>
        ${data.clarify_options.map(opt => `
          <button class="clarify-btn" onclick="handleSendMessage('${escapeHtml(opt)}')">
            👉 ${opt}
          </button>
        `).join("")}
      </div>
    `;
  }

  const msg = document.createElement("div");
  msg.className = "chat-message assistant";
  msg.innerHTML = `
    <div class="avatar">🤖</div>
    <div class="bubble">
      <div class="message-meta">
        <span class="decision-pill ${decisionClass}">${decisionLabel}</span>
        <span class="sender-name">Tutor VLearn</span>
      </div>
      <div class="message-text">
        ${formatMarkdown(data.answer)}
      </div>
      ${citationsHtml}
      ${clarifyHtml}
      <div class="message-footer">
        <span>⚡ Gemini API: ${data.latency_ms || 0}ms (${data.model_used || "gemini-1.5-flash"})</span>
        <div>
          <button class="btn-feedback" title="Hữu ích" onclick="this.innerText='👍 Đã gửi!'">👍</button>
          <button class="btn-feedback" title="Chưa đúng" onclick="this.innerText='👎 Đã ghi nhận!'">👎</button>
        </div>
      </div>
    </div>
  `;
  chatContainer.appendChild(msg);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  // Auto highlight first citation
  if (data.citations && data.citations.length) {
    highlightSection(data.citations[0]);
  }
}

function appendErrorMessage(errText) {
  const msg = document.createElement("div");
  msg.className = "chat-message assistant";
  msg.innerHTML = `
    <div class="avatar">⚠️</div>
    <div class="bubble" style="border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.1);">
      <div class="message-meta">
        <span class="decision-pill out_of_bounds">LỖI XỬ LÝ</span>
      </div>
      <div class="message-text" style="color: #fca5a5;">
        ${escapeHtml(errText)}
      </div>
      <div class="message-footer">
        <span style="color: #fca5a5;">Vui lòng kiểm tra lại API Key ở nút ⚙️ Cấu hình API.</span>
      </div>
    </div>
  `;
  chatContainer.appendChild(msg);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 5. Preset Buttons
function setupEventListeners() {
  // Presets
  preset1.addEventListener("click", () => {
    handleSendMessage("Quick win trong ma trận tác động - nỗ lực có ý nghĩa gì và tại sao cần ưu tiên?");
  });

  preset2.addEventListener("click", () => {
    handleSendMessage("Ma trận");
  });

  preset3.addEventListener("click", () => {
    handleSendMessage("Thầy ơi nộp bài tập lab ở link nào vậy ạ?");
  });

  // Chat Form
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    handleSendMessage();
  });

  // Search in Lecture
  searchInput.addEventListener("input", (e) => {
    const q = e.target.value.toLowerCase().trim();
    if (!q) {
      renderLectureSections(lectureSections);
      return;
    }
    const filtered = lectureSections.filter(s => 
      s.title.toLowerCase().includes(q) || s.content.toLowerCase().includes(q) || s.id.toLowerCase().includes(q)
    );
    renderLectureSections(filtered);
  });

  // Clear quote
  btnClearSelection.addEventListener("click", clearQuote);

  // Config Modal
  btnOpenConfig.addEventListener("click", () => {
    configModal.classList.add("open");
    testResultBox.style.display = "none";
  });
  btnCloseConfig.addEventListener("click", () => configModal.classList.remove("open"));

  btnToggleKey.addEventListener("click", () => {
    apiKeyInput.type = (apiKeyInput.type === "password") ? "text" : "password";
  });

  btnSaveConfig.addEventListener("click", () => {
    apiKey = apiKeyInput.value.trim();
    selectedModel = modelSelect.value;
    localStorage.setItem("vlearn_gemini_api_key", apiKey);
    localStorage.setItem("vlearn_gemini_model", selectedModel);
    configModal.classList.remove("open");
    updateStatus(Boolean(apiKey), apiKey ? "Gemini API đã lưu" : "Chưa có API Key");
  });

  btnTestApi.addEventListener("click", async () => {
    const testKey = apiKeyInput.value.trim();
    if (!testKey) {
      showTestResult(false, "Vui lòng nhập API Key để kiểm tra!");
      return;
    }
    btnTestApi.disabled = true;
    btnTestApi.innerText = "Đang thử...";
    try {
      const res = await fetch(`${API_BASE}/api/check-connection`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: testKey, model: modelSelect.value })
      });
      const data = await res.json();
      btnTestApi.disabled = false;
      btnTestApi.innerText = "⚡ Thử kết nối API";
      if (data.success) {
        showTestResult(true, `✅ Kết nối thành công! Độ trễ: ${data.latency_ms} ms (Model: ${data.model})`);
      } else {
        showTestResult(false, `❌ Thất bại: ${data.error}`);
      }
    } catch (e) {
      btnTestApi.disabled = false;
      btnTestApi.innerText = "⚡ Thử kết nối API";
      showTestResult(false, "Lỗi gọi máy chủ: " + e.message);
    }
  });

  // Inspector Modal
  btnOpenInspector.addEventListener("click", () => {
    renderInspectorLogs();
    inspectorModal.classList.add("open");
  });
  btnCloseInspector.addEventListener("click", () => inspectorModal.classList.remove("open"));
}

function clearQuote() {
  selectedQuoteText = "";
  selectedTextPreview.style.display = "none";
}

function showTestResult(isSuccess, text) {
  testResultBox.style.display = "block";
  testResultBox.className = isSuccess ? "test-result-box success" : "test-result-box error";
  testResultBox.innerText = text;
}

function renderInspectorLogs() {
  if (!inspectorLogs.length) {
    inspectorContent.innerHTML = `<div class="empty-state"><p>Chưa có lượt gọi API nào. Hãy hỏi một câu để xem log!</p></div>`;
    return;
  }

  inspectorContent.innerHTML = inspectorLogs.map((log, idx) => `
    <div class="inspector-log-item">
      <div class="inspector-grid">
        <div class="metric-box">
          <div class="metric-title">Thời gian</div>
          <div class="metric-value">${log.timestamp}</div>
        </div>
        <div class="metric-box">
          <div class="metric-title">Quyết định</div>
          <div class="metric-value" style="color:#34d399;">${log.response.decision || "N/A"}</div>
        </div>
        <div class="metric-box">
          <div class="metric-title">Độ trễ API</div>
          <div class="metric-value">${log.response.latency_ms || 0} ms</div>
        </div>
        <div class="metric-box">
          <div class="metric-title">Model</div>
          <div class="metric-value">${log.response.model_used || "gemini-1.5-flash"}</div>
        </div>
      </div>
      <div style="margin-bottom:6px; color:var(--text-muted); font-size:11px;">
        <strong>Câu hỏi:</strong> "${escapeHtml(log.question)}"
      </div>
      <div class="json-dump">${escapeHtml(JSON.stringify(log.response, null, 2))}</div>
    </div>
  `).join("");
}

// Simple text escape & formatting
function escapeHtml(text) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return (text || "").replace(/[&<>"']/g, m => map[m]);
}

function formatMarkdown(text) {
  if (!text) return "";
  let formatted = escapeHtml(text);
  // Bold
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Code
  formatted = formatted.replace(/`(.*?)`/g, '<code>$1</code>');
  // Paragraphs
  formatted = formatted.split("\n\n").map(p => `<p>${p.replace(/\n/g, "<br>")}</p>`).join("");
  return formatted;
}
