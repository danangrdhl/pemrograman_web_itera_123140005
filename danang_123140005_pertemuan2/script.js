/* ==========================================================
   Dashboard Mahasiswa ITERA
   Praktikum Pemrograman Aplikasi Web, Pertemuan 2 (ES6+)
   ========================================================== */
"use strict";

// ---------- Konstanta ----------
const STORAGE_KEY = "dashboardMahasiswa.tasks";
const SEEDED_KEY = "dashboardMahasiswa.seeded";

const API_URL = {
  weather: "https://api.open-meteo.com/v1/forecast?latitude=-5.36&longitude=105.31&current_weather=true",
  quote: "https://dummyjson.com/quotes/random",
  todos: "https://jsonplaceholder.typicode.com/todos?_limit=5",
};

const WEATHER_CODE = {
  0: ["Cerah", "☀️"],
  1: ["Cerah berawan", "🌤️"],
  2: ["Berawan sebagian", "⛅"],
  3: ["Berawan", "☁️"],
  45: ["Berkabut", "🌫️"],
  48: ["Berkabut", "🌫️"],
  51: ["Gerimis ringan", "🌦️"],
  53: ["Gerimis", "🌦️"],
  55: ["Gerimis lebat", "🌧️"],
  61: ["Hujan ringan", "🌧️"],
  63: ["Hujan sedang", "🌧️"],
  65: ["Hujan lebat", "🌧️"],
  80: ["Hujan lokal ringan", "🌦️"],
  81: ["Hujan lokal", "🌧️"],
  82: ["Hujan lokal deras", "⛈️"],
  95: ["Badai petir", "⛈️"],
  96: ["Badai petir dan es", "⛈️"],
  99: ["Badai petir dan es", "⛈️"],
};

const PRIORITY_LABEL = { tinggi: "Tinggi", sedang: "Sedang", rendah: "Rendah" };
const PRIORITY_ORDER = { tinggi: 0, sedang: 1, rendah: 2 };

// ---------- Fungsi bantu (arrow functions) ----------
const $ = (selector) => document.querySelector(selector);

const escapeHtml = (text) =>
  String(text).replace(/[&<>"']/g, (char) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]
  ));

const generateId = () => `t-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`;

const formatTanggal = (iso) =>
  iso
    ? new Date(`${iso}T00:00:00`).toLocaleDateString("id-ID", { day: "numeric", month: "short", year: "numeric" })
    : "Tanpa tenggat";

const describeWeather = (code) => {
  const [label, icon] = WEATHER_CODE[code] ?? ["Kondisi tidak diketahui", "🌡️"];
  return { label, icon };
};

const capitalize = (text) => text.charAt(0).toUpperCase() + text.slice(1);

// Fungsi asinkron (async/await) untuk mengambil data dari API publik
const fetchJSON = async (url) => {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
};

// ---------- Class TaskItem: model data satu tugas ----------
class TaskItem {
  constructor({
    id = generateId(),
    title,
    course = "Umum",
    deadline = "",
    priority = "sedang",
    done = false,
    createdAt = Date.now(),
  }) {
    this.id = id;
    this.title = title;
    this.course = course;
    this.deadline = deadline;
    this.priority = priority;
    this.done = done;
    this.createdAt = createdAt;
  }

  get isOverdue() {
    if (!this.deadline || this.done) return false;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return new Date(`${this.deadline}T00:00:00`) < today;
  }

  // Mengembalikan TaskItem baru (immutable) dengan perubahan yang diberikan
  with(changes) {
    return new TaskItem({ ...this.toJSON(), ...changes });
  }

  toJSON() {
    const { id, title, course, deadline, priority, done, createdAt } = this;
    return { id, title, course, deadline, priority, done, createdAt };
  }

  static fromJSON(data) {
    return new TaskItem(data);
  }
}

// ---------- Class DashboardApp: state, localStorage, fetch, render ----------
class DashboardApp {
  constructor() {
    this.tasks = [];
    this.filter = "semua";
    this.editingId = null;

    this.els = {
      greeting: $("#greeting"),
      tanggal: $("#tanggal"),
      jam: $("#jam"),
      weather: $("#weather"),
      quote: $("#quote"),
      btnQuote: $("#btn-quote"),
      stats: $("#stats"),
      form: $("#task-form"),
      formTitle: $("#form-title"),
      inputTitle: $("#input-title"),
      formError: $("#form-error"),
      btnSubmit: $("#btn-submit"),
      btnCancel: $("#btn-cancel"),
      btnClear: $("#btn-clear"),
      list: $("#task-list"),
      filterBtns: document.querySelectorAll(".filter-btn"),
      toast: $("#toast"),
    };
  }

  async init() {
    this.loadTasks();
    this.bindEvents();
    this.startClock();
    this.render();
    await Promise.all([this.loadWeather(), this.loadQuote(), this.seedIfFirstRun()]);
  }

  // ----- localStorage -----
  loadTasks() {
    try {
      const raw = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "[]");
      this.tasks = Array.isArray(raw) ? raw.map(TaskItem.fromJSON) : [];
    } catch (error) {
      this.tasks = [];
    }
  }

  saveTasks() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(this.tasks));
  }

  // Semua perubahan state lewat satu pintu agar selalu tersimpan dan dirender
  setTasks(newTasks) {
    this.tasks = newTasks;
    this.saveTasks();
    this.render();
  }

  // ----- Operasi data (immutable dengan spread) -----
  addTask({ title, course, deadline, priority }) {
    const task = new TaskItem({ title, course: course || "Umum", deadline, priority });
    this.setTasks([...this.tasks, task]);
  }

  updateTask(id, changes) {
    this.setTasks(this.tasks.map((task) => (task.id === id ? task.with(changes) : task)));
  }

  deleteTask(id) {
    this.setTasks(this.tasks.filter((task) => task.id !== id));
  }

  toggleTask(id) {
    const target = this.tasks.find((task) => task.id === id);
    if (target) this.updateTask(id, { done: !target.done });
  }

  // ----- Data dari API publik (async/await) -----
  async loadWeather() {
    const { weather } = this.els;
    try {
      const { current_weather: { temperature, windspeed, weathercode } } = await fetchJSON(API_URL.weather);
      const { label, icon } = describeWeather(weathercode);
      weather.innerHTML = `
        <div class="weather-main">
          <span class="weather-icon">${icon}</span>
          <div>
            <div class="weather-temp">${temperature}°C</div>
            <div>${label}</div>
          </div>
        </div>
        <p class="muted">Angin ${windspeed} km/jam, Lampung Selatan</p>`;
    } catch (error) {
      weather.innerHTML = `<p class="muted">Cuaca belum bisa dimuat (${escapeHtml(error.message)}).</p>`;
    }
  }

  async loadQuote() {
    const { quote } = this.els;
    try {
      const { quote: text, author } = await fetchJSON(API_URL.quote);
      quote.innerHTML = `
        <p class="quote-text">"${escapeHtml(text)}"</p>
        <p class="quote-author">${escapeHtml(author)}</p>`;
    } catch (error) {
      quote.innerHTML = `<p class="muted">Kutipan belum bisa dimuat (${escapeHtml(error.message)}).</p>`;
    }
  }

  // Saat pertama kali dibuka, isi daftar tugas dari JSONPlaceholder
  async seedIfFirstRun() {
    if (localStorage.getItem(SEEDED_KEY)) return;
    if (this.tasks.length > 0) {
      localStorage.setItem(SEEDED_KEY, "1");
      return;
    }
    try {
      const todos = await fetchJSON(API_URL.todos);
      const seeded = todos.map(({ title, completed }) =>
        new TaskItem({ title: capitalize(title), course: "Contoh dari API", done: completed })
      );
      this.setTasks(seeded);
      localStorage.setItem(SEEDED_KEY, "1");
      this.showToast("Daftar awal dimuat dari JSONPlaceholder");
    } catch (error) {
      this.showToast("Data contoh gagal dimuat, kamu bisa mulai dari kosong");
    }
  }

  // ----- Event -----
  bindEvents() {
    const { form, list, filterBtns, btnCancel, btnClear, btnQuote, inputTitle } = this.els;

    form.addEventListener("submit", (event) => this.handleSubmit(event));
    btnCancel.addEventListener("click", () => this.cancelEdit());
    btnQuote.addEventListener("click", () => this.loadQuote());

    btnClear.addEventListener("click", () => {
      const remaining = this.tasks.filter(({ done }) => !done);
      if (remaining.length === this.tasks.length) {
        this.showToast("Belum ada tugas yang selesai");
        return;
      }
      if (confirm("Hapus semua tugas yang sudah selesai?")) this.setTasks(remaining);
    });

    filterBtns.forEach((btn) =>
      btn.addEventListener("click", () => {
        this.filter = btn.dataset.filter;
        this.render();
      })
    );

    list.addEventListener("click", (event) => {
      const button = event.target.closest("[data-action]");
      if (!button) return;
      const { action, id } = button.dataset;

      if (action === "toggle") this.toggleTask(id);
      if (action === "edit") this.startEdit(id);
      if (action === "delete" && confirm("Hapus tugas ini?")) {
        if (this.editingId === id) this.cancelEdit();
        this.deleteTask(id);
      }
    });

    inputTitle.addEventListener("input", () => this.setFormError(""));
  }

  handleSubmit(event) {
    event.preventDefault();
    const { title = "", course = "", deadline = "", priority = "sedang" } =
      Object.fromEntries(new FormData(this.els.form));
    const data = { title: title.trim(), course: course.trim(), deadline, priority };

    if (data.title.length < 3) {
      this.setFormError("Judul tugas wajib diisi, minimal 3 karakter.");
      return;
    }

    if (this.editingId) {
      this.updateTask(this.editingId, { ...data, course: data.course || "Umum" });
      this.showToast("Tugas berhasil diperbarui");
      this.cancelEdit();
    } else {
      this.addTask(data);
      this.showToast("Tugas berhasil ditambahkan");
      this.els.form.reset();
    }
    this.setFormError("");
  }

  startEdit(id) {
    const task = this.tasks.find((item) => item.id === id);
    if (!task) return;
    const { form, formTitle, btnSubmit, btnCancel, inputTitle } = this.els;

    this.editingId = id;
    form.elements.title.value = task.title;
    form.elements.course.value = task.course;
    form.elements.deadline.value = task.deadline;
    form.elements.priority.value = task.priority;
    formTitle.textContent = "Edit Tugas";
    btnSubmit.textContent = "Simpan Perubahan";
    btnCancel.hidden = false;
    inputTitle.focus();
    form.scrollIntoView?.({ behavior: "smooth", block: "center" });
  }

  cancelEdit() {
    const { form, formTitle, btnSubmit, btnCancel } = this.els;
    this.editingId = null;
    form.reset();
    formTitle.textContent = "Tambah Tugas Kuliah";
    btnSubmit.textContent = "Tambah Tugas";
    btnCancel.hidden = true;
    this.setFormError("");
  }

  setFormError(message) {
    this.els.formError.textContent = message;
    this.els.inputTitle.classList.toggle("invalid", Boolean(message));
  }

  showToast(message) {
    const { toast } = this.els;
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(this.toastTimer);
    this.toastTimer = setTimeout(() => toast.classList.remove("show"), 2600);
  }

  // ----- Jam & sapaan -----
  startClock() {
    const tick = () => {
      const now = new Date();
      const hour = now.getHours();
      let sapaan = "Selamat malam Danang"; // let: nilainya berubah sesuai jam
      if (hour < 11) sapaan = "Selamat pagi Danang";
      else if (hour < 15) sapaan = "Selamat siang Danang";
      else if (hour < 18) sapaan = "Selamat sore Danang";

      this.els.greeting.textContent = `${sapaan}, semangat kuliahnya!`;
      this.els.tanggal.textContent = now.toLocaleDateString("id-ID", {
        weekday: "long", day: "numeric", month: "long", year: "numeric",
      });
      this.els.jam.textContent = now.toLocaleTimeString("id-ID", { hour12: false }).replace(/\./g, ":");
    };
    tick();
    setInterval(tick, 1000);
  }

  // ----- Render -----
  getVisibleTasks() {
    const filtered = this.tasks.filter(({ done }) =>
      this.filter === "aktif" ? !done : this.filter === "selesai" ? done : true
    );

    return [...filtered].sort((a, b) => {
      if (a.done !== b.done) return a.done ? 1 : -1;
      if (a.deadline !== b.deadline) {
        if (!a.deadline) return 1;
        if (!b.deadline) return -1;
        return a.deadline.localeCompare(b.deadline);
      }
      return PRIORITY_ORDER[a.priority] - PRIORITY_ORDER[b.priority];
    });
  }

  taskTemplate({ id, title, course, deadline, priority, done, isOverdue }) {
    return `
      <li class="task prio-${priority} ${done ? "done" : ""}">
        <input type="checkbox" data-action="toggle" data-id="${id}" ${done ? "checked" : ""} aria-label="Tandai selesai">
        <div>
          <div class="task-title">${escapeHtml(title)}</div>
          <div class="task-meta">
            <span>📚 ${escapeHtml(course)}</span>
            <span>📅 ${formatTanggal(deadline)}</span>
            <span class="badge">Prioritas ${PRIORITY_LABEL[priority] ?? priority}</span>
            ${isOverdue ? '<span class="badge overdue">Terlambat</span>' : ""}
          </div>
        </div>
        <div class="task-actions">
          <button type="button" class="icon-btn" data-action="edit" data-id="${id}">Edit</button>
          <button type="button" class="icon-btn delete" data-action="delete" data-id="${id}">Hapus</button>
        </div>
      </li>`;
  }

  renderTasks() {
    const visible = this.getVisibleTasks();
    this.els.list.innerHTML = visible.length
      ? visible.map((task) => this.taskTemplate(task)).join("")
      : `<li class="empty">Belum ada tugas di kategori ini.</li>`;

    this.els.filterBtns.forEach((btn) =>
      btn.classList.toggle("active", btn.dataset.filter === this.filter)
    );
  }

  renderStats() {
    const total = this.tasks.length;
    const selesai = this.tasks.filter(({ done }) => done).length;
    const terlambat = this.tasks.filter(({ isOverdue }) => isOverdue).length;
    const persen = total === 0 ? 0 : Math.round((selesai / total) * 100);

    this.els.stats.innerHTML = `
      <div class="progress-number">${persen}%</div>
      <div class="progress-bar"><div class="progress-fill" style="width:${persen}%"></div></div>
      <p class="stat-line"><strong>${selesai}</strong> dari <strong>${total}</strong> tugas selesai</p>
      <p class="stat-line"><strong>${terlambat}</strong> tugas melewati tenggat</p>`;
  }

  render() {
    this.renderTasks();
    this.renderStats();
  }
}

// ---------- Inisialisasi ----------
const app = new DashboardApp();
app.init();
