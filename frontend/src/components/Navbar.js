import { NavLink } from "react-router-dom";

const Navbar = () => (
  <nav>
    <div className="nav-inner">
      <div className="nav-brand">CodeSphere</div>

      <div className="nav-links">
        <NavLink to="/">Home</NavLink>
        <NavLink to="/analysis">Analysis</NavLink>
        <NavLink to="/system">System</NavLink>
        <NavLink to="/risk">Risk</NavLink>
        <NavLink to="/terms">Terms</NavLink>
      </div>
    </div>
  </nav>
);

export default Navbar;
