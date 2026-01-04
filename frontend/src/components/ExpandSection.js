import { useState } from "react";

const ExpandSection = ({ title, children }) => {
  const [open, setOpen] = useState(false);

  return (
    <div className="expand-box">
      <h3>{title}</h3>

      {!open && (
        <button onClick={() => setOpen(true)}>
          Read Full Explanation
        </button>
      )}

      {open && (
        <div className="expand-content">
          {children}
        </div>
      )}
    </div>
  );
};

export default ExpandSection;
