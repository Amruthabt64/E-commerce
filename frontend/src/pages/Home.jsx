import React, { useContext, useEffect, useState } from "react";
import { StoreContext } from "../context/StoreContext";
import "../styles/Home.css";

function Home() {
  const { addToCart } = useContext(StoreContext);
  const [products, setProducts] = useState([]);

  // Fetch products from backend when page loads
  useEffect(() => {
    fetch("http://localhost:5000/api/products")  // Flask endpoint
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error("Error fetching products:", err));
  }, []);

  return (
    <div>
      <h2 className="home-title">Products</h2>
      <div className="products-grid">
        {products.length === 0 ? (
          <p>Loading products...</p>
        ) : (
          products.map((p) => (
            <div key={p.id} className="product-card">
              <h3>{p.name}</h3>
              <p>${p.price}</p>
              <button onClick={() => addToCart(p)}>Add to Cart</button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Home;
