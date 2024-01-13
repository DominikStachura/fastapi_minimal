import React from 'react';
import Item from './Item';

const ItemList = ({ items, onUpdate, onDelete }) => {
  return (
    <div>
      <h2>Items List</h2>
      <ul>
        {items.map((item) => (
          <Item key={item.id} item={item} onUpdate={onUpdate} onDelete={onDelete} />
        ))}
      </ul>
    </div>
  );
};

export default ItemList;