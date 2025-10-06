import React, { createContext, useState } from "react";

export const StoreContext = createContext();

export const StoreProvider = ({ children }) => {
  const [cart, setCart] = useState([]);
  const [orders, setOrders] = useState([]);
  const [user, setUser] = useState(null);

  // Cart Logic
  const addToCart = (product) => {
    setCart((prev) => [...prev, product]);
  };

  const removeFromCart = (id) => {
    setCart((prev) => prev.filter((p) => p.id !== id));
  };

  const placeOrder = () => {
    setOrders((prev) => [...prev, { id: Date.now(), items: cart }]);
    setCart([]);
  };

  // User Logic
  const login = (username, password) => {
    if (username === "user" && password === "pass") {
      setUser({ username });
      return true;
    }
    return false;
  };

  const logout = () => setUser(null);

  return (
    <StoreContext.Provider
      value={{
        cart,
        orders,
        user,
        addToCart,
        removeFromCart,
        placeOrder,
        login,
        logout,
      }}
    >
      {children}
    </StoreContext.Provider>
  );
};
