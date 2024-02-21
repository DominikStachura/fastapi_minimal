import React, { useState } from 'react';

const CreateItem = ({ onCreate }) => {
  const [newItemName, setNewItemName] = useState('');

  const handleCreate = () => {
    onCreate(newItemName);
    setNewItemName('');
  };

  return (
    <div>
      <h2>Create Item</h2>
      <input
        type="text"
        placeholder="Enter item name"
        value={newItemName}
        onChange={(e) => setNewItemName(e.target.value)}
      />
      <button onClick={handleCreate}>Create</button>
    </div>
  );
};

export default CreateItem;