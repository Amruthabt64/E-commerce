import React, { useContext } from "react";
import { StoreContext } from "../context/StoreContext";
import "../styles/Orders.css";

function Orders() {
  const { orders } = useContext(StoreContext);

  return (
    <div>
      <h2 className="orders-title">Your Orders</h2>
      {orders.length === 0 ? (
        <p className="orders-empty">No orders yet.</p>
      ) : (
        orders.map((order) => (
          <div key={order.id} className="order-card">
            <h3>Order #{order.id}</h3>
            <ul className="order-items">
              {order.items.map((i) => (
                <li key={i.id}>{i.name} - ${i.price}</li>
              ))}
            </ul>
          </div>
        ))
      )}
    </div>
  );
}

export default Orders;
