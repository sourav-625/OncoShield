import React from 'react';
import { Link } from 'react-router-dom';

const Nav = () => {
    return (
        <nav className="navbar navbar-expand-lg bg-body-tertiary">

            <div className="container-fluid">
                <a className="navbar-brand" href="#">Navbar</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        <li className="nav-item">
                        <Link
                                to="/"
                                className="nav-link"
                                role="button"
                                data-bs-toggle="dropdown"
                                aria-expanded="false"
                            >
                                Home
                            </Link>
                        </li>
                        <li className="nav-item">
                        <Link
                                to="/About"
                                className="nav-link"
                                role="button"
                                data-bs-toggle="dropdown"
                                aria-expanded="false"
                            >
                                About
                            </Link>
                        </li>
                        <li className="nav-item dropdown">
                            <Link
                                to="/Devices"
                                className="nav-link dropdown-toggle"
                                role="button"
                                data-bs-toggle="dropdown"
                                aria-expanded="false"
                            >
                                Devices
                            </Link>
                            <ul className="dropdown-menu">
                                <li><Link className='nav-link' to="/">Electrodes</Link></li>
                                <li><Link className='nav-link' to="/">Electrodes</Link></li>
                                <li><hr className="dropdown-divider" /></li>
                                <li><a className="dropdown-item" href="#">Something else here</a></li>
                            </ul>
                        </li>
                    </ul>
                    <form className="d-flex" role="search">
                        <input className="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
                        <button className="btn btn-outline-success" type="submit">Search</button>
                    </form>
                </div>
            </div>
        </nav>
    );
}
export default Nav;