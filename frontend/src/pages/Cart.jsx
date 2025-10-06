import React, { useContext } from "react";
import { StoreContext } from "../context/StoreContext";
import "../styles/Cart.css";

function Cart() {
  const { cart, removeFromCart, placeOrder } = useContext(StoreContext);

  return (
    <div>
      <h2 className="cart-title">Your Cart</h2>
      {cart.length === 0 ? (
        <p className="cart-empty">No items in cart.</p>
      ) : (
        <div>
          {cart.map((item) => (
            <div key={item.id} className="cart-item">
              <span>{item.name} - ${item.price}</span>
              <button onClick={() => removeFromCart(item.id)}>
                Remove
              </button>
            </div>
          ))}
          <button onClick={placeOrder} className="place-order-btn">
            Place Order
          </button>
        </div>
      )}
    </div>
  );
}

export default Cart;
