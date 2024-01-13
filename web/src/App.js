// src/App.js
import React, { useState, useEffect } from 'react';
import ItemList from './components/ItemList';
import CreateItem from './components/CreateItem';
import api from './services/api';

const App = () => {
  const [items, setItems] = useState([]);

  useEffect(() => {
    // Fetch all items on component mount
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      const itemsData = await api.getItems();
      setItems(itemsData);
    } catch (error) {
      console.error('Error fetching items:', error);
    }
  };

  const createItem = async (name) => {
    try {
      await api.createItem(name);
      // After creating, fetch the updated list
      fetchItems();
    } catch (error) {
      console.error('Error creating item:', error);
    }
  };

  const updateItem = async (itemId, isActive) => {
    try {
      await api.updateItem(itemId, isActive);
      // After updating, fetch the updated list
      fetchItems();
    } catch (error) {
      console.error('Error updating item:', error);
    }
  };

  const deleteItem = async (itemId) => {
    try {
      await api.deleteItem(itemId);
      // After deleting, fetch the updated list
      fetchItems();
    } catch (error) {
      console.error('Error deleting item:', error);
    }
  };

  return (
    <div>
      <h1>FastAPI React Frontend</h1>
      <CreateItem onCreate={createItem} />
      <ItemList items={items} onUpdate={updateItem} onDelete={deleteItem} />
    </div>
  );
};

export default App;
