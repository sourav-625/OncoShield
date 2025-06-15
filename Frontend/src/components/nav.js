import React from 'react';
import { Link } from 'react-router-dom';

const Nav = () => {
    return (
        <nav className="navbar navbar-expand-lg bg-body-tertiary">

            <div className="container-fluid">
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        <li className="nav-item">
                        <Link
                                to="/"
                                className="nav-link"
                                role="button"
                                aria-expanded="false"
                            >
                                Home
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link
                                to="/Devices"
                                className="nav-link"
                                role="button"
                                aria-expanded="false"
                            >
                                Devices
                            </Link>
                        </li>
                        <li className="nav-item">
                        <Link
                                to="/About"
                                className="nav-link"
                                role="button"
                                aria-expanded="false"
                            >
                                About
                            </Link>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
}
export default Nav;