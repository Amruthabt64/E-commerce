import React, { createContext, useState, useEffect } from "react";

export const StoreContext = createContext();

export const StoreProvider = ({ children }) => {
  const [cart, setCart] = useState([]);
  const [orders, setOrders] = useState([]);
  const [user, setUser] = useState(null);

  // Restore user from localStorage on mount
  useEffect(() => {
    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");
    if (token && username) {
      setUser({ username });
    }
  }, []);

  const addToCart = (product) => setCart((prev) => [...prev, product]);
  const removeFromCart = (id) => setCart((prev) => prev.filter((p) => p.id !== id));
  const placeOrder = () => { setOrders([...orders, { id: Date.now(), items: cart }]); setCart([]); };
  const logout = () => { setUser(null); localStorage.removeItem("token"); localStorage.removeItem("username"); };

  return (
    <StoreContext.Provider value={{ cart, orders, user, setUser, addToCart, removeFromCart, placeOrder, logout }}>
      {children}
    </StoreContext.Provider>
  );
};
