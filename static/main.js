(() => {
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const esc = value => String(value ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const stars = (rating) => "★".repeat(Math.round(rating || 0)) + "☆".repeat(5 - Math.round(rating || 0));

  // Reveal elements as they enter the viewport.
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  $$(".reveal").forEach(el => observer.observe(el));

  // Background responds subtly to scrolling.
  let ticking = false;
  window.addEventListener("scroll", () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      document.documentElement.style.setProperty("--scroll-y", `${window.scrollY * 0.16}px`);
      ticking = false;
    });
  }, { passive: true });

  const menuToggle = $(".menu-toggle");
  if (menuToggle) menuToggle.addEventListener("click", () => $(".nav-links")?.classList.toggle("open"));

  if ($(".home-page")) {
    fetch("/api/stats").then(r => r.json()).then(data => {
      $("#stat-reviews").textContent = data.reviews.toLocaleString();
      $("#stat-items").textContent = data.items.toLocaleString();
      $("#stat-average").textContent = data.reviews ? Number(data.average).toFixed(1) : "–";
    }).catch(() => { });

    // Per-outlet analytics cards
    fetch("/api/analytics").then(r => r.json()).then(data => {
      $("#analytics-grid").innerHTML = data.outlets.map(o => `
        <a class="analytics-card ${esc(o.cover)}" href="/outlet/${esc(o.slug)}">
          <div class="analytics-card-top"><span class="analytics-emoji">${o.emoji}</span><span class="arrow-circle">↗</span></div>
          <h3>${esc(o.name)}</h3>
          <div class="analytics-avg"><strong>${o.reviews ? Number(o.average).toFixed(1) : "–"}</strong><span>/ 5</span></div>
          <div class="stars">${stars(o.average)}</div>
          <div class="analytics-meter"><i data-w="${(Number(o.average) / 5) * 100}"></i></div>
          <div class="analytics-meta"><b>${o.reviews}</b> ${o.reviews === 1 ? "review" : "reviews"}</div>
        </a>`).join("");
      requestAnimationFrame(() => $$("#analytics-grid .analytics-meter i").forEach(i => i.style.width = i.dataset.w + "%"));
    }).catch(() => {
      $("#analytics-grid").innerHTML = `<div class="empty-state">Couldn't load analytics. Check that the Flask server is running.</div>`;
    });

    // Hovering a place card tints the whole page in that place's colour
    const THEMES = ["safal", "nescafe", "canteen", "gym"];
    $$(".place-card").forEach(card => {
      const theme = THEMES.find(t => card.classList.contains(t));
      if (!theme) return;
      const on = () => { document.body.dataset.theme = theme; };
      const off = () => { document.body.dataset.theme = "home"; };
      card.addEventListener("mouseenter", on);
      card.addEventListener("mouseleave", off);
      card.addEventListener("focus", on);
      card.addEventListener("blur", off);
    });
  }

  const page = $(".listing-page");
  if (!page) return;
  const slug = page.dataset.outlet;
  const grid = $("#items-grid");
  let allItems = [], activeCategory = "", selectedRating = 0, activeItem = null;


  function renderItems() {
    const q = ($("#search").value || "").trim().toLowerCase();
    const items = allItems.filter(item =>
      (!activeCategory || item.category === activeCategory) &&
      (!q || item.name.toLowerCase().includes(q) || item.category.toLowerCase().includes(q))
    );
    if (!items.length) {
      grid.innerHTML = `<div class="empty-state">No items found. Try another search.</div>`;
      return;
    }
    grid.innerHTML = items.map(item => `
      <article class="item-card">
        <div class="item-top"><span class="item-category">${esc(item.category)}</span><span class="item-price">${item.price ? "₹" + item.price + "+" : "Facility"}</span></div>
        <h3>${esc(item.name)}</h3>
        <p class="item-note">${esc(item.note || "Tell other students what you think.")}</p>
        <div class="item-rating"><span class="stars">${item.review_count ? stars(item.average_rating) : "☆☆☆☆☆"}</span><span>${item.review_count ? `${Number(item.average_rating).toFixed(1)} · ${item.review_count} reviews` : "No reviews yet"}</span></div>
        <button class="review-item-button" data-id="${item.id}" data-name="${esc(item.name)}">Rate & review <span>↗</span></button>
      </article>`).join("");
    $$(".review-item-button", grid).forEach(btn => btn.addEventListener("click", () => openReview(Number(btn.dataset.id), btn.dataset.name)));
  }

  function renderFilters(categories) {
    $("#filters").innerHTML = `<button class="filter-chip active" data-category="">All items</button>` +
      categories.map(c => `<button class="filter-chip" data-category="${esc(c)}">${esc(c)}</button>`).join("");
    $$(".filter-chip").forEach(btn => btn.addEventListener("click", () => {
      activeCategory = btn.dataset.category;
      $$(".filter-chip").forEach(b => b.classList.toggle("active", b === btn));
      renderItems();
    }));
  }

  async function loadAnalytics() {
    try {
      const a = await (await fetch(`/api/analytics/${slug}`)).json();
      const has = a.total_reviews > 0;
      const avg = Number(a.average) || 0;
      $("#avg-big").textContent = has ? avg.toFixed(1) : "–";
      $("#avg-stars").textContent = has ? stars(avg) : "☆☆☆☆☆";
      $("#avg-sub").textContent = has ? `from ${a.total_reviews} student review${a.total_reviews === 1 ? "" : "s"}` : "No reviews yet. Be the first to rate something.";
      $("#avg-rating").textContent = has ? avg.toFixed(1) : "—";
      $("#review-count").textContent = a.total_reviews;

      const max = Math.max(1, ...Object.values(a.distribution));
      $("#rating-bars").innerHTML = [5, 4, 3, 2, 1].map(n => `
        <div class="bar-row"><span>${n} ★</span><div class="bar"><i data-w="${(a.distribution[n] / max) * 100}"></i></div><b>${a.distribution[n]}</b></div>`).join("");
      requestAnimationFrame(() => $$("#rating-bars .bar i").forEach(i => i.style.width = i.dataset.w + "%"));

      $("#top-items").innerHTML = a.top_items.length
        ? a.top_items.map(i => `<li><span>${esc(i.name)}</span><b>${Number(i.average).toFixed(1)} ★ · ${i.reviews}</b></li>`).join("")
        : `<li class="muted">No reviews yet</li>`;
    } catch { }
  }

  async function loadItems() {
    try {
      const response = await fetch(`/api/items/${slug}`);
      const data = await response.json();
      allItems = data.items;
      $("#total-count").textContent = allItems.length;
      $("#review-count").textContent = allItems.reduce((sum, item) => sum + item.review_count, 0);
      renderFilters(data.categories);
      renderItems();
      loadAnalytics();
    } catch {
      grid.innerHTML = `<div class="empty-state">Couldn't load the menu. Check that the Flask server is running.</div>`;
    }
  }
  $("#search").addEventListener("input", renderItems);

  const modal = $("#review-modal");
  function openReview(id, name) {
    activeItem = id; selectedRating = 0;
    $("#item-id").value = id; $("#modal-item").innerHTML = `${esc(name)}<span class="gradient-text">.</span>`;
    $("#form-message").textContent = "";
    $("#review-comment").value = "";
    $$(".star-picker button").forEach(b => b.classList.remove("selected"));
    $("#existing-reviews").innerHTML = "";
    modal.classList.add("show"); modal.setAttribute("aria-hidden", "false");
    fetch(`/api/reviews/${id}`).then(r => r.json()).then(reviews => {
      if (!reviews.length) return;
      $("#existing-reviews").innerHTML = `<h3>Recent student reviews</h3>` + reviews.map(r => `
        <div class="review-entry"><div><b>${esc(r.student_name)}</b><span class="stars">${stars(r.rating)}</span></div><p>${esc(r.comment)}</p><small>${esc(r.created_at)}</small></div>`).join("");
    }).catch(() => { });
  }
  function closeModal() { modal.classList.remove("show"); modal.setAttribute("aria-hidden", "true"); }
  $("#close-modal").addEventListener("click", closeModal);
  modal.addEventListener("click", e => { if (e.target === modal) closeModal(); });
  document.addEventListener("keydown", e => { if (e.key === "Escape") closeModal(); });
  $$(".star-picker button").forEach(btn => btn.addEventListener("click", () => {
    selectedRating = Number(btn.dataset.rating);
    $$(".star-picker button").forEach(b => b.classList.toggle("selected", Number(b.dataset.rating) <= selectedRating));
  }));

  $("#review-form").addEventListener("submit", async e => {
    e.preventDefault();
    const message = $("#form-message");
    if (!selectedRating) { message.textContent = "Please select a star rating."; return; }
    const button = $(".submit-review"); button.disabled = true; button.innerHTML = "Posting…";
    try {
      const response = await fetch("/api/reviews", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ item_id: activeItem, student_name: $("#student-name").value, rating: selectedRating, comment: $("#review-comment").value })
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Something went wrong.");
      message.textContent = result.message; message.className = "form-message success";
      await loadItems();
      setTimeout(closeModal, 1000);
    } catch (err) { message.textContent = err.message; message.className = "form-message error"; }
    finally { button.disabled = false; button.innerHTML = 'Post review <span>↗</span>'; }
  });
  loadItems();
})();