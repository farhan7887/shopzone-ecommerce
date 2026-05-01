/* ═══════════════════════════════════════════════
   ShopZone — Main JavaScript
   ═══════════════════════════════════════════════ */

const API = 'https://shopzone-ecommerce-production.up.railway.app/api';
// ── Auth Helpers ─────────────────────────────────
const Auth = {
  getToken:  ()      => localStorage.getItem('sz_token'),
  getUser:   ()      => JSON.parse(localStorage.getItem('sz_user') || 'null'),
  setSession:(token, user) => {
    localStorage.setItem('sz_token', token);
    localStorage.setItem('sz_user', JSON.stringify(user));
  },
  clear:     ()      => {
    localStorage.removeItem('sz_token');
    localStorage.removeItem('sz_user');
  },
  isLoggedIn:()      => !!localStorage.getItem('sz_token'),
  isAdmin:   ()      => {
    const u = Auth.getUser();
    return u && u.role === 'admin';
  }
};

// ── HTTP Helpers ─────────────────────────────────
async function apiFetch(endpoint, options = {}) {
  const token = Auth.getToken();
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(API + endpoint, { headers, ...options });
  const data = await res.json().catch(() => ({}));

  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data;
}

const api = {
  get:    (url)          => apiFetch(url),
  post:   (url, body)    => apiFetch(url, { method: 'POST',   body: JSON.stringify(body) }),
  put:    (url, body)    => apiFetch(url, { method: 'PUT',    body: JSON.stringify(body) }),
  delete: (url)          => apiFetch(url, { method: 'DELETE' }),
};

// ── Toast Notifications ───────────────────────────
function toast(msg, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const icons = { success: '✅', error: '❌', info: 'ℹ️' };
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.innerHTML = `<span>${icons[type]}</span><span>${msg}</span>`;
  container.appendChild(el);

  setTimeout(() => { el.style.opacity = '0'; el.style.transform = 'translateX(100%)';
    setTimeout(() => el.remove(), 300); }, 3500);
}

// ── Format Price (PKR) ───────────────────────────
function formatPrice(amount) {
  return 'PKR ' + Number(amount).toLocaleString('en-PK');
}

// ── Cart Badge ────────────────────────────────────
async function updateCartBadge() {
  if (!Auth.isLoggedIn()) return;
  try {
    const items = await api.get('/cart/');
    const badge = document.getElementById('cart-badge');
    const total = items.reduce((s, i) => s + i.quantity, 0);
    if (badge) badge.textContent = total > 0 ? total : '';
  } catch (_) {}
}

// ── Navbar Renderer ───────────────────────────────
function renderNav(activePage = '') {
  const user = Auth.getUser();
  const nav  = document.getElementById('navbar');
  if (!nav) return;

  nav.innerHTML = `
    <a href="index.html" class="nav-logo">Shop<span>Zone</span></a>
    <div class="nav-search">
      <span class="search-icon">🔍</span>
      <input type="text" id="nav-search-input" placeholder="Search products…" value="${getSearchParam()}">
    </div>
    <div class="nav-links">
      <a href="index.html" ${activePage==='home'?'style="color:var(--accent)"':''}>Home</a>
      ${user ? `
        <a href="orders.html" ${activePage==='orders'?'style="color:var(--accent)"':''}>My Orders</a>
        ${user.role === 'admin' ? `<a href="admin/dashboard.html" style="color:var(--info)">⚙ Admin</a>` : ''}
        <div class="nav-user" onclick="handleLogout()">👤 ${user.name.split(' ')[0]} &nbsp;·&nbsp; Logout</div>
      ` : `
        <a href="login.html">Login</a>
        <a href="register.html" class="btn btn-outline btn-sm">Sign Up</a>
      `}
      <a href="cart.html" class="nav-cart">
        🛒 Cart
        <span class="cart-badge" id="cart-badge"></span>
      </a>
    </div>
  `;

  // Search handler
  const searchInput = document.getElementById('nav-search-input');
  if (searchInput) {
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        window.location.href = `index.html?search=${encodeURIComponent(searchInput.value)}`;
      }
    });
  }

  updateCartBadge();
}

function getSearchParam() {
  return new URLSearchParams(window.location.search).get('search') || '';
}

function handleLogout() {
  Auth.clear();
  toast('Logged out successfully', 'info');
  setTimeout(() => window.location.href = 'index.html', 800);
}

// ── Render Footer ─────────────────────────────────
function renderFooter() {
  const footer = document.getElementById('footer');
  if (!footer) return;
  footer.innerHTML = `
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="nav-logo">Shop<span style="color:var(--white)">Zone</span></div>
        <p>Your premium destination for electronics, fashion, books, and everything in between.</p>
      </div>
      <div class="footer-col">
        <h4>Shop</h4>
        <a href="index.html?category=Electronics">Electronics</a>
        <a href="index.html?category=Clothing">Clothing</a>
        <a href="index.html?category=Footwear">Footwear</a>
        <a href="index.html?category=Books">Books</a>
      </div>
      <div class="footer-col">
        <h4>Account</h4>
        <a href="login.html">Login</a>
        <a href="register.html">Register</a>
        <a href="orders.html">My Orders</a>
        <a href="cart.html">My Cart</a>
      </div>
      <div class="footer-col">
        <h4>Support</h4>
        <a href="#">Help Center</a>
        <a href="#">Returns</a>
        <a href="#">Track Order</a>
        <a href="#">Contact Us</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 ShopZone. All rights reserved.</span>
      <span>Built with ❤️ · COMSATS University · CSC101</span>
    </div>
  `;
}

// ── Product Card HTML ─────────────────────────────
function productCardHTML(product) {
  const isNew = (Date.now() - new Date(product.created_at)) < 7 * 86400000;
  return `
    <div class="product-card" onclick="window.location='product.html?id=${product.id}'">
      ${isNew ? `<span class="product-badge">New</span>` : ''}
      <div class="product-img">
        <img src="${product.image || 'https://images.unsplash.com/photo-1560393464-5c69a73c5770?w=400'}"
             alt="${product.name}" loading="lazy"
             onerror="this.src='https://images.unsplash.com/photo-1560393464-5c69a73c5770?w=400'">
      </div>
      <div class="product-info">
        <div class="product-category">${product.category}</div>
        <div class="product-name">${product.name}</div>
        <div class="product-price">${formatPrice(product.price)}</div>
        <div class="product-stock">${product.stock > 0 ? `${product.stock} in stock` : '⚠ Out of stock'}</div>
      </div>
      <div class="product-actions">
        <button class="btn btn-primary btn-sm" style="flex:1"
          onclick="event.stopPropagation(); addToCart(${product.id})"
          ${product.stock === 0 ? 'disabled' : ''}>
          🛒 Add to Cart
        </button>
      </div>
    </div>
  `;
}

// ── Add to Cart ────────────────────────────────────
async function addToCart(productId, quantity = 1) {
  if (!Auth.isLoggedIn()) {
    toast('Please login to add items to cart', 'error');
    setTimeout(() => window.location.href = 'login.html', 1000);
    return;
  }
  try {
    await api.post('/cart/', { product_id: productId, quantity });
    toast('Added to cart! 🛒', 'success');
    updateCartBadge();
  } catch (err) {
    toast(err.message, 'error');
  }
}

// ── Status Badge HTML ─────────────────────────────
function statusBadge(status) {
  const icons = { pending: '⏳', processing: '⚙️', shipped: '📦', delivered: '✅', cancelled: '❌' };
  return `<span class="status-badge status-${status}">${icons[status] || ''} ${status}</span>`;
}
