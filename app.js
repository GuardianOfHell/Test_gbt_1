const cart = new Map();
const cartList = document.querySelector('[data-cart-items]');
const cartTotal = document.querySelector('[data-cart-total]');
const cartCount = document.querySelector('[data-cart-count]');

const formatPrice = (value) => `₴${value.toFixed(0)}`;

const updateCartUI = () => {
  cartList.innerHTML = '';
  let total = 0;
  let count = 0;

  if (cart.size === 0) {
    cartList.innerHTML = '<p class="cart__empty">Кошик порожній. Додайте джерки до замовлення.</p>';
  }

  cart.forEach((item) => {
    total += item.price * item.qty;
    count += item.qty;

    const row = document.createElement('div');
    row.className = 'cart__row';
    row.innerHTML = `
      <div>
        <strong>${item.name}</strong>
        <p>${item.note}</p>
      </div>
      <div class="cart__qty">
        <button type="button" data-action="decrease" data-id="${item.id}">−</button>
        <span>${item.qty}</span>
        <button type="button" data-action="increase" data-id="${item.id}">+</button>
      </div>
      <div class="cart__price">${formatPrice(item.price * item.qty)}</div>
    `;
    cartList.appendChild(row);
  });

  cartTotal.textContent = formatPrice(total);
  cartCount.textContent = count;
};

const addToCart = (product) => {
  const current = cart.get(product.id);
  if (current) {
    current.qty += 1;
  } else {
    cart.set(product.id, { ...product, qty: 1 });
  }
  updateCartUI();
};

const changeQty = (id, delta) => {
  const item = cart.get(id);
  if (!item) return;

  item.qty += delta;
  if (item.qty <= 0) {
    cart.delete(id);
  }
  updateCartUI();
};

const products = document.querySelectorAll('[data-product]');
products.forEach((card) => {
  const id = card.dataset.id;
  const name = card.dataset.name;
  const note = card.dataset.note;
  const price = Number(card.dataset.price);

  card.querySelector('button').addEventListener('click', () => {
    addToCart({ id, name, note, price });
  });
});

cartList.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLButtonElement)) return;

  const { action, id } = target.dataset;
  if (!action || !id) return;

  changeQty(id, action === 'increase' ? 1 : -1);
});

updateCartUI();
