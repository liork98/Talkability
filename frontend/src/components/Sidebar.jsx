// Sidebar.jsx
import React from 'react';
import './Sidebar.css';
import logo from "../logo.png";

const Sidebar = ({ activeTab, setActiveTab }) => {
    return (
        <div className="sidebar">
            <img src={logo} alt="Talkability Logo" className="app-logo"/>

            <ul className="sidebar-menu">

                <li className={activeTab === 'home' ? 'active' : ''} onClick={() => setActiveTab('home')}>
                    Home
                </li>
                <li
                    className={activeTab === 'Technical Support' ? 'active' : ''}
                    onClick={() => setActiveTab('Technical Support')}
                >
                    Technical Support
                </li>
                <li className={activeTab === 'Billing' ? 'active' : ''} onClick={() => setActiveTab('Billing')}>
                    Billing
                </li>
                <li className={activeTab === 'Sales' ? 'active' : ''} onClick={() => setActiveTab('Sales')}>
                    Sales
                </li>
                <li className={activeTab === 'Insurance' ? 'active' : ''} onClick={() => setActiveTab('Insurance')}>
                    Insurance
                </li>
                <li className={activeTab === 'General' ? 'active' : ''} onClick={() => setActiveTab('General')}>
                    General
                </li>
                <li className={activeTab === 'Appointments' ? 'active' : ''}
                    onClick={() => setActiveTab('Appointments')}>
                    Appointments
                </li>
                <li className={activeTab === 'Medical Records' ? 'active' : ''}
                    onClick={() => setActiveTab('Medical Records')}>
                    Medical Records
                </li>
                <li className={activeTab === 'Patient Support' ? 'active' : ''}
                    onClick={() => setActiveTab('Patient Support')}>
                    Patient Support
                </li>
                <li className={activeTab === 'Pharmacy' ? 'active' : ''} onClick={() => setActiveTab('Pharmacy')}>
                    Pharmacy
                </li>
                <li className={activeTab === 'Nursing Services' ? 'active' : ''}
                    onClick={() => setActiveTab('Nursing Services')}>
                    Nursing Services
                </li>
                <li className={activeTab === 'Lab Services' ? 'active' : ''}
                    onClick={() => setActiveTab('Lab Services')}>
                    Lab Services
                </li>
                <li className={activeTab === 'Health Insurance Claims' ? 'active' : ''}
                    onClick={() => setActiveTab('Health Insurance Claims')}>
                    Health Insurance Claims
                </li>
                <li className={activeTab === 'IT Support' ? 'active' : ''} onClick={() => setActiveTab('IT Support')}>
                    IT Support
                </li>
            </ul>
        </div>
    );
};

export default Sidebar;