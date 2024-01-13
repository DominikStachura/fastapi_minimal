import React from 'react';

const Item = ({ item, onUpdate, onDelete }) => {
  return (
    <li>
      {item.name} - {item.is_active ? 'Active' : 'Inactive'}
      <button onClick={() => onUpdate(item.id, !item.is_active)}>
        {item.is_active ? 'Deactivate' : 'Activate'}
      </button>
      <button onClick={() => onDelete(item.id)}>Delete</button>
    </li>
  );
};

export default Item;
