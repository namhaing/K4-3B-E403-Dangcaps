"use strict";

const DEFAULT_API_URL = "http://localhost:8000";
const LETTERS = ["A", "B", "C", "D"];
const LEVEL_NAMES = { 1: "Nhận biết", 2: "Phân biệt", 3: "Áp dụng" };
const DEMO_TOTAL = 5;
const DEMO_OPPONENTS = [
  { name: "Minh Anh", initials: "MA", rank: "Tân binh", color: "#d92736" },
  { name: "Quang Huy", initials: "QH", rank: "Nhà thám hiểm", color: "#6d4bd1" },
  { name: "Ngọc Linh", initials: "NL", rank: "Chuỗi 3 ngày", color: "#138464" },
];
const RANKING_PLAYERS = [
  { name: "Hoàng Nam", initials: "HN", rating: 1688, wins: 34, streak: 7, color: "#6d4bd1" },
  { name: "Minh Anh", initials: "MA", rating: 1624, wins: 31, streak: 5, color: "#d92736" },
  { name: "Ngọc Linh", initials: "NL", rating: 1572, wins: 27, streak: 4, color: "#138464" },
  { name: "Quang Huy", initials: "QH", rating: 1496, wins: 24, streak: 2, color: "#d17b22" },
  { name: "Bảo Trân", initials: "BT", rating: 1430, wins: 20, streak: 3, color: "#2675ba" },
  { name: "Đức Minh", initials: "ĐM", rating: 1365, wins: 18, streak: 1, color: "#70558e" },
  { name: "Khánh Vy", initials: "KV", rating: 1308, wins: 15, streak: 2, color: "#b44677" },
];
const DEMO_BANK = [
  {
    concept_name: "Các tầng của AI",
    level: 1,
    page: "Demo 01",
    question: "Trong bản đồ khái niệm AI, tầng nào có phạm vi rộng nhất?",
    options: ["Machine Learning", "Deep Learning", "Generative AI", "Artificial Intelligence"],
    answer: 3,
    explanation: "Artificial Intelligence là phạm vi tổng quát; các khái niệm còn lại là những nhánh hoặc cách tiếp cận nằm bên trong.",
    evidence_quote: "Nội dung mẫu frontend: AI là phạm vi rộng, bao gồm nhiều phương pháp như Machine Learning và Deep Learning.",
  },
  {
    concept_name: "Token và context",
    level: 2,
    page: "Demo 02",
    question: "Một cuộc hội thoại quá dài vượt giới hạn context sẽ gây ra điều gì dễ thấy nhất?",
    options: ["Model tự tăng bộ nhớ", "Một phần nội dung cũ có thể không còn được xét", "Token không còn được tính phí", "Mọi câu trả lời trở nên giống nhau"],
    answer: 1,
    explanation: "Context là lượng thông tin model có thể xét trong một lần xử lý. Khi vượt giới hạn, một phần nội dung phải bị lược bỏ hoặc tóm tắt.",
    evidence_quote: "Nội dung mẫu frontend: context có giới hạn và quyết định lượng thông tin model nhìn thấy trong một lượt xử lý.",
  },
  {
    concept_name: "Giới hạn của LLM",
    level: 2,
    page: "Demo 03",
    question: "Model trả lời rất tự tin nhưng đưa ra một sự kiện không có thật. Đây là hiện tượng gì?",
    options: ["Tokenization", "Fine-tuning", "Hallucination", "Retrieval"],
    answer: 2,
    explanation: "Hallucination là khi model tạo ra thông tin nghe hợp lý nhưng không chính xác hoặc không có căn cứ.",
    evidence_quote: "Nội dung mẫu frontend: LLM có thể tạo thông tin sai với cách diễn đạt tự tin, thường gọi là hallucination.",
  },
  {
    concept_name: "Chọn model",
    level: 3,
    page: "Demo 04",
    question: "Bạn cần phân loại hàng nghìn phản hồi ngắn mỗi ngày với ngân sách thấp. Cách chọn model hợp lý nhất là gì?",
    options: ["Luôn chọn model lớn nhất", "Bắt đầu bằng model nhỏ đáp ứng chất lượng rồi mới nâng cấp", "Không cần đo chất lượng", "Dùng nhiều model ngẫu nhiên"],
    answer: 1,
    explanation: "Nên bắt đầu từ model nhỏ, nhanh và rẻ nếu nó đã đạt quality bar; chỉ nâng cấp khi số đo cho thấy cần thiết.",
    evidence_quote: "Nội dung mẫu frontend: chọn model theo yêu cầu chất lượng, độ trễ và chi phí thay vì mặc định dùng model lớn nhất.",
  },
  {
    concept_name: "AI Agent",
    level: 2,
    page: "Demo 05",
    question: "Điểm nào phân biệt agent với một lời gọi LLM đơn lẻ?",
    options: ["Agent luôn có giao diện chat", "Agent có mục tiêu và có thể thực hiện nhiều bước hành động", "Agent không dùng model", "Agent chỉ trả lời câu hỏi trắc nghiệm"],
    answer: 1,
    explanation: "Agent kết hợp model với mục tiêu, trạng thái và hành động để hoàn thành một chuỗi bước, thay vì chỉ sinh một phản hồi.",
    evidence_quote: "Nội dung mẫu frontend: agent sử dụng model trong một vòng lặp có mục tiêu, quan sát và hành động.",
  },
  {
    concept_name: "Temperature",
    level: 2,
    page: "Demo 06",
    question: "Khi cần kết quả ổn định và ít biến động giữa các lần chạy, nên điều chỉnh temperature thế nào?",
    options: ["Giảm temperature", "Tăng temperature tối đa", "Luôn đặt bằng 1", "Temperature không ảnh hưởng đầu ra"],
    answer: 0,
    explanation: "Temperature thấp thường làm phân phối lựa chọn tập trung hơn, giúp đầu ra ổn định hơn.",
    evidence_quote: "Nội dung mẫu frontend: temperature điều khiển mức độ đa dạng trong quá trình chọn token tiếp theo.",
  },
  {
    concept_name: "Grounding",
    level: 3,
    page: "Demo 07",
    question: "Một câu hỏi không có căn cứ trong tài liệu nguồn nên được hệ thống xử lý thế nào?",
    options: ["Tự đoán câu trả lời", "Dùng kiến thức bất kỳ trên Internet", "Từ chối hoặc chuyển sang chủ đề có đủ căn cứ", "Ẩn nguồn khỏi người học"],
    answer: 2,
    explanation: "Khi thiếu căn cứ, hệ thống nên thu hẹp phạm vi hoặc từ chối thay vì tạo nội dung có nguy cơ sai.",
    evidence_quote: "Nội dung mẫu frontend: không đủ nguồn thì không sinh câu; hệ thống chuyển sang nội dung có thể kiểm chứng.",
  },
];

const app = document.querySelector("#app");
const connection = document.querySelector("#connection");
const connectionLabel = document.querySelector("#connection-label");
const toastRegion = document.querySelector("#toast-region");
const reportDialog = document.querySelector("#report-dialog");
const reportForm = document.querySelector("#report-form");
const settingsDialog = document.querySelector("#settings-dialog");
const settingsForm = document.querySelector("#settings-form");
const apiUrlField = document.querySelector("#api-url");
const soloNav = document.querySelector("#solo-nav");
const rankingNav = document.querySelector("#ranking-nav");

const state = {
  apiUrl: getApiUrl(),
  sessionId: null,
  question: null,
  selectedChoice: null,
  questionStartedAt: 0,
  feedback: null,
  nextQuestion: null,
  answered: [],
  notice: "",
  busy: false,
  demoMode: false,
  demoCursor: 0,
  battleMode: false,
  opponent: null,
  playerScore: 0,
  opponentScore: 0,
  opponentLastCorrect: null,
  matchSearchId: 0,
  profile: loadProfile(),
  battleRated: false,
  lastRatingDelta: 0,
};

function loadProfile() {
  const fallback = { name: "Bạn", initials: "T", rating: 1240, wins: 8, matches: 13, streak: 2 };
  try {
    return { ...fallback, ...JSON.parse(localStorage.getItem("solo-arena-profile") || "{}") };
  } catch {
    return fallback;
  }
}

function saveProfile() {
  localStorage.setItem("solo-arena-profile", JSON.stringify(state.profile));
}

function rankedPlayers() {
  return [
    ...RANKING_PLAYERS,
    { ...state.profile, isCurrent: true, color: "#0c559b" },
  ].sort((a, b) => b.rating - a.rating);
}

function setActiveNav(target) {
  soloNav.classList.toggle("active", target === "solo");
  rankingNav.classList.toggle("active", target === "ranking");
  soloNav.toggleAttribute("aria-current", target === "solo");
  rankingNav.toggleAttribute("aria-current", target === "ranking");
}

function getApiUrl() {
  const queryUrl = new URLSearchParams(window.location.search).get("api");
  const savedUrl = localStorage.getItem("solo-arena-api");
  return (queryUrl || savedUrl || DEFAULT_API_URL).replace(/\/$/, "");
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function request(path, options = {}) {
  const response = await fetch(`${state.apiUrl}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });

  let payload;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const message = payload?.detail || `Máy chủ trả về lỗi ${response.status}.`;
    throw new Error(message);
  }
  return payload;
}

async function checkHealth({ quiet = false } = {}) {
  connection.dataset.status = "checking";
  connectionLabel.textContent = "Đang kiểm tra hệ thống";
  try {
    const health = await request("/health");
    connection.dataset.status = "online";
    connectionLabel.textContent = `${health.concepts} chủ đề sẵn sàng`;
    return true;
  } catch (error) {
    connection.dataset.status = "offline";
    connectionLabel.textContent = "Chưa kết nối API";
    if (!quiet) showToast(`Không kết nối được API: ${error.message}`);
    return false;
  }
}

function showToast(message, duration = 4600) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  toastRegion.append(toast);
  window.setTimeout(() => toast.remove(), duration);
}

function focusApp() {
  app.focus({ preventScroll: true });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function setBusy(value) {
  state.busy = value;
}

function delay(ms) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

function demoQuestion(cursor = state.demoCursor) {
  const source = DEMO_BANK[cursor % DEMO_BANK.length];
  return {
    question_id: `demo-${cursor + 1}`,
    index: state.answered.length + 1,
    total: DEMO_TOTAL,
    concept_name: source.concept_name,
    level: source.level,
    page: source.page,
    question: source.question,
    options: [...source.options],
    _answer: source.answer,
    _explanation: source.explanation,
    _evidence_quote: source.evidence_quote,
  };
}

function resetBattleState(enabled = false) {
  state.battleMode = enabled;
  state.playerScore = 0;
  state.opponentScore = 0;
  state.opponentLastCorrect = null;
  state.battleRated = false;
  state.lastRatingDelta = 0;
  if (enabled && !state.opponent) {
    state.opponent = DEMO_OPPONENTS[Math.floor(Math.random() * DEMO_OPPONENTS.length)];
  }
}

function renderStart() {
  setActiveNav("solo");
  const preview = rankedPlayers().slice(0, 5);
  const currentRank = rankedPlayers().findIndex((player) => player.isCurrent) + 1;
  app.innerHTML = `
    <section class="arena-dashboard" aria-labelledby="hero-title">
      <div class="arena-heading">
        <div>
          <p class="arena-breadcrumb">Trang chủ <span>/</span> Solo Arena</p>
          <h1 id="hero-title">SOLO ARENA <span aria-hidden="true">⚡</span></h1>
          <p>Luyện nhanh sau mỗi buổi học để biết chính xác phần nào bạn cần ôn lại.</p>
        </div>
        <span class="module-label">Tính năng mới</span>
      </div>

      <section class="arena-banner">
        <div class="arena-banner-copy">
          <p class="eyebrow">Day 1 · AI &amp; LLM Foundation</p>
          <h2>Một lượt ngắn.<br>Một điểm yếu rõ ràng.</h2>
          <p>5 câu hỏi thích ứng theo kết quả của bạn. Mỗi câu đều có giải thích và nguồn trong bài học.</p>
          <div class="hero-actions">
            <button class="button button-primary button-large" id="start-button" type="button">
              Luyện một mình <span aria-hidden="true">→</span>
            </button>
            <button class="button button-battle button-large" id="battle-button" type="button">Ghép trận 1v1</button>
            <button class="button button-ghost button-large" id="demo-button" type="button">Demo offline</button>
          </div>
        </div>
        <div class="arena-visual" aria-hidden="true">
          <div class="arena-rings">
            <span class="ring-label ring-one">5 câu</span>
            <span class="ring-label ring-two">Có nguồn</span>
            <span class="ring-label ring-three">Thích ứng</span>
            <strong>V</strong>
          </div>
        </div>
      </section>

      <div class="arena-grid">
        <section class="dashboard-card session-card">
          <div class="card-title-row"><div><p class="eyebrow">Lượt luyện của bạn</p><h2>Sẵn sàng bắt đầu?</h2></div><span class="session-time">~ 3 phút</span></div>
          <div class="session-steps">
            <div><span>01</span><strong>Làm 5 câu</strong><small>Câu hỏi thay đổi theo đúng/sai.</small></div>
            <div><span>02</span><strong>Xem căn cứ</strong><small>Đối chiếu lại ngay trong slide.</small></div>
            <div><span>03</span><strong>Chốt phần ôn</strong><small>Nhận một gợi ý cụ thể cuối lượt.</small></div>
          </div>
        </section>

        <aside class="dashboard-card trust-card">
          <p class="eyebrow">Bạn luôn kiểm soát</p>
          <h2>AI không tự chấm năng lực của bạn.</h2>
          <ul>
            <li><span>✓</span> Không đủ dữ liệu thì không kết luận</li>
            <li><span>✓</span> Có thể đổi hoặc báo câu hỏi</li>
            <li><span>✓</span> Kết quả chỉ hiển thị cho bạn</li>
          </ul>
        </aside>
      </div>

      <section class="ranking-preview dashboard-card">
        <div class="ranking-preview-heading">
          <div><p class="eyebrow">Bảng xếp hạng mùa 01</p><h2>Đường đua Solo Arena</h2></div>
          <button class="text-button ranking-link" id="open-ranking-button" type="button">Xem toàn bộ <span aria-hidden="true">→</span></button>
        </div>
        <div class="ranking-preview-grid">
          <div class="my-rank-card">
            <span class="rank-number">#${currentRank}</span>
            <div><small>Hạng hiện tại của bạn</small><strong>${state.profile.rating} rating</strong><p>${state.profile.wins} trận thắng · ${state.profile.streak} chuỗi thắng</p></div>
          </div>
          <div class="mini-leaderboard">
            ${preview.map((player, index) => miniRankRow(player, index + 1)).join("")}
          </div>
        </div>
      </section>
    </section>`;

  document.querySelector("#start-button").addEventListener("click", () => startSession(false));
  document.querySelector("#battle-button").addEventListener("click", startBattleMatch);
  document.querySelector("#demo-button").addEventListener("click", () => startDemoSession(false));
  document.querySelector("#open-ranking-button").addEventListener("click", renderRanking);
  focusApp();
}

function miniRankRow(player, rank) {
  return `
    <div class="mini-rank-row ${player.isCurrent ? "current-player" : ""}">
      <span class="mini-position">${rank}</span>
      <span class="mini-avatar" style="--avatar-color:${escapeHtml(player.color)}">${escapeHtml(player.initials)}</span>
      <div><strong>${escapeHtml(player.name)}</strong><small>${player.wins} trận thắng</small></div>
      <b>${player.rating}</b>
    </div>`;
}

function renderRanking() {
  setActiveNav("ranking");
  const players = rankedPlayers();
  const podium = players.slice(0, 3);
  const currentRank = players.findIndex((player) => player.isCurrent) + 1;
  app.innerHTML = `
    <section class="ranking-page" aria-labelledby="ranking-title">
      <div class="ranking-page-heading">
        <div>
          <p class="arena-breadcrumb">Solo Arena <span>/</span> Bảng xếp hạng</p>
          <p class="eyebrow">Mùa 01 · Day 1</p>
          <h1 id="ranking-title">BẢNG XẾP HẠNG</h1>
          <p>Thi đấu, tích lũy rating và giữ chuỗi thắng để leo hạng.</p>
        </div>
        <button class="button button-primary" id="ranking-match-button" type="button">Ghép trận ngay</button>
      </div>

      <section class="season-summary">
        <div><small>Hạng của bạn</small><strong>#${currentRank}</strong><span>trên ${players.length} người chơi</span></div>
        <div><small>Rating</small><strong>${state.profile.rating}</strong><span>${rankTier(state.profile.rating)}</span></div>
        <div><small>Trận thắng</small><strong>${state.profile.wins}</strong><span>${state.profile.matches} trận đã chơi</span></div>
        <div><small>Chuỗi hiện tại</small><strong>${state.profile.streak}</strong><span>trận thắng liên tiếp</span></div>
      </section>

      <section class="podium" aria-label="Ba người dẫn đầu">
        ${podium.map((player, index) => podiumCard(player, index)).join("")}
      </section>

      <section class="leaderboard-card">
        <div class="leaderboard-head"><span>Hạng</span><span>Học viên</span><span>Thắng</span><span>Chuỗi</span><span>Rating</span></div>
        ${players.map((player, index) => rankingRow(player, index + 1)).join("")}
      </section>

      <div class="ranking-note">BXH prototype được lưu trên trình duyệt này. Khi tích hợp thật, rating sẽ đồng bộ theo tài khoản VLearn.</div>
    </section>`;
  document.querySelector("#ranking-match-button").addEventListener("click", startBattleMatch);
  focusApp();
}

function rankTier(rating) {
  if (rating >= 1600) return "Kim cương";
  if (rating >= 1450) return "Bạch kim";
  if (rating >= 1300) return "Vàng";
  if (rating >= 1150) return "Bạc";
  return "Đồng";
}

function podiumCard(player, index) {
  const places = ["Hạng 1", "Hạng 2", "Hạng 3"];
  return `
    <article class="podium-card podium-${index + 1} ${player.isCurrent ? "current-player" : ""}">
      <span class="podium-medal">${index + 1}</span>
      <span class="podium-avatar" style="--avatar-color:${escapeHtml(player.color)}">${escapeHtml(player.initials)}</span>
      <small>${places[index]}</small><h2>${escapeHtml(player.name)}</h2><strong>${player.rating}</strong><p>${player.wins} trận thắng</p>
    </article>`;
}

function rankingRow(player, rank) {
  return `
    <div class="leaderboard-row ${player.isCurrent ? "current-player" : ""}">
      <strong class="leaderboard-position">${rank}</strong>
      <div class="leaderboard-player"><span class="mini-avatar" style="--avatar-color:${escapeHtml(player.color)}">${escapeHtml(player.initials)}</span><div><strong>${escapeHtml(player.name)}</strong><small>${player.isCurrent ? "Hạng của bạn" : rankTier(player.rating)}</small></div></div>
      <span>${player.wins}</span><span>${player.streak || 0}</span><b>${player.rating}</b>
    </div>`;
}

function updateProfileAfterBattle() {
  if (!state.battleMode || state.battleRated) return;

  const won = state.playerScore > state.opponentScore;
  const drew = state.playerScore === state.opponentScore;
  const delta = won ? 24 : drew ? 4 : -12;

  state.profile.rating = Math.max(0, state.profile.rating + delta);
  state.profile.matches += 1;
  if (won) {
    state.profile.wins += 1;
    state.profile.streak += 1;
  } else if (!drew) {
    state.profile.streak = 0;
  }

  state.lastRatingDelta = delta;
  state.battleRated = true;
  saveProfile();
}

function renderLoading(title = "Đang chuẩn bị câu hỏi", detail = "Hệ thống đang kiểm tra nội dung với slide bài học…") {
  app.innerHTML = `
    <section class="state-card loading-card" aria-busy="true" aria-live="polite">
      <div class="loading-content">
        <div class="loader" aria-hidden="true"></div>
        <h2>${escapeHtml(title)}</h2>
        <p>${escapeHtml(detail)}</p>
      </div>
    </section>`;
  focusApp();
}

async function startSession(battleMode = false) {
  if (state.busy) return;
  resetBattleState(battleMode === true);
  setBusy(true);
  renderLoading(
    state.battleMode ? `Đã ghép với ${state.opponent.name}` : "Đang tạo câu đầu tiên",
    state.battleMode ? "Đang đồng bộ câu hỏi đầu tiên cho trận đấu…" : "Câu hỏi được đối chiếu với slide trước khi hiển thị.",
  );
  try {
    const payload = await request("/session/start", {
      method: "POST",
      body: JSON.stringify({ lecture: "D01" }),
    });
    state.sessionId = payload.session_id;
    state.demoMode = false;
    state.question = payload.question;
    state.selectedChoice = null;
    state.feedback = null;
    state.nextQuestion = null;
    state.answered = [];
    state.notice = payload.status === "no_evidence" && payload.question
      ? "Một chủ đề chưa đủ căn cứ nên hệ thống đã chuyển sang chủ đề khác."
      : "";

    if (!state.question) {
      renderNoEvidence();
      return;
    }
    state.questionStartedAt = performance.now();
    renderQuestion();
  } catch (error) {
    if (state.battleMode) {
      showToast("API chưa sẵn sàng, chuyển trận đấu sang bộ câu hỏi demo.");
      startDemoSession(true);
    } else {
      renderConnectionError(error.message);
    }
  } finally {
    setBusy(false);
  }
}

function startDemoSession(battleMode = false) {
  resetBattleState(battleMode === true);
  state.demoMode = true;
  state.demoCursor = 0;
  state.sessionId = "frontend-demo";
  state.answered = [];
  state.selectedChoice = null;
  state.feedback = null;
  state.nextQuestion = null;
  state.notice = "Bạn đang xem bản DEMO frontend. Nội dung bên dưới là dữ liệu mẫu, không gọi AI và không dùng slide thật.";
  state.question = demoQuestion();
  state.questionStartedAt = performance.now();
  connection.dataset.status = "online";
  connectionLabel.textContent = "Demo frontend · không dùng API";
  renderQuestion();
}

async function startBattleMatch() {
  if (state.busy) return;
  const searchId = ++state.matchSearchId;
  state.opponent = DEMO_OPPONENTS[Math.floor(Math.random() * DEMO_OPPONENTS.length)];
  resetBattleState(true);
  setBusy(true);
  renderMatchmaking();
  await delay(1450);
  if (searchId !== state.matchSearchId) return;
  setBusy(false);
  await startSession(true);
}

function renderMatchmaking() {
  app.innerHTML = `
    <section class="matchmaking-card" aria-live="polite" aria-busy="true">
      <p class="eyebrow">Solo Arena · Đấu 1v1</p>
      <div class="match-radar" aria-hidden="true">
        <span class="radar-wave wave-one"></span>
        <span class="radar-wave wave-two"></span>
        <span class="radar-player">T</span>
        <span class="radar-opponent">?</span>
      </div>
      <h1>Đang tìm đối thủ…</h1>
      <p>Ưu tiên học viên có nhịp độ và mức luyện gần với bạn.</p>
      <div class="matchmaking-status"><span></span> Hàng chờ thử nghiệm · đối thủ mô phỏng</div>
      <button class="text-button" id="cancel-match-button" type="button">Huỷ tìm trận</button>
    </section>`;
  document.querySelector("#cancel-match-button").addEventListener("click", () => {
    state.matchSearchId += 1;
    setBusy(false);
    resetBattleState(false);
    renderStart();
  });
  focusApp();
}

function renderQuestion() {
  const q = state.question;
  if (!q) return;
  const progress = Math.max(0, Math.min(100, ((q.index - 1) / q.total) * 100));

  app.innerHTML = `
    <section class="quiz-shell" aria-labelledby="question-title">
      ${state.battleMode ? battleBoardTemplate() : ""}
      <div class="progress-card">
        <div class="progress-meta">
          <span>Câu ${q.index} / ${q.total}</span>
          <span>${q.total - q.index + 1} câu còn lại</span>
        </div>
        <div class="progress-track" role="progressbar" aria-label="Tiến độ lượt luyện" aria-valuemin="0" aria-valuemax="${q.total}" aria-valuenow="${q.index - 1}">
          <div class="progress-fill" style="width: ${progress}%"></div>
        </div>
      </div>

      ${state.notice ? `<div class="notice"><strong aria-hidden="true">!</strong><span>${escapeHtml(state.notice)}</span></div>` : ""}

      <article class="question-card">
        <div class="question-meta">
          <span class="concept-label">${escapeHtml(q.concept_name)}</span>
          <span class="level-badge">Mức ${q.level} · ${escapeHtml(LEVEL_NAMES[q.level] || "Luyện tập")}</span>
        </div>
        <h1 class="question-title" id="question-title">${escapeHtml(q.question)}</h1>

        <div class="options" role="group" aria-label="Các lựa chọn">
          ${q.options.map((option, index) => optionTemplate(option, index)).join("")}
        </div>

        ${state.feedback ? feedbackTemplate() : ""}

        <div class="question-actions">
          <div class="minor-actions">
            ${state.feedback ? "" : `
              <button class="text-button" id="skip-button" type="button">Đổi câu khác</button>
              <button class="text-button danger" id="report-button" type="button">Báo câu sai</button>`}
          </div>
          ${state.feedback
            ? `<button class="button button-primary" id="continue-button" type="button">${state.feedback.done ? "Xem kết quả" : state.nextQuestion ? "Câu tiếp theo" : "Xem kết quả"} <span aria-hidden="true">→</span></button>`
            : `<button class="button button-primary" id="answer-button" type="button" ${state.selectedChoice === null ? "disabled" : ""}>Kiểm tra đáp án</button>`}
        </div>
      </article>
    </section>`;

  if (state.feedback) {
    document.querySelector("#continue-button").addEventListener("click", continueAfterFeedback);
  } else {
    document.querySelectorAll(".option").forEach((button) => {
      button.addEventListener("click", () => selectChoice(Number(button.dataset.choice)));
    });
    document.querySelector("#answer-button").addEventListener("click", submitAnswer);
    document.querySelector("#skip-button").addEventListener("click", skipQuestion);
    document.querySelector("#report-button").addEventListener("click", () => reportDialog.showModal());
  }

  focusApp();
}

function battleBoardTemplate() {
  const opponent = state.opponent;
  const round = Math.min(state.feedback ? state.answered.length : state.answered.length + 1, DEMO_TOTAL);
  return `
    <section class="battle-board" aria-label="Bảng điểm trận đấu">
      <div class="fighter player-fighter">
        <span class="fighter-avatar">T</span>
        <div><small>Bạn</small><strong>${state.playerScore} điểm</strong></div>
      </div>
      <div class="battle-round"><span>Vòng ${round}/${DEMO_TOTAL}</span><strong>VS</strong><small>Đối thủ mô phỏng</small></div>
      <div class="fighter opponent-fighter">
        <div><small>${escapeHtml(opponent.name)} · ${escapeHtml(opponent.rank)}</small><strong>${state.opponentScore} điểm</strong></div>
        <span class="fighter-avatar" style="--avatar-color:${escapeHtml(opponent.color)}">${escapeHtml(opponent.initials)}</span>
      </div>
    </section>`;
}

function optionTemplate(option, index) {
  const selected = state.selectedChoice === index;
  let className = "option";
  let indicator = "";

  if (state.feedback) {
    if (index === state.feedback.correct_choice) {
      className += " is-correct";
      indicator = "✓";
    } else if (selected) {
      className += " is-wrong";
      indicator = "×";
    }
  }

  return `
    <button class="${className}" type="button" data-choice="${index}" aria-pressed="${selected}" ${state.feedback ? "disabled" : ""}>
      <span class="option-key">${LETTERS[index]}</span>
      <span class="option-text">${escapeHtml(option)}</span>
      <span class="option-indicator" aria-hidden="true">${indicator}</span>
    </button>`;
}

function feedbackTemplate() {
  const feedback = state.feedback;
  const title = feedback.correct ? "Chính xác" : "Chưa đúng — xem lại căn cứ";
  return `
    <section class="feedback ${feedback.correct ? "correct" : "incorrect"}" aria-live="polite">
      <div class="feedback-heading">
        <h3>${title}</h3>
        <span class="status-badge">Trang ${escapeHtml(feedback.page)}</span>
      </div>
      <p>${escapeHtml(feedback.explanation)}</p>
      ${state.battleMode ? `<div class="opponent-update ${state.opponentLastCorrect ? "opponent-correct" : "opponent-wrong"}">${escapeHtml(state.opponent.name)} ${state.opponentLastCorrect ? "cũng trả lời đúng · +100 điểm" : "đã trả lời sai vòng này"}</div>` : ""}
    </section>
    <aside class="source-card">
      <div class="source-heading"><strong>Nguồn trong bài học</strong><span>Slide ${escapeHtml(feedback.page)}</span></div>
      <blockquote>“${escapeHtml(feedback.evidence_quote)}”</blockquote>
    </aside>`;
}

function selectChoice(index) {
  if (state.feedback || state.busy) return;
  state.selectedChoice = index;
  renderQuestion();
  const selected = document.querySelector(`[data-choice="${index}"]`);
  selected?.focus();
}

async function submitAnswer() {
  if (state.selectedChoice === null || state.busy) return;
  setBusy(true);
  const choice = state.selectedChoice;
  const answerMs = Math.max(0, Math.round(performance.now() - state.questionStartedAt));
  const answerButton = document.querySelector("#answer-button");
  answerButton.disabled = true;
  answerButton.textContent = "Đang kiểm tra…";

  try {
    if (state.demoMode) {
      await delay(320);
      const correct = choice === state.question._answer;
      state.feedback = {
        correct,
        correct_choice: state.question._answer,
        explanation: state.question._explanation,
        page: state.question.page,
        evidence_quote: state.question._evidence_quote,
        done: state.answered.length + 1 >= DEMO_TOTAL,
        status: "ok",
      };
      state.answered.push({ ...state.question, correct });
      updateBattleScore(correct);
      state.demoCursor += 1;
      state.nextQuestion = state.feedback.done ? null : demoQuestion();
      state.notice = "";
      renderQuestion();
      return;
    }
    const payload = await request("/answer", {
      method: "POST",
      body: JSON.stringify({
        session_id: state.sessionId,
        question_id: state.question.question_id,
        choice,
        answer_ms: answerMs,
      }),
    });
    state.feedback = payload;
    state.nextQuestion = payload.next_question;
    state.answered.push({ ...state.question, correct: payload.correct });
    updateBattleScore(payload.correct);
    state.notice = payload.status === "no_evidence" && payload.next_question
      ? "Chủ đề dự kiến tiếp theo chưa đủ căn cứ; hệ thống đã chọn một chủ đề khác."
      : "";
    renderQuestion();
  } catch (error) {
    showToast(`Chưa gửi được đáp án: ${error.message}`);
    answerButton.disabled = false;
    answerButton.textContent = "Kiểm tra đáp án";
  } finally {
    setBusy(false);
  }
}

function updateBattleScore(playerCorrect) {
  if (!state.battleMode) return;
  if (playerCorrect) state.playerScore += 100;
  const roundIndex = state.answered.length - 1;
  const opponentPattern = [true, false, true, true, false];
  state.opponentLastCorrect = opponentPattern[roundIndex % opponentPattern.length];
  if (state.opponentLastCorrect) state.opponentScore += 100;
}

async function continueAfterFeedback() {
  if (state.busy) return;
  if (state.feedback.done || !state.nextQuestion) {
    await loadResult();
    return;
  }
  state.question = state.nextQuestion;
  state.nextQuestion = null;
  state.feedback = null;
  state.selectedChoice = null;
  state.questionStartedAt = performance.now();
  renderQuestion();
}

async function skipQuestion() {
  if (state.busy) return;
  setBusy(true);
  renderLoading("Đang đổi câu hỏi", "Giữ nguyên chủ đề và mức hiện tại nếu còn đủ căn cứ.");
  try {
    if (state.demoMode) {
      await delay(300);
      state.demoCursor += 1;
      state.question = demoQuestion();
      state.selectedChoice = null;
      state.feedback = null;
      state.notice = "Đã đổi sang một câu mẫu khác. Câu vừa rồi không được tính điểm.";
      state.questionStartedAt = performance.now();
      renderQuestion();
      return;
    }
    const payload = await request("/skip", {
      method: "POST",
      body: JSON.stringify({ session_id: state.sessionId, question_id: state.question.question_id }),
    });
    state.question = payload.question;
    state.selectedChoice = null;
    state.feedback = null;
    state.notice = payload.status === "no_evidence" && payload.question
      ? "Không tạo được câu thay thế cho chủ đề này; hệ thống đã chuyển sang chủ đề khác."
      : "";
    if (!state.question) {
      renderNoEvidence();
      return;
    }
    state.questionStartedAt = performance.now();
    renderQuestion();
  } catch (error) {
    showToast(`Chưa thể đổi câu: ${error.message}`);
    renderQuestion();
  } finally {
    setBusy(false);
  }
}

async function submitReport(reason) {
  if (state.busy) return;
  setBusy(true);
  renderLoading("Đã ghi nhận báo cáo", "Câu này không tính điểm. Hệ thống đang tìm câu thay thế…");
  try {
    if (state.demoMode) {
      await delay(300);
      state.demoCursor += 1;
      state.question = demoQuestion();
      state.selectedChoice = null;
      state.feedback = null;
      state.notice = `Đã ghi nhận báo cáo demo (${reason}). Câu vừa rồi không được tính điểm.`;
      state.questionStartedAt = performance.now();
      renderQuestion();
      return;
    }
    const payload = await request("/report", {
      method: "POST",
      body: JSON.stringify({ session_id: state.sessionId, question_id: state.question.question_id, reason }),
    });
    state.question = payload.question;
    state.selectedChoice = null;
    state.feedback = null;
    state.notice = "Đã ghi nhận báo cáo. Câu vừa rồi không được tính vào kết quả.";
    if (!state.question) {
      renderNoEvidence();
      return;
    }
    state.questionStartedAt = performance.now();
    renderQuestion();
  } catch (error) {
    showToast(`Chưa gửi được báo cáo: ${error.message}`);
    renderQuestion();
  } finally {
    setBusy(false);
  }
}

async function loadResult() {
  if (!state.sessionId || state.busy) return;
  setBusy(true);
  renderLoading("Đang tổng hợp kết quả", "Chỉ kết luận khi lượt luyện có đủ tín hiệu.");
  try {
    if (state.demoMode) {
      await delay(350);
      const wrong = state.answered.find((item) => !item.correct);
      renderResult({
        status: state.answered.length < 3 ? "not_enough_data" : "ok",
        items: state.answered.map((item) => ({
          concept_name: item.concept_name,
          level: item.level,
          correct: item.correct,
        })),
        review_concept: wrong?.concept_name || null,
        page: wrong?.page || null,
        evidence_quote: wrong?._evidence_quote || null,
      });
      return;
    }
    const result = await request(`/session/${encodeURIComponent(state.sessionId)}/result`);
    renderResult(result);
  } catch (error) {
    renderConnectionError(error.message, true);
  } finally {
    setBusy(false);
  }
}

function renderResult(result) {
  if (result.status === "not_enough_data") {
    renderLowConfidence(result);
    return;
  }

  const correct = result.items.filter((item) => item.correct).length;
  const total = result.items.length;
  const summary = total && correct === total
    ? "Bạn đã trả lời đúng toàn bộ câu hỏi trong lượt này."
    : "Kết quả này giúp bạn chọn một điểm bắt đầu cụ thể cho lần ôn tiếp theo.";

  const battleOutcome = state.playerScore > state.opponentScore
    ? { title: "Bạn chiến thắng!", label: "Thắng trận", className: "win" }
    : state.playerScore < state.opponentScore
      ? { title: "Đối thủ thắng sát nút", label: "Kết thúc trận", className: "loss" }
      : { title: "Trận đấu hòa", label: "Ngang tài", className: "draw" };
  updateProfileAfterBattle();
  const resultTitle = state.battleMode ? battleOutcome.title : "Bạn đã về đích.";

  app.innerHTML = `
    <section class="result-card" aria-labelledby="result-title">
      <div class="result-kicker" aria-hidden="true">✓</div>
      ${state.battleMode ? `
        <div class="battle-result ${battleOutcome.className}">
          <div><span class="fighter-avatar">T</span><strong>${state.playerScore}</strong><small>Bạn</small></div>
          <p><span>${battleOutcome.label}</span><b>VS</b><small>Trận thử nghiệm</small></p>
          <div><span class="fighter-avatar" style="--avatar-color:${escapeHtml(state.opponent.color)}">${escapeHtml(state.opponent.initials)}</span><strong>${state.opponentScore}</strong><small>${escapeHtml(state.opponent.name)}</small></div>
        </div>
        <div class="rating-change ${state.lastRatingDelta >= 0 ? "positive" : "negative"}">
          <span>${state.lastRatingDelta >= 0 ? "+" : ""}${state.lastRatingDelta} rating</span>
          <strong>${state.profile.rating}</strong>
          <small>${rankTier(state.profile.rating)} · ${state.profile.streak} chuỗi thắng</small>
        </div>` : ""}
      <div class="result-heading">
        <div>
          <p class="eyebrow">${state.battleMode ? "Hoàn thành trận Solo" : "Hoàn thành lượt luyện"}</p>
          <h1 id="result-title">${resultTitle}</h1>
          <p>${escapeHtml(summary)}</p>
        </div>
        <div class="score-ring" aria-label="${correct} trên ${total} câu đúng"><span>${correct}/${total}</span></div>
      </div>

      <div class="result-list" aria-label="Chi tiết từng câu">
        ${result.items.map((item, index) => `
          <div class="result-row">
            <div><strong>Câu ${index + 1} · ${escapeHtml(item.concept_name)}</strong><small>Mức ${item.level} · ${escapeHtml(LEVEL_NAMES[item.level] || "Luyện tập")}</small></div>
            <span class="result-mark ${item.correct ? "correct" : "incorrect"}" aria-label="${item.correct ? "Đúng" : "Sai"}">${item.correct ? "✓" : "×"}</span>
          </div>`).join("")}
      </div>

      ${result.review_concept ? `
        <aside class="review-card">
          <p class="eyebrow">Nên ôn lại trước</p>
          <h2>${escapeHtml(result.review_concept)}</h2>
          <p>Mở lại slide ${escapeHtml(result.page)} và đối chiếu ý chính dưới đây.</p>
          <blockquote>“${escapeHtml(result.evidence_quote)}”</blockquote>
        </aside>` : `
        <aside class="review-card">
          <p class="eyebrow">Không có điểm yếu nổi bật</p>
          <h2>Bạn đang nắm khá chắc lượt kiến thức này.</h2>
          <p>Hãy thử một lượt khác để kiểm tra thêm các khái niệm còn lại.</p>
        </aside>`}

      <button class="button button-primary button-large button-full" id="restart-button" type="button">${state.battleMode ? "Ghép trận khác" : "Luyện một lượt mới"}</button>
    </section>`;
  document.querySelector("#restart-button").addEventListener("click", state.battleMode ? startBattleMatch : state.demoMode ? () => startDemoSession(false) : () => startSession(false));
  focusApp();
}

function renderLowConfidence(result) {
  const answered = result.items?.length || state.answered.length;
  app.innerHTML = `
    <section class="state-card" aria-labelledby="state-title">
      <div class="state-icon" aria-hidden="true">?</div>
      <p class="eyebrow">Chưa đủ dữ liệu</p>
      <h1 id="state-title">Chưa nên kết luận vội.</h1>
      <p>Bạn đã hoàn thành ${answered} câu, nhưng lượt này chưa có đủ tín hiệu ổn định để xác định phần cần ôn. Kết quả không được dùng để đánh giá năng lực của bạn.</p>
      <button class="button button-primary button-large" id="restart-button" type="button">Làm lượt mới</button>
    </section>`;
  document.querySelector("#restart-button").addEventListener("click", state.battleMode ? startBattleMatch : state.demoMode ? () => startDemoSession(false) : () => startSession(false));
  focusApp();
}

function renderNoEvidence() {
  app.innerHTML = `
    <section class="state-card" aria-labelledby="state-title">
      <div class="state-icon" aria-hidden="true">!</div>
      <p class="eyebrow">Không đủ căn cứ</p>
      <h1 id="state-title">Tạm dừng để không đưa câu sai.</h1>
      <p>Hệ thống chưa tìm được câu hỏi có trích dẫn phù hợp từ slide. Các câu chưa đủ căn cứ sẽ không được hiển thị cho bạn.</p>
      <button class="button button-primary button-large" id="result-button" type="button">Xem phần đã làm</button>
    </section>`;
  document.querySelector("#result-button").addEventListener("click", loadResult);
  focusApp();
}

function renderConnectionError(message, canShowResult = false) {
  app.innerHTML = `
    <section class="state-card" aria-labelledby="state-title">
      <div class="state-icon" aria-hidden="true">×</div>
      <p class="eyebrow">Mất kết nối</p>
      <h1 id="state-title">Chưa thể tiếp tục.</h1>
      <p>${escapeHtml(message)} Kiểm tra backend đang chạy và địa chỉ API đã đúng.</p>
      <button class="button button-primary button-large" id="retry-button" type="button">Kiểm tra lại</button>
      ${canShowResult ? `<button class="text-button" id="back-button" type="button">Quay lại câu hỏi</button>` : ""}
    </section>`;
  document.querySelector("#retry-button").addEventListener("click", async () => {
    const online = await checkHealth();
    if (online) {
      if (state.sessionId && canShowResult) await loadResult();
      else renderStart();
    }
  });
  document.querySelector("#back-button")?.addEventListener("click", renderQuestion);
  focusApp();
}

reportForm.addEventListener("submit", (event) => {
  if (event.submitter?.value !== "default") return;
  event.preventDefault();
  const reason = new FormData(reportForm).get("reason");
  reportDialog.close();
  submitReport(reason);
});

document.querySelector("#api-settings").addEventListener("click", () => {
  apiUrlField.value = state.apiUrl;
  settingsDialog.showModal();
});

settingsForm.addEventListener("submit", async (event) => {
  if (event.submitter?.value !== "default") return;
  event.preventDefault();
  state.apiUrl = apiUrlField.value.trim().replace(/\/$/, "");
  localStorage.setItem("solo-arena-api", state.apiUrl);
  settingsDialog.close();
  const online = await checkHealth();
  if (online) showToast("Đã kết nối API thành công.");
});

document.addEventListener("keydown", (event) => {
  if (reportDialog.open || settingsDialog.open || state.feedback || state.busy || !state.question) return;
  const number = Number(event.key);
  if (number >= 1 && number <= 4) {
    event.preventDefault();
    selectChoice(number - 1);
  } else if (event.key === "Enter" && state.selectedChoice !== null) {
    event.preventDefault();
    submitAnswer();
  }
});

soloNav.addEventListener("click", (event) => {
  event.preventDefault();
  history.replaceState(null, "", `${window.location.pathname}${window.location.search}`);
  renderStart();
});

rankingNav.addEventListener("click", (event) => {
  event.preventDefault();
  history.replaceState(null, "", `${window.location.pathname}${window.location.search}#ranking`);
  renderRanking();
});

if (window.location.hash === "#ranking") renderRanking();
else renderStart();
checkHealth({ quiet: true });
